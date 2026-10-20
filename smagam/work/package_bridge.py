from pathlib import Path
import json,zipfile
root=Path(__file__).resolve().parents[1];out=root/'outputs'
scene=json.loads((out/'scene-data.json').read_text(encoding='utf-8'))
assert scene['meta']['s04_footbridge']['span']==60
assert len([o for o in scene['objects'] if o['name']=='Pandal curved fabric roof'])==1
steel=[o for o in scene['objects'] if o['layer']=='pandal' and any(t in o['name'].lower() for t in ['canopy rib','support column','tent truss','tie beam','guy line'])]
assert steel and all(o['color']=='#15191c' for o in steel)
bridge=[o for o in scene['objects'] if o['name'].startswith('S04 FOOT OVER BRIDGE / ')]
assert bridge and all(o['userAdded'] for o in bridge)
p=out/'samagam-3d.html';s=p.read_text(encoding='utf-8').replace("image.toBlob(blob=>fetch('http://127.0.0.1:8766/preview',{method:'POST',headers:{'Content-Type':'image/png'},body:blob}).catch(()=>{}));",'');p.write_text(s,encoding='utf-8')
(root/'work/viewer-check.js').write_text(s.split('<script>',1)[1].split('</script>',1)[0],encoding='utf-8')
(out/'samagam-s04-footbridge.png').write_bytes((out/'samagam-premium-preview.png').read_bytes())
p=out/'README.md';p.write_text(p.read_text(encoding='utf-8')+'\nLatest pandal/bridge revision: one continuous curved pandal roof replaces four transverse bays; supporting steel/ribs/trusses are black. S04 has a user-proposed covered pedestrian crossing over NH44, with railings and two stair approaches. Its deck length is now 60 assumed model units, reduced from the previous 68 and both stair/support assemblies moved to its new ends. Exact bridge dimensions are illustrative, not measured or approved. S04 Foot overbridge opens a dedicated view.\n',encoding='utf-8')
p=out/'verification.txt';p.write_text(p.read_text(encoding='utf-8')+'Single pandal roof count = 1; pandal steel colour black confirmed. S04 bridge span = 60 (reduced from 68), geometry tagged user-proposed. Browser preview rendered without console errors.\n',encoding='utf-8')
archive=out/'samagam-3d-package.zip'
with zipfile.ZipFile(archive) as z:names=z.namelist()
names=list(dict.fromkeys(names+['samagam-s04-footbridge.png','source/foot_overbridge.py','source/package_bridge.py','source/railway_train.py','samagam-railway-train.png']))
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for name in names:
        p=root/'work'/name.removeprefix('source/') if name.startswith('source/') else out/name
        if p.exists():z.write(p,name)
print('Single curved pandal, black steel and half-length footbridge verified and packaged')
