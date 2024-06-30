import pandas as pd

from src.config.Config import DirNames, FileNames, TaskStates

with open(DirNames.RESULTS.value + FileNames.RESULTS.value, "r") as f:
    results = pd.read_csv(f)

result = results.query('tick == 10 and id == 2 and state == "ACTIVATED"')
print(result)
print("*" * 5)
print(len(result))
