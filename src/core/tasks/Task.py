from typing import Optional
from pydantic import BaseModel

from src.core.tasks.Job import Job


class Task(BaseModel):
    """
    This class simulate the behavior of the simulated task. It controls the
    release of the jobs
    """

    id: int
    name: str
    period: int
    activation_date: int
    deadline: int
    wcet: int  # worst-case execution time
    energy_requirement: int
    priority: Optional[int]
    description: Optional[str]

    next_activation: int

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
            next_activation=activation_date,
        )

    def is_ready(self, tick: int) -> bool:
        return tick >= self.next_activation

    def generate_job(self, job_id: int, tick: int) -> Job:
        job = Job(
            id=job_id,
            task_id=self.id,
            name=self.name,
            deadline=tick + self.deadline,
            wcet=self.wcet,
            energy_requirement=self.energy_requirement,
        )
        self.next_activation += self.period
        return job
