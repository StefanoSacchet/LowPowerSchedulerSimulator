import time

from generate_dataset import generate_dataset
from run_sim import run_dataset
from sim_eval import sim_eval

if __name__ == "__main__":
    start_time = time.time()
    generate_dataset(num_task_set=5)
    dataset_time = time.time() - start_time
    print(f"Generated dataset in {dataset_time:.2f} seconds")

    run_dataset(save=True)
    run_time = time.time() - dataset_time
    print(f"Ran simulation in {run_time:.2f} seconds")

    sim_eval()
    eval_time = time.time() - run_time
    print(f"Evaluated simulation in {eval_time:.2f} seconds")

    print("***")
    print(f"Total time: {time.time() - start_time:.2f} seconds")
