from src.core.tasks.AbstractJob import AbstractJob

class NOP(AbstractJob):
    """
    NOP task when MCU can not do nothing
    """

    id: int = -1
    task_id: int = -1
    name: str = "NOP"

    def __init__(self):
        super().__init__()
