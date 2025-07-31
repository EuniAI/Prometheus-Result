import json


def analyze_resolved_instances(evaluation_result, log_dict, patches):
    resolved_instances = evaluation_result["resolved_ids"]
    resolved_log_files = []
    for instance in resolved_instances:
        if instance in log_dict:
            resolved_log_files.append(f"answer_issue_logs/{log_dict[instance]}.log")
    total_resolved_instances = len(resolved_instances)
    total_resolved_log_files = len(resolved_log_files)
    total_resolved_instances_with_reproducing_test_passed = sum([1 if is_passed_reproducing_test(log_file)
                                                                 else 0 for log_file in resolved_log_files])
    print(f"Total resolved instances: {total_resolved_instances}")
    print(f"Total resolved instance with log files: {total_resolved_log_files}")
    print(f"Total resolved instances with reproducing test passed:"
          f" {total_resolved_instances_with_reproducing_test_passed}")


def is_passed_reproducing_test(log_file_path: str):
    """
    Check if the log file indicates that the reproducing test was passed.
    """
    try:
        with open(log_file_path, "r") as log_file:
            for line in log_file:
                if "passed_reproducing_test: True" in line:
                    return True
    except FileNotFoundError:
        print(f"Log file {log_file_path} not found.")
    return False


if __name__ == "__main__":
    evaluation_result_file_path = "swe-bench_lite__test__new_strategy-1.json"
    log_dict_file_path = "predictions_20250726_211021_timestamps.json"
    patch_file_path = "predictions_20250726_211021.json"

    with open(log_dict_file_path, "r") as data_file:
        log_dict = json.load(data_file)

    with open(patch_file_path, "r") as data_file:
        patches = json.load(data_file)

    with open(evaluation_result_file_path, "r") as data_file:
        evaluation_result = json.load(data_file)

    analyze_resolved_instances(evaluation_result, log_dict, patches)
