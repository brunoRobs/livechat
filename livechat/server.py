import socket
import threading

class Server: 
    running = True

    def __init__(self, host, port): 
        self.host = host
        self.port = port

    def _add_code(self, code, message): 
        return f"HTTP/1.1 {code} {message}\r\n"

    def _add_header(self, key, value): 
        return f"{key}: {value}\r\n"
    
    def _end_headers(self): 
        return '\n'
    
    def _read_content(self, file_path): 
        with open(file_path, 'rb') as file: 
            return file.read()

    def _handler(self, client_socket): 
        request = client_socket.recv(1024).decode('utf-8')

        path = request.split('\r\n', 1)[0].split(' ')[1]

        response = ''

        try:
            if path == '/': 
                response = self._add_code(200, 'OK')
                response += self._add_header('Content-Length', len(self._read_content('livechat/index.html')))
                response += self._end_headers()
                response += self._read_content('livechat/index.html').decode('utf-8')

            elif path == '/login': 
                response = self._add_code(200, 'OK')
                response += self._add_header('Content-Length', 0)
                response += self._end_headers()

            elif path == '/chat': 
                response = self._add_code(200, 'OK')
                response += self._add_header('Content-Length', len(self._read_content('livechat/chat.html')))
                response += self._end_headers()
                response += self._read_content('livechat/chat.html').decode('utf-8')

           
            elif path == '/exit': 
                response = self._add_code(200, 'OK')
                response += self._add_header('Content-Length', 0)
                response += self._end_headers()

            else:
                raise FileNotFoundError
                    
        except FileNotFoundError:
            response = self._add_code(404, 'Not Found')
            response += self._add_header('Content-Length', len(self._read_content('livechat/not_found.html')))
            response += self._end_headers()
            response += self._read_content('livechat/not_found.html').decode('utf-8')

        client_socket.sendall(response.encode('utf-8'))

        client_socket.close()
    
    def start(self): 
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(20)
        print(f"Running on {self.host}:{self.port}")

        while self.running: 
            client_socket, client_address = server_socket.accept()
            print(f"Connected: {client_address[0]}")
            client_thread = threading.Thread(target=self._handler, args=(client_socket, ))
            client_thread.start()

        server_socket.close()

    def stop(self): 
        self.running = False