from src.core.tasks.AbstractJob import AbstractJob


class Harvest(AbstractJob):
    """
    Harvest task when MCU can harvest energy
    """

    id: int = -2
    task_id: int = -2
    name: str = "Harvest"
