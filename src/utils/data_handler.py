from pathlib import Path
from datetime import datetime
from default_values import DefaultValues

from src.utils.files_handler import make_dir


def save_general_log():
    pass


def save_artifacts_to_corr_files(actual_results: dict):
    results_dir = DefaultValues.RESULTS_ROOT_DIR
    dir_name_with_curr_date_time = Path(
        results_dir / datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    )

    if not make_dir(results_dir) or not make_dir(str(dir_name_with_curr_date_time)):
        raise Exception(f"Error: cannot create results directories")

    for deck_name, result_for_separate_deck in actual_results.items():
        all_reply_statuses = {}
        for artifacts in result_for_separate_deck:
            if all_reply_statuses.get(artifacts[0].status, None):
                all_reply_statuses[artifacts[0].status] = all_reply_statuses[
                    artifacts[0].status
                ] + [artifacts[1]]
            else:
                all_reply_statuses[artifacts[0].status] = [artifacts[1]]

        for status, response_data in all_reply_statuses.items():
            with open(
                Path(dir_name_with_curr_date_time / str(status)), mode="w"
            ) as file:
                for data in response_data:
                    file.write(f"{data}\n")
