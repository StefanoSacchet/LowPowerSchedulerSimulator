from typing import Dict, List, Set

from src.core.schedulers.Scheduler import Scheduler
from src.core.tasks.Job import Job
from src.core.tasks.NOP import NOP


class Celebi(Scheduler):
    """
    Earliest Deadline First scheduler

    Attributes:
        ready_list: List[Job] - list of jobs that are ready to be scheduled
        energy: int - energy of the capacitor
        prediction: List[int] - list to store next n energy values
    """

    scheduled_jobs: Dict[int, Job] = {}
    unscheduled_jobs: List[Job] = []
    occupied_ticks: Set[int] = set()  # Track occupied time slots

    def init(self, energy: float, prediction: List[int]) -> None:
        self.ready_list = []
        self.energy = energy
        # Celebi doesn't use prediction
        # self.prediction = prediction
        self.prediction = []

    def on_activate(self, job: Job) -> None:
        self.ready_list.append(job)

    def on_terminate(self, job: Job) -> None:
        self.ready_list.remove(job)

    def on_energy_update(self, energy: int, prediction: List[int]) -> None:
        self.energy = energy
        # self.prediction = prediction

    # Find the latest start tick that does not overlap with other jobs.
    def find_non_overlapping_start_tick(
        self, latest_start_tick: int, wcet: int, current_tick: int
    ) -> int | None:
        for start_tick in range(latest_start_tick, current_tick, -1):
            if all(
                tick not in self.occupied_ticks
                for tick in range(start_tick, start_tick + wcet)
            ):
                return start_tick
        return None

    # Mark the time slots as occupied.
    def mark_ticks_as_occupied(self, start_tick: int, wcet: int) -> None:
        for tick in range(start_tick, start_tick + wcet):
            self.occupied_ticks.add(tick)

    def schedule(self, current_tick: int) -> Job | NOP:
        # TODO heap q

        if len(self.ready_list) == 0:
            return NOP()

        # Schedule each job as late as possible without overlapping
        for job in self.ready_list:
            latest_start_tick = job.deadline - job.wcet
            start_tick = self.find_non_overlapping_start_tick(
                latest_start_tick, job.wcet, current_tick
            )
            if start_tick is not None:
                for i in range(start_tick, start_tick + job.wcet):
                    self.scheduled_jobs[i] = job
                self.mark_ticks_as_occupied(start_tick, job.wcet)
                # return job

        # if at current tick there is a scheduled job, return it
        if current_tick in self.scheduled_jobs:
            job = self.scheduled_jobs.pop(current_tick)
            return job

        return NOP()
