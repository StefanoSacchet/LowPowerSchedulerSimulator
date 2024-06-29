from pydantic import BaseModel
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
from itertools import cycle
from typing import List, Dict
import pandas as pd

from src.models.Task import Task
from src.config.Config import DirNames, FileNames


class Plot(BaseModel):
    """Used to plot simulation data"""

    task_list: List[Task]
    task_color_map: Dict[int, str] = {}

    def __init__(self, task_list: List[Task]):
        super().__init__(task_list=task_list)
        colors = cycle(plt.cm.tab10.colors)  # Use a predefined colormap
        for task in task_list:
            self.task_color_map[task.id] = next(colors)

    def plot_results(self, save=False) -> None:
        # Read the CSV file
        df = pd.read_csv(os.path.join(DirNames.RESULTS.value, FileNames.RESULTS.value))

        # Extract unique tasks
        tasks = df["name"].unique()

        # Function to map task names to task IDs
        task_id_map = {name: idx + 1 for idx, name in enumerate(tasks)}

        # Initialize the plot
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot each task
        for task in tasks:
            task_data = df[df["name"] == task]
            task_id = task_id_map[task]

            for i, row in task_data.iterrows():
                if row["state"] == "EXECUTING":
                    ax.broken_barh(
                        [
                            (row["tick"], 1)
                        ],  # assuming each tick represents 1 unit of time
                        (task_id - 0.4, 0.8),
                        facecolors=(self.task_color_map.get(task_id)),
                    )

        time_range = len(df)
        for task in self.task_list:
            periods = range(task.activation_date, time_range, task.period)
            for start in periods:
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
        ax.set_yticks([task_id_map[task] for task in tasks])
        ax.set_yticklabels(tasks)
        ax.grid(True)

        # Create legend for tasks
        patches = [
            mpatches.Patch(color=self.task_color_map.get(task), label=task)
            for task in tasks
        ]
        # Add legend for deadlines
        patches.append(
            mpatches.Patch(color="red", linestyle="dashed", label="Deadline")
        )
        plt.legend(handles=patches)

        # Set title
        plt.title("Simulation Gantt Chart")

        if save:
            # Save plot
            if not os.path.exists(DirNames.RESULTS.value):
                os.makedirs(DirNames.RESULTS.value)
            plt.savefig(
                os.path.join(DirNames.RESULTS.value, FileNames.PLOT_RESULTS.value)
            )

        # Show plot
        plt.show()

    def plot_task_set(self, num_ticks: int, save: bool = False) -> None:
        time_range = num_ticks

        # Plot Gantt chart
        fig, ax = plt.subplots(figsize=(10, 6))

        for task in self.task_list:
            periods = range(task.activation_date, time_range, task.period)
            for start in periods:
                ax.broken_barh(
                    [(start, task.wcet)],
                    (task.id - 0.4, 0.8),
                    facecolors=(self.task_color_map.get(task.id)),
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
        ax.set_yticks([task.id for task in self.task_list])
        ax.set_yticklabels([task.name for task in self.task_list])
        ax.grid(True)

        # Create legend for task execution
        patches = [
            mpatches.Patch(
                color=self.task_color_map.get(task.id), label=f"Task {task.id}"
            )
            for task in self.task_list
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
