import http.server
import socket
import socketserver
import threading

users = {}

users_lock = threading.Lock()

server_address = (socket.gethostbyname(socket.gethostname()), 8000)

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

class Handler(http.server.SimpleHTTPRequestHandler): 
    def do_GET(self): 
        server_paths = ['/', '/login','/chat', '/livechat/public/chat.txt']

        request_path = self.path

        file_path = ''

        response = ''

        try: 
            if request_path in server_paths: 
                if request_path == '/login': 
                    with users_lock:
                        if self.headers['User']: 
                            users[self.client_address[0]] = self.headers['User']

                elif request_path =='/chat': 
                    file_path = 'livechat/public/chat.html'

                elif request_path == '/': 
                    file_path = 'livechat/public/index.html'

                self.send_response(200)

            else: 
                file_path = 'livechat/public/page_not_found.html'
                
                self.send_response(404)

            self.send_header('Content-type', 'text/html')

            self.send_header('Cache-Control', 'no-store, must-revalidate')

            self.send_header('Pragma', 'no-cache')

            self.send_header('Expires', '0')

            self.end_headers()
            
            if file_path: 
                response = open(file_path).read()

                self.wfile.write(bytes(response, 'utf-8'))

        except: 
            file_path = 'livechat/public/page_not_found.html'
                
            self.send_response(404)

            self.send_header('Content-type', 'text/html')

            self.send_header('Cache-Control', 'no-store, must-revalidate')

            self.send_header('Pragma', 'no-cache')
            
            self.send_header('Expires', '0')

            self.end_headers()

            response = open(file_path).read()

            self.wfile.write(bytes(response, 'utf-8'))
    
    def do_POST(self): 
        length = int(self.headers['Content-Length'])

        data_bytes = self.rfile.read(length)

        data_message = data_bytes.decode('utf-8')

        message = f"{self.headers['User']}: {data_message}\n\n"

        with open('livechat/public/chat.txt', 'a') as file:
            file.write(message)

        self.send_response(200)

        self.send_header('Content-type', 'text/html')

        self.send_header('Cache-Control', 'no-store, must-revalidate')

        self.send_header('Pragma', 'no-cache')
            
        self.send_header('Expires', '0')

        self.end_headers()

        self.wfile.write(bytes(message, 'utf-8'))

    def do_DELETE(self): 
        try: 
            with users_lock:
                del users[self.client_address[0]]

            self.send_response(200)

            self.send_header('Cache-Control', 'no-store, must-revalidate')

            self.send_header('Pragma', 'no-cache')
            
            self.send_header('Expires', '0')

            self.end_headers()

        except KeyError as e: 
            print('Overloaded request:', str(e))

with ThreadedHTTPServer(server_address, Handler) as httpd:
    print(f"Running in {server_address[0]}:{server_address[1]}")
    httpd.serve_forever()
