import json
from typing import List, Optional

from pydantic import BaseModel

from src.config.Config import ConfigParams, DirNames, FileNames
from src.core.Capacitor import Capacitor
from src.core.EnergyTrace import EnergyTrace
from src.core.schedulers.EDFLowPower import EDFLowPower
from src.core.schedulers.Scheduler import Scheduler
from src.core.tasks.Task import Task
from src.logger.Logger import Logger


class Configuration(BaseModel):
    """Configuration params for simulation"""

    tick_duration: int  # duration of a tick in ms
    prediction_len: int  # how many energy values the scheduler sees in the future

    capacitor: Optional[Capacitor] = None
    scheduler: Optional[Scheduler] = None
    logger: Optional[Logger] = None
    task_list: List[Task] = []
    energy_trace: List[int] = []

    def __init__(
        self,
        tick_duration: int = 1,
        prediction_len: int = 3,
    ):
        super().__init__(
            tick_duration=tick_duration,
            prediction_len=prediction_len,
        )
        # default setup
        self.set_capacitor()
        self.set_scheduler()
        self.set_logger()
        self.set_task_list()
        self.set_energy_trace()

    def set_capacitor(self, capacitor: Optional[Capacitor] = None) -> None:
        if capacitor is None:
            self.capacitor = Capacitor(
                ConfigParams.ENERGY.value, ConfigParams.MAX_ENERGY.value
            )
        else:
            assert isinstance(capacitor, Capacitor)
            print("Using provided capacitor")
            self.capacitor = capacitor

    def set_scheduler(self, scheduler: Optional[Scheduler] = None) -> None:
        if scheduler is None:
            self.scheduler = EDFLowPower()
        else:
            assert isinstance(scheduler, Scheduler)
            print("Using provided scheduler")
            self.scheduler = scheduler

    def set_task_list(self, path: Optional[str] = None) -> None:
        if path is None:
            with open(
                DirNames.SIMULATION_PARAMS.value
                + DirNames.NORMAL.value
                + FileNames.TASK_SET.value,
                "r",
            ) as f:
                task_list = json.load(f)
        else:
            print("Using provided task list", path.split("/")[-1])
            with open(path, "r") as f:
                task_list = json.load(f)

        self.task_list = [Task(**task) for task in task_list["task_set"]]

    def set_energy_trace(self, energy_trace: Optional[List[int]] = None) -> None:
        if energy_trace is None:
            self.energy_trace = EnergyTrace().get_energy_trace()
        else:
            print("Using provided energy trace")
            self.energy_trace = energy_trace

    def set_logger(self, logger: Optional[Logger] = None) -> None:
        if logger is None:
            self.logger = Logger(DirNames.RESULTS.value, FileNames.RESULTS.value)
        else:
            assert isinstance(logger, Logger)
            print("Using provided logger")
            self.logger = logger
