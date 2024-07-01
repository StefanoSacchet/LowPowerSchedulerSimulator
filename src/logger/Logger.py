from pydantic import BaseModel
import os

from src.core.tasks.Job import Job
from src.config.Config import TaskStates


class Logger(BaseModel):
    """Logger class to log simulation events"""

    log_dir: str
    log_file: str

    def __init__(self, log_dir: str, log_file: str):
        super().__init__(log_dir=log_dir, log_file=log_file)

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        with open(os.path.join(self.log_dir, self.log_file), "w") as f:
            f.write("job_id,task_id,name,state,tick\n")

    def log_csv(self, job: Job, state: TaskStates, tick: int) -> None:
        with open(os.path.join(self.log_dir, self.log_file), "a") as f:
            f.write(f"{job.id},{job.task_id},{job.name},{state},{tick}\n")
