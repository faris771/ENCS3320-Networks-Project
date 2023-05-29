import socket
import time
from colors import Colors

HOST_IP = socket.gethostbyname(socket.gethostname())  # my IP add 255 instead of last octet
hostlist = HOST_IP.split('.')  # Split the IP address by '.'

if hostlist[-3] == '255':
    hostlist[-3] = '255'  # Change the  octet to 255
if hostlist[-2] == '255':
    hostlist[-2] = '255'  # Change the  octet to 255
hostlist[-1] = '255'  # Change the last octet to 255
HOST_IP = '.'.join(hostlist)  # Join the list again by '.'
HOST_PORT = 8855  # Port that will be used by the server
FORMAT = 'utf-8'  # Format of the message that will be sent by the client

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a socket for the client with IPv4 and UDP
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable broadcasting mode 1 is for True


student_name = input('Enter your name: ')   # Get the name of the student from the user
def udp_client(): # Function to handle the client
    while True:
        message = f"{student_name}".encode(FORMAT) # Encode the message to bytes
        client_socket.sendto(message, (HOST_IP, HOST_PORT)) # Send the message to the server
        print(f"{Colors.OKCYAN}[CLIENT]Sent broadcast message: {message.decode(FORMAT)}{Colors.ENDC}") # Print the message that will be sent
        time.sleep(2) # Wait for 2 seconds before sending the next message


if __name__ == '__main__':
    udp_client()
