from pydantic import BaseModel


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
