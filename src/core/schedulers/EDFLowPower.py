from typing import List

from src.core.schedulers.Scheduler import Scheduler
from src.core.tasks.Job import Job
from src.core.tasks.NOP import NOP


class EDFLowPower(Scheduler):
    """
    Earliest Deadline First scheduler

    Attributes:
        ready_list: List[Job] - list of jobs that are ready to be scheduled
        energy: int - energy of the capacitor
        prediction: List[int] - list to store next n energy values
    """

    def init(self) -> None:
        self.ready_list = []

    def on_activate(self, task: Job) -> None:
        self.ready_list.append(task)

    def on_terminate(self, task: Job) -> None:
        self.ready_list.remove(task)

    def on_energy_update(self, energy: int, prediction: List[int]) -> None:
        self.energy = energy
        self.prediction = prediction

    def schedule(self, current_tick: int) -> Job:
        # TODO heap q

        if len(self.ready_list) == 0:
            return NOP()

        self.ready_list.sort(key=lambda x: x.deadline)

        for job in self.ready_list:
            if (
                job.energy_requirement <= self.energy
                and current_tick + job.time_remaining <= job.deadline
            ):
                return job
            else:
                print("Job cannot be scheduled", current_tick)

        return NOP()
