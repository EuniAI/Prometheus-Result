import os
import json
import argparse


def rename_logs(log_dir, timestamp_file):
    # Load timestamp mapping from the JSON file
    with open(timestamp_file, "r", encoding="utf-8") as f:
        ts_map = json.load(f)

    # Create a reverse mapping: timestamp -> instance_id
    timestamp_to_id = {v: k for k, v in ts_map.items()}

    # Iterate over all log files in the directory
    for filename in os.listdir(log_dir):
        if filename.endswith(".log"):
            ts = filename.replace(".log", "")
            if ts in timestamp_to_id:
                instance_id = timestamp_to_id[ts]
                new_name = f"{instance_id}.log"
                old_path = os.path.join(log_dir, filename)
                new_path = os.path.join(log_dir, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_name}")
            else:
                print(f"Timestamp {ts} not found in mapping, skipped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename log files based on timestamp mapping.")
    parser.add_argument("--log_dir", required=True, help="Path to the directory containing log files.")
    parser.add_argument("--timestamp_file", required=True, help="Path to the JSON file with timestamp mapping.")

    args = parser.parse_args()

    rename_logs(args.log_dir, args.timestamp_file)
