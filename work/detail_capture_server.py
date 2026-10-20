from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
out=Path('outputs/detail-views');out.mkdir(exist_ok=True)
class H(BaseHTTPRequestHandler):
 def do_OPTIONS(self):
  self.send_response(204);self.send_header('Access-Control-Allow-Origin','http://127.0.0.1:8765');self.send_header('Access-Control-Allow-Methods','POST,OPTIONS');self.send_header('Access-Control-Allow-Headers','Content-Type');self.end_headers()
 def do_POST(self):
  name=self.path.strip('/');n=int(self.headers.get('Content-Length',0));data=self.rfile.read(n)
  if name not in ['pandal','parking','langar','residential','police','railway','gate','road','ground','traffic'] or not data.startswith(b'\x89PNG'):self.send_error(400);return
  (out/(name+'.png')).write_bytes(data);self.send_response(200);self.send_header('Access-Control-Allow-Origin','http://127.0.0.1:8765');self.end_headers()
HTTPServer(('127.0.0.1',8766),H).serve_forever()
