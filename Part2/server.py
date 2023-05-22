import socket
import time
from colors import Colors

# no need to print the msg from the clien, just the reciever
HOST_IP = socket.gethostbyname(socket.gethostname())  # my IP
HOST_PORT = 8855 # Port that will be used by the server
ADDRESS = (HOST_IP, HOST_PORT) # Address of the server
FORMAT = 'utf-8'# Format of the message that will be sent by the client

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a socket
server_socket.bind(ADDRESS) # Bind the address to the socket
last_received_msg = {}  # Dictionary to store last received message from each client


def get_current_time(): # Function to get current time
    # get current time
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time


def handle_client(): # Function to handle clients
    while True: # Loop to make the server running forever
        client_message, client_address = server_socket.recvfrom(1024)  # Receive message from the client
        received_time = get_current_time() # Get current time
        msg = client_message.decode(FORMAT) # Decode the message to get a string
        last_received_msg[client_address] = f'{msg} at {received_time}' # Store the client address with its last message
        print(f'[{client_address}]: {msg}')
        if len(last_received_msg) >= 3:  # if we have >= 3 clients
            print(f'{Colors.OKBLUE}----------------------------------{Colors.ENDC}')
            print(f'{Colors.OKGREEN}[SERVER] OFN server ON{Colors.ENDC}')
            cnt = 1 # Counter to print the number of the client
            for address, msg in last_received_msg.items():
                print(f'{cnt}- received message from  {address} {msg}')
                cnt += 1
            print(f'{Colors.OKBLUE}----------------------------------{Colors.ENDC}')


def start():
    print(f'{Colors.OKGREEN}[ONLINE] server is running on {HOST_IP} {Colors.ENDC}') # Print that the server is running
    handle_client()


if __name__ == '__main__':
    start()
