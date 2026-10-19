import json, subprocess, time, urllib.request, base64, socket
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

# 1. Start local HTTP server
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args): pass

httpd = HTTPServer(('127.0.0.1', 8780), lambda *args: QuietHandler(*args, directory=str(OUT)))
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()
print("Local HTTP server running on port 8780")

# 2. Launch headless Chrome with CDP
chrome_proc = subprocess.Popen([
    CHROME,
    '--headless=new',
    '--remote-debugging-port=9222',
    '--use-gl=angle',
    '--enable-webgl',
    '--window-size=1600,1050',
    '--hide-scrollbars',
    '--mute-audio',
    'about:blank'
])
time.sleep(2)

def cdp_request(ws_sock, msg_id, method, params=None):
    payload = {'id': msg_id, 'method': method, 'params': params or {}}
    raw = json.dumps(payload)
    # Simple websocket text frame
    data = bytearray([0x81])
    n = len(raw)
    if n < 126:
        data.append(0x80 | n)
    elif n < 65536:
        data.extend([0x80 | 126, (n >> 8) & 0xff, n & 0xff])
    else:
        raise ValueError("Payload too large")
    mask = [0x12, 0x34, 0x56, 0x78]
    data.extend(mask)
    for i, b in enumerate(raw.encode('utf-8')):
        data.append(b ^ mask[i % 4])
    ws_sock.sendall(data)

def cdp_recv(ws_sock):
    buf = bytearray()
    while True:
        hdr = ws_sock.recv(2)
        if not hdr: return None
        b1, b2 = hdr
        plen = b2 & 0x7f
        if plen == 126:
            plen = int.from_bytes(ws_sock.recv(2), 'big')
        elif plen == 127:
            plen = int.from_bytes(ws_sock.recv(8), 'big')
        mask = ws_sock.recv(4) if (b2 & 0x80) else None
        chunk = bytearray()
        while len(chunk) < plen:
            c = ws_sock.recv(plen - len(chunk))
            if not c: break
            chunk.extend(c)
        if mask:
            for i in range(len(chunk)): chunk[i] ^= mask[i % 4]
        return json.loads(chunk.decode('utf-8'))

try:
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json').read())
    ws_url = tabs[0]['webSocketDebuggerUrl']
    host, port_path = ws_url.replace('ws://', '').split(':', 1)
    port_str, path = port_path.split('/', 1)
    path = '/' + path

    s = socket.create_connection((host, int(port_str)), timeout=10)
    # Handshake
    key = base64.b64encode(b"0123456789abcdef").decode()
    req = f"GET {path} HTTP/1.1\r\nHost: {host}:{port_str}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
    s.sendall(req.encode())
    resp = s.recv(1024)
    assert b"101 Switching Protocols" in resp, "WebSocket upgrade failed"
    print("Connected to Chrome via DevTools Protocol")

    msg_id = 1
    def send(method, params=None):
        global msg_id
        mid = msg_id; msg_id += 1
        cdp_request(s, mid, method, params)
        while True:
            r = cdp_recv(s)
            if r and r.get('id') == mid: return r.get('result', {})

    def evaluate(expression):
        res = send('Runtime.evaluate', {'expression': expression, 'returnByValue': True})
        return res.get('result', {}).get('value')

    send('Page.enable')
    send('Runtime.enable')

    # Navigate to samagam-3d.html
    print("Navigating to http://127.0.0.1:8780/samagam-3d.html ...")
    send('Page.navigate', {'url': 'http://127.0.0.1:8780/samagam-3d.html'})
    time.sleep(3)

    # Check for console errors or loading state
    title = evaluate('document.title')
    triangles = evaluate('typeof triangles !== "undefined" ? triangles : 0')
    print(f"Page loaded: '{title}' with {triangles} triangles")

    # Helper to capture screenshot after evaluating setup code
    def capture_shot(filename, setup_code, wait_s=1.5):
        evaluate(setup_code)
        time.sleep(wait_s)
        evaluate('render()')
        res = send('Page.captureScreenshot', {'format': 'png'})
        if 'data' in res:
            img_bytes = base64.b64decode(res['data'])
            (OUT / filename).write_bytes(img_bytes)
            print(f"Captured: {filename} ({len(img_bytes)} bytes)")
        else:
            print(f"Failed to capture {filename}:", res)

    # Shot 1: Grand Overview with Trees, Highway, High Masts, Camp Grounds
    capture_shot('samagam-overview-v2.png', """
        go('overview');
        yaw = 0.52; elevation = 0.78; distance = 2400; target = [50, 0, 280];
        document.getElementById('labels').checked = false;
        render();
    """, wait_s=2.0)

    # Shot 2: Main Satsang Pandal with illuminated stage, golden canopy, red carpet, and avenue trees
    capture_shot('samagam-pandal-v2.png', """
        go('pandal');
        yaw = 0.65; elevation = 0.62; distance = 720; target = [250, 6, 260];
        document.getElementById('labels').checked = false;
        render();
    """, wait_s=1.5)

    # Shot 3: Ceremonial Gates (Gate 1 with ivory marble, gold trims, and Nirankari peace flags)
    capture_shot('samagam-gates-preview.png', """
        go('gates');
        yaw = 1.35; elevation = 0.38; distance = 280; target = [390, 16, 490];
        document.getElementById('labels').checked = false;
        render();
    """, wait_s=1.5)

    # Shot 4: Street View Walkthrough (Tree-lined Avenue with Tents and High-Mast Lighting)
    capture_shot('samagam-realistic-street.png', """
        exitNavigation();
        streetMode = true;
        walker = [320, 2.5, 420];
        heading = 0.2; pitch = 0.08;
        document.getElementById('labels').checked = false;
        render();
    """, wait_s=1.5)

    # Shot 5: Evening Mode (High-mast stadium floodlights illuminating grounds, golden glowing pandal)
    capture_shot('samagam-premium-preview.png', """
        exitNavigation();
        evening = true;
        document.getElementById('light').textContent = 'Daylight';
        document.getElementById('light').classList.add('active');
        go('pandal');
        yaw = 0.62; elevation = 0.58; distance = 850; target = [260, 10, 260];
        document.getElementById('labels').checked = false;
        render();
    """, wait_s=2.0)

    # Update aliases
    (OUT / 'samagam-street-view.png').write_bytes((OUT / 'samagam-realistic-street.png').read_bytes())
    (OUT / 'samagam-overview.png').write_bytes((OUT / 'samagam-overview-v2.png').read_bytes())
    print("All realistic previews captured and saved successfully!")

finally:
    chrome_proc.kill()
    httpd.shutdown()
