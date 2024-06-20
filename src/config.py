from enum import Enum


# file names
class FileNames(Enum):
    RESULTS_DIR = "results/"  # direcotry for simulation results
    TASKS_DIR = "tasks/"  # directory for task sets
    LOGS_NAME = "logs.log"
    TASKS_NAME = "task_set.json"
    COMP_TIMES_NAME = "comp_times.log"
