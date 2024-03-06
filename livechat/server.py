import socket
import threading
from string import Template

def handler(client_socket):
    request = client_socket.recv(1024).decode('utf-8')

    request_path = request.split(' ')[1][1:]

    if not request_path: 
        try:
            with open('livechat/index.html', 'rb') as file: 
                content = file.read()
            page = Template('HTTP/1.1 200 OK\n\n$content')
            response = page.substitute(content=content.decode('utf-8'))
        except FileNotFoundError:
            response = 'HTTP/1.1 404 Not Found\n\n404 Not Found'
    else: 
        if request_path == 'send':
            response = 'HTTP/1.1 200 OK\n\nsend'
        elif request_path == 'download':
            response = 'HTTP/1.1 200 OK\n\ndownload'
        else:
            response = 'HTTP/1.1 501 Not Implemented\n\n501 Not Implemented'

    client_socket.sendall(response.encode('utf-8'))
    
    client_socket.close()

def start_server(): 
    host = socket.gethostbyname(socket.gethostname())

    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    message = Template('Running on $host:$port')

    server_socket.bind((host, port))

    server_socket.listen(100)

    print(message.substitute(host=host, port=port))

    while True: 
        client_socket, client_address = server_socket.accept()

        message = Template('$client is here')

        print(message.substitute(client=client_address))

        client_handler = threading.Thread(target=handler, args=(client_socket, ))

        client_handler.start()

start_server()