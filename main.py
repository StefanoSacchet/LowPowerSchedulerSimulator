from src.models.Simulation import Simulation
from src.models.Configuration import Configuration
from src.plots.Plot import Plot
from src.models.EnergyTrace import EnergyTrace

if __name__ == "__main__":
    # generate energy trace
    EnergyTrace().generate_energy_trace(20, 150)

    # setup configuration for simulation, in this case we are using default values
    configuration = Configuration()

    configuration.set_task_list("./simulation_params/task_set_2.json")

    # run simulation
    sim = Simulation(configuration)
    sim.run()

    plot = Plot(sim.task_list)
    # plot task set
    plot.plot_task_set(sim.num_ticks, save=True)
    # plot results
    plot.plot_results(save=True)

    input("Press Enter to close...")
