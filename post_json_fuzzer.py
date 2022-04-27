import argparse
import aiohttp
import asyncio
import csv
import os
import pathlib

from datetime import datetime

from src.core.fuzz_data_creators import get_jsons_for_fuzzing
from src.utils.files_handler import get_filename
from src.data_structures.fuzzer import Fuzzer
from src.data_structures.fuzzy import Fuzzy, extract_here
from src.data_structures.test_method import TestMethod as tm

class ParseKwargs(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


url = str()
headers = dict()
file = str()

parser = argparse.ArgumentParser(
    description="Make POST json fuzzing easy.", formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-url", type=str, dest="url", required=True, help="URL to which requests will be made.", default='127.0.0.1'
)
parser.add_argument('-file', type=str, dest='file', required=True, help="Path to file with pseudo-JSON metainfo.",)
parser.add_argument("--headers", '-H', nargs='*', default=dict(), help="Additional headers.", action=ParseKwargs)
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
            response_body = await response.text()
            return response, request_metainfo, response_body


if __name__ == '__main__':
    with open(file, 'rb') as handle:
        native_file_contetns = handle.read()
        try:
            d_base = eval(native_file_contetns)  #
        except Exception:
            raise Exception(f"Error: cannot make eval method for {get_filename(file)}")

    fuzzer = Fuzzer(d_base)
    result_jsons = fuzzer.get_result_jsons_for_fuzzing()
    # result_jsons = get_jsons_for_fuzzing(d_base)

    # TODO first of all, try to send request with default json body, make sure the reply is 200 OK

    loop = asyncio.get_event_loop()
    coroutines = [post(url, json_params[0], headers, json_params[1]) for json_params in result_jsons]
    print(f'Start sending {len(coroutines)} requests:')
    results = loop.run_until_complete(asyncio.gather(*coroutines))
    for num, result in enumerate(results):
        print(f'{num}: current request with {result[1]} parameters results {result[0].status}: {result[0].reason}')

    curr_path = os.path.dirname(os.path.abspath(__file__))
    results_dir = '/results/'  # TODO make parameter with name
    curr_path += results_dir
    pathlib.Path(curr_path).mkdir(parents=True, exist_ok=True)
    curr_date_time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    filename = get_filename(file)
    path_to_file = curr_path + f'{curr_date_time}_{filename}_results.csv'

    with open(path_to_file, mode='w') as results_file:
        employee_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        title_list = list()
        title_list.append('request_number')
        title_list += list(results[0][1].keys())
        title_list.append('result')
        title_list.append('body')
        employee_writer.writerow(title_list)
        for i, result in enumerate(results):
            lst = list() + [i]
            lst += list(result[1].values())
            lst.append(result[0].status)
            lst.append(result[2])
            employee_writer.writerow(lst)

# TODO known issues:
# cannot make case with lack of current parameter AND doubled string

# TODO improvements
# ssdeep hash for quick reply investigation
# add json_code filename to output file with results like antibot_YYMMDD.csv - DONE
# replace list with set for not getting duplicates items
# add (for Docker) dir with custom generators/mutators ot both dirs. First, post_json_fuzzrt will try to find and registrate those generators in those folders
# USE both structed mutations(my own or try to find a good project) AND random(radamsa)
# add system time mutator (time bombs) - libfaketime
# add lazy generator(lazy?): "id": (132, '#FUNC#random_every_time$'), "test": (1, 2, 3) means that for every permutation
# id will make different random numbers: "id": 1928399182, "test": 1, "id": 9898934982034, "test": 2, etc. make it
# universal: #FUNC#LAZY#random_every_time$'

# add parameters from other hints and services (to HintsdB from APIGW)
# merge parameters from other hints and services, other variant /|\
# add id field to csv(-DATASET!!!) as first field

# TODO results analys:
# long execution check
# ssdeep suspicious (99% 404 ... but 1% is .........)
