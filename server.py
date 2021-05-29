from http.server import HTTPServer, BaseHTTPRequestHandler

# from io import BytesIO


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        with open('index.html', 'rb') as file:
            self.wfile.write(file.read())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        self.send_response(200)
        self.send_header('Content-Type', 'text/csv')
        self.send_header('Content-Disposition', 'attachment; filename="vocab.csv"')
        self.end_headers()
        with open('out.csv', 'rb') as file:
            self.wfile.write(file.read())


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
