from pydantic import BaseModel
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
from itertools import cycle
from typing import List

from src.models.Configuration import Configuration
from src.models.Task import Task
from src.config.Config import DirNames, FileNames


class Plot(BaseModel):
    """Used to plot simulation data"""

    def plot_results(self) -> None:
        pass

    def plot_task_set(self, num_ticks: int, task_list: List[Task], save: bool = False) -> None:
        time_range = num_ticks

        # Determine the plotting range
        # if num_ticks:
        #     time_range = num_ticks
        # else:
        #     time_range = max(task.deadline for task in task_list) * 2

        # Define a set of colors to use for tasks
        colors = cycle(plt.cm.tab10.colors)  # Use a predefined colormap

        # Plot Gantt chart
        fig, ax = plt.subplots(figsize=(10, 6))

        color_map = {}
        for task in task_list:
            color_map[task.id] = next(colors)

        for task in task_list:
            periods = range(task.activation_date, time_range, task.period)
            for start in periods:
                ax.broken_barh(
                    [(start, task.wcet)],
                    (task.id - 0.4, 0.8),
                    facecolors=(color_map[task.id]),
                )
                # Draw the deadline
                ax.vlines(
                    start + task.deadline,
                    ymin=task.id - 0.4,
                    ymax=task.id + 0.4,
                    colors="red",
                    linestyles="dashed",
                )

        # Configure plot
        ax.set_xlabel("Time")
        ax.set_ylabel("Task Identifier")
        ax.set_yticks([task.id for task in task_list])
        ax.set_yticklabels([task.name for task in task_list])
        ax.grid(True)

        # Create legend for task execution
        patches = [
            mpatches.Patch(color=color_map[task.id], label=f"Task {task.id}")
            for task in task_list
        ]
        plt.legend(handles=patches, title="Tasks")

        # Set title
        plt.title("Task Set Gantt Chart")

        if save:
            # Save plot
            if not os.path.exists(DirNames.RESULTS.value):
                os.makedirs(DirNames.RESULTS.value)
            plt.savefig(
                os.path.join(DirNames.RESULTS.value, FileNames.PLOT_TASK_SET.value)
            )

        # Show plot
        plt.show()
