from pydantic import BaseModel
from typing import List

from src.models.Capacitor import Capacitor
from src.models.Task import Task
from src.models.Configuration import Configuration
from src.models.Scheduler import Scheduler


class Simulation(BaseModel):
    """Model to simulate task scheduling"""

    __tick: int = 0  # current tick

    tick_duration: int  # duration of a tick in ms
    num_ticks: int = 0  # simulation duration
    capacitor: Capacitor
    task_list: List[Task]
    energy_trace: List[int]  # energy trace in mJ
    scheduler: Scheduler

    def __init__(
        self,
        configuration: Configuration,
    ):
        super().__init__(
            tick_duration=configuration.tick_duration,
            capacitor=configuration.capacitor,
            task_list=configuration.task_list,
            energy_trace=configuration.energy_trace,
            scheduler=configuration.scheduler,
        )
        self.num_ticks = len(configuration.energy_trace)

    def activate_tasks(self) -> None:
        for task in self.task_list:
            if task.is_ready(self.__tick) and not task.is_active:
                task.is_active = True
                task.next_activaton += task.period  # update next activation time
                self.scheduler.on_activate(task)

    def execute_task(self, task: Task) -> None:
        if (
            task.is_active
            and task.time_remaining > 0
            # and self.capacitor.consume(task.energy_required)
        ):
            task.time_remaining -= 1
            if task.time_remaining == 0:
                task.is_active = False
                task.time_remaining = task.wcet  # reset time remaining
                self.scheduler.on_terminate(task)

    def run(self):
        # initialize scheduler
        self.scheduler.init()

        for energy_input in self.energy_trace:
            # charge the capacitor
            self.capacitor.charge(energy_input)

            # check if any task is ready to be activated
            self.activate_tasks()

            # call scheduler to choose task
            task = self.scheduler.schedule()

            # execute task
            if task is not None:
                self.execute_task(task)

            self.__tick += 1
