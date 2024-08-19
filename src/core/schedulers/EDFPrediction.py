import heapq
from typing import List, Tuple

from pydantic import BaseModel

from src.core.schedulers.Scheduler import Scheduler
from src.core.tasks.AbstractJob import AbstractJob
from src.core.tasks.Harvest import Harvest
from src.core.tasks.Job import Job
from src.core.tasks.NOP import NOP


class EDFPrediction(Scheduler, BaseModel):
    name: str = "EDFPrediction"

    ready_list: List[Tuple[int, int, Job]] = []
    energy: float = 0.0
    future_energy: List[int] = []

    def init(self, energy: float, future_energy: List[int]) -> None:
        self.ready_list = []
        self.energy = energy
        self.future_energy = future_energy

    def on_activate(self, job: Job) -> None:
        heapq.heappush(self.ready_list, (job.deadline, job.id, job))

    def on_terminate(self, job: Job) -> None:
        # Filter out the job from the ready_list by creating a new list
        self.ready_list = [(dl, id, j) for dl, id, j in self.ready_list if j != job]
        heapq.heapify(self.ready_list)

    def on_energy_update(self, energy: int, future_energy: List[int]) -> None:
        self.energy = energy
        self.future_energy = future_energy

    def schedule(self, current_tick: int) -> AbstractJob:
        if not self.ready_list:
            if self.future_energy and self.future_energy[0] > 0:
                return Harvest()
            return NOP()

        # Track jobs that can't be scheduled right now
        deferred_jobs: List[Tuple[int, int, Job]] = []

        while self.ready_list:
            _, _, job = heapq.heappop(self.ready_list)

            # Calculate the required energy for this job
            energy_required = job.energy_requirement / job.wcet * job.time_remaining

            if energy_required <= self.energy:
                return job
            else:
                deferred_jobs.append((job.deadline, job.id, job))

        # Re-push all deferred jobs back to the heapq
        for job in deferred_jobs:
            heapq.heappush(self.ready_list, job)

        # No job can be scheduled, check if we can harvest energy
        if self.future_energy[0] > 0:
            return Harvest()

        return NOP()
