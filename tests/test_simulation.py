import pytest
import json
import pandas as pd
from typing import List

from src.models.Simulation import Simulation
from src.models.Configuration import Configuration
from src.models.Task import Task
from src.config.Config import ConfigParams, DirNames, FileNames
from src.models.EnergyTrace import EnergyTrace
from src.config.Config import TaskStates


@pytest.fixture
def task_list() -> List[Task]:
    with open(DirNames.SIMULATION_PARAMS.value + "task_set_2.json", "r") as f:
        task_list = json.load(f)

    return [Task(**task) for task in task_list["task_set"]]


class TestSimulation:
    configuration: Configuration
    simulation: Simulation

    def setup_method(self):
        self.configuration = Configuration()
        self.configuration.set_task_list("./simulation_params/task_set_2.json")
        self.simulation = Simulation(self.configuration)

    def test_initialization(self, task_list: List[Task]):
        assert self.simulation.tick_duration == ConfigParams.TICK_DURATION.value
        assert self.simulation.capacitor.energy == ConfigParams.ENERGY.value
        assert self.simulation.capacitor.max_energy == ConfigParams.MAX_ENERGY.value
        assert self.simulation.scheduler.ready_list == []
        assert self.simulation.task_list == task_list
        assert self.simulation.energy_trace == EnergyTrace().get_energy_trace()

    def test_task_set_2(self):
        self.simulation.run()
        with open(DirNames.RESULTS.value + FileNames.RESULTS.value, "r") as f:
            results = pd.read_csv(f)

        # test task activation
        assert results["state"][0] == TaskStates.ACTIVATED.value
        assert results["state"][1] == TaskStates.ACTIVATED.value

        results_tick_50 = results[results["tick"] == 50]
        assert TaskStates.ACTIVATED.value in results_tick_50["state"].values

        results_tick_75 = results[results["tick"] == 75]
        assert TaskStates.ACTIVATED.value in results_tick_75["state"].values

        results_tick_100 = results[results["tick"] == 100]
        assert TaskStates.ACTIVATED.value in results_tick_100["state"].values

        # test task termination
        results_tick_24 = results[results["tick"] == 24]
        assert TaskStates.TERMINATED.value in results_tick_24["state"].values

        results_tick_54 = results[results["tick"] == 54]
        assert TaskStates.TERMINATED.value in results_tick_54["state"].values

        results_tick_79 = results[results["tick"] == 79]
        assert TaskStates.TERMINATED.value in results_tick_79["state"].values

        results_tick_109 = results[results["tick"] == 109]
        assert TaskStates.TERMINATED.value in results_tick_109["state"].values

        results_tick_134 = results[results["tick"] == 134]
        assert TaskStates.TERMINATED.value in results_tick_134["state"].values
