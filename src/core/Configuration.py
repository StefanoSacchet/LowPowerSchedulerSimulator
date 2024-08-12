import json
from typing import List, Optional

from pydantic import BaseModel, field_validator

from src.config.Config import ConfigParams, DirNames, FileNames
from src.core.Capacitor import Capacitor
from src.core.EnergyTrace import EnergyTrace
from src.core.schedulers.Celebi import Celebi
from src.core.schedulers.Scheduler import Scheduler
from src.core.tasks.Task import Task
from src.logger.Logger import Logger


class Configuration(BaseModel):
    """Configuration params for simulation"""

    tick_duration: int  # duration of a tick in ms
    prediction_len: int  # how many energy values the scheduler sees in the future
    charge_mutually_exclusive: bool = False

    capacitor: Optional[Capacitor] = None
    scheduler: Optional[Scheduler] = None
    logger: Optional[Logger] = None
    task_list: List[Task] = []
    energy_trace: List[int] = []

    class Config:
        validate_assignment = True

    @field_validator("tick_duration")
    def check_tick_duration(cls, value: int):
        assert value > 0, "Tick duration must be greater than 0"
        return value

    @field_validator("prediction_len")
    def check_prediction_len(cls, value: int):
        assert value >= 0, "Prediction length must be greater or equal than 0"
        return value

    @field_validator("task_list")
    def check_task_list(cls, value: List[Task]):
        assert len(value) > 0, "Task list must not be empty"
        return value

    @field_validator("energy_trace")
    def check_energy_trace(cls, value: List[int]):
        assert len(value) > 0, "Energy trace must not be empty"
        return value

    def __init__(
        self,
        tick_duration: int = 1,
        prediction_len: int = 3,
        charge_mutually_exclusive: bool = False,
    ):
        super().__init__(
            tick_duration=tick_duration,
            prediction_len=prediction_len,
            charge_mutually_exclusive=charge_mutually_exclusive,
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
            # print("ℹ️ Using provided capacitor", capacitor.__str__())
            self.capacitor = capacitor

    def set_scheduler(self, scheduler: Optional[Scheduler] = None) -> None:
        if scheduler is None:
            self.scheduler = Celebi()
        else:
            assert isinstance(scheduler, Scheduler)
            # print("ℹ️ Using provided scheduler", scheduler.name)
            self.scheduler = scheduler

    def set_task_list(self, path: Optional[str] = None) -> None:
        if path is None:
            with open(
                DirNames.SIMULATION_PARAMS.value
                + DirNames.LOW_POWER.value
                + "celebi.json",
                "r",
            ) as f:
                task_list = json.load(f)
                self.task_list = [Task(**task) for task in task_list["task_set"]]
        else:
            # print("ℹ️ Using provided task list", path.split("/")[-1])
            with open(path, "r") as f:
                task_list = json.load(f)
                self.task_list = [Task(**task) for task in task_list]

    def set_energy_trace(self, path: Optional[str] = None) -> None:
        if path is None:
            with open(
                DirNames.SIMULATION_PARAMS.value + "energy_trace.log",
                "r",
            ) as f:
                self.energy_trace = [int(line) for line in f]
        else:
            # print("ℹ️ Using provided energy trace", path.split("/")[-1])
            with open(path, "r") as f:
                self.energy_trace = [int(line) for line in f]

    def set_logger(self, logger: Optional[Logger] = None) -> None:
        if logger is None:
            self.logger = Logger(
                DirNames.RESULTS.value,
                FileNames.RESULTS.value,
                FileNames.ENERGY_LEVEL.value,
            )
        else:
            assert isinstance(logger, Logger)
            # print("ℹ️ Using provided logger")
            self.logger = logger
