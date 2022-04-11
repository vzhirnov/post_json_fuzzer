import argparse
import aiohttp
import asyncio
import csv
import os
import pathlib

from datetime import datetime

from src.core.fuzz_data_creators import get_jsons_for_fuzzing

# TODO: add EMPTY or EXCESS in stratgies, ANOMALIES
# TODO: make interactive work with 500 responses:
#  repeat 500th requests until all random 500th answers turn into 200th answers

url = str()
headers = dict()
file = str()


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


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
    default='127.0.0.1'
)
parser.add_argument(
    '-file',
    type=str,
    dest='file',
    required=True,
    help="Path to file with pseudo-JSON metainfo.",
)
parser.add_argument(
    "--headers",
    '-H',
    nargs='*',
    default=dict(),
    help="Additional headers.",
    action=ParseKwargs
)
args = parser.parse_args()

if args.headers:
    headers = args.headers
if args.url:
    url = args.url
if args.file:
    file = args.file


async def post(url_aim, json_params, hdrs, request_metainfo):
    async with aiohttp.ClientSession() as session:
        async with session.post(url_aim, json=json_params, headers=hdrs, ssl=False) as response:
            return response, request_metainfo

if __name__ == '__main__':
    with open(file, 'rb') as handle:
        native_file_contetns = handle.read()
        d_base = eval(native_file_contetns)  # TODO need to check if file is correct dict

    result_jsons = get_jsons_for_fuzzing(d_base)

    loop = asyncio.get_event_loop()

    coroutines = [post(url, json_params[0], headers, json_params[1]) for json_params in result_jsons]
    print(f'start sending {len(coroutines)} requests')
    results = loop.run_until_complete(asyncio.gather(*coroutines))
    for result in results:
        print(f'current request with {result[1]} parameters results {result[0].status}: {result[0].reason}')

    curr_path = os.path.dirname(os.path.abspath(__file__))
    results_dir = '/results/'  # TODO make parameter with name
    curr_path += results_dir
    pathlib.Path(curr_path).mkdir(parents=True, exist_ok=True)
    curr_date_time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    path_to_file = curr_path + f'{curr_date_time}_results.csv'

    with open(path_to_file, mode='w') as results_file:
        employee_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        title_list = list(result[1].keys())  # TODO : result?
        title_list.append('result')
        employee_writer.writerow(title_list)
        for result in results:
            l = list(result[1].values())
            l.append(result[0].status)
            employee_writer.writerow(l)

# TODO known issues:
# cannot make case with lack of current parameter AND doubled string

# TODO improvements
# ssdeep hash for quick reply investigation
# add json_code filename to output file with results like antibot_YYMMDD.csv
# replace list with set for not getting duplicates items
# add (for Docker) dir with custom generators/mutators ot both dirs. First, post_json_fuzzrt will try to find and registrate those generators in those folders
# USE both structed mutations(my own or try to find a good project) AND random(radamsa)
# add system time mutator (time bombs) - libfaketime