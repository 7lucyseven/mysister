from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write('GETメソッドを実装'.encode())

    def do_POST(self):
        self.check_URI()

    def check_URI(self):
        if(self.path == '/'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            html_context = "ルート"
            self.wfile.write(html_context.encode())
    
        if(self.path == '/test'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            html_context = "test"
            self.wfile.write(html_context.encode())

server_address = ('localhost', 8080)
httpd = HTTPServer(server_address, CustomHTTPRequestHandler)
httpd.serve_forever()