import os
import argparse
from datasets import load_dataset

SWEBENCH_IMAGE_FORMAT = (
    "swebench/sweb.eval.x86_64.{repo_prefix}_1776_{instance_id_suffix}:v1"
)


def get_swebench_image(instance_id: str, repo: str) -> str:
    """
    Get the SWEbench Docker image name for a given instance ID.
    """
    repo_prefix = repo.split("/")[0]
    instance_id_suffix = instance_id.split("__")[-1]
    return SWEBENCH_IMAGE_FORMAT.format(
        repo_prefix=repo_prefix, instance_id_suffix=instance_id_suffix
    )


def rename_log(log_dir, filename, instance_id):
    new_name = f"{instance_id}.log"
    old_path = os.path.join(log_dir, filename)
    new_path = os.path.join(log_dir, new_name)
    os.rename(old_path, new_path)
    print(f"Renamed: {filename} -> {new_name}")


def rename_logs(log_dir, dataset_name):
    dataset = load_dataset(dataset_name, split='test')
    num = 0
    num_already_renamed = 0

    for data in dataset:
        logs = os.listdir(log_dir)
        logs.sort()

        instance_id = data['instance_id']
        result = None

        # skip if already renamed
        if f"{instance_id}.log" in logs:
            num_already_renamed += 1
            continue

        repo = data['repo']
        image_name = get_swebench_image(instance_id, repo)

        for filename in logs:
            if filename.endswith(".log"):
                with open(os.path.join(log_dir, filename), "r") as f:
                    content = f.read()
                if image_name in content:
                    result = filename
        if not result:
            print(f"Warning: No log file found for instance_id {instance_id}")
            continue

        num += 1
        rename_log(log_dir, result, instance_id)
    print(f"Renamed {num} log files")
    print(f"Already renamed {num_already_renamed} log files")


def remove_non_log_files(log_dir, dataset_name):
    dataset = load_dataset(dataset_name, split='test')

    instance_ids = [data['instance_id'] for data in dataset]

    for filename in os.listdir(log_dir):
        if filename[:-4] not in instance_ids:
            input(f"Press Enter to remove non-log file: {filename}")
            os.remove(os.path.join(log_dir, filename))
            print(f"Removed non-log file: {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename log files based on timestamp mapping.")
    parser.add_argument("--log_dir", required=True, help="Path to the directory containing log files.")
    parser.add_argument("--dataset_name", required=True, help="Name of the dataset.")

    args = parser.parse_args()

    rename_logs(args.log_dir, args.dataset_name)

    remove_non_log_files(args.log_dir, args.dataset_name)
