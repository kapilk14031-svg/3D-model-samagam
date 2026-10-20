from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
import re,json
out=Path('outputs/deployment-preview');out.mkdir(exist_ok=True)
class H(BaseHTTPRequestHandler):
 def do_OPTIONS(self):
  self.send_response(204);self.send_header('Access-Control-Allow-Origin','http://127.0.0.1:8765');self.send_header('Access-Control-Allow-Methods','POST,OPTIONS');self.send_header('Access-Control-Allow-Headers','Content-Type');self.end_headers()
 def do_POST(self):
  name=self.path.strip('/');n=int(self.headers.get('Content-Length',0))
  if not 0<n<10000000:self.send_error(400);return
  data=self.rfile.read(n)
  if name=='deployment-data':
   plan=json.loads(data);assert len(plan['units'])<=3000
   Path('outputs/samagam-duty-deployment.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
  elif re.fullmatch('[A-Za-z0-9-]+',name) and data.startswith(b'\x89PNG'):(out/(name+'.png')).write_bytes(data)
  else:self.send_error(400);return
  self.send_response(200);self.send_header('Access-Control-Allow-Origin','http://127.0.0.1:8765');self.end_headers()
HTTPServer(('127.0.0.1',8766),H).serve_forever()
