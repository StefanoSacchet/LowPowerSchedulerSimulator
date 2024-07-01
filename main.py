from src.core.Simulation import Simulation
from src.core.Configuration import Configuration
from src.plots.Plot import Plot
from src.core.EnergyTrace import EnergyTrace


def run_task_set_1() -> Simulation:
    # generate energy trace
    EnergyTrace().generate_energy_trace(20, 20)

    # setup configuration for simulation, in this case we are using default values
    configuration = Configuration()

    configuration.set_task_list("./simulation_params/task_set_1.json")

    # run simulation
    sim = Simulation(configuration)
    sim.run()

    return sim


def run_task_set_2() -> Simulation:
    # generate energy trace
    EnergyTrace().generate_energy_trace(20, 150)

    # setup configuration for simulation, in this case we are using default values
    configuration = Configuration()

    configuration.set_task_list("./simulation_params/task_set_2.json")

    # run simulation
    sim = Simulation(configuration)
    sim.run()

    return sim


def run_task_set_3() -> Simulation:
    # generate energy trace
    EnergyTrace().generate_energy_trace(20, 25)

    # setup configuration for simulation, in this case we are using default values
    configuration = Configuration()

    configuration.set_task_list("./simulation_params/task_set_3.json")

    # run simulation
    sim = Simulation(configuration)
    sim.run()

    return sim


if __name__ == "__main__":
    # sim = run_task_set_1()
    # sim = run_task_set_2()
    sim = run_task_set_3()

    plot = Plot(sim.task_list)
    # plot task set
    plot.plot_task_set(sim.num_ticks, save=True)
    # plot results
    plot.plot_results(sim.num_ticks, save=True)

    input("Press Enter to close...")
