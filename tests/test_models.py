from src.core.Capacitor import Capacitor
from src.core.tasks.Task import Task


class TestTask:
    task: Task

    def setup_method(self):
        self.task = Task(
            id=1,
            name="T1",
            period=20,
            activation_date=5,
            deadline=20,
            wcet=10,
            energy_requirement=5,
        )

    def test_initialization(self):
        assert self.task.id == 1
        assert self.task.name == "T1"
        assert self.task.period == 20
        assert self.task.activation_date == 5
        assert self.task.deadline == 20
        assert self.task.wcet == 10
        assert self.task.energy_requirement == 5
        assert self.task.next_activation == self.task.activation_date

    def test_is_ready(self):
        assert not self.task.is_ready(4)
        assert self.task.is_ready(5)
        assert self.task.is_ready(6)

    def test_activate_task(self):
        job = self.task.generate_job(1, 0)
        assert job.id == 1
        assert job.task_id == 1
        assert job.name == "T1"
        assert job.deadline == 20
        assert job.wcet == 10
        assert job.energy_requirement == 5
        assert job.time_remaining == 10
        assert self.task.next_activation == 25


class TestCapacitor:
    capacitor: Capacitor

    def setup_method(self):
        self.capacitor = Capacitor(100, 200)

    def test_initialization(self):
        assert self.capacitor.energy == 100
        assert self.capacitor.max_energy == 200

    def test_charge(self):
        self.capacitor.charge(50)
        assert self.capacitor.energy == 150
        self.capacitor.charge(100)
        assert self.capacitor.energy == 200

    def test_discharge(self):
        self.capacitor.discharge(50)
        assert self.capacitor.energy == 50
        self.capacitor.discharge(100)
        assert self.capacitor.energy == 0
