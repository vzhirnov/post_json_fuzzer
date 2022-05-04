import argparse
import tqdm
import aiohttp
import asyncio
import os

from datetime import datetime

from src.strategies.metadata_aggregator import *

from src.utils.files_handler import get_filename, make_dir
from src.data_structures.fuzzer import Fuzzer
from src.data_structures.fuzzy import Fuzzy
from src.data_structures.test_method import TestMethod as tm
from src.utils.console_widgets import (
    show_start_fuzz_info,
    show_fuzz_results_brief,
    add_line_separator,
    show_post_json_fuzzer_title,
    clear_console
)


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split("=")
            getattr(namespace, self.dest)[key] = value


url = str()
headers = dict()
file = str()

parser = argparse.ArgumentParser(
    description="Make POST json fuzzing easy.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-url",
    type=str,
    dest="url",
    required=True,
    help="URL to which requests will be made.",
    default="127.0.0.1",
)
parser.add_argument(
    "-file",
    type=str,
    dest="file",
    required=True,
    help="Path to file with pseudo-JSON metainfo.",
)
parser.add_argument(
    "--headers",
    "-H",
    nargs="*",
    default=dict(),
    help="Additional headers.",
    action=ParseKwargs,
)
args = parser.parse_args()

if args.headers:
    headers = args.headers
if args.url:
    url = args.url
if args.file:
    file = args.file


async def post(url_aim, json_params, hdrs, suspicious_replies):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url_aim, json=json_params, headers=hdrs, ssl=False, timeout=10000000
        ) as response:
            got_suspicious_reply = (
                {"suspicious_reply": True}
                if response.status in suspicious_replies
                else {"suspicious_reply": False}
            )
            response_body = await response.text()
            return response, json_params, response_body, got_suspicious_reply


async def start_fuzz(jsons):
    request_tasks = [
        post(url, json_params[0], headers, json_params[1]) for json_params in jsons
    ]
    responses_bundle = [
        await f
        for f in tqdm.tqdm(
            asyncio.as_completed(request_tasks), total=len(request_tasks)
        )
    ]
    return responses_bundle


if __name__ == "__main__":
    with open(file, "rb") as handle:
        native_file_contetns = handle.read()
        try:
            d_base = eval(native_file_contetns)  #
        except Exception:
            raise Exception(f"Error: cannot make eval method for {get_filename(file)}")

    fuzzer = Fuzzer(d_base)
    result_jsons = fuzzer.get_result_jsons_for_fuzzing()

    # TODO first of all, try to send request with default json body, make sure the reply is 200 OK
    clear_console()
    add_line_separator()
    show_post_json_fuzzer_title()
    add_line_separator()
    show_start_fuzz_info(url, headers, file)
    add_line_separator()

    print(f"Start fuzzing with {len(result_jsons)} requests:")
    actual_responses = asyncio.run(start_fuzz(jsons=result_jsons))

    result_to_save = {}
    for response in actual_responses:  # TODO replace tuples with named tuple
        if response[3]['suspicious_reply']:
            result_to_save[('Suspicious', response[0].status, response[0].reason)] = (
                [response[1]]
                if result_to_save.get(('Suspicious', response[0].status, response[0].reason)) is None
                else result_to_save[('Suspicious', response[0].status, response[0].reason)] + [response[1]]
            )
            continue
        result_to_save[(response[0].status, response[0].reason)] = (
            [response[1]]
            if result_to_save.get((response[0].status, response[0].reason)) is None
            else result_to_save[(response[0].status, response[0].reason)]
            + [response[1]]
        )

    add_line_separator()
    show_fuzz_results_brief(get_filename(file), result_to_save)

    results_dir = "results"
    curr_path = os.path.dirname(os.path.abspath(__file__)) + "/" + results_dir
    if not make_dir(curr_path):
        raise Exception(f"Error: cannot create {results_dir} directory")

    curr_date_time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    curr_path = curr_path + "/" + get_filename(file) + "_" + curr_date_time
    if not make_dir(curr_path):
        raise Exception(f"Error: cannot create {get_filename(file)} directory")

    for request_result, jsons_to_save in result_to_save.items():
        file_name = str(request_result[0])
        path_to_file = curr_path + "/" + file_name

        with open(path_to_file, mode="w") as results_file:
            for item in jsons_to_save:
                results_file.write(f"{item}\n")
