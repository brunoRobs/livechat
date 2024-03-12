import http.server
import socket
import socketserver
import os

server_address = (socket.gethostbyname(socket.gethostname()), 8000)

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

class Handler(http.server.SimpleHTTPRequestHandler): 
    def do_GET(self): 
        server_paths = ['/', '/chat']

        request_path = self.path

        file_path = ''

        response = ''

        if request_path in server_paths: 
            if request_path == '/': 
                file_path = 'livechat/index.html'

            else: 
                file_path = 'livechat/chat.html'

        else: 
            file_path = 'livechat/file_not_found.html'

        try: 
            response = open(file_path).read()

            self.send_response(200)
            
        except: 
            response = open(file_path).read()

            self.send_response(404)

        self.end_headers()

        self.wfile.write(bytes(response, 'utf-8'))
    
    def do_POST(self): 
        length = int(self.headers['Content-Length'])

        data_bytes = self.rfile.read(length)

        data_message = data_bytes.decode('utf-8')

        with open('livechat/chat.txt', 'a') as file:
            file.write(f"{data_message}\n\n")

        self.send_response(200)

        self.end_headers()

with ThreadedHTTPServer(server_address, Handler) as httpd:
    print(f"Running in {server_address[0]}:{server_address[1]}")
    httpd.serve_forever()
