from pydantic import BaseModel
import random
from typing import List
import os

from src.config.Config import DirNames, FileNames


class EnergyTrace(BaseModel):
    """Model for energy trace"""

    def save_energy_trace(self, energy_trace: List[int]) -> None:
        # save energy trace to file
        if not os.path.exists(DirNames.SIMULATION_PARAMS.value):
            os.makedirs(DirNames.SIMULATION_PARAMS.value)
        with open(
            DirNames.SIMULATION_PARAMS.value + FileNames.ENERGY_TRACE.value, "w"
        ) as f:
            for energy in energy_trace:
                f.write(f"{energy}\n")

    def generate_energy_trace(self, max_energy: int, num_ticks: int) -> None:
        # generate list long num_ticks, between 0 and max_energy mJ
        energy_trace = [random.randint(0, max_energy) for _ in range(num_ticks)]
        self.save_energy_trace(energy_trace)

    def get_energy_trace(self) -> List[int]:
        # read energy trace from file
        energy_trace: List[int] = []
        with open(
            DirNames.SIMULATION_PARAMS.value + FileNames.ENERGY_TRACE.value, "r"
        ) as f:
            for line in f:
                energy_trace.append(int(line))
        return energy_trace
