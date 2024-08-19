import os
import random
import shutil
from typing import List

from pydantic import BaseModel

from src.config.Config import DirNames, FileNames
from src.core.tasks.Task import Task

# Define the energy consumption levels
ENERGY_CONSUMPTION_LEVELS = {
    "level_1": 6,  # Low energy consumption rate (e.g., low power mode)
    "level_2": 8,  # Medium energy consumption rate (e.g., active mode)
    "level_3": 10,  # High energy consumption rate (e.g., with sensors)
}


class Generator(BaseModel):
    cpu_utilization: float
    min_period: int
    max_period: int
    min_task_num: int
    max_task_num: int

    _task_sets: List[List[Task]] = []
    _energy_traces: List[List[int]] = []

    def __init__(
        self,
        cpu_utilization: float,
        min_period: int = 4,
        max_period: int = 600,
        min_task_num: int = 2,
        max_task_num: int = 10,
    ):
        super().__init__(
            cpu_utilization=cpu_utilization,
            min_period=min_period,
            max_period=max_period,
            min_task_num=min_task_num,
            max_task_num=max_task_num,
        )

    @staticmethod
    def delete_dataset() -> None:
        if os.path.exists(DirNames.SIM_CONFIG.value):
            shutil.rmtree(DirNames.SIM_CONFIG.value)
        else:
            raise FileNotFoundError(f"Dataset not found at {DirNames.SIM_CONFIG.value}")

    def generate_task_set(self) -> List[Task]:
        # Randomly select the number of tasks
        num_tasks = random.randint(self.min_task_num, self.max_task_num)

        # Generate random periods for each task
        periods = [
            random.randint(self.min_period, self.max_period) for _ in range(num_tasks)
        ]

        # Calculate the initial WCETs based on CPU utilization
        total_utilization = 0
        wcets = []
        for period in periods:
            wcet = random.uniform(
                1, period // 2
            )  # Ensure WCET is bounded between 1 and half the period
            wcets.append(wcet)
            total_utilization += wcet / period

        # Scale WCETs to match the desired CPU utilization
        scaling_factor = self.cpu_utilization / total_utilization
        wcets = [max(1, round(wcet * scaling_factor)) for wcet in wcets]

        # Generate the list of Task objects
        tasks = []
        for i in range(num_tasks):
            # Randomly select an energy consumption rate
            energy_requirement = random.choice(list(ENERGY_CONSUMPTION_LEVELS.values()))

            task = Task(
                id=i + 1,
                name=f"T{i + 1}",
                period=periods[i],
                activation_date=0,  # Assuming all tasks are activated at time 0
                deadline=periods[i],  # Assuming the deadline equals the period
                wcet=wcets[i],
                energy_requirement=energy_requirement,
            )
            tasks.append(task)

        return tasks

    def generate_dataset(self, num_task_sets: int) -> None:
        assert num_task_sets > 0, "Number of task sets must be greater than 0"

        for _ in range(num_task_sets):
            # generate task set
            task_set = self.generate_task_set()
            self._task_sets.append(task_set)

            # generate energy trace
            energy_trace = [
                random.randint(1, 3)
                for _ in range(sum(task.period for task in task_set))
            ]
            self._energy_traces.append(energy_trace)

    def save_dataset(self, path: str) -> None:
        os.makedirs(os.path.join(path + DirNames.TASK_SETS.value))
        os.makedirs(os.path.join(path + DirNames.ENERGY_TRACES.value))

        # Save task sets
        for i, task_set in enumerate(self._task_sets):
            with open(
                f"{os.path.join(path, DirNames.TASK_SETS.value)}{FileNames.TASK_SET.value}_{i + 1}.json",
                "w",
            ) as f:
                f.write("[\n")
                for j, task in enumerate(task_set):
                    # Check if it's the last element
                    if j < len(task_set) - 1:
                        f.write(task.model_dump_json() + ",\n")
                    else:
                        f.write(task.model_dump_json() + "\n")
                f.write("]\n")

        # Save energy traces
        for i, energy_trace in enumerate(self._energy_traces):
            with open(
                f"{os.path.join(path, DirNames.ENERGY_TRACES.value)}{FileNames.ENERGY_TRACE.value}_{i + 1}.log",
                "w",
            ) as f:
                for energy in energy_trace:
                    f.write(f"{energy}\n")
