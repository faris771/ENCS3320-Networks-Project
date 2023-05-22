import socket
import time
from colors import Colors

HOST_IP = socket.gethostbyname(socket.gethostname())  # my IP add 255 instead of last ocatate
hostlist = HOST_IP.split('.')
hostlist[-1] = '255'
HOST_IP = '.'.join(hostlist)
HOST_PORT = 8855
FORMAT = 'utf-8'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
student_name = input('Enter your name: ')


def udp_client():
    while True:
        message = f"{student_name}".encode(FORMAT)
        client_socket.sendto(message, (HOST_IP, HOST_PORT))
        print(f"{Colors.OKCYAN}[CLIENT]Sent broadcast message: {message.decode(FORMAT)}{Colors.ENDC}")
        time.sleep(2)


if __name__ == '__main__':
    udp_client()
