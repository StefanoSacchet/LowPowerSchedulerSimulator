from pydantic import BaseModel
from typing import Optional


class Task(BaseModel):
    """Model for task's parameters"""

    id: int
    name: str
    period: int
    deadline: int
    wcet: int  # worst-case execution time
    energy_requirement: int
    priority: Optional[int] = None
    description: Optional[str] = None

    def __init__(
        self,
        id: int,
        name: str,
        period: int,
        deadline: int,
        wcet: int,
        energy_requirement: int,
        priority: Optional[int] = None,
        description: Optional[str] = None,
    ):
        super().__init__(
            id=id,
            name=name,
            period=period,
            deadline=deadline,
            wcet=wcet,
            energy_requirement=energy_requirement,
            priority=priority,
            description=description,
        )
        self.id = id
        self.name = name
        self.period = period
        self.deadline = deadline
        self.wcet = wcet
        self.energy_requirement = energy_requirement
        self.priority = priority
        self.description = description
