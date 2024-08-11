from typing import Optional

from pydantic import BaseModel, field_validator

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

    class Config:
        validate_assignment = True

    @field_validator("id")
    def check_id(cls, value: int):
        assert value >= 0, "ID must be greater than or equal to 0"
        return value

    @field_validator("name")
    def check_name(cls, value: str):
        assert len(value) > 0, "Name must not be empty"
        return value

    @field_validator("period")
    def check_period(cls, value: int):
        assert value > 0, "Period must be greater than 0"
        return value

    @field_validator("activation_date")
    def check_activation_date(cls, value: int):
        assert value >= 0, "Activation date must be greater than or equal to 0"
        return value

    @field_validator("deadline")
    def check_deadline(cls, value: int):
        assert value > 0, "Deadline must be greater than 0"
        return value

    @field_validator("wcet")
    def check_wcet(cls, value: int):
        assert value > 0, "WCET must be greater than 0"
        return value

    @field_validator("energy_requirement")
    def check_energy_requirement(cls, value: int):
        assert value >= 0, "Energy requirement must be greater or equal to 0"
        return value

    @field_validator("priority")
    def check_priority(cls, value: Optional[int]):
        if value is not None:
            assert value >= 0, "Priority must be greater than or equal to 0"
        return value

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
            period=self.period,
            wcet=self.wcet,
            energy_requirement=self.energy_requirement,
        )
        self.next_activation += self.period
        return job
