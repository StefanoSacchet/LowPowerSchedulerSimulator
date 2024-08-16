from src.config.Config import DirNames
from src.dataset_generator.Generator import Generator

NUM_TASK_SET = 10


def generate_cpu_utilization() -> None:
    print("  Generating CPU utilization")
    for i in range(20, 100, 20):
        generator = Generator(cpu_utilization=i / 100)
        generator.generate_dataset(num_task_sets=NUM_TASK_SET)
        path = DirNames.SIM_CONFIG.value + f"cpu_utilization/{i}/"
        generator.save_dataset(path)
    print("  ✅CPU utilization dataset generated")


def generate_task_num() -> None:
    print("  Generating task number")
    for i in range(2, 10, 2):
        generator = Generator(cpu_utilization=0.5, min_task_num=i, max_task_num=i)
        generator.generate_dataset(num_task_sets=NUM_TASK_SET)
        path = DirNames.SIM_CONFIG.value + f"task_num/{i}/"
        generator.save_dataset(path)
    print("  ✅Task number dataset generated")


def generate_period_variation() -> None:
    print("  Generating period variation")

    # low period variation
    generator = Generator(cpu_utilization=0.5, min_period=1, max_period=10)
    generator.generate_dataset(num_task_sets=NUM_TASK_SET)
    path = DirNames.SIM_CONFIG.value + "period_variation/low/"
    generator.save_dataset(path)

    # medium period variation
    generator = Generator(cpu_utilization=0.5, min_period=1, max_period=30)
    generator.generate_dataset(num_task_sets=NUM_TASK_SET)
    path = DirNames.SIM_CONFIG.value + "period_variation/medium/"
    generator.save_dataset(path)

    # high period variation
    generator = Generator(cpu_utilization=0.5, min_period=1, max_period=60)
    generator.generate_dataset(num_task_sets=NUM_TASK_SET)
    path = DirNames.SIM_CONFIG.value + "period_variation/high/"
    generator.save_dataset(path)

    print("  ✅Period variation dataset generated")


def generate_dataset() -> None:
    Generator.delete_dataset()

    print("Generating dataset...")

    generate_cpu_utilization()
    generate_task_num()
    generate_period_variation()

    print("Dataset generated")


if __name__ == "__main__":
    generate_dataset()
