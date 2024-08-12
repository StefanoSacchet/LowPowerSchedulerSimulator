from abc import ABC, abstractmethod
from typing import List, Optional

from pydantic import BaseModel, field_validator

from src.core.tasks.Job import Job


class Scheduler(ABC, BaseModel):
    """
    Abstract class for scheduler. To create a new scheduler, inherit from this class and implement the abstract methods
    """

    name: str  # name of the scheduler

    ready_list: List[Job] = []  # list of jobs that are ready to be scheduled
    energy: float = 0  # energy available to the scheduler
    prediction: List[int] = []  # list to store next n energy values

    class Config:
        validate_assignment = True

    @field_validator("energy")
    def check_energy(cls, value: float):
        assert value >= 0, "Energy must be greater than or equal to 0"
        return value

    @abstractmethod
    def init(self, energy: float, prediction: List[int]) -> None:
        pass

    @abstractmethod
    def on_activate(self, task: Job) -> None:
        pass

    @abstractmethod
    def on_terminate(self, task: Job) -> None:
        pass

    @abstractmethod
    def on_energy_update(self, energy: float, prediction: List[int]) -> None:
        pass

    @abstractmethod
    def schedule(self, current_tick: int) -> Job:
        pass
