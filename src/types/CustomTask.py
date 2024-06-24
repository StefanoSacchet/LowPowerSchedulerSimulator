from src.types.Task import Task


class CustomTask(Task):
    """Custom task class that adds energy consumption to task class"""

    energy_consumption: int = 0

    def __init__(
        self,
        name: str,
        identifier: int,
        period: int,
        activation_date: int,
        wcet: int,
        deadline: int,
        energy_consumption: int,
    ):
        super().__init__(
            name=name,
            identifier=identifier,
            period=period,
            activation_date=activation_date,
            wcet=wcet,
            deadline=deadline,
        )
        self.energy_consumption = energy_consumption
