import curlify

from pathlib import Path
from datetime import datetime

from default_values import DefaultValues
from src.utils.files_handler import make_dir, get_filename


class ResultsSaverFactory:
    @classmethod
    def create_saver(cls, actual_results: dict):
        return cls.ResultsSaver(actual_results)


def create_results_saver(factory, actual_results):
    return factory.create_saver(actual_results)


class SyncResultsSaverFactory(ResultsSaverFactory):  # TODO: get rid of code duplication
    class ResultsSaver:
        def __init__(self, actual_results: dict):
            self.actual_results = actual_results

        def save_artifacts_to_corr_files(self):
            results_dir = DefaultValues.RESULTS_ROOT_DIR
            dir_name_with_curr_date_time = Path(
                results_dir / datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
            )

            if not make_dir(results_dir) or not make_dir(str(dir_name_with_curr_date_time)):
                raise Exception(f"Error: cannot create results directories")

            for deck_name, result_for_separate_deck in self.actual_results.items():
                all_reply_statuses = {}
                deck_file_name = get_filename(deck_name)
                path_to_deck_folder = Path(dir_name_with_curr_date_time / deck_file_name)
                if not make_dir(str(path_to_deck_folder)):
                    raise Exception(f"Error: cannot create results directories")
                for artifacts in result_for_separate_deck:
                    if all_reply_statuses.get(artifacts[0].status_code, None):
                        all_reply_statuses[artifacts[0].status_code] += [(artifacts[1], artifacts[0])]
                    else:
                        all_reply_statuses[artifacts[0].status_code] = [] + [(artifacts[1], artifacts[0])]

                for status, response_data in all_reply_statuses.items():
                    with open(Path(path_to_deck_folder / str(status)), mode="w") as file, \
                            open(Path(path_to_deck_folder / str('curls_for_' + str(status))), mode="w") as file_with_curls:
                        for item in response_data:
                            file.write(f"{item[0]}\n")
                            file_with_curls.write(
                                f"{curlify.to_curl(item[1].request, compressed=True, verify=False)}\n\n"
                            )


class AsyncResultsSaverFactory(ResultsSaverFactory):
    class ResultsSaver:
        def __init__(self, actual_results: dict):
            self.actual_results = actual_results

        def save_artifacts_to_corr_files(self):
            results_dir = DefaultValues.RESULTS_ROOT_DIR
            dir_name_with_curr_date_time = Path(
                results_dir / datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
            )

            if not make_dir(results_dir) or not make_dir(str(dir_name_with_curr_date_time)):
                raise Exception(f"Error: cannot create results directories")

            for deck_name, result_for_separate_deck in self.actual_results.items():
                all_reply_statuses = {}
                deck_file_name = get_filename(deck_name)
                path_to_deck_folder = Path(dir_name_with_curr_date_time / deck_file_name)
                if not make_dir(str(path_to_deck_folder)):
                    raise Exception(f"Error: cannot create results directories")
                for artifacts in result_for_separate_deck:
                    if all_reply_statuses.get(artifacts[0].status, None):
                        all_reply_statuses[artifacts[0].status] = all_reply_statuses[
                                                                           artifacts[0].status
                                                                       ] + [artifacts[1]]
                    else:
                        all_reply_statuses[artifacts[0].status] = [artifacts[1]]

                for status, response_data in all_reply_statuses.items():
                    with open(
                            Path(path_to_deck_folder / str(status)), mode="w"
                    ) as file:
                        for data in response_data:
                            file.write(f"{data}\n")
