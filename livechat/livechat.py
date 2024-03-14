import socket
import threading
from server import Server
from chat import Chat

host = socket.gethostbyname(socket.gethostname())

server_port = 8080

websocket_port = 9090

server = Server(host, server_port)

chat = Chat(host, websocket_port)

server_thread = threading.Thread(target=server.start)

server_thread.start()

chat.start()

server_thread.join()