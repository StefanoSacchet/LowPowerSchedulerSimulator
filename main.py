from src.models.Simulation import Simulation
from src.models.Capacitor import Capacitor
from src.models.Task import Task
from src.models.EnergyTrace import EnergyTrace

task_list = [
    Task(
        id=1,
        name="T1",
        period=10,
        deadline=10,
        wcet=3,
        energy_requirement=1,
    ),
    Task(
        id=2,
        name="T2",
        period=20,
        deadline=20,
        wcet=3,
        energy_requirement=2,
    ),
    Task(
        id=3,
        name="T3",
        period=30,
        deadline=30,
        wcet=5,
        energy_requirement=3,
    ),
]

if __name__ == "__main__":
    capacitor = Capacitor()
    sim = Simulation(
        tick_duration=1,
        capacitor=capacitor,
        task_list=task_list,
        energy_trace=EnergyTrace().get_energy_trace(),
    )
    sim.run()
