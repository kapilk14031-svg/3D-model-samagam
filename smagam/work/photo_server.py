from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
from io import BytesIO
from PIL import Image
from urllib.parse import urlparse,parse_qs
root=Path(__file__).resolve().parents[1];folder=root/'outputs/photos';folder.mkdir(exist_ok=True)
names=['01-Venue-Overview.jpg','02-Pandal-Canopy.jpg','03-Footbridge-VIP-Side.jpg','04-Residential-Tent-Grounds.jpg','05-Water-Supply-Tanks.jpg','06-Railway-Station-Train.jpg','07-AK-Street-View-MiniMap.jpg'];captured=0
class Capture(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204);self.send_header('Access-Control-Allow-Origin','http://127.0.0.1:8765');self.send_header('Access-Control-Allow-Methods','POST, OPTIONS');self.send_header('Access-Control-Allow-Headers','Content-Type');self.end_headers()
    def do_POST(self):
        global captured
        n=int(self.headers.get('Content-Length','0'))
        view=parse_qs(urlparse(self.path).query).get('view',[''])[0]
        key={'overview':0,'pandal':1,'footbridge':2,'sleeping':3,'water':4,'station':5,'ak':6}.get(view)
        if urlparse(self.path).path!='/photo' or not 0<n<15_000_000 or key is None:self.send_error(400);return
        data=self.rfile.read(n)
        if not data.startswith(b'\x89PNG\r\n\x1a\n'):self.send_error(400);return
        im=Image.open(BytesIO(data)).convert('RGB');im.save(folder/names[key],quality=95,subsampling=0)
        captured+=1
        self.send_response(200);self.send_header('Access-Control-Allow-Origin','http://127.0.0.1:8765');self.end_headers();self.wfile.write(b'saved')
HTTPServer(('127.0.0.1',8766),Capture).serve_forever()
