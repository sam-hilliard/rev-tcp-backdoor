"""
Common utilities that can be used across different
applications.
"""

import requests
import subprocess

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