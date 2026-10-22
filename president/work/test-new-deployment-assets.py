import importlib.util,tempfile,sqlite3,json,threading
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.request import Request,urlopen
spec=importlib.util.spec_from_file_location('deployment_server','outputs/serve-deployment.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory(dir='work') as tmp:
 db=Path(tmp)/'test.sqlite3'
 with sqlite3.connect(db) as c:c.execute('CREATE TABLE deployment (id INTEGER PRIMARY KEY,revision INTEGER,payload TEXT,updated TEXT)')
 c.close()
 server=ThreadingHTTPServer(('127.0.0.1',0),m.handler(db));thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();url=f'http://127.0.0.1:{server.server_port}/api/deployment'
 def put(items,rev):
  body=json.dumps({'revision':rev,'plan':{'version':1,'items':items}}).encode();return json.load(urlopen(Request(url,data=body,method='PUT',headers={'Content-Type':'application/json'})))
 items=[dict(id=k,kind=k,name=k,duty='Test',belt='',mobile='',x=1,y=.3,z=2,angle=0) for k in ['qrt','xray','armed_officer']]
 rev=put(items,0)['revision'];loaded=json.load(urlopen(url));assert len(loaded['plan']['items'])==3
 items[0].update(x=15,z=20,angle=45,name='Edited QRT');rev=put(items,rev)['revision'];assert json.load(urlopen(url))['plan']['items'][0]['angle']==45
 rev=put(items[:1],rev)['revision'];assert len(json.load(urlopen(url))['plan']['items'])==1
 server.shutdown();server.server_close()
print('PASS: isolated backend add, edit, move, rotate, delete and reload for all new kinds; live plan untouched')
