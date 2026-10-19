from pathlib import Path
import zipfile
root=Path(__file__).resolve().parents[1];out=root/'outputs'
p=out/'samagam-3d.html';s=p.read_text(encoding='utf-8').replace("image.toBlob(blob=>fetch('http://127.0.0.1:8766/preview',{method:'POST',headers:{'Content-Type':'image/png'},body:blob}).catch(()=>{}));",'');p.write_text(s,encoding='utf-8')
(root/'work/viewer-check.js').write_text(s.split('<script>',1)[1].split('</script>',1)[0],encoding='utf-8')
(out/'samagam-pandal-earth.png').write_bytes((out/'samagam-premium-preview.png').read_bytes())
p=out/'README.md';p.write_text(p.read_text(encoding='utf-8')+'\nPandal roof refinement: subdivided fabric shell with soft sag between supports, tension folds and raised stitched seams; golden-brown styling retained. Ground now uses an earth-brown GLB base and mainly soil/dry-earth shading with sparse grass patches and subdued grit in the viewer. The canopy stays within its previous fitted footprint.\n',encoding='utf-8')
p=out/'verification.txt';p.write_text(p.read_text(encoding='utf-8')+'Pandal fabric shell/seam refinement rendered without browser console errors. Earth material recognition corrected for linear colour rendering. Tent-wall clearance and GLB checks passed.\n',encoding='utf-8')
archive=out/'samagam-3d-package.zip'
with zipfile.ZipFile(archive) as z:names=z.namelist()
names=list(dict.fromkeys(names+['samagam-pandal-earth.png','source/package_pandal_earth.py']))
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for name in names:
        p=root/'work'/name.removeprefix('source/') if name.startswith('source/') else out/name
        if p.exists():z.write(p,name)
print('Pandal/earth edition packaged')
