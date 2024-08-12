from enum import Enum


class DirNames(Enum):
    RESULTS = "results/"
    SIMULATION_PARAMS = "simulation_params/"
    SIM_CONFIG = "sim_config/"
    TASK_SETS = "task_sets/"
    ENERGY_TRACES = "energy_traces/"
    NORMAL = "normal/"
    LOW_POWER = "low_power/"


class FileNames(Enum):
    ENERGY_TRACE = "energy_trace"
    TASK_SET = "task_set"
    PLOT_TASK_SET = "plot_task_set.png"
    PLOT_RESULTS = "plot_results.png"
    PLOT_ENERGY_LEVEL = "plot_energy_level.png"
    RESULTS = "results.csv"
    ENERGY_LEVEL = "energy_level.csv"


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
