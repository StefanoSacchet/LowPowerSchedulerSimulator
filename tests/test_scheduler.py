import pytest

from src.schedulers.EDF import EDF
from src.models.Task import Task


@pytest.fixture
def tasks():
    return [
        Task(
            id=1,
            name="T1",
            period=20,
            activation_date=5,
            deadline=20,
            wcet=10,
            energy_requirement=5,
        ),
        Task(
            id=2,
            name="T2",
            period=30,
            activation_date=10,
            deadline=30,
            wcet=15,
            energy_requirement=10,
        ),
    ]


class TestSchedulerEDF:
    scheduler: EDF

    def setup_method(self):
        self.scheduler = EDF()

    def test_init(self):
        self.scheduler.init()
        assert self.scheduler.ready_list == []

    def test_on_activate(self, tasks):
        self.scheduler.on_activate(tasks[0])
        assert self.scheduler.ready_list == [tasks[0]]
        self.scheduler.on_activate(tasks[1])
        assert self.scheduler.ready_list == [tasks[0], tasks[1]]

    def test_on_terminate(self, tasks):
        self.scheduler.on_activate(tasks[0])
        self.scheduler.on_activate(tasks[1])
        assert self.scheduler.ready_list == tasks
        self.scheduler.on_terminate(tasks[0])
        assert self.scheduler.ready_list == [tasks[1]]
        self.scheduler.on_terminate(tasks[1])
        assert self.scheduler.ready_list == []
