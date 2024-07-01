import pytest
import json
import pandas as pd
from typing import List

from src.core.Simulation import Simulation
from src.core.Configuration import Configuration
from src.core.tasks.Task import Task
from src.config.Config import ConfigParams, DirNames, FileNames
from src.core.EnergyTrace import EnergyTrace
from src.config.Config import TaskStates
from src.core.schedulers.EDF import EDF

"""
ALL TESTS ARE BASED ON THE EDF SCHEDULER
"""


@pytest.fixture
def task_list_1() -> List[Task]:
    with open(
        DirNames.SIMULATION_PARAMS.value + DirNames.NORMAL.value + "task_set_1.json",
        "r",
    ) as f:
        task_list = json.load(f)

    return [Task(**task) for task in task_list["task_set"]]


@pytest.fixture
def task_list_2() -> List[Task]:
    with open(
        DirNames.SIMULATION_PARAMS.value + DirNames.NORMAL.value + "task_set_2.json",
        "r",
    ) as f:
        task_list = json.load(f)

    return [Task(**task) for task in task_list["task_set"]]


@pytest.fixture
def task_list_3() -> List[Task]:
    with open(
        DirNames.SIMULATION_PARAMS.value + DirNames.NORMAL.value + "task_set_3.json",
        "r",
    ) as f:
        task_list = json.load(f)

    return [Task(**task) for task in task_list["task_set"]]


