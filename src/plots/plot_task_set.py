import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import List

from src.config import FileNames
from src.types.CustomTask import CustomTask


def plot_task_set(tasks: List[CustomTask], save: bool = False) -> None:
    # Determine the plotting range
    time_range = max(task.deadline for task in tasks) * 2

    # Plot Gantt chart
    fig, ax = plt.subplots(figsize=(10, 6))

    for task in tasks:
        periods = range(task.activation_date, time_range, task.period)
        for start in periods:
            ax.broken_barh(
                [(start, task.wcet)],
                (task.identifier - 0.4, 0.8),
                facecolors=("tab:orange"),
            )

    # Configure plot
    ax.set_xlabel("Time")
    ax.set_ylabel("Task Identifier")
    ax.set_yticks([task.identifier for task in tasks])
    ax.set_yticklabels([task.name for task in tasks])
    ax.grid(True)

    # Create legend
    patch = mpatches.Patch(color="tab:orange", label="Task Execution")
    plt.legend(handles=[patch])

    # Set title
    plt.title("Task Set Gantt Chart")

    if save:
        # Save plot
        plt.savefig(FileNames.RESULTS_DIR.value + "task_set.png")

    # Show plot
    plt.show()
