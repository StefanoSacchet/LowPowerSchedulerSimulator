from pydantic import BaseModel


class Task(BaseModel):
    name: str
    identifier: int
    period: int
    activation_date: int
    wcet: int
    deadline: int

    def __init__(
        self,
        name: str,
        identifier: int,
        period: int,
        activation_date: int,
        wcet: int,
        deadline: int,
    ):
        super().__init__(
            name=name,
            identifier=identifier,
            period=period,
            activation_date=activation_date,
            wcet=wcet,
            deadline=deadline,
        )
