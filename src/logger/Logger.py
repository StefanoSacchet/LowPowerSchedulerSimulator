from pydantic import BaseModel
import os


class Logger(BaseModel):
    """Logger class to log simulation events"""

    log_dir: str
    log_file: str

    def __init__(self, log_dir: str, log_file: str):
        super().__init__(log_dir=log_dir, log_file=log_file)

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        with open(os.path.join(self.log_dir, self.log_file), "w") as f:
            f.write("id,name,state,tick\n")

    def log_csv(self, id: int, name: str, state: str, tick: int):
        with open(os.path.join(self.log_dir, self.log_file), "a") as f:
            f.write(f"{id},{name},{state},{tick}\n")
