from src.config.Config import DirNames
from src.core.Capacitor import Capacitor
from src.core.Configuration import Configuration
from src.core.EnergyTrace import EnergyTrace
from src.core.Simulation import Simulation
from src.plots.Plot import Plot


def run_task_set_1() -> Simulation:
    # generate energy trace
    # EnergyTrace().generate_energy_trace(5, 20)

    # setup configuration for simulation, in this case we are using default values
    configuration = Configuration()
    configuration.set_capacitor(Capacitor(energy=50, max_energy=100))

    configuration.set_task_list(
        DirNames.SIMULATION_PARAMS.value + DirNames.LOW_POWER.value + "task_set_1.json"
    )

    # run simulation
    sim = Simulation(configuration)
    sim.run()

    return sim


def run_task_set_2() -> Simulation:
    # generate energy trace
    EnergyTrace().generate_energy_trace(20, 150)

    # setup configuration for simulation, in this case we are using default values
    configuration = Configuration()

    configuration.set_task_list(
        DirNames.SIMULATION_PARAMS.value + DirNames.LOW_POWER.value + "task_set_2.json"
    )

    # run simulation
    sim = Simulation(configuration)
    sim.run()

    return sim


def run_task_set_3() -> Simulation:
    # generate energy trace
    EnergyTrace().generate_energy_trace(20, 25)

    # setup configuration for simulation, in this case we are using default values
    configuration = Configuration()

    configuration.set_task_list(
        DirNames.SIMULATION_PARAMS.value + DirNames.NORMAL.value + "task_set_3.json"
    )

    # run simulation
    sim = Simulation(configuration)
    sim.run()

    return sim


if __name__ == "__main__":
    sim = run_task_set_1()
    # sim = run_task_set_2()
    # sim = run_task_set_3()

    plot = Plot(sim.task_list)
    # plot task set
    plot.plot_task_set(sim.num_ticks, save=True)
    # plot results
    plot.plot_results(sim.num_ticks, save=True)

    input("Press Enter to close...")
 