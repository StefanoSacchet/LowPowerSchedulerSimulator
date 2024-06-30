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
    priority: Optional[int]
    description: Optional[str]

    is_active: bool = False
    next_activation: int = 0
    time_remaining: int = 0
    next_deadline: int = 0

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
        self.next_activation = activation_date

    def is_ready(self, tick: int) -> bool:
        return tick >= self.next_activation

    def activate_task(self) -> None:
        self.is_active = True
        self.next_deadline = self.next_activation + self.deadline
        self.next_activation += self.period

    # check if task missed its deadline
    def missed_deadline(self, tick: int) -> bool:
        return tick >= self.next_deadline and self.is_active
