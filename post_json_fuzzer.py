import argparse
import time

import tqdm
import aiohttp
import asyncio


from default_values import DefaultValues

from src.utils.network.service_avail_checker import check_service_is_available
from src.utils.files_handler import (
    load_cartridge_from_file,
    load_cartridges_from_folder,
)
from src.data_structures.fuzzer import Fuzzer
from src.utils.data_handler import save_artifacts_to_corr_files

from src.utils.console_widgets import (
    show_start_fuzz_info,
    show_fuzz_results_brief,
    add_line_separator,
    show_post_json_fuzzer_title,
    clear_console,
    add_blank_line,
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
folder = str()

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
    required=False,
    help="Path to file with pseudo-JSON metainfo.",
)
parser.add_argument(
    "-folder",
    type=str,
    dest="folder",
    required=False,
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
if args.folder:
    folder = args.folder

if file and folder:
    print(
        "Error: You should choose either folder or file to get fuzzy data, but not both"
    )  # TODO: make both? add possibility to add several files?
    exit(0)


async def post(url_aim, json_params, hdrs, suspicious_replies):
    async with aiohttp.ClientSession(trust_env=True) as session:
        for _ in range(120):
            try:
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
            except Exception:  # TODO handle exception correctly to get correct return at the end
                time.sleep(1)
                continue
        return None, {}, None, False


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


# TODO add to doc:
#  cartridge is the set of fuzzy items within json
#  cartridge_bundle is set of cartridges
cartridge_bundle = []
if __name__ == "__main__":
    if file:
        cartridge_bundle = load_cartridge_from_file(file)
    elif folder:
        cartridge_bundle = load_cartridges_from_folder(folder)

    fuzzers = {}
    result_jsons = {}
    for relative_file_path, cartridge in cartridge_bundle.items():
        fuzzers[relative_file_path] = Fuzzer(cartridge)
        result_jsons[relative_file_path] = fuzzers[
            relative_file_path
        ].get_result_jsons_for_fuzzing()

    clear_console()
    add_line_separator()
    show_post_json_fuzzer_title()
    add_line_separator()
    show_start_fuzz_info(url, headers, file if file else folder)
    add_blank_line()
    print("Waiting for fuzzed service status: ", end="")
    asyncio.run(check_service_is_available(url_aim=url, hdrs=headers))
    add_line_separator()
    print(
        f"Start fuzzing with {sum([len(x) for x in result_jsons.values()])} requests:"
    )

    actual_results = {}
    for relative_file_path, jsons in result_jsons.items():
        actual_results[relative_file_path] = asyncio.run(start_fuzz(jsons=jsons))

    add_line_separator()
    show_fuzz_results_brief(actual_results)

    save_artifacts_to_corr_files(actual_results)
