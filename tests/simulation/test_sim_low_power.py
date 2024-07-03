import json
from typing import List

import pytest

from src.config.Config import ConfigParams, DirNames
from src.core.Configuration import Configuration
from src.core.EnergyTrace import EnergyTrace
from src.core.schedulers.EDFLowPower import EDFLowPower
from src.core.Simulation import Simulation
from src.core.tasks.Task import Task


@pytest.fixture
def task_list_3() -> List[Task]:
    with open(
        DirNames.SIMULATION_PARAMS.value + DirNames.LOW_POWER.value + "task_set_2.json",
        "r",
    ) as f:
        task_list = json.load(f)

    return [Task(**task) for task in task_list["task_set"]]


class TestSimLowPower:
    def setup_method(self):
        EnergyTrace().generate_energy_trace(20, 20)
        self.configuration = Configuration()
        self.configuration.set_scheduler(EDFLowPower())
        self.configuration.set_task_list(
            DirNames.SIMULATION_PARAMS.value
            + DirNames.LOW_POWER.value
            + "task_set_2.json"
        )
        self.simulation = Simulation(self.configuration)

    def test_initialization(self, task_list_3: List[Task]):
        assert self.simulation.tick_duration == ConfigParams.TICK_DURATION.value
        assert self.simulation.capacitor.energy == ConfigParams.ENERGY.value
        assert self.simulation.capacitor.max_energy == ConfigParams.MAX_ENERGY.value
        assert self.simulation.scheduler.ready_list == []
        assert self.simulation.task_list == task_list_3
        assert self.simulation.energy_trace == EnergyTrace().get_energy_trace()
        assert isinstance(self.simulation.scheduler, EDFLowPower)

    def test_task_set_2(self):
        pass
        pass
