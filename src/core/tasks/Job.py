from pydantic import BaseModel, field_validator


class Job(BaseModel):
    """
    Model for a job that is generated from a task
    """

    id: int
    task_id: int
    name: str
    deadline: int
    wcet: int  # worst-case execution time
    energy_requirement: int

    time_remaining: int

    is_active: bool = False

    @field_validator("id")
    def check_id(cls, value: int):
        assert value >= 0, "ID must be greater than or equal to 0"
        return value

    @field_validator("task_id")
    def check_task_id(cls, value: int):
        assert value >= 0, "Task ID must be greater than or equal to 0"
        return value

    @field_validator("name")
    def check_name(cls, value: str):
        assert len(value) > 0, "Name must not be empty"
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
        assert value >= 0, "Energy requirement must be greater than or equal to 0"
        return value

    def __init__(
        self,
        id: int,
        task_id: int,
        name: str,
        deadline: int,
        wcet: int,
        energy_requirement: int,
    ):
        super().__init__(
            id=id,
            task_id=task_id,
            name=name,
            deadline=deadline,
            wcet=wcet,
            energy_requirement=energy_requirement,
            time_remaining=wcet,
        )

    def execute(self) -> bool:
        if self.time_remaining > 0:
            self.time_remaining -= 1
            return True
        return False

    def is_complete(self) -> bool:
        return self.time_remaining == 0
