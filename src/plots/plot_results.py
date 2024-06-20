import matplotlib.pyplot as plt
import os
import ast

from src.config import FileNames


def parse_logs() -> dict[str, list[tuple[float, float]]]:
    # Initialize an empty list to store the logs
    logs = []

    # Read the log file
    with open(
        os.path.join(FileNames.RESULTS_DIR.value, FileNames.LOGS_NAME.value), "r"
    ) as file:
        for line in file:
            # Use ast.literal_eval to safely evaluate the string as a Python expression
            log_entry = ast.literal_eval(line.strip())
            logs.append(log_entry)

    # Parse the logs to extract task events
    events = []
    for log in logs:
        timestamp, (event, _) = log
        events.append((timestamp, event))

    # Store task execution intervals
    task_intervals = {}
    for timestamp, event in events:
        task_name = event.split()[0].split("_")[0]
        action = event.split()[1]

        if task_name not in task_intervals:
            task_intervals[task_name] = []

        if action == "Executing":
            start = timestamp / 1e6
        elif action == "Terminated.":
            end = timestamp / 1e6
            task_intervals[task_name].append((start, end))

    return task_intervals


def plot_chart(
    task_intervals: dict[str, list[tuple[float, float]]], save: bool
) -> None:
    # Create a Gantt chart
    fig, ax = plt.subplots(figsize=(10, 6))

    # Colors for different tasks
    colors = [
        "tab:blue",
        "tab:orange",
        "tab:green",
        "tab:red",
        "tab:purple",
        "tab:brown",
        "tab:pink",
        "tab:gray",
        "tab:olive",
        "tab:cyan",
    ]
    color_index = 0

    # Plot each task interval
    for task, intervals in task_intervals.items():
        for start, end in intervals:
            ax.barh(
                task,
                end - start,
                left=start,
                height=0.5,
                color=colors[color_index % len(colors)],
            )
        color_index += 1

    # Set labels
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Tasks")
    ax.set_title("Task Execution Gantt Chart")

    # Show grid
    ax.grid(True)

    if save:
        # Save the plot
        plt.savefig(FileNames.RESULTS_DIR.value + "task_execution.png")

    # Display the plot
    plt.show()


def plot_results(save: bool = False) -> None:
    plot_chart(parse_logs(), save)
