from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
root=Path(__file__).resolve().parents[1];folder=root/'outputs/videos';folder.mkdir(exist_ok=True)
class Capture(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204);self.send_header('Access-Control-Allow-Origin','http://127.0.0.1:8765');self.send_header('Access-Control-Allow-Methods','POST, OPTIONS');self.send_header('Access-Control-Allow-Headers','Content-Type');self.end_headers()
    def do_POST(self):
        n=int(self.headers.get('Content-Length','0'))
        if self.path not in ['/video','/cinematic','/street'] or not 0<n<200_000_000:self.send_error(400);return
        data=self.rfile.read(n)
        if not data.startswith(b'\x1a\x45\xdf\xa3'):self.send_error(400);return
        (folder/('samagam-ak-street-60s.webm' if self.path=='/street' else 'samagam-vip-cinematic-60s.webm' if self.path=='/cinematic' else 'samagam-guided-60s.webm')).write_bytes(data)
        self.send_response(200);self.send_header('Access-Control-Allow-Origin','http://127.0.0.1:8765');self.end_headers();self.wfile.write(b'saved')
HTTPServer(('127.0.0.1',8767),Capture).serve_forever()
