import http.client
import importlib.util
import json
from contextlib import closing
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path
from http.server import ThreadingHTTPServer

spec = importlib.util.spec_from_file_location('backend', Path(__file__).resolve().parents[1]/'outputs/serve-deployment.py')
backend = importlib.util.module_from_spec(spec); spec.loader.exec_module(backend)

class BackendTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.db = Path(self.temp.name)/'test.sqlite3'
        with closing(sqlite3.connect(self.db)) as db:
            db.execute('CREATE TABLE deployment (id INTEGER PRIMARY KEY, revision INTEGER, payload TEXT, updated TEXT)')
        handler = backend.handler(self.db); handler.log_message = lambda *args: None
        self.server = ThreadingHTTPServer(('127.0.0.1',0),handler)
        threading.Thread(target=self.server.serve_forever,daemon=True).start()
        self.plan = dict(version=1,origin=backend.ORIGIN,items=[dict(id='test',kind='officer',name='Demo',duty='Gate',belt='',mobile='',x=1.,y=.3,z=2.,angle=0.)])
    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.temp.cleanup()
    def request(self,method='GET',body=None,extra=None):
        connection = http.client.HTTPConnection('127.0.0.1',self.server.server_port)
        headers={'Content-Type':'application/json','X-GMS-Plan':'1'}
        headers.update(extra or {})
        connection.request(method,'/api/deployment',json.dumps(body) if body else None,headers)
        response=connection.getresponse(); result=(response.status,json.loads(response.read())); connection.close(); return result
    def test_save_edit_delete_and_disk_persistence(self):
        self.assertEqual(self.request()[1]['revision'],0)
        self.assertEqual(self.request('PUT',dict(revision=0,plan=self.plan))[0],200)
        self.plan['items'][0].update(x=8,angle=90,belt='DEMO')
        self.assertEqual(self.request('PUT',dict(revision=1,plan=self.plan))[0],200)
        self.assertEqual(self.request()[1]['plan']['items'][0]['x'],8)
        with closing(sqlite3.connect(self.db)) as db:
            self.assertEqual(json.loads(db.execute('SELECT payload FROM deployment').fetchone()[0])['items'][0]['angle'],90)
        self.plan['items']=[]
        self.assertEqual(self.request('PUT',dict(revision=2,plan=self.plan))[0],200)
        self.assertEqual(self.request()[1]['plan']['items'],[])
    def test_stale_revision_does_not_overwrite(self):
        self.request('PUT',dict(revision=0,plan=self.plan))
        self.assertEqual(self.request('PUT',dict(revision=0,plan=self.plan))[0],409)
        self.assertEqual(self.request()[1]['revision'],1)
    def test_invalid_data_rejected(self):
        self.plan['items'][0]['y']=-1
        self.assertEqual(self.request('PUT',dict(revision=0,plan=self.plan))[0],400)
        self.assertEqual(self.request()[1]['revision'],0)
    def test_cross_origin_rejected(self):
        self.assertEqual(self.request('PUT',dict(revision=0,plan=self.plan),{'Origin':'https://example.org'})[0],403)
    def test_json_header_required(self):
        self.assertEqual(self.request('PUT',dict(revision=0,plan=self.plan),{'Content-Type':'text/plain'})[0],415)

if __name__=='__main__': unittest.main()
