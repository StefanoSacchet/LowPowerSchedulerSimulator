import json
from typing import List

import pytest

from src.config.Config import ConfigParams, DirNames, FileNames
from src.core.Capacitor import Capacitor
from src.core.Configuration import Configuration
from src.core.EnergyTrace import EnergyTrace
from src.core.Simulation import Simulation
from src.core.tasks.Task import Task


@pytest.fixture
def task_list() -> List[Task]:
    with open(
        DirNames.SIMULATION_PARAMS.value + DirNames.NORMAL.value + "task_set_1.json",
        "r",
    ) as f:
        task_list = json.load(f)

    return [Task(**task) for task in task_list["task_set"]]


@pytest.fixture
def energy_trace() -> List[int]:
    energy_trace: List[int] = []
    with open(
        DirNames.SIMULATION_PARAMS.value + FileNames.ENERGY_TRACE.value,
        "r",
    ) as f:
        for line in f:
            energy_trace.append(int(line))
    return energy_trace


class TestConfiguration:
    simulation: Simulation

    def setup_method(self):
        configuration = Configuration()
        self.simulation = Simulation(configuration)

    def test_initialization(self, task_list: List[Task]):
        assert self.simulation.tick_duration == ConfigParams.TICK_DURATION.value
        assert self.simulation.capacitor.energy == ConfigParams.ENERGY.value
        assert self.simulation.capacitor.max_energy == ConfigParams.MAX_ENERGY.value
        assert self.simulation.scheduler.ready_list == []
        assert self.simulation.task_list == task_list
        assert self.simulation.energy_trace == EnergyTrace().get_energy_trace()

    def test_initialization_2(self, task_list, energy_trace):
        configuration = Configuration(tick_duration=2)
        capacitor = Capacitor(20, 20)
        configuration.set_capacitor(capacitor)
        configuration.set_task_list("./simulation_params/normal/task_set_1.json")
        configuration.set_energy_trace(energy_trace)
        self.simulation = Simulation(configuration)

        assert self.simulation.tick_duration == 2
        assert self.simulation.capacitor.energy == 20
        assert self.simulation.capacitor.max_energy == 20
        assert self.simulation.scheduler.ready_list == []
        assert self.simulation.task_list == task_list
        assert self.simulation.energy_trace == energy_trace
