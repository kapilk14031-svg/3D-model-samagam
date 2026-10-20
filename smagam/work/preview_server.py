from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
OUT=Path(__file__).resolve().parents[1]/'outputs'
class Capture(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204);self.send_header('Access-Control-Allow-Origin','http://127.0.0.1:8765');self.send_header('Access-Control-Allow-Methods','POST, OPTIONS');self.send_header('Access-Control-Allow-Headers','Content-Type');self.end_headers()
    def do_POST(self):
        n=int(self.headers.get('Content-Length','0'))
        if self.path!='/preview' or not 0<n<10000000:self.send_error(400);return
        data=self.rfile.read(n)
        if not data.startswith(b'\x89PNG\r\n\x1a\n'):self.send_error(400);return
        (OUT/'samagam-premium-preview.png').write_bytes(data)
        self.send_response(200);self.send_header('Access-Control-Allow-Origin','http://127.0.0.1:8765');self.end_headers();self.wfile.write(b'saved')
HTTPServer(('127.0.0.1',8766),Capture).serve_forever()
