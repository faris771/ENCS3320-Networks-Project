import socket
import time

from colors import Colors

HOST_IP = socket.gethostbyname(socket.gethostname())  # IP of the server, this case my PC is both server and client
PORT = 8855
ADDRESS = (HOST_IP, PORT)  # tuple
HEADER = 64  # HEADER represnets 64 Bytes, maximum int size that the client will send
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(ADDRESS)


def send(msg: str):
    msg = msg.encode(FORMAT)
    msg_len = len(msg)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(
        send_len))  # ex len = 100, what we do is making a string that 64 byte long, 100 _ concat 63 blanks
    print(f'[debugging] {send_len} ')
    client_socket.send(send_len)
    client_socket.send(msg)


if __name__ == '__main__':

    CLIENT_NAME = 'Faris Abufarha'
    while True:
        time.sleep(2)  # sleep 2 sec
        send(f'{CLIENT_NAME}')

        # if msg == DISCONNECT_MESSAGE:
        #     break
