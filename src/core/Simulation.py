from typing import List

from pydantic import BaseModel, field_validator

from src.config.Config import TaskStates
from src.core.Capacitor import Capacitor
from src.core.Configuration import Configuration
from src.core.schedulers.Scheduler import Scheduler
from src.core.tasks.Job import Job
from src.core.tasks.NOP import NOP
from src.core.tasks.Task import Task
from src.logger.Logger import Logger


class Simulation(BaseModel):
    """Model to simulate task scheduling"""

    _tick: int = 0  # current tick

    tick_duration: int  # duration of a tick in ms
    num_ticks: int  # simulation duration
    capacitor: Capacitor
    task_list: List[Task]
    energy_trace: List[int]  # energy trace in mJ
    scheduler: Scheduler
    logger: Logger
    prediction_len: int  # how many energy values the scheduler sees in the future

    job_list: List[Job] = []  # list to store active jobs
    next_job_id: int = 1  # counter that gives jobs their ID

    class Config:
        validate_assignment = True

    @field_validator("tick_duration")
    def check_tick_duration(cls, value: int):
        assert value > 0, "Tick duration must be greater than 0"
        return value

    @field_validator("num_ticks")
    def check_num_ticks(cls, value: int):
        assert value > 0, "Number of ticks must be greater than 0"
        return value

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
            if task.is_ready(self._tick):
                job = task.generate_job(self.next_job_id, self._tick)
                self.next_job_id += 1
                self.job_list.append(job)
                self.scheduler.on_activate(job)
                self.logger.log_csv(
                    job,
                    TaskStates.ACTIVATED,
                    self._tick,
                )

    def execute_job(self, job: Job) -> None:
        # consumed energy per time unit by the job
        energy_required = job.energy_requirement / job.wcet
        # execute job and discharge capacitor
        if self.capacitor.discharge(energy_required) and job.execute():
            self.logger.log_csv(job, TaskStates.EXECUTING, self._tick)
            if job.is_complete():
                job.is_active = False
                self.job_list.remove(job)
                self.scheduler.on_terminate(job)
                self.logger.log_csv(job, TaskStates.TERMINATED, self._tick + 1)
        else:
            print("Energy not sufficient to execute job", job)

    def handle_missed_deadline(self) -> None:
        for job in self.job_list:
            if self._tick >= job.deadline:
                self.job_list.remove(job)
                self.scheduler.on_terminate(job)
                self.logger.log_csv(
                    job,
                    TaskStates.MISSED_DEADLINE,
                    self._tick,
                )

    def run(self):
        # initialize scheduler
        self.scheduler.init(
            self.capacitor.energy, self.energy_trace[: self.prediction_len]
        )

        for i, energy_input in enumerate(self.energy_trace):

            self.logger.log_energy_level(self.capacitor.energy, self._tick)

            # charge the capacitor
            self.capacitor.charge(energy_input)

            # update scheduler with current energy and next energy values
            next_n_energy = self.energy_trace[i + 1 : i + self.prediction_len + 1]
            self.scheduler.on_energy_update(self.capacitor.energy, next_n_energy)

            # check if any job missed deadline
            self.handle_missed_deadline()

            # check if any task is ready to be activated
            self.activate_jobs()

            # call scheduler to choose job
            job = self.scheduler.schedule(self._tick)

            # execute job
            if not isinstance(job, NOP):
                self.execute_job(job)
            else:
                self.logger.log_csv(job, TaskStates.NOP, self._tick)

            self._tick += 1
