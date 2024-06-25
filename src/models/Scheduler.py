from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List

from src.models.Task import Task


class Scheduler(ABC, BaseModel):
    """Abstract class for scheduler. To create a new scheduler, inherit from this class and implement the abstract methods"""

    ready_list: List[Task] = []  # list of tasks that are ready to be scheduled

    @abstractmethod
    def init(self) -> None:
        pass

    @abstractmethod
    def on_activate(self, task: Task) -> None:
        pass

    @abstractmethod
    def on_terminate(self, task: Task) -> None:
        pass

    @abstractmethod
    def schedule(self) -> Task:
        pass
