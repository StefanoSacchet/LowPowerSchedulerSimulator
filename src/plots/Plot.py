from pydantic import BaseModel
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

from src.models.Configuration import Configuration
from src.config.Config import DirNames, FileNames


class Plot(BaseModel):
    """Used to plot simulation data"""

    def plot_results(self) -> None:
        pass

    def plot_task_set(self, num_ticks: int = None, save: bool = False) -> None:
        task_set = Configuration().get_task_list()
        # Determine the plotting range
        if num_ticks:
            time_range = num_ticks
        else:
            time_range = max(task.deadline for task in task_set) * 2

        # Plot Gantt chart
        fig, ax = plt.subplots(figsize=(10, 6))

        for task in task_set:
            periods = range(task.activation_date, time_range, task.period)
            for start in periods:
                ax.broken_barh(
                    [(start, task.wcet)],
                    (task.id - 0.4, 0.8),
                    facecolors=("tab:orange"),
                )

        # Configure plot
        ax.set_xlabel("Time")
        ax.set_ylabel("Task Identifier")
        ax.set_yticks([task.id for task in task_set])
        ax.set_yticklabels([task.name for task in task_set])
        ax.grid(True)

        # Create legend
        patch = mpatches.Patch(color="tab:orange", label="Task Execution")
        plt.legend(handles=[patch])

        # Set title
        plt.title("Task Set Gantt Chart")

        if save:
            # Save plot
            if not os.path.exists(DirNames.RESULTS.value):
                os.makedirs(DirNames.RESULTS.value)
            plt.savefig(DirNames.RESULTS.value + FileNames.PLOT_TASK_SET.value)

        # Show plot
        plt.show()
