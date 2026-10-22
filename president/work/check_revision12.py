import json, math, struct, zipfile
from pathlib import Path
import numpy as np
out=Path('outputs');d=json.loads((out/'model-data.json').read_text(encoding='utf-8'));o=d['objects']
a=[x for x in o if x['name'].startswith('Hall solid scalloped arcade')];a.sort(key=lambda x:x['p'][2])
def ends(x):
 u=np.array([math.cos(x['rot']),-math.sin(x['rot'])])*x['s'][0]/2;c=np.array(x['p'])[::2];return [c-u,c+u]
gaps=[min(np.linalg.norm(x-y) for x in ends(p) for y in ends(q)) for p,q in zip(a,a[1:])]
assert len(a)==8 and max(gaps)<1e-5,gaps
assert sum(x['name']=='Hall pink circular arcade column' for x in o)==9
assert sum(x['name']=='Hall continuous pink parapet coping' for x in o)==1
assert not any(x['name'].startswith('Hall pink parapet cap') for x in o)
for side in ['left','right']:assert sum(x['name'].startswith('Stage '+side+' side green stair') for x in o)==5
assert all(np.isfinite(x['p']+x['s']).all() for x in o)
b=(out/'gyan-mansarovar-concept.glb').read_bytes();magic,version,size=struct.unpack_from('<III',b);assert magic==0x46546c67 and version==2 and size==len(b)
n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);assert len(g['images'])==12
assert len(json.loads((out/'site-footprints.geojson').read_text())['features'])==20
print('PASS: contiguous 8 arches; 9 columns; single coping; both stage stairs; finite geometry; GLB 12 images; GeoJSON 20 features. Max arch join gap:',max(gaps))