# @pytest.mark.skip()
class TestSimulation1:
    configuration: Configuration
    simulation: Simulation

    def setup_method(self):
        EnergyTrace().generate_energy_trace(20, 20)
        self.configuration = Configuration()
        self.configuration.set_scheduler(EDF())
        self.configuration.set_task_list(
            DirNames.SIMULATION_PARAMS.value + DirNames.NORMAL.value + "task_set_1.json"
        )
        self.simulation = Simulation(self.configuration)

    def test_initialization(self, task_list_1: List[Task]):
        assert self.simulation.tick_duration == ConfigParams.TICK_DURATION.value
        assert self.simulation.capacitor.energy == ConfigParams.ENERGY.value
        assert self.simulation.capacitor.max_energy == ConfigParams.MAX_ENERGY.value
        assert self.simulation.scheduler.ready_list == []
        assert self.simulation.task_list == task_list_1
        assert self.simulation.energy_trace == EnergyTrace().get_energy_trace()
        assert isinstance(self.simulation.scheduler, EDF)

    def test_task_set_1(self):
        self.simulation.run()
        with open(DirNames.RESULTS.value + FileNames.RESULTS.value, "r") as f:
            results = pd.read_csv(f)

        # test intitial task activation
        assert results["state"][0] == TaskStates.ACTIVATED.value
        assert results["state"][1] == TaskStates.ACTIVATED.value
        assert results["state"][2] == TaskStates.ACTIVATED.value

        # test task activation
        res = results.query(
            f'tick == 5 and task_id == 2 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) > 0
        res = results.query(
            f'tick == 10 and task_id == 2 and state =="{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) > 0
        res = results.query(
            f'tick == 10 and task_id == 3 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) > 0
        res = results.query(
            f'tick == 15 and task_id == 2 and state == "{TaskStates.ACTIVATED.value}"'
        )

        # test that taks are activated the correct number of times
        res = results.query(f'task_id == 1 and state == "{TaskStates.ACTIVATED.value}"')
        assert len(res) == 1
        res = results.query(f'task_id == 2 and state == "{TaskStates.ACTIVATED.value}"')
        assert len(res) == 4
        res = results.query(f'task_id == 3 and state == "{TaskStates.ACTIVATED.value}"')
        assert len(res) == 2

        # test task termination
        res = results.query(
            f'tick == 2 and task_id == 2 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) > 0
        res = results.query(
            f'tick == 5 and task_id == 1 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) > 0
        res = results.query(
            f'tick == 7 and task_id == 3 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) > 0
        res = results.query(
            f'tick == 9 and task_id == 2 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) > 0
        res = results.query(
            f'tick == 12 and task_id == 2 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) > 0
        res = results.query(
            f'tick == 14 and task_id == 3 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) > 0
        res = results.query(
            f'tick == 17 and task_id == 2 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) > 0

        # test no missed deadlines
        res = results.query(f'state == "{TaskStates.MISSED_DEADLINE.value}"')
        assert len(res) == 0


class TestSimulation2:
    configuration: Configuration
    simulation: Simulation

    def setup_method(self):
        EnergyTrace().generate_energy_trace(20, 150)
        self.configuration = Configuration()
        self.configuration.set_scheduler(EDF())
        self.configuration.set_task_list(
            DirNames.SIMULATION_PARAMS.value + DirNames.NORMAL.value + "task_set_2.json"
        )
        self.simulation = Simulation(self.configuration)

    def test_initialization(self, task_list_2: List[Task]):
        assert self.simulation.tick_duration == ConfigParams.TICK_DURATION.value
        assert self.simulation.capacitor.energy == ConfigParams.ENERGY.value
        assert self.simulation.capacitor.max_energy == ConfigParams.MAX_ENERGY.value
        assert self.simulation.scheduler.ready_list == []
        assert self.simulation.task_list == task_list_2
        assert self.simulation.energy_trace == EnergyTrace().get_energy_trace()
        assert isinstance(self.simulation.scheduler, EDF)

    def test_task_set_2(self):
        self.simulation.run()
        with open(DirNames.RESULTS.value + FileNames.RESULTS.value, "r") as f:
            results = pd.read_csv(f)

        # test initial task activation
        assert results["state"][0] == TaskStates.ACTIVATED.value
        assert results["state"][1] == TaskStates.ACTIVATED.value

        # test task activation
        res = results.query(
            f'tick == 50 and task_id == 1 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) > 0
        res = results.query(
            f'tick == 75 and task_id == 2 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) > 0
        res = results.query(
            f'tick == 100 and task_id == 1 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) > 0

        # test that taks are activated the correct number of times
        res = results.query(f'task_id == 1 and state == "{TaskStates.ACTIVATED.value}"')
        assert len(res) == 3
        res = results.query(f'task_id == 2 and state == "{TaskStates.ACTIVATED.value}"')
        assert len(res) == 2

        # test task termination
        res = results.query(
            f'tick == 25 and task_id == 1 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) > 0
        res = results.query(
            f'tick == 55 and task_id == 2 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) > 0
        res = results.query(
            f'tick == 80 and task_id == 1 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) > 0
        res = results.query(
            f'tick == 110 and task_id == 2 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) > 0
        res = results.query(
            f'tick == 135 and task_id == 1 and state == "{TaskStates.TERMINATED.value}"'
        )

        # test no missed deadlines
        res = results.query(f'state == "{TaskStates.MISSED_DEADLINE.value}"')
        assert len(res) == 0


# @pytest.mark.skip()
class TestSimulation3:
    configuration: Configuration
    simulation: Simulation

    def setup_method(self):
        EnergyTrace().generate_energy_trace(20, 25)
        self.configuration = Configuration()
        self.configuration.set_scheduler(EDF())
        self.configuration.set_task_list(
            DirNames.SIMULATION_PARAMS.value + DirNames.NORMAL.value + "task_set_3.json"
        )
        self.simulation = Simulation(self.configuration)

    def test_initialization(self, task_list_3: List[Task]):
        assert self.simulation.tick_duration == ConfigParams.TICK_DURATION.value
        assert self.simulation.capacitor.energy == ConfigParams.ENERGY.value
        assert self.simulation.capacitor.max_energy == ConfigParams.MAX_ENERGY.value
        assert self.simulation.scheduler.ready_list == []
        assert self.simulation.task_list == task_list_3
        assert self.simulation.energy_trace == EnergyTrace().get_energy_trace()
        assert isinstance(self.simulation.scheduler, EDF)

    def test_task_set_3(self):
        self.simulation.run()
        with open(DirNames.RESULTS.value + FileNames.RESULTS.value, "r") as f:
            results = pd.read_csv(f)

        # test initial task activation
        assert results["state"][0] == TaskStates.ACTIVATED.value
        assert results["state"][1] == TaskStates.ACTIVATED.value
        assert results["state"][2] == TaskStates.ACTIVATED.value
        assert results["state"][3] == TaskStates.ACTIVATED.value

        # test task activation
        res = results.query(
            f'tick == 5 and task_id == 1 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 6 and task_id == 2 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 7 and task_id == 3 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 8 and task_id == 4 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 10 and task_id == 1 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 12 and task_id == 2 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 14 and task_id == 3 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 15 and task_id == 1 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 16 and task_id == 4 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 18 and task_id == 2 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 20 and task_id == 1 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 21 and task_id == 3 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 24 and task_id == 2 and state == "{TaskStates.ACTIVATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 24 and task_id == 4 and state == "{TaskStates.ACTIVATED.value}"'
        )

        # test that taks are activated the correct number of times
        res = results.query(f'task_id == 1 and state == "{TaskStates.ACTIVATED.value}"')
        assert len(res) == 5
        res = results.query(f'task_id == 2 and state == "{TaskStates.ACTIVATED.value}"')
        assert len(res) == 5
        res = results.query(f'task_id == 3 and state == "{TaskStates.ACTIVATED.value}"')
        assert len(res) == 4
        res = results.query(f'task_id == 4 and state == "{TaskStates.ACTIVATED.value}"')
        assert len(res) == 4

        # test task termination
        res = results.query(
            f'tick == 2 and task_id == 1 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 4 and task_id == 2 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 6 and task_id == 3 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 8 and task_id == 4 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 10 and task_id == 1 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 12 and task_id == 2 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 14 and task_id == 3 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 16 and task_id == 1 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) == 0
        res = results.query(
            f'tick == 16 and task_id == 4 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) == 0
        res = results.query(
            f'tick == 18 and task_id == 2 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 20 and task_id == 1 and state == "{TaskStates.TERMINATED.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 23 and task_id == 4 and state == "{TaskStates.TERMINATED.value}"'
        )

        # test missed deadlines
        res = results.query(
            f'tick == 15 and task_id == 1 and state == "{TaskStates.MISSED_DEADLINE.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 16 and task_id == 4 and state == "{TaskStates.MISSED_DEADLINE.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 21 and task_id == 3 and state == "{TaskStates.MISSED_DEADLINE.value}"'
        )
        assert len(res) == 1
        res = results.query(
            f'tick == 24 and task_id == 2 and state == "{TaskStates.MISSED_DEADLINE.value}"'
        )
        assert len(res) == 1
