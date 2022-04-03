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

## Description
POST JSON Fuzzer: "Your API could have been in his place"
<p align="center">
  <img src="pics/500.jpg" width = 480 height =220>
</p>
POST JSON Fuzzer is a lightweight WEB fuzzer for API validation. If you want to find unexpected responses from the application being checked - take it and use it.
POST JSON Fuzzer makes API check for critical bugs, and you can define test scripts yourself in a clear and concise way, using a short Domain-specific language. The DSL code will be embedded directly into the JSON body of the request. Each test suite will thus be concise and declarative. It will be obvious which parameters are being tested, and how. Write your own data generators, mutators, datasets - it won't be hard!

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
WIP

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
