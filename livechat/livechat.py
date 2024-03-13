import socket
import threading
from server import Server

host = socket.gethostbyname(socket.gethostname())

port = 8000

server = Server(host, port)

server_thread = threading.Thread(target=server.start)

server_thread.start()

server_thread.join()