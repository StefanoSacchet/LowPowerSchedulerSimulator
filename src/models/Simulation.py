from pydantic import BaseModel
from typing import List

from src.models.Capacitor import Capacitor
from src.models.Task import Task
from src.models.Configuration import Configuration


class Simulation(BaseModel):
    """Model to simulate task scheduling"""

    __tick: int = 0  # current tick

    tick_duration: int  # duration of a tick in ms
    num_ticks: int = 0  # simulation duration
    capacitor: Capacitor
    task_list: List[Task]
    energy_trace: List[int]  # energy trace in mJ

    def __init__(
        self,
        configuration: Configuration,
    ):
        super().__init__(
            tick_duration=configuration.tick_duration,
            capacitor=configuration.capacitor,
            task_list=configuration.task_list,
            energy_trace=configuration.energy_trace,
        )
        self.num_ticks = len(configuration.energy_trace)

    def run(self):
        print("tick_duration", self.tick_duration)
        print("num_ticks", self.num_ticks)
        print("capacitor", self.capacitor)
        print("task_list", self.task_list)
        print("energy_trace", self.energy_trace)
