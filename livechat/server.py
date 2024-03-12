import http.server
import socket
import socketserver

users = []

class ConflictNameError(Exception): 
    def __init__(self, message='Username already in use'): 
        super().__init__(message)

server_address = (socket.gethostbyname(socket.gethostname()), 8000)

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

class Handler(http.server.SimpleHTTPRequestHandler): 
    def do_GET(self): 
        server_paths = ['/', '/chat', '/livechat/public/chat.txt']

        request_path = self.path

        file_path = ''

        response = ''

        try: 
            if request_path in server_paths: 
                if request_path == '/chat': 
                    if self.headers['User'] in users: 
                        raise ConflictNameError()
                    
                    users.append(self.headers['User'])

                    file_path = 'livechat/public/chat.html'

                elif request_path == '/': 
                    file_path = 'livechat/public/index.html'

                self.send_response(200)

            else: 
                file_path = 'livechat/public/file_not_found.html'
                
                self.send_response(404)

            self.send_header('Content-type', 'text/html')

            self.end_headers()

            response = open(file_path).read()

            self.wfile.write(bytes(response, 'utf-8'))

        except ConflictNameError as e: 
            self.send_response(309, str(e))

            self.end_headers()
    
    def do_POST(self): 
        length = int(self.headers['Content-Length'])

        data_bytes = self.rfile.read(length)

        data_message = data_bytes.decode('utf-8')

        message = f"{self.headers['User']}: {data_message}\n\n"

        with open('livechat/public/chat.txt', 'a') as file:
            file.write(message)

        self.send_response(200)

        self.send_header('Content-type', 'text/html')

        self.end_headers()

        self.wfile.write(bytes(message, 'utf-8'))

    def do_DELETE(self): 
        users.remove(self.headers['User'])

        self.send_response(200)

        self.end_headers()



with ThreadedHTTPServer(server_address, Handler) as httpd:
    print(f"Running in {server_address[0]}:{server_address[1]}")
    httpd.serve_forever()
