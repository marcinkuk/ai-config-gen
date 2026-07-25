import http.server
import json
import os

PORT = 8011

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/instrukcje.html'
        path_map = {
            '/instrukcje.html': 'static/instrukcje.html',
            '/landing.html': 'static/landing.html',
        }
        filepath = path_map.get(self.path, self.path.lstrip('/'))
        fullpath = os.path.join(os.getcwd(), filepath)
        if os.path.isfile(fullpath):
            ct = 'text/html' if fullpath.endswith('.html') else 'text/plain'
            self.send_response(200)
            self.send_header('Content-Type', ct + '; charset=utf-8')
            self.end_headers()
            self.wfile.write(open(fullpath, 'rb').read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

    def do_POST(self):
        if self.path == '/api/save-token':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode()
            data = json.loads(body)
            token = data.get('token', '')
            with open(os.path.join(os.getcwd(), 'pypi_token.txt'), 'w') as f:
                f.write(token)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # silence logs

print(f'Serving on port {PORT}')
http.server.HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()