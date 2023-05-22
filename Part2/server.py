import socket
import time
from colors import Colors

# no need to print the msg from the clien, just the reciever
HOST_IP = socket.gethostbyname(socket.gethostname())  # my IP
HOST_PORT = 8855
ADDRESS = (HOST_IP, HOST_PORT)
HEADER = 64  # HEADER represents 64 Bytes, maximum int size that the client will send
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP SERVER
server_socket.bind(ADDRESS)
last_received_msg = {}  # Dictionary to store last received message from each client


def get_current_time():
    # get current time
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time


def handle_client():
    while True:
        client_message, client_address = server_socket.recvfrom(1024)  # Receive message from client
        received_time = get_current_time()
        msg = client_message.decode(FORMAT)
        last_received_msg[client_address] = f'{msg} at {received_time}'
        print(f'[{client_address}]: {msg}')
        if len(last_received_msg) >= 3:  # if we have > 3 clients
            print(f'{Colors.OKBLUE}----------------------------------{Colors.ENDC}')
            print(f'{Colors.OKGREEN}[SERVER] OFN server ON{Colors.ENDC}')
            cnt = 1
            for address, msg in last_received_msg.items():
                print(f'{cnt}- received message from  {address} {msg}')
                cnt += 1
            print(f'{Colors.OKBLUE}----------------------------------{Colors.ENDC}')


def start():
    print(f'{Colors.OKGREEN}[ONLINE] server is running on {HOST_IP} {Colors.ENDC}')
    handle_client()


if __name__ == '__main__':
    start()
