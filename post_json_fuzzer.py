import argparse
import aiohttp
import asyncio
import requests

from src.core.fuzz_data_creators import get_jsons_for_fuzzing

# TODO: add EMPTY or EXCESS in stratgies, ANOMALIES
# TODO: make interactive work with 500 responses:
#  repeat 500th requests until all random 500th answers turn into 200th answers

# TODO agrparse
# json file with json bodies and tules
# url to send
# additional headers, if required

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


d_base = {
    "clientid": (132, 'STRATEGY_1'),
    "type": ("disable_attack_type", 'STRATEGY_2'),
    # "attack_type": (["xss"], 'STAR'),
    # "point": ("action_ext_1", 'STRATEGY_1', "[]^[]^", "action_ext_2", 'STRATEGY_2', "[]^", "action_ext_star", 'STAR', '++'),
    # "dict_field": ({"point": ["path", 0], "type": "absent"}, 'STAR'),
    # "validated": (True, False),

    # ("action", "another_action"):  # (0, 1, True)
    #     [
    #         {("point", '*'): ["header", "HOST"], "type": ("iequal", "equal", "absent"), "value": ("testcom", '*')},
    #         {"point": ["path", 0], "type": "absent"},
    #         {"point": ["action_name"], "type": "equal", "value": ""},
    #         {"point": ["action_ext"], "type": "absent"}
    #     ],
    # "token": "1b64c60e7d3e5cdabd63ba61f6e997ee",
}


# d_base = {
#     "clientid":(132, 'STRATEGY_1'),
#     "type":"disable_attack_type",
#     "attack_type":"sqli",
#     "point":[["action_ext"]],
#     "validated":False,
#     "action":
#         [
#             {"point":["header","HOST"],"type":"iequal","value":"test.com"},
#             {"point":["path",0],"type":("equal", None, 1, "1"),"value":"1"},
#             {"point":["path",1],"type":"equal","value":"2"},
#             {"point":["path",2],"type":"equal","value":"3"},
#             {"point":["path",3],"type":"absent"},
#             {"point":["action_name"],"type":"equal","value":"index"},
#             {"point":["action_ext"],"type":"equal","value":"php"}
#         ],
#     "group_uuid":"26797500-9733-40c4-b4fe-6c47d56c647d",
#     "group_action":"create",
#     "token":"8417d67f4737a93970c40dc3e6251d65",
#
# }

# headers = {
#     "X-WallarmAPI-UUID": "a5ed3d6a-aeba-43ad-8f9c-431bf558dbb9",
#     "X-WallarmAPI-Secret": "65a31fd20b35bba95a4a1e1ba92d0dba73eddf5d46e3792a6ac965a1f28f3282"
# }

async def post(url_aim, json_params, hdrs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url_aim, json=json_params, headers=hdrs, ssl=False) as response:
            return response, json_params

if __name__ == '__main__':
    with open(file, 'rb') as handle:
        d_base = eval(handle.read())  # TODO need to check if file is correct dict

    result_jsons = get_jsons_for_fuzzing(d_base)
    print(result_jsons)

#     loop = asyncio.get_event_loop()
#
#     coroutines = [post(url, json_params, headers) for json_params in result_jsons]
#     print(f'start sending {len(coroutines)}')
#     results = loop.run_until_complete(asyncio.gather(*coroutines))
#
#     for result in results:
#         if result[0].status == 500:
#             print(f"The request with \n{result[1]} \nparameters returned with status 500\n\n")
#
#
# print("hello")



# for params in result_jsons:
#     r = requests.post(
#         url=url,
#         json=params,
#         verify=False,
#         headers=headers
#     )
#     if r.status_code == 500:
#         print(f"500 detected on request with params \n{params}")

# TODO known issues:
# test.com is splitted into ['test', 'com']
# wrong handle of -1 - numbers with minus
# wrong handle of "validated":("", 'STRATEGY_1'), - empty field
# wrong handle of "validated":(111, 222, 'STRATEGY_1') - several items plus strategy
# cannot make case with lack of current parameter AND doubled string
# "value":("test.com") - one value handles incorrectly
# if basic json has no any ()s, -> error