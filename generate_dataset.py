from src.dataset_generator.Generator import Generator


def generate_dataset():
    generator = Generator(cpu_utilization=0.8)
    print("Generating dataset...")
    task_set = generator.generate_dataset(num_task_sets=10)
    generator.save_dataset()
    print("✅Dataset generated and saved successfully.")


if __name__ == "__main__":
    generate_dataset()
