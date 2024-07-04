import os

from pydantic import BaseModel

from src.config.Config import TaskStates
from src.core.tasks.Job import Job


class Logger(BaseModel):
    """Logger class to log simulation events"""

    log_dir: str
    res_file: str
    energy_level_file: str

    def __init__(self, log_dir: str, res_file: str, energy_level_file: str):
        super().__init__(
            log_dir=log_dir, res_file=res_file, energy_level_file=energy_level_file
        )

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        with open(os.path.join(self.log_dir, self.res_file), "w") as f:
            f.write("job_id,task_id,name,state,tick\n")

        with open(os.path.join(self.log_dir, self.energy_level_file), "w") as f:
            f.write("energy,tick\n")

    def log_csv(self, job: Job, state: TaskStates, tick: int) -> None:
        with open(os.path.join(self.log_dir, self.res_file), "a") as f:
            f.write(f"{job.id},{job.task_id},{job.name},{state.value},{tick}\n")

    def log_energy_level(self, energy: float, tick: int) -> None:
        with open(os.path.join(self.log_dir, self.energy_level_file), "a") as f:
            f.write(f"{energy},{tick}\n")
