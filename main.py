import os
import shutil
from typing import List

from src.config.Config import DirNames, FileNames
from src.core.Capacitor import Capacitor
from src.core.Configuration import Configuration
from src.core.EnergyTrace import EnergyTrace
from src.core.schedulers.ALAP import ALAP
from src.core.schedulers.Celebi import Celebi
from src.core.schedulers.EDF import EDF
from src.core.schedulers.RM import RM
from src.core.schedulers.Scheduler import Scheduler
from src.core.Simulation import Simulation
from src.logger.Logger import Logger
from src.plots.Plot import Plot


def plot_results(sim: Simulation, input_path: str, output_path: str) -> None:
    plot = Plot(sim.task_list)
    # plot task set
    plot.plot_task_set(sim.num_ticks, output_path=output_path)
    # plot results
    plot.plot_results(
        time_range=sim.num_ticks, input_path=input_path, output_path=output_path
    )
    # plot energy level
    plot.plot_energy_level(input_path=input_path, output_path=output_path)


def run_dataset() -> None:
    if os.path.exists(DirNames.RESULTS.value):
        shutil.rmtree(DirNames.RESULTS.value)

    capacitor = Capacitor(energy=100, max_energy=100)

    #! ALAP and Celebi are bugged
    scheduler_list: List[Scheduler] = [ALAP()]

    # for every task_set file in the task_sets directory
    for task_set_filename in os.listdir(
        DirNames.SIM_CONFIG.value + DirNames.TASK_SETS.value
    ):
        if not task_set_filename.endswith(".json"):
            raise ValueError("Invalid file format", task_set_filename)

        print(f"Running simulation {task_set_filename}")

        # get the corresponding energy trace file
        energy_trace_filename = task_set_filename.replace(
            "task_set", "energy_trace"
        ).replace(".json", ".log")

        config = Configuration(prediction_len=1, charge_mutually_exclusive=True)

        # simulate each scheduler
        for scheduler in scheduler_list:
            res_path = (
                DirNames.RESULTS.value
                + scheduler.name
                + "/"
                + task_set_filename.replace(".json", "")
            )

            config.set_capacitor(Capacitor(energy=100, max_energy=100))
            config.set_energy_trace(
                DirNames.SIM_CONFIG.value
                + DirNames.ENERGY_TRACES.value
                + energy_trace_filename
            )
            config.set_task_list(
                DirNames.SIM_CONFIG.value + DirNames.TASK_SETS.value + task_set_filename
            )
            config.set_scheduler(scheduler)
            # change logger to set the right path
            logger = Logger(
                res_path,
                FileNames.RESULTS.value,
                FileNames.ENERGY_LEVEL.value,
            )
            config.set_logger(logger)

            sim = Simulation(config)
            sim.run()

            plot_results(sim, input_path=res_path, output_path=res_path)

        print(f"Finished simulation {task_set_filename}")


def run_task_set_6() -> Simulation:
    # setup configuration for simulation, in this case we are using default values
    configuration = Configuration(prediction_len=1, charge_mutually_exclusive=True)
    configuration.set_capacitor(Capacitor(energy=100, max_energy=100))
    configuration.set_scheduler(ALAP())
    configuration.set_task_list(
        DirNames.SIM_CONFIG.value + DirNames.TASK_SETS.value + "task_set_6.json"
    )
    configuration.set_energy_trace(
        DirNames.SIM_CONFIG.value + DirNames.ENERGY_TRACES.value + "energy_trace_6.log"
    )

    # run simulation
    sim = Simulation(configuration)
    sim.run()

    return sim


if __name__ == "__main__":
    # sim = run_task_set_6()
    # plot_results(sim, "results/")

    sim = run_dataset()

    input("Press Enter to close...")
