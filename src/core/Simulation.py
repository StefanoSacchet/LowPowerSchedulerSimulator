from pydantic import BaseModel
from typing import List

from src.core.Capacitor import Capacitor
from src.core.tasks.Task import Task
from src.core.tasks.Job import Job
from src.core.tasks.NOP import NOP
from src.core.Configuration import Configuration
from src.core.schedulers.Scheduler import Scheduler
from src.logger.Logger import Logger
from src.config.Config import TaskStates


class Simulation(BaseModel):
    """Model to simulate task scheduling"""

    __tick: int = 0  # current tick

    tick_duration: int  # duration of a tick in ms
    num_ticks: int  # simulation duration
    capacitor: Capacitor
    task_list: List[Task]
    energy_trace: List[int]  # energy trace in mJ
    scheduler: Scheduler
    logger: Logger
    prediction_len: int  # how many energy values the scheduler sees in the future

    job_list: List[Job] = []  # list to store active jobs
    next_job_id: int = 1  # counter for job IDs

    def __init__(self, configuration: Configuration):
        super().__init__(
            tick_duration=configuration.tick_duration,
            capacitor=configuration.capacitor,
            task_list=configuration.task_list,
            energy_trace=configuration.energy_trace,
            scheduler=configuration.scheduler,
            logger=configuration.logger,
            prediction_len=configuration.prediction_len,
            num_ticks=len(configuration.energy_trace),
        )

    def activate_jobs(self) -> None:
        for task in self.task_list:
            if task.is_ready(self.__tick):
                job = task.generate_job(self.next_job_id, self.__tick)
                self.next_job_id += 1
                self.job_list.append(job)
                self.scheduler.on_activate(job)
                self.logger.log_csv(
                    job,
                    TaskStates.ACTIVATED.value,
                    self.__tick,
                )

    def execute_job(self, job: Job) -> None:
        if job.execute() and self.capacitor.discharge(job.energy_requirement):
            self.logger.log_csv(job, TaskStates.EXECUTING.value, self.__tick)
            if job.is_complete():
                job.is_active = False
                self.job_list.remove(job)
                self.scheduler.on_terminate(job)
                self.logger.log_csv(job, TaskStates.TERMINATED.value, self.__tick + 1)

    def handle_missed_deadline(self) -> None:
        for job in self.job_list:
            if self.__tick >= job.deadline:
                self.logger.log_csv(
                    job,
                    TaskStates.MISSED_DEADLINE.value,
                    self.__tick,
                )
                self.job_list.remove(job)
                self.scheduler.on_terminate(job)

    def run(self):
        # initialize scheduler
        self.scheduler.init()

        for i, energy_input in enumerate(self.energy_trace):
            # charge the capacitor
            self.capacitor.charge(energy_input)
            # update scheduler with energy and next energy values
            next_n_energy = self.energy_trace[i + 1 : i + self.prediction_len + 1]
            self.scheduler.on_energy_update(self.capacitor.energy, next_n_energy)

            # check if any job missed deadline
            self.handle_missed_deadline()

            # check if any task is ready to be activated
            self.activate_jobs()

            # call scheduler to choose job
            job = self.scheduler.schedule(self.__tick)

            # execute job
            if not isinstance(job, NOP):
                self.execute_job(job)
            else:
                self.logger.log_csv(job, TaskStates.NOP.value, self.__tick)

            self.__tick += 1
