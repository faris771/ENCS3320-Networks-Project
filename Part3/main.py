from socket import *

# Define the server port
serverPort = 9977

# Create a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind the socket to the specified port
serverSocket.bind(("", serverPort))

# Listen for incoming connections
serverSocket.listen(1)

# Print a message indicating that the server is ready to receive connections
print("The server is ready to receive")

while True:
    try:
        # Accept a connection from a client
        connectionSocket, addr = serverSocket.accept()

        # Receive the request sentence from the client and decode it
        sentence = connectionSocket.recv(2048).decode()

        # Print the client's address and the received sentence
        print(addr)
        print(sentence)

        # Extract the client's IP address and port number
        ip = addr[0]
        port = addr[1]

        # Check the requested URL
        if sentence.startswith("GET /") and (" HTTP/1.1" in sentence or " HTTP/1.0" in sentence):
            # Extract the requested path
            path = sentence.split(" ")[1]

            # Redirect requests to specific paths
            if path == "/yt":
                connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode())
                connectionSocket.send("Location: https://www.youtube.com\r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.close()
                continue
            elif path == "/so":
                connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode())
                connectionSocket.send("Location: https://stackoverflow.com\r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.close()
                continue
            elif path == "/rt":
                connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode())
                connectionSocket.send("Location: https://ritaj.birzeit.edu\r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.close()
                continue

            # Set default content type to "text/html"
            content_type = "text/html"

            # Determine the requested file based on the path and set appropriate content type
            if path in ["/", "/index.html", "/main_en.html", "/en"]:
                filename = "main_en.html"
                content_type = "text/html"
            elif path == "/ar":
                filename = "main_ar.html"
                content_type = "text/html"
            elif path.endswith(".html"):
                filename = path[1:]
                content_type = "text/html"
            elif path.endswith((".css")):
                filename = path[1:]
                content_type = "text/css"
            elif path.endswith((".png")):
                filename = path[1:]
                content_type = "image/png"
            elif path.endswith((".jpg")):
                filename = path[1:]
                content_type = "image/jpg"
            else:
                # If path is not found, send a 404 Not Found response
                with open("NotFound.html", "rb") as file:
                    data = file.read()
                connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
                connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.send(data)
                connectionSocket.close()
                continue

            try:
                # Open and send the requested file
                with open(filename, "rb") as file:
                    data = file.read()
                    connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                    connectionSocket.send(f"Content-Type: {content_type}; charset=utf-8\r\n".encode())
                    connectionSocket.send("\r\n".encode())
                    connectionSocket.send(data)
            except FileNotFoundError:
                # Send a 404 Not Found response if the file doesn't exist
                with open("NotFound.html", "rb") as file:
                    data = file.read()
                connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
                connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.send(data)
                connectionSocket.close()
        else:
            # Send a 404 Not Found response for invalid requests
            with open("NotFound.html", "rb") as file:
                data = file.read()
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
            connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.send(data)
            connectionSocket.close()

        connectionSocket.close()
    except OSError:
        print("IO error")
    else:
        print("OK")
