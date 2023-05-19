import socket
import threading
import time
from colors import Colors

HOST_IP = socket.gethostbyname(socket.gethostname())  # my IP
HOST_PORT = 8855
ADDRESS = (HOST_IP, HOST_PORT)
HEADER = 64  # HEADER represents 64 Bytes, maximum int size that the client will send
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP SERVER
server.bind(ADDRESS)

last_received_msg = {}  # HashMap


def get_current_time():
    # get current time
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time

def handle_client(communication_socket, client_address):
    received_time = get_current_time()
    print(f'[NEW CONNECTION] {client_address} connected')
    connected = True
    while connected:
        msg_length = communication_socket.recv(HEADER).decode(FORMAT)
        if msg_length:  # not empty message
            msg_length = int(msg_length)
            msg = communication_socket.recv(msg_length).decode(FORMAT)
            last_received_msg[client_address] = f'{msg} at {received_time}'
            #communication_socket.send('[SERVER]: MESSAGE RECIEVED'.encode(FORMAT))

            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f'[{client_address}]: {msg}')

            if len(last_received_msg) >= 3: # if we have > 3 clients
                print(f'[SERVER] OFN server ON')
                for ip, msg in last_received_msg:
                    print( ip, msg)




def start():
    print(f'{Colors.OKGREEN}[ONLINE] server is running on {HOST_IP} {Colors.ENDC}')
    server.listen()
    while True:
        communication_socket, client_address = server.accept()
        print(f'{communication_socket} {client_address}')
        # thread = threading.Thread(target=handle_client, args=(communication_socket, address))
        # thread.start()
        handle_client(communication_socket, client_address)
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')


if __name__ == '__main__':
    start()
