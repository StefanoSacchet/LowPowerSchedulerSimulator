from src.models.Scheduler import Scheduler
from src.models.Task import Task


class EDF(Scheduler):
    """Earliest Deadline First scheduler"""

    def init(self) -> None:
        self.ready_list = []

    def on_activate(self, task: Task) -> None:
        self.ready_list.append(task)

    def on_terminate(self, task: Task) -> None:
        self.ready_list.remove(task)

    def schedule(self) -> Task:
        if len(self.ready_list) == 0:
            return None

        self.ready_list.sort(key=lambda x: x.next_deadline)
        return self.ready_list[0]
