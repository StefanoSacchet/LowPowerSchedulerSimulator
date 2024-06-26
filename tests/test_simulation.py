import pytest

from src.models.Simulation import Simulation
from src.models.Configuration import Configuration
from src.models.Task import Task


class TestSimulation:
    simulation: Simulation

    def setup_method(self):
        configuration = Configuration()
        self.simulation = Simulation(configuration)

    # def test_initialization(self):
    #     assert self.simulation.tick_duration == 1
    #     # assert self.simulation.__tick == 0
    #     assert self.simulation.capacitor.energy == 100
    #     assert self.simulation.task_list == []
    #     assert self.simulation.energy_trace == []
    #     assert self.simulation.scheduler.ready_list == []
