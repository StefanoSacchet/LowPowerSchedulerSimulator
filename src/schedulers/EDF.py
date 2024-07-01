from src.models.Scheduler import Scheduler
from src.models.Job import Job


class EDF(Scheduler):
    """
    Earliest Deadline First scheduler
    """

    def init(self) -> None:
        self.ready_list = []

    def on_activate(self, task: Job) -> None:
        self.ready_list.append(task)

    def on_terminate(self, task: Job) -> None:
        self.ready_list.remove(task)

    def schedule(self) -> Job:
        # TODO heap q
        if len(self.ready_list) == 0:
            return None

        self.ready_list.sort(key=lambda x: x.deadline)
        return self.ready_list[0]
