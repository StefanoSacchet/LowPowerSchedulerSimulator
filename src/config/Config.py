from enum import Enum


class DirNames(Enum):
    RESULTS = "results/"
    SIMULATION_PARAMS = "simulation_params/"
    NORMAL = "normal/"
    LOW_POWER = "low_power/"


class FileNames(Enum):
    ENERGY_TRACE = "energy_trace.log"
    TASK_SET = "task_set_1.json"
    PLOT_TASK_SET = "plot_task_set.png"
    PLOT_RESULTS = "plot_results.png"
    RESULTS = "results.csv"


class Schedulers(Enum):
    EDF = "EDF"


class TaskStates(Enum):
    ACTIVATED = "ACTIVATED"
    EXECUTING = "EXECUTING"
    TERMINATED = "TERMINATED"
    MISSED_DEADLINE = "MISSED_DEADLINE"
    NOP = "NOP"


class ConfigParams(Enum):
    TICK_DURATION = 1

    # capacitor
    ENERGY = 100.0
    MAX_ENERGY = 100
