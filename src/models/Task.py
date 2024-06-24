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
