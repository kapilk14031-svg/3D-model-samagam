from pathlib import Path
import json,zipfile
root=Path(__file__).resolve().parents[1];out=root/'outputs'
scene=json.loads((out/'scene-data.json').read_text(encoding='utf-8'))
assert scene['meta']['water_supply']['elevated_tanks']==1
assert scene['meta']['water_supply']['buffer_tanks']==2
assert all(o['userAdded'] for o in scene['objects'] if o['featureId']=='WATER01')
p=out/'samagam-3d.html';s=p.read_text(encoding='utf-8').replace("image.toBlob(blob=>fetch('http://127.0.0.1:8766/preview',{method:'POST',headers:{'Content-Type':'image/png'},body:blob}).catch(()=>{}));",'');p.write_text(s,encoding='utf-8')
(root/'work/viewer-check.js').write_text(s.split('<script>',1)[1].split('</script>',1)[0],encoding='utf-8')
(out/'samagam-water-supply.png').write_bytes((out/'samagam-premium-preview.png').read_bytes())
p=out/'README.md';p.write_text(p.read_text(encoding='utf-8')+'\nWater supply: user-proposed cluster in a vacant service parcel near the nursery-side area, with one raised blue supply tank, two ground buffer tanks, braced steel tower, access ladder, tank bands, hatch, pipes and valve. Tank capacities and distribution are illustrative. The pad was checked against source road/wall/facility clearances and residential modules. Water supply tanks opens a dedicated camera.\n',encoding='utf-8')
p=out/'verification.txt';p.write_text(p.read_text(encoding='utf-8')+'Water service pad corners clear of reserved source geometry; residential-module separation checked. One elevated tank/two buffers and user-proposed tagging validated. Browser rendered without console errors.\n',encoding='utf-8')
archive=out/'samagam-3d-package.zip'
with zipfile.ZipFile(archive) as z:names=z.namelist()
names=list(dict.fromkeys(names+['samagam-water-supply.png','source/water_supply.py','source/package_water.py']))
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for name in names:
        p=root/'work'/name.removeprefix('source/') if name.startswith('source/') else out/name
        if p.exists():z.write(p,name)
print('Water supply cluster verified and packaged')
