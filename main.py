from src.models.Simulation import Simulation
from src.models.Configuration import Configuration

if __name__ == "__main__":
    # get configuration for simulation, task_list is read from file
    configuration = Configuration()
    # run simulation
    sim = Simulation(configuration)
    sim.run()
