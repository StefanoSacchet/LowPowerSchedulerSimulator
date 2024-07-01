from src.core.schedulers.Scheduler import Scheduler
from src.core.tasks.Job import Job


class EDF(Scheduler):
    """
    Earliest Deadline First scheduler

    Attributes:
        ready_list: List[Job] - list of jobs that are ready to be scheduled
        energy: int - energy of the capacitor
    """

    def init(self) -> None:
        self.ready_list = []

    def on_activate(self, task: Job) -> None:
        self.ready_list.append(task)

    def on_terminate(self, task: Job) -> None:
        self.ready_list.remove(task)

    def on_energy_update(self, energy: int) -> None:
        self.energy = energy

    def schedule(self) -> Job:
        # TODO heap q

        if len(self.ready_list) == 0:
            return None

        self.ready_list.sort(key=lambda x: x.deadline)

        # find first job with sufficient energy
        for job in self.ready_list:
            if job.energy_requirement <= self.energy:
                return job

        return None
