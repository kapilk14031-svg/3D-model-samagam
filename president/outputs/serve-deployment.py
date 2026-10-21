"""Local 3D deployment viewer with transactional SQLite persistence."""
import argparse
import json
import math
from contextlib import closing
import sqlite3
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
KINDS = {'officer','barricade','binocular','dfmd','hhmd','radio','cone','cctv','light','square_box','ambulance','firebrigade','qbelt'}
ORIGIN = [76.848831, 29.413077]

def valid(plan):
    if not isinstance(plan, dict) or plan.get('version') != 1:
        return False
    items = plan.get('items')
    if not isinstance(items, list) or len(items) > 1000:
        return False
    ids = set()
    for item in items:
        if not isinstance(item, dict):
            return False
        kind = item.get('kind')
        if not isinstance(kind, str) or not kind or len(kind) > 50:
            return False
        uid = item.get('id')
        if not isinstance(uid, str) or not uid or len(uid) > 150 or uid in ids:
            return False
        ids.add(uid)
        for k in ('name','duty','belt','mobile'):
            val = item.get(k)
            if val is not None and (not isinstance(val, str) or len(val) > 300):
                return False
        for k in ('x','y','z','angle'):
            val = item.get(k)
            if type(val) not in (int,float) or not math.isfinite(val):
                return False
        if abs(item['x']) > 5000 or abs(item['z']) > 5000 or not -10 <= item['y'] <= 200:
            return False
    return True

def handler(db_path):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT), **kwargs)
        def reply(self, status, payload):
            body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type','application/json; charset=utf-8')
            self.send_header('Cache-Control','no-store')
            self.send_header('Content-Length',str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        def allowed(self):
            host = self.headers.get('Host','')
            if host not in (f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}'):
                self.reply(403, {'error':'Local host required'})
                return False
            origin = self.headers.get('Origin')
            if origin and origin not in ('http://'+host,):
                self.reply(403, {'error':'Same origin required'})
                return False
            return True
        def do_GET(self):
            if not self.allowed(): return
            path = urlsplit(self.path).path
            if path == '/api/deployment':
                with closing(sqlite3.connect(db_path)) as db:
                    row = db.execute('SELECT revision, payload, updated FROM deployment WHERE id=1').fetchone()
                self.reply(200, {'revision':row[0], 'plan':json.loads(row[1]), 'updated':row[2]} if row else {'revision':0,'plan':None})
                return
            if path == '/':
                self.send_response(302); self.send_header('Location','/outputs/gyan-mansarovar-3d.html'); self.end_headers(); return
            if path.startswith('/outputs/'):
                self.path = self.path[len('/outputs'):]
            elif path.startswith('/api/'):
                self.reply(404, {'error':'Unknown API'}); return
            if '..' in urlsplit(self.path).path or self.path.endswith('/'):
                self.send_error(404); return
            super().do_GET()
        def do_POST(self):
            return self.do_PUT()
        def do_PUT(self):
            if not self.allowed(): return
            if urlsplit(self.path).path != '/api/deployment':
                self.reply(404, {'error':'Unknown API'}); return
            ct = self.headers.get('Content-Type','').split(';')[0].strip()
            if ct not in ('application/json', 'text/plain', ''):
                self.reply(415, {'error':'JSON plan required'}); return
            try:
                size = int(self.headers.get('Content-Length','0'))
                if not 0 < size <= 2000000: raise ValueError('Plan exceeds size limit')
                request = json.loads(self.rfile.read(size))
                plan = request.get('plan')
                if not valid(plan): raise ValueError('Invalid deployment plan')
                with closing(sqlite3.connect(db_path, timeout=10)) as db:
                    db.execute('BEGIN IMMEDIATE')
                    row = db.execute('SELECT revision FROM deployment WHERE id=1').fetchone()
                    cur_rev = row[0] if row else 0
                    req_rev = request.get('revision')
                    new_rev = (max(cur_rev, req_rev) + 1) if isinstance(req_rev, int) else (cur_rev + 1)
                    updated = datetime.now(timezone.utc).isoformat()
                    db.execute('INSERT OR REPLACE INTO deployment(id,revision,payload,updated) VALUES(1,?,?,?)', (new_rev,json.dumps(plan,ensure_ascii=False),updated))
                    db.commit()
                # Mirror save to JSON file on disk for dual persistence
                try:
                    draft_file = ROOT / 'deployment-draft.json'
                    draft_file.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
                except Exception:
                    pass
                self.reply(200, {'revision':new_rev,'updated':updated})
            except (ValueError, TypeError, AttributeError) as error:
                self.reply(400, {'error':str(error)})
            except sqlite3.Error as e:
                self.reply(503, {'error':'Database save unavailable: ' + str(e)})
    return Handler

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8794)
    parser.add_argument('--db', type=Path, default=ROOT.parent/'work'/'deployment.sqlite3')
    args = parser.parse_args()
    args.db.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(args.db)) as db:
        db.execute('CREATE TABLE IF NOT EXISTS deployment (id INTEGER PRIMARY KEY CHECK(id=1), revision INTEGER NOT NULL, payload TEXT NOT NULL, updated TEXT NOT NULL)')
    server = ThreadingHTTPServer(('127.0.0.1',args.port), handler(args.db))
    print(f'3D viewer: http://127.0.0.1:{args.port}/outputs/gyan-mansarovar-3d.html', flush=True)
    print(f'Database: {args.db}', flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: server.server_close()
