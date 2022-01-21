"""
Common utilities.
"""

import requests
import subprocess
import argparse

# downloads a file from a url to a specific location
def download(url, filename):
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)

# executes a command and returns the output
def execute_cmd(cmd):
    output = subprocess.run(cmd.split(" "), capture_output=True, shell=True)

    if output.returncode == 0:
        return output.stdout.decode('utf-8')
    else:
        return output.stderr.decode('utf-8')

def init_argparse(desc):
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("--port", "-p", type=int, required=True, help="The port to transmit on.")
    parser.add_argument("ip", type=str, help="The ip of the host to connect to.")
    return parser.parse_args()