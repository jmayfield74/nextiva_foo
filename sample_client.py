"""
A Sample client for making calls to the endpoints exposed by the `nextiva_foo` server.


example:

    $ python sample_client.py -h
    usage: sample_client.py [-h] [-m MIN_CHARS] [-M MAX_CHARS] [-i INTEGERS]
                            [-s SPECIALS] [-u UPPERS] [-x MATRIX]
                            command

    Make nextiva_foo calls.

    positional arguments:
    command               command to execute: password|spiral

    optional arguments:
    -h, --help            show this help message and exit

    password:
    -m MIN_CHARS, --min-chars MIN_CHARS
                            Minimum length of resulting pw.
    -M MAX_CHARS, --max-chars MAX_CHARS
                            Maximum length of resulting pw.
    -i INTEGERS, --integers INTEGERS
                            Number of integers in resulting pw.
    -s SPECIALS, --specials SPECIALS
                            Number of special chars in resulting pw.
    -u UPPERS, --uppers UPPERS
                            Number of uppercase chars in resulting pw.

    spiral:
    -x MATRIX, --matrix MATRIX
                            JSON repr of 2d matrix.


    $ python sample_client.py password -m 3 -M 16 -i 2 -u 2 -s 2
    Yr$a84Gz{

    $ python sample_client.py spiral -x '[[1,2,3],[4,5,6],[7,8,9]]'
    [1, 2, 3, 6, 9, 8, 7, 4, 5]


"""

import argparse
import json

import requests

BASE_URL = "http://localhost:5000"

parser = argparse.ArgumentParser(description="Make nextiva_foo calls.")
parser.add_argument("command", help="command to execute: password|spiral")

pw_group = parser.add_argument_group('password')
sp_group = parser.add_argument_group('spiral')

pw_group.add_argument("-m", "--min-chars",
                      help="Minimum length of resulting pw.",
                      default=6)
pw_group.add_argument("-M", "--max-chars",
                      help="Maximum length of resulting pw.",
                      default=64)
pw_group.add_argument("-i", "--integers",
                      help="Number of integers in resulting pw.",
                      default=1)
pw_group.add_argument("-s", "--specials",
                      help="Number of special chars in resulting pw.",
                      default=1)
pw_group.add_argument("-u", "--uppers",
                      help="Number of uppercase chars in resulting pw.",
                      default=1)

sp_group.add_argument("-x", "--matrix",
                      help="JSON repr of 2d matrix.", default="[]")


def make_request(args):
    """
    Make HTTP request based on passed in args.
    """
    url = "{}/rpc/{}".format(BASE_URL, args.command)
    request_fun, params = get_request_details(args)
    result = request_fun(url, **params)
    if result.status_code == 200:
        print result.json()["result"]
    else:
        print "ERROR ({}): {}".format(result.status_code, result.text)


def get_request_details(args):
    """
    Return the `requests` function and proper kwargs for handling
    the request specified in the args.
    """
    if args.command == "password":
        req_fun = requests.get
        params = {
                "params":
                {
                    "min_chars": args.min_chars,
                    "max_chars": args.max_chars,
                    "integers": args.integers,
                    "specials": args.specials,
                    "uppers": args.uppers
                    }
                }
    elif args.command == "spiral":
        req_fun = requests.post
        matrix = json.loads(args.matrix)
        params = {
                "data": json.dumps({"matrix": matrix}),
                "headers": {"content-type": "application/json"}
                }
    else:
        raise Exception("bad command!")
    return req_fun, params


if __name__ == "__main__":
    args = parser.parse_args()
    make_request(args)
