import sys
from simso.core import Model
from simso.configuration import Configuration
from typing import List

from src.types.Task import Task


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


def main(argv):
    if len(argv) == 2:
        # configuration load from a file
        configuration = Configuration(argv[1])
    else:
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

    # print logs
    for log in model.logs:
        print(log)

    # print computation times
    for task in model.results.tasks:
        print(task.name + ":")
        for job in task.jobs:
            print("%s %.3f ms" % (job.name, job.computation_time))


if __name__ == "__main__":
    main(sys.argv)
