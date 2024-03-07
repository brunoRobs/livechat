import socket
import threading
import json

users = {}

def handler(client_socket, client_address_ip):
    while True: 
        request = client_socket.recv(1024).decode('utf-8')

        print(request)

        path = request.split('\r\n', 1)[0].split(' ')[1][1:]

        headers, body = request.split('\r\n\r\n', 1)

        if body: 
            body = json.loads(body)

        try:
            if not path: 
                with open('livechat/index.html', 'rb') as file: 
                    content = file.read()

                response = f"HTTP/1.1 200 OK\r\nCache-Control: no-store, no-cache, must-revalidate, proxy-revalidate\r\nPragma: no-cache\r\nExpires: 0\r\nContent-Length: {len(content)}\n\n{content.decode('utf-8')}"

            elif path == 'chat': 
                with open('livechat/chat.html', 'rb') as file: 
                    content = file.read()

                if users.get(client_address_ip): 
                    'HTTP/1.1 409 Conflict\r\nContent-Length: 0\n\n'

                else: 
                    users[client_address_ip] = body['name']
                    response = f"HTTP/1.1 200 OK\r\nCache-Control: no-store, no-cache, must-revalidate, proxy-revalidate\r\nPragma: no-cache\r\nExpires: 0\r\nContent-Length: {len(content)}\n\n{content.decode('utf-8')}"           

            else: 
                if path == 'send':
                    response = f"HTTP/1.1 200 OK\r\nContent-Length: 0\n\n"

                elif path == 'download':
                    response = 'HTTP/1.1 200 OK\r\nContent-Length: 0\n\n'

                elif path == 'exit': 
                    client_socket.close()
                    break

                else:
                    response = 'HTTP/1.1 501 Not Implemented\r\nContent-Length: 0\n\n'
                    
        except FileNotFoundError:
            response = 'HTTP/1.1 404 Not Found\r\nContent-Length: 0\n\n' 

        client_socket.sendall(response.encode('utf-8'))

def start_server(): 
    host = socket.gethostbyname(socket.gethostname())

    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    message = f"Running on {host}:{port}"

    server_socket.bind((host, port))

    server_socket.listen(20)

    print(message)

    while True: 
        client_socket, client_address = server_socket.accept()

        if not users.get(client_address[0]): 
            users[client_address[0]] = ''

            print(f"{client_address[0]} is here")

            threading.Thread(target=handler, args=(client_socket, client_address[0], )).start()

start_server()