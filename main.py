import os
from simso.core import Model
from simso.configuration import Configuration
from typing import List

from src.types.Task import Task
from src.plots.plot_task_set import plot_task_set
from src.plots.plot_results import plot_results
from src.config import FileNames


# This function is used to generate tasks for the simulation
def generate_tasks() -> List[Task]:
    return [
        Task(
            name="T1",
            identifier=1,
            period=7,
            activation_date=0,
            wcet=3,
            deadline=7,
        ),
        Task(
            name="T2",
            identifier=2,
            period=12,
            activation_date=0,
            wcet=3,
            deadline=12,
        ),
        Task(
            name="T3",
            identifier=3,
            period=20,
            activation_date=0,
            wcet=5,
            deadline=20,
        ),
    ]


def save_results(model: Model) -> None:
    # create a directory to save the results
    os.path.exists(FileNames.RESULTS_DIR.value) or os.makedirs(
        FileNames.RESULTS_DIR.value
    )

    # save logs
    with open(
        os.path.join(FileNames.RESULTS_DIR.value, FileNames.LOGS_NAME.value), "w"
    ) as f:
        for log in model.logs:
            f.write(str(log) + "\n")

    # save computation times
    with open(
        os.path.join(FileNames.RESULTS_DIR.value, FileNames.COMP_TIMES_NAME.value), "w"
    ) as f:
        for task in model.results.tasks:
            f.write(task.name + ":\n")
            for job in task.jobs:
                f.write("%s %.3f ms\n" % (job.name, job.computation_time))


def main():
    # manual configuration
    configuration = Configuration()

    configuration.duration = 420 * configuration.cycles_per_ms

    # get generates tasks
    task_list: List[Task] = generate_tasks()

    # add tasks to the configuration
    for task in task_list:
        configuration.add_task(
            name=task.name,
            identifier=task.identifier,
            period=task.period,
            activation_date=task.activation_date,
            wcet=task.wcet,
            deadline=task.deadline,
        )

    # add a processor
    configuration.add_processor(name="CPU 1", identifier=1)

    # add a scheduler
    configuration.scheduler_info.filename = "./src/schedulers/EDF_mono.py"
    # configuration.scheduler_info.clas = "simso.schedulers.RM"

    # check the config before trying to run it
    configuration.check_all()

    # init a model from the configuration
    model = Model(configuration)

    # execute the simulation
    model.run_model()

    # save the results
    save_results(model)

    # plot the gantt chart
    plot_task_set(task_list)
    # plot the results
    plot_results()


if __name__ == "__main__":
    main()
