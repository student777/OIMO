from http.server import BaseHTTPRequestHandler, HTTPServer
from read_data import render


class myHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = bytes(render(), "utf8")
        self.wfile.write(response)
        return


server_address = ('127.0.0.1', 8000)
httpd = HTTPServer(server_address, myHandler)
print('running server...')
httpd.serve_forever()
