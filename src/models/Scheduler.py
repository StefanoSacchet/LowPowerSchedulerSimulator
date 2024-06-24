from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List

from models.Task import Task


class Scheduler(ABC, BaseModel):
    """Abstract class for scheduler"""

    task_list: List[Task]

    @abstractmethod
    def schedule(self, tasks: List[Task]) -> List[Task]:
        pass
