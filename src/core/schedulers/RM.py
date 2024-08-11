from typing import Dict, List, Set

from src.core.schedulers.Scheduler import Scheduler
from src.core.tasks.AbstractJob import AbstractJob
from src.core.tasks.Harvest import Harvest
from src.core.tasks.Job import Job
from src.core.tasks.NOP import NOP


class RM(Scheduler):
    """
    Earliest Deadline First scheduler

    Attributes:
        ready_list: List[Job] - list of jobs that are ready to be scheduled
        energy: int - energy of the capacitor
        prediction: List[int] - list to store next n energy values
    """

    scheduled_jobs_map: Dict[int, Job] = {}
    unscheduled_jobs: List[Job] = []
    occupied_ticks: Set[int] = set()  # Track occupied time slots
    current_harvestable_energy: List[int] = []

    def init(self, energy: float, prediction: List[int]) -> None:
        self.ready_list = []
        self.energy = energy
        # just knows the current energy value
        self.current_harvestable_energy = prediction

    def on_activate(self, job: Job) -> None:
        self.ready_list.append(job)

    def on_terminate(self, job: Job) -> None:
        self.ready_list.remove(job)

    def on_energy_update(self, energy: int, prediction: List[int]) -> None:
        self.energy = energy
        # just knows the current energy value
        self.current_harvestable_energy = prediction

    def schedule(self, current_tick: int) -> AbstractJob:
        if len(self.ready_list) == 0:
            return NOP()

        # find the job with the higher freqency
        self.ready_list.sort(key=lambda x: x.period)

        for job in self.ready_list:
            energy_required = job.energy_requirement / job.wcet * job.time_remaining
            if energy_required <= self.energy:
                return job

        # if no task can be executed, check if there is enough energy to harvest
        if self.current_harvestable_energy[0] > 0:
            return Harvest()

        return NOP()
