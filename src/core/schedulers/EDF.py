from typing import List

from src.core.schedulers.Scheduler import Scheduler
from src.core.tasks.Job import Job
from src.core.tasks.NOP import NOP


class EDF(Scheduler):
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

    def schedule(self, current_tick: int) -> Job | NOP:
        # TODO heap q

        if len(self.ready_list) == 0:
            return NOP()

        self.ready_list.sort(key=lambda x: x.deadline)

        # find first job with sufficient energy
        for job in self.ready_list:
            if job.energy_requirement <= self.energy:
                return job

        return NOP()
