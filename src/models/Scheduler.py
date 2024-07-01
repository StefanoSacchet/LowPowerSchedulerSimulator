from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List

from src.models.Job import Job


class Scheduler(ABC, BaseModel):
    """
    Abstract class for scheduler. To create a new scheduler, inherit from this class and implement the abstract methods
    """

    ready_list: List[Job] = []  # list of jobs that are ready to be scheduled

    @abstractmethod
    def init(self) -> None:
        pass

    @abstractmethod
    def on_activate(self, task: Job) -> None:
        pass

    @abstractmethod
    def on_terminate(self, task: Job) -> None:
        pass

    @abstractmethod
    def schedule(self) -> Job:
        pass
