import os
from itertools import cycle
from tkinter import font
from typing import Dict, List, Optional

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
from pydantic import BaseModel

from src.config.Config import FileNames
from src.core.tasks.Task import Task


class Plot(BaseModel):
    """Used to plot simulation data"""

    task_list: List[Task]
    task_color_map: Dict[int, str] = {}

    def __init__(self, task_list: List[Task]):
        super().__init__(task_list=task_list)
        colors = cycle(plt.cm.tab10.colors)  # type: ignore # Use a predefined colormap
        for task in task_list:
            self.task_color_map[task.id] = next(colors)

    def save_plot(self, plt: plt, path: Optional[str], filename) -> None:  # type: ignore
        if path is None:
            return

        if not os.path.exists(path):
            os.makedirs(path)
        plt.savefig(os.path.join(path, filename))

    def show_plot(self, plt: plt, show: bool) -> None:  # type: ignore
        if show:
            plt.show(block=False)
        else:
            plt.close()

    def plot_results(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        time_range: Optional[int] = None,
        show: bool = False,
    ) -> None:
        # Read the CSV file
        df = pd.read_csv(os.path.join(input_path, FileNames.RESULTS.value))

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

            # Identify contiguous execution blocks
            exec_blocks = []
            start_tick = None
            for i in range(len(task_data)):
                row = task_data.iloc[i]
                if row["state"] == "EXECUTING":
                    if start_tick is None:
                        start_tick = row["tick"]
                    # Check if it's the last row or if the next row is not 'EXECUTING'
                    if (
                        i == len(task_data) - 1
                        or df.query(
                            f'task_id == {task_id} and tick == {row["tick"] + 1} and state == "EXECUTING"'
                        ).empty
                    ):
                        end_tick = row["tick"]
                        exec_blocks.append((start_tick, end_tick - start_tick + 1))
                        start_tick = None

            # Plot execution blocks and add annotations
            for start, length in exec_blocks:
                ax.broken_barh(
                    [(start, length)],  # assuming each tick represents 1 unit of time
                    (task_id - 0.4, 0.8),
                    facecolors=(self.task_color_map[task_id]),
                )
                # Annotate each execution block
                ax.text(
                    start + length / 2,
                    task_id,
                    str(length),
                    verticalalignment="center",
                    horizontalalignment="center",
                    color="black",
                )

        # Plot deadlines
        if time_range is None:
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
        ax.set_xlabel("Time", fontsize=22)  # Increased font size for x-axis label
        ax.set_ylabel("Task Identifier", fontsize=22)  # Increased font size for y-axis label
        ax.set_yticks([task_id_map[task] for task in tasks])
        ax.set_yticklabels(tasks, fontsize=20)  # Increased font size for y-tick labels
        ax.tick_params(axis='x', labelsize=20)  # Increased font size for x-tick labels
        ax.grid(True)

        # Create legend for tasks
        patches = [
            mpatches.Patch(
                color=self.task_color_map.get(task.id), label=f"Task {task.id}"
            )
            for task in self.task_list
        ]
        # Add legend for deadlines
        patches.append(
            mpatches.Patch(color="red", linestyle="dashed", label="Deadline")
        )
        plt.legend(handles=patches, title="Tasks", fontsize=18)

        # Set title
        plt.title("Simulation Results", fontsize=22)

        self.save_plot(plt, output_path, FileNames.PLOT_RESULTS.value)

        # Show plot
        self.show_plot(plt, show)

    def plot_task_set(
        self, num_ticks: int, show: bool = False, output_path: Optional[str] = None
    ) -> None:
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
        ax.set_xlabel("Time", fontsize=22)
        ax.set_ylabel("Task Identifier", fontsize=22)
        ax.set_yticks([task.id for task in self.task_list])
        ax.set_yticklabels([task.name for task in self.task_list], fontsize=20)
        ax.tick_params(axis='x', labelsize=20)
        ax.grid(True)

        # Create legend for task execution
        patches = [
            mpatches.Patch(
                color=self.task_color_map.get(task.id), label=f"Task {task.id}"
            )
            for task in self.task_list
        ]
        # Add legend for deadlines
        patches.append(
            mpatches.Patch(color="red", linestyle="dashed", label="Deadline")
        )
        plt.legend(handles=patches, title="Tasks", fontsize=18)

        # Set title
        plt.title("Task Set Gantt Chart", fontsize=22)

        self.save_plot(plt, output_path, FileNames.PLOT_TASK_SET.value)

        # Show plot
        self.show_plot(plt, show)

    def plot_energy_level(
        self, input_path: str, output_path: Optional[str] = None, show: bool = False
    ) -> None:
        # Read the CSV file
        df = pd.read_csv(
            os.path.join(input_path, FileNames.ENERGY_LEVEL.value)
        )

        # Plot the energy levels against the ticks
        plt.figure(figsize=(10, 6))
        plt.plot(
            df["tick"],
            df["energy"],
            marker="o",
            linestyle="-",
            color="b",
            label="Energy Level",
        )

        # Add labels and title
        plt.xlabel("Tick", fontsize=22)
        plt.ylabel("Energy Level", fontsize=22)
        plt.title("Energy Level Over Time", fontsize=22)
        plt.grid(True)
        # Adjust tick label sizes
        plt.tick_params(axis='both', which='major', labelsize=16)
        plt.legend(fontsize=20)

        self.save_plot(plt, output_path, FileNames.PLOT_ENERGY_LEVEL.value)

        # Show plot
        self.show_plot(plt, show)
