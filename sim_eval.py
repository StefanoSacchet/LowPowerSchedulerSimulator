import os
import shutil

import matplotlib.pyplot as plt
import pandas as pd

from src.config.Config import DirNames, FileNames


def plot_scheduling_ratio(
    tot_actual_ratio: float, scheduler: str, task_sets_len: int, output_path: str
) -> None:
    optimal_ratio = 1
    ratios = [tot_actual_ratio / task_sets_len, optimal_ratio]
    labels = ["Actual Scheduling Ratio", "Optimal Ratio"]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, ratios, color=["blue", "red"])
    plt.ylim(0, 1.2)
    plt.ylabel("Ratio")
    plt.title("Scheduling Ratio vs. Optimal Ratio")
    plt.grid(True, axis="y")

    # annotate the bars with the ratio values
    for i, v in enumerate(ratios):
        plt.text(i, v + 0.02, f"{v:.2f}", ha="center", fontweight="bold")

    plt.savefig(os.path.join(output_path, f"{scheduler}_scheduling_ratio.png"))

    plt.close()


def sim_eval() -> None:
    print("Evaluating simulation results...")

    if os.path.exists(DirNames.EVAL.value):
        shutil.rmtree(DirNames.EVAL.value)

    output_path: str = ""

    for sim_type in os.listdir(DirNames.RESULTS.value):
        if sim_type.endswith(".csv"):
            continue

        for type_config in os.listdir(os.path.join(DirNames.RESULTS.value, sim_type)):
            output_path = os.path.join(DirNames.EVAL.value, sim_type, type_config)
            os.makedirs(output_path)

            for scheduler in os.listdir(
                os.path.join(DirNames.RESULTS.value, sim_type, type_config)
            ):
                tot_actual_ratio = 0
                task_sets = os.listdir(
                    os.path.join(
                        DirNames.RESULTS.value, sim_type, type_config, scheduler
                    )
                )

                for task_set in task_sets:
                    input_path = os.path.join(
                        DirNames.RESULTS.value,
                        sim_type,
                        type_config,
                        scheduler,
                        task_set,
                    )

                    # load the CSV data
                    data = pd.read_csv(
                        os.path.join(input_path, FileNames.RESULTS.value)
                    )

                    # identify tasks that were both activated and terminated
                    total_activated = data.query("state == 'ACTIVATED'")
                    missed_deadline = data.query("state == 'MISSED_DEADLINE'")

                    scheduled_tasks = total_activated.size - missed_deadline.size

                    # calculate the actual scheduling ratio
                    tot_actual_ratio += scheduled_tasks / total_activated.size

                plot_scheduling_ratio(
                    tot_actual_ratio, scheduler, len(task_sets), output_path
                )

    print("Simulation results evaluated")


if __name__ == "__main__":
    sim_eval()
