from pydantic import BaseModel
from typing import List
import json

from src.models.Scheduler import Scheduler
from src.models.Task import Task
from src.config.Config import DirNames, FileNames, ConfigCapacitor, Schedulers
from src.models.Capacitor import Capacitor
from src.models.EnergyTrace import EnergyTrace
from src.schedulers.EDF import EDF


class Configuration(BaseModel):
    """Configuration params for simulation"""

    tick_duration: int  # duration of a tick in ms
    capacitor: Capacitor = None
    task_list: List[Task] = []
    energy_trace: List[int] = []
    scheduler: Scheduler = None

    def __init__(
        self,
        scheduler: Schedulers = Schedulers.EDF.value,
        tick_duration: int = 1,
    ):
        super().__init__(
            tick_duration=tick_duration,
        )
        self.capacitor = self.create_capacitor()
        self.task_list = self.get_task_list()
        self.energy_trace = EnergyTrace().get_energy_trace()
        self.scheduler = self.get_scheduler(scheduler)

    def get_task_list(self) -> List[Task]:
        with open(
            DirNames.SIMULATION_PARAMS.value + FileNames.TASK_SET.value, "r"
        ) as f:
            task_list = json.load(f)
        return [Task(**task) for task in task_list["task_set"]]

    def create_capacitor(self) -> Capacitor:
        return Capacitor(ConfigCapacitor.ENERGY.value, ConfigCapacitor.MAX_ENERGY.value)

    def get_scheduler(self, scheduler: Schedulers) -> Scheduler:
        if scheduler == Schedulers.EDF.value:
            return EDF()
        else:
            raise NotImplementedError(f"Scheduler: {scheduler.value} not implemented")
