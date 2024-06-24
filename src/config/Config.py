from enum import Enum


class DirNames(Enum):
    RESULTS = "results/"
    SIMULATION_PARAMS = "simulation_params/"


class FileNames(Enum):
    ENERGY_TRACE = "energy_trace.log"
    TASK_SET = "task_set.json"


class ConfigCapacitor(Enum):
    ENERGY = 0
    MAX_ENERGY = 100
