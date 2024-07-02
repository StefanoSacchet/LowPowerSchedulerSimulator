from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List

from src.core.tasks.Job import Job


class Scheduler(ABC, BaseModel):
    """
    Abstract class for scheduler. To create a new scheduler, inherit from this class and implement the abstract methods
    """

    ready_list: List[Job] = []  # list of jobs that are ready to be scheduled
    energy: int = 0  # energy available to the scheduler
    prediction: List[int] = []  # list to store next n energy values

    @abstractmethod
    def init(self, energy: int, prediction: List[int]) -> None:
        pass

    @abstractmethod
    def on_activate(self, task: Job) -> None:
        pass

    @abstractmethod
    def on_terminate(self, task: Job) -> None:
        pass

    @abstractmethod
    def on_energy_update(self, energy: int) -> None:
        pass

    @abstractmethod
    def schedule(self, current_tick: int) -> Job:
        pass
