import argparse
import asyncio
import urllib3

from src.data_structures.fuzzer import Fuzzer
from src.utils.network.service_avail_checker import check_service_is_available

from src.utils.files_handler import (
    load_deck_from_file,
    load_decks_from_folder,
)
from src.utils.results_saver import (
    AsyncResultsSaverFactory,
    SyncResultsSaverFactory,
    create_results_saver
)
from src.utils.console_widgets import (
    show_start_fuzz_info,
    add_line_separator,
    show_post_json_fuzzer_title,
    clear_console,
)
from src.utils.network.request_generator.request_generator import (
    AsyncRequestHandlerFactory,
    SyncRequestHandlerFactory,
    create_request_handler
)
from src.utils.results_handler import (
    AsyncResultsHandlerFactory,
    SyncResultsHandlerFactory,
    create_results_handler
)

if __name__ == "__main__":  # TODO check right position for this check

    urllib3.disable_warnings()


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
    use_async = bool()

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
    parser.add_argument(
        '--useasync'
        , action='store_true'
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
    if args.useasync:
        use_async = True

    if file and folder:
        print(
            "Error: You should choose either folder or file to get fuzzy data, but not both"
        )  # TODO: make both? add possibility to add several files?
        exit(0)



    deck_bundle = []
    if file:
        deck_bundle = load_deck_from_file(file)
    elif folder:
        deck_bundle = load_decks_from_folder(folder)

    fuzzers = {}
    result_jsons = {}
    for relative_file_path, deck in deck_bundle.items():
        fuzzers[relative_file_path] = Fuzzer(deck)  # should it really be named Fuzzer?
        result_jsons[relative_file_path] = fuzzers[
            relative_file_path
        ].get_result_jsons_for_fuzzing()

    clear_console()
    add_line_separator()
    show_post_json_fuzzer_title()
    add_line_separator()
    show_start_fuzz_info(url, headers, file if file else folder)
    add_line_separator()
    print("Waiting for fuzzed service status: ", end="")
    asyncio.run(check_service_is_available(url_aim=url, hdrs=headers))
    print(
        f"Start fuzzing with {sum([len(x) for x in result_jsons.values()])} requests:"
    )

    actual_results = {}
    if use_async:
        async_rg = create_request_handler(AsyncRequestHandlerFactory, url, headers)
        for relative_file_path, jsons in result_jsons.items():
            actual_results[relative_file_path] = asyncio.run(async_rg.start_fuzz(jsons=jsons))

        async_results_handler = create_results_handler(AsyncResultsHandlerFactory, actual_results)
        async_results_handler.show_fuzz_results_brief()

        async_results_saver = create_results_saver(AsyncResultsSaverFactory, actual_results)
        async_results_saver.save_artifacts_to_corr_files()
    else:
        sync_rg = create_request_handler(SyncRequestHandlerFactory, url, headers)
        for relative_file_path, jsons in result_jsons.items():
            actual_results[relative_file_path] = sync_rg.start_fuzz(jsons=jsons)

        sync_results_handler = create_results_handler(SyncResultsHandlerFactory, actual_results)
        sync_results_handler.show_fuzz_results_brief()

        sync_results_saver = create_results_saver(SyncResultsSaverFactory, actual_results)
        sync_results_saver.save_artifacts_to_corr_files()

