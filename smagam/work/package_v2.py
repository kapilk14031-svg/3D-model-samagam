from pathlib import Path
import zipfile,json,struct
p=Path(__file__).resolve().parents[1]/'outputs'
scene=json.loads((p/'scene-data.json').read_text());b=(p/'samagam-schematic.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n])
assert len(g['nodes'])==len(scene['objects'])
assert sum(o['kind']=='roof' and o['layer']=='tents' for o in scene['objects'])==223
for layer in ['pandal','tents','bridges','toilets','traffic','pedestrian','parking','east']:assert any(o['layer']==layer for o in scene['objects'])
assert any(o['kind']=='ramp' and o['layer']=='flyover' for o in scene['objects'])
fb=(p/'samalkha-nh44-flyover.glb').read_bytes();magic,version,length=struct.unpack_from('<III',fb)
assert magic==0x46546c67 and version==2 and length==len(fb)
fn=struct.unpack_from('<I',fb,12)[0];fg=json.loads(fb[20:20+fn])
assert len(fg['nodes'])==sum(o['layer']=='flyover' for o in scene['objects'])
assert all(abs(node['translation'][0])<2000 and abs(node['translation'][2])<2000 for node in fg['nodes'])
for asset in [g,fg]:
    for view in asset['bufferViews']:assert view['byteOffset']+view['byteLength']<=asset['buffers'][0]['byteLength']
with zipfile.ZipFile(p/'samagam-3d-package.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in ['samagam-3d.html','samagam-3d-basic.html','samagam-schematic.glb','samalkha-nh44-flyover.glb','scene-data.json','model-inventory.csv','samagam-overview-v2.png','samagam-pandal-v2.png','samagam-east-side.png','samagam-bridge-detail.png','samalkha-nh44-flyover.png','nh44-flyover-reference.md','README.md']:z.write(p/name,name)
print(f"Package verified: {len(g['nodes'])} named nodes; 223 representative tent modules; east-side context included.")
