from generate_dataset import generate_dataset
from run_sim import run_dataset
from sim_eval import sim_eval

if __name__ == "__main__":
    generate_dataset(num_task_set=10)
    run_dataset(save=False)
    sim_eval()
