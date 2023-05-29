from socket import *

serverPort = 9977
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
print("The server is ready to receive")

while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        sentence = connectionSocket.recv(2048).decode()
        print(addr)
        print(sentence)
        ip = addr[0]
        port = addr[1]

        # Check the requested URL
        if sentence.startswith("GET /") and (" HTTP/1.1" in sentence or " HTTP/1.0" in sentence):
            # Extract the requested path
            path = sentence.split(" ")[1]

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

            content_type = "text/html"
            # Set the appropriate file name and Content-Type based on the requested path
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
                with open("NotFound.html", "rb") as file:
                    data = file.read()
                # Send a 404 Not Found response for invalid paths
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
                    # Send a 404 Not Found response for invalid paths
                connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
                connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.send(data)
                connectionSocket.close()
        else:
            with open("NotFound.html", "rb") as file:
                data = file.read()
                # Send a 404 Not Found response for invalid requests
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
