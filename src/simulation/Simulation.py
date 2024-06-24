from pydantic import BaseModel, ConfigDict
from typing import List
from simso.core import Model
from simso.configuration import Configuration
import os
import json

from src.config import FileNames
from src.plots.plot_task_set import plot_task_set
from src.plots.plot_results import plot_results
from src.types.CustomTask import CustomTask


class Simulation(BaseModel):
    """Simulation class that runs the simulation using the task set and configuration"""

    task_list: List[CustomTask] = []
    configuration: Configuration = None
    model: Model = None

    def get_task_set(self) -> List[CustomTask]:
        # read json file
        task_list: List[CustomTask] = []
        with open(FileNames.TASKS_DIR.value + FileNames.TASKS_NAME.value) as f:
            data = json.load(f)
            # Convert JSON data to Task objects
            task_list = [CustomTask(**task_data) for task_data in data["tasks"]]

        return task_list

    def save_results(self) -> None:
        # create a directory to save the results
        os.path.exists(FileNames.RESULTS_DIR.value) or os.makedirs(
            FileNames.RESULTS_DIR.value
        )

        # save logs
        with open(FileNames.RESULTS_DIR.value + FileNames.LOGS_NAME.value, "w") as f:
            for log in self.model.logs:
                f.write(str(log) + "\n")

        # save computation times
        with open(
            FileNames.RESULTS_DIR.value + FileNames.COMP_TIMES_NAME.value,
            "w",
        ) as f:
            for task in self.model.results.tasks:
                f.write(task.name + ":\n")
                for job in task.jobs:
                    f.write("%s %.3f ms\n" % (job.name, job.computation_time))

    def set_config(self) -> None:
        config = Configuration()
        config.duration = 420 * config.cycles_per_ms
        # add tasks to the configuration
        for task in self.task_list:
            config.add_task(
                name=task.name,
                identifier=task.identifier,
                period=task.period,
                activation_date=task.activation_date,
                wcet=task.wcet,
                deadline=task.deadline,
                data=task.energy_consumption,  # use data field to store energy
            )

        # add a processor
        config.add_processor(name="CPU 1", identifier=1)

        # add a scheduler
        config.scheduler_info.filename = "./src/schedulers/EDF_mono.py"
        # configuration.scheduler_info.clas = "simso.schedulers.RM"

        # check the config before trying to run it
        config.check_all()

        return config

    def run_sim(self, plot: bool) -> None:
        self.model.run_model()
        self.save_results()
        if plot:
            # plot tasks gantt chart
            plot_task_set(self.task_list, save=True)
            # plot results gantt chart
            plot_results(save=True)

    def __init__(self):
        super().__init__()
        self.task_list = self.get_task_set()
        self.configuration = self.set_config()
        self.model = Model(self.configuration)

    # Pydantic configuration
    model_config = ConfigDict(arbitrary_types_allowed=True)
