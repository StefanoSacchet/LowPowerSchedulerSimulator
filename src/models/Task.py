from pydantic import BaseModel
from typing import Optional


class Task(BaseModel):
    """Model for task's parameters"""

    id: int
    name: str
    period: int
    activation_date: int
    deadline: int
    wcet: int  # worst-case execution time
    energy_requirement: int
    priority: Optional[int] = None
    description: Optional[str] = None

    is_active: bool = False
    next_activaton: int = 0
    time_remaining: int = 0

    def __init__(
        self,
        id: int,
        name: str,
        period: int,
        activation_date: int,
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
            activation_date=activation_date,
            deadline=deadline,
            wcet=wcet,
            energy_requirement=energy_requirement,
            priority=priority,
            description=description,
        )
        self.time_remaining = wcet
        self.next_activaton = activation_date

    def is_ready(self, tick: int) -> bool:
        return tick >= self.next_activaton
