from pydantic import BaseModel
from typing import List
import json

from src.models.Scheduler import Scheduler
from src.models.Task import Task
from src.config.Config import DirNames, FileNames, ConfigParams
from src.models.Capacitor import Capacitor
from src.models.EnergyTrace import EnergyTrace
from src.schedulers.EDF import EDF


class Configuration(BaseModel):
    """Configuration params for simulation"""

    tick_duration: int  # duration of a tick in ms
    capacitor: Capacitor = None
    scheduler: Scheduler = None
    task_list: List[Task] = []
    energy_trace: List[int] = []

    def __init__(
        self,
        tick_duration: int = 1,
    ):
        super().__init__(
            tick_duration=tick_duration,
        )
        # default setup
        self.set_capacitor()
        self.set_scheduler()
        self.set_task_list()
        self.set_energy_trace()

    def set_capacitor(self, capacitor: Capacitor = None) -> None:
        if capacitor is not None and not isinstance(capacitor, Capacitor):
            raise ValueError(
                f"Capacitor must be of type Capacitor, not {type(capacitor)}"
            )
        if capacitor is None:
            self.capacitor = Capacitor(
                ConfigParams.ENERGY.value, ConfigParams.MAX_ENERGY.value
            )
        else:
            print("Using provided capacitor")
            self.capacitor = capacitor

    def set_scheduler(self, scheduler: Scheduler = None) -> None:
        if scheduler is not None and not isinstance(scheduler, Scheduler):
            raise ValueError(
                f"Scheduler must be of type Scheduler, not {type(scheduler)}"
            )
        if scheduler is None:
            self.scheduler = EDF()
        else:
            print("Using provided scheduler")
            self.scheduler = scheduler

    def set_task_list(self, path: str = None) -> None:
        if path is None:
            with open(
                DirNames.SIMULATION_PARAMS.value + FileNames.TASK_SET.value, "r"
            ) as f:
                task_list = json.load(f)
        else:
            print("Using provided task list")
            with open(path, "r") as f:
                task_list = json.load(f)

        self.task_list = [Task(**task) for task in task_list["task_set"]]

    def set_energy_trace(self, energy_trace: List[int] = None) -> None:
        if energy_trace is None:
            self.energy_trace = EnergyTrace().get_energy_trace()
        else:
            print("Using provided energy trace")
            self.energy_trace = energy_trace
