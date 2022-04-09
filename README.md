# POST JSON Fuzzer

## Table of Contents

0. [Description](#Description)
1. [Who is this fuzzer for](#Who-is-this-fuzzer-for)
2. [What this fuzzer is not](#What-this-fuzzer-is-not)
3. [POST JSON fuzzer workflow](#POST-JSON-fuzzer-workflow)
4. [Requirements](#Requirements)
5. [Building and Running in Docker](#Building-and-Running-in-Docker)
6. [Tests](#Tests)
7. [CLI Interface](#CLI-Interface)
8. [Restrictions](#Restrictions)

## Description
POST JSON Fuzzer: "Your API could have been in his place"
<p align="center">
  <img src="pics/500.jpg" width = 480 height =220>
</p>
POST JSON Fuzzer is a lightweight WEB fuzzer for API validation. It tries to find as many unexpected responses from the service as possible.
POST JSON Fuzzer makes API check for critical bugs, and you can define test scripts yourself in a clear and concise way, using a small Domain-specific language. The DSL code will be embedded directly into the JSON body of the request. Each test suite will thus be concise and declarative. It will be obvious which parameters are being tested, and how. Write your own data generators, mutators, datasets - it won't be hard!

## Who is this fuzzer for
POST JSON Fuzzer is suitable in everyday work:
* for a developer who needs API checks for the slightest changes in the code (for example, 2K checks in ~ 2 minutes). Unit tests have already been written, but additional system or integration testing is needed
* for a QA engineer or a test engineer to automate those API checks that are done by hand. At the same time, solutions like Postman or Burp Suite are not suitable, or they don’t like it (with all due respect to these wonderful products), or their functionality is redundant for urgent tasks. At the same time, I would like to see a declarative description of the test suite in a concise form
* if you have your own opinion on how to test the API, and do not want to use fuzzers, which are more complicated and may not find the right issue. You want to write your own scripts (strategies) for each JSON parameter (sets, mutations, random data in the right places, etc.)
* if you need somke tests in the pipeline
* if you need an additional fuzzer that is easier to adjust for spot checks

## What this fuzzer is not
POST JSON Fuzzer does not look for vulnerabilities, but tries to break the service and show under what conditions it turned out to be possible.

## POST JSON fuzzer workflow
Let's say you have a service with an API that expects a body with a JSON document of the following structure in the incoming POST request:
```
{
	"id": 31,
	"title": "Buy some stuff",
	"price": 109.95,
	"category": "gadgets",
	"description": "Cool watches",
	"image": "https://anyadressyouwant.com/img/UL640_QL65_.jpg"
}
```
How to find the maximum set of parameter combinations that will lead to unexpected errors in your service? A similar class of problems is solved by fuzzers. There are a lot of fuzzers. Some of them are able to parse the Open API specification by parsing the swagger file. After the analysis, the fuzzer is able to check the compliance with the specification and the real API.

But what if you want to do basic checks on the most frequent cases? Change the id in the range from 1 to 100K, or try to put a number instead of a string in the value of the title field. Change the price value from 109 dollars to two cents, etc. These are routine checks that are sometimes still done manually, oh horror! 
This phaser suggests using a special small DSL that will generate as many variants of JSON bodies for your POST request as you need, based on your own work cases. At the same time, our goal is to get as many unexpected responses from the service as possible (500, 400, 404, etc.)

Let's check the above id, price and title fields, for example:
- let id change in the range 1-100K (as indicated above),
- we will make the price zero, in the value of two cents, a negative number, and very large. We will also add some garbage data.
- just try to change the title to a number, make it longer, shorter, and an empty string

Create a test_api.py file with the following content:
```
{
	"id": (31, -1, 0, 1, 1000, 100000, 100001),
	"title": (1, "Buy some stuff", "Buy", ""),
	"price": (109.95, 0, -1, 0.01, 127387126928357098597264823687398345093485893278573648572683746187641876, "Îäíàæäû"),
	"category": "gadgets",
	"description": "Cool watches",
	"image": "https://anyadressyouwant.com/img/UL640_QL65_.jpg"
}
```
This file will be read by the fuzzer using the eval method, and will be converted to a typical dict. After that, the fuzzer will begin its analysis and processing.

The key point here is that you, as a fuzzer user:
1. Create a JSON-like structure that you understand. There is no need to describe each parameter in an unreadable way, as in other fuzzers. Everything is familiar and obvious.
2. In this structure, you use a DSL whose code is inside tuple-like structures. In fact, this is a tuple from python. And JSON has no analogue of tuple, so we can freely use it and not be afraid of anything.
3. The fuzzer will cut each such tuple-like structure from the test_api.py file, parse them, and at the final stage create all possible combinations of parameters for JSON. After that, each created combination will be inserted into its own JSON structure, which will no longer have any tuples. 
An example of a structure from a similar set:
```
{
	"id": -1,
	"title": "Buy",
	"price": 109.95,
	"category": "gadgets",
	"description": "Cool watches",
	"image": "https://anyadressyouwant.com/img/UL640_QL65_.jpg"
}
```
After that, the fuzzer will start sending all created json bodies one by one(asynchronously) via POST request to the URL that you specify in the fuzzer launch parameters (see below, there is also information about authentication tokens).
The results are printed to the console and also saved to a csv file.
An example of console output:
```
current request with {'id': -1, 'title':'Buy', 'price': 109.95} parameters results 500: Server Error
```

## Requirements
* aiohttp~=3.8.1
* asyncio~=3.4.3
* pytest~=7.1.1

## Building and Running in Docker
```bash
docker build --tag post_json_fuzzer:0.0.1 .
docker run -v /tmp/cartridges:/cartridges -v /tmp/results:/results --rm --name post_json_fuzzer.container post_json_fuzzer:0.0.1 -url="https://YOUR_ENDPOINT" -H "X-HEADER-UUID=HEADER-UUID" "X-API-Secret=API-Secret" -file "cartridges/json_tests_dsl_description.txt"
```
## Tests
To run basic tests go to tests/ dir and run:
```bash
pytest .
```
## CLI Interface
```bash
usage: post_json_fuzzer.py [-h] -url URL -file FILE
                           [--headers [HEADERS [HEADERS ...]]]
```
## Restrictions
Works with secret token only, there is no other authentication scenarios yet
