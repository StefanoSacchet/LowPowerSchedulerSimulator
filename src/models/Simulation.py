from pydantic import BaseModel
from typing import List

from src.models.Capacitor import Capacitor
from src.models.Task import Task


class Simulation(BaseModel):
    """Model to simulate task scheduling"""

    __tick: int

    tick_duration: int  # duration of a tick in ms
    num_ticks: int = 0  # simulation duration
    capacitor: Capacitor
    task_list: List[Task]
    energy_trace: List[int]  # energy trace in mJ

    def __init__(
        self,
        tick_duration: int,
        capacitor: Capacitor,
        task_list: List[Task],
        energy_trace: List[int],
    ):
        super().__init__(
            tick_duration=tick_duration,
            capacitor=capacitor,
            task_list=task_list,
            energy_trace=energy_trace,
        )
        self.num_ticks = len(energy_trace)
        # self.tick_duration = tick_duration
        # self.capacitor = capacitor
        # self.task_list = task_list
        # self.energy_trace = energy_trace

    def run(self):
        print("tick_duration", self.tick_duration)
        print("num_ticks", self.num_ticks)
        print("capacitor", self.capacitor)
        print("task_list", self.task_list)
        print("energy_trace", self.energy_trace)
