from typing import Dict, List, Optional, Set

from pydantic import BaseModel

from src.core.schedulers.Scheduler import Scheduler
from src.core.tasks.AbstractJob import AbstractJob
from src.core.tasks.Harvest import Harvest
from src.core.tasks.Job import Job
from src.core.tasks.NOP import NOP


class Celebi(Scheduler, BaseModel):
    name: str = "Celebi"

    scheduled_jobs_map: Dict[int, Job] = {}
    unscheduled_jobs: List[Job] = []
    occupied_ticks: Set[int] = set()  # Track occupied time slots
    current_harvestable_energy: List[int] = []

    def init(self, energy: float, prediction: List[int]) -> None:
        self.ready_list = []
        self.scheduled_jobs_map = {}
        self.unscheduled_jobs = []
        self.occupied_ticks = set()

        self.energy = energy
        # Celebi just knows the current energy value
        self.current_harvestable_energy = prediction

    def on_activate(self, job: Job) -> None:
        self.ready_list.append(job)

    def on_terminate(self, job: Job) -> None:
        self.ready_list.remove(job)

    def on_energy_update(self, energy: int, prediction: List[int]) -> None:
        self.energy = energy
        # Celebi just knows the current energy value
        self.current_harvestable_energy = prediction

    # Find the latest start tick that does not overlap with other jobs
    def find_non_overlapping_start_tick(
        self, latest_start_tick: int, wcet: int, current_tick: int
    ) -> Optional[int]:
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

    def schedule(self, current_tick: int) -> AbstractJob:
        # Step 1: Pre-schedule using ALAP
        for job in self.ready_list:
            if job in self.scheduled_jobs_map.values():
                continue  # Skip already scheduled jobs

            latest_start_tick = job.deadline - job.wcet
            start_tick = self.find_non_overlapping_start_tick(
                latest_start_tick, job.wcet, current_tick
            )
            if start_tick is not None:
                for i in range(start_tick, start_tick + job.wcet):
                    self.scheduled_jobs_map[i] = job
                self.mark_ticks_as_occupied(start_tick, job.wcet)
            else:
                self.unscheduled_jobs.append(job)

        # Step 2: Execute scheduled jobs if possible
        if current_tick in self.scheduled_jobs_map:
            job = self.scheduled_jobs_map[current_tick]
            energy_required = job.energy_requirement / job.wcet * job.time_remaining
            if energy_required <= self.energy:
                self.scheduled_jobs_map.pop(current_tick)
                return job
            else:
                self.unscheduled_jobs.append(
                    job
                )  # Re-add to unscheduled jobs if energy is insufficient

        # Step 3: Execute unscheduled jobs early if possible
        for job in self.unscheduled_jobs:
            energy_required = job.energy_requirement / job.wcet * job.time_remaining
            if energy_required <= self.energy:
                self.unscheduled_jobs.remove(job)
                if current_tick < job.deadline:
                    return job

        # Step 4: Harvest energy if no jobs can be executed and energy is harvestable
        if self.current_harvestable_energy and self.current_harvestable_energy[0] > 0:
            return Harvest()

        return NOP()
