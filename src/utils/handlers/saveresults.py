import curlify


from pathlib import Path
from datetime import datetime

from defaults.constants import ProjectValues
from src.utils.handlers.files import make_dir, get_filename
from src.core.analyzedata import DataAnalyzer
from src.utils.network.asyncurlify import to_curl


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
            results_dir = ProjectValues.RESULTS_ROOT_DIR
            dir_name_with_curr_date_time = Path(
                results_dir / datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
            )

            if not make_dir(results_dir) or not make_dir(
                str(dir_name_with_curr_date_time)
            ):
                raise Exception(f"Error: cannot create results directories")

            for deck_name, result_for_separate_deck in self.actual_results.items():
                replies = [len(x[0].text) for x in result_for_separate_deck]
                data_analyzer = DataAnalyzer(replies)
                anomalies = data_analyzer.find_anomalies()
                if len(anomalies):
                    print(
                        f"\nAnomaly is found in the following requests"
                        f"(mean request length is {int(data_analyzer.mean)}):",
                        sep="\n",
                    )
                    for item in anomalies:
                        print(
                            "response number "
                            + str(item[0])
                            + f" has length {str(item[1])}",
                            sep=" ",
                        )
                    print("\n\n")

                deck_file_name = get_filename(deck_name)
                path_to_deck_folder = Path(
                    dir_name_with_curr_date_time / deck_file_name
                )
                if not make_dir(str(path_to_deck_folder)):
                    raise Exception(f"Error: cannot create results directories")

                all_reply_statuses = {}
                for artifacts in result_for_separate_deck:
                    if all_reply_statuses.get(artifacts[0].status_code, None):
                        all_reply_statuses[artifacts[0].status_code] += [
                            (artifacts[1], artifacts[0])
                        ]
                    else:
                        all_reply_statuses[artifacts[0].status_code] = [] + [
                            (artifacts[1], artifacts[0])
                        ]

                for status, response_data in all_reply_statuses.items():
                    with open(
                        Path(path_to_deck_folder / str(status)), mode="w"
                    ) as file, open(
                        Path(path_to_deck_folder / str("curls_for_" + str(status))),
                        mode="w",
                    ) as file_with_curls:
                        for i, item in enumerate(response_data):
                            file.write(f"{i}: {item[0]}\n")
                            file_with_curls.write(
                                f"{i}: {curlify.to_curl(item[1].request, compressed=True, verify=False)}\n\n"
                            )

                with open(
                    Path(path_to_deck_folder / str(f"fuzzing-{deck_file_name}.log")),
                    mode="w",
                ) as log:
                    log.write("Results for " + str(deck_name) + "\n\n")
                    for i, response in enumerate(result_for_separate_deck):
                        log.write(f"({i}):" + "\n\n")
                        log.write("URL: " + response[0].url + "\n")
                        log.write(
                            "Request body: " + str(response[0].request.body) + "\n"
                        )
                        log.write("Status code: " + str(response[0].status_code) + "\n")
                        log.write("Reason: " + response[0].reason + "\n")
                        log.write("Time elapsed: " + str(response[0].elapsed) + "\n")
                        log.write("Text: " + response[0].text)
                        log.write("\n\n")


class AsyncResultsSaverFactory(ResultsSaverFactory):
    class ResultsSaver:
        def __init__(self, actual_results: dict):
            self.actual_results = actual_results

        def save_artifacts_to_corr_files(self):
            results_dir = ProjectValues.RESULTS_ROOT_DIR
            dir_name_with_curr_date_time = Path(
                results_dir / datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
            )
            if not make_dir(results_dir) or not make_dir(
                str(dir_name_with_curr_date_time)
            ):
                raise Exception(f"Error: cannot create results directories")

            for deck_name, result_for_separate_deck in self.actual_results.items():

                replies = [len(x[2]) for x in result_for_separate_deck]
                data_analyzer = DataAnalyzer(replies)
                anomalies = data_analyzer.find_anomalies()
                if len(anomalies):
                    print(
                        f"\nAnomaly is found in the following requests"
                        f"(mean request length is {int(data_analyzer.mean)}):",
                        sep="\n",
                    )
                    for item in anomalies:
                        print(
                            "response number "
                            + str(item[0])
                            + f" has length {str(item[1])}",
                            sep=" ",
                        )
                        print("\t response trailer: ", result_for_separate_deck[item[0]][2][:100])
                    print("\n\n")

                deck_file_name = get_filename(deck_name)
                path_to_deck_folder = Path(
                    dir_name_with_curr_date_time / deck_file_name
                )
                if not make_dir(str(path_to_deck_folder)):
                    raise Exception(f"Error: cannot create results directories")
                all_reply_statuses = {}
                for artifacts in result_for_separate_deck:
                    if all_reply_statuses.get(artifacts[0].status, None):
                        all_reply_statuses[artifacts[0].status] += [
                            (artifacts[1], artifacts[0])
                        ]
                    else:
                        all_reply_statuses[artifacts[0].status] = [] + [
                            (artifacts[1], artifacts[0])
                        ]

                for status, response_data in all_reply_statuses.items():
                    with open(
                        Path(path_to_deck_folder / str("curls_for_" + str(status))),
                        mode="w",
                    ) as file_with_curls:
                        for i, item in enumerate(response_data):
                            file_with_curls.write(
                                f"{i}: {to_curl(item[1], body=item[0], compressed=True, verify=False)}\n\n"
                            )

                for status, response_data in all_reply_statuses.items():
                    with open(
                        Path(path_to_deck_folder / str(status)), mode="w"
                    ) as file:
                        for i, data in enumerate(response_data):
                            file.write(f"{i}: {data[0]}\n")

                with open(
                    Path(path_to_deck_folder / str(f"fuzzing-{deck_file_name}.log")),
                    mode="w",
                ) as log:
                    log.write("Results for " + str(deck_name) + "\n\n")
                    for i, response in enumerate(result_for_separate_deck):
                        log.write(f"({i}):" + "\n\n")
                        log.write("URL: " + str(response[0].url) + "\n")
                        log.write("Requst body: " + str(response[1]) + "\n")
                        log.write("Status code: " + str(response[0].status) + "\n")
                        log.write("Reason: " + response[0].reason + "\n")
                        log.write("Text: " + response[2])
                        log.write("\n\n")
