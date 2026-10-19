from pathlib import Path
import zipfile
root=Path(__file__).resolve().parents[1];out=root/'outputs'
p=out/'samagam-3d.html';s=p.read_text(encoding='utf-8').replace("image.toBlob(blob=>fetch('http://127.0.0.1:8766/preview',{method:'POST',headers:{'Content-Type':'image/png'},body:blob}).catch(()=>{}));",'');p.write_text(s,encoding='utf-8')
(out/'samagam-ground-finish.png').write_bytes((out/'samagam-premium-preview.png').read_bytes())
p=out/'README.md';p.write_text(p.read_text(encoding='utf-8')+'\nGround material refinement: irregular layered loam/dust patches, subdued dry vegetation, close-range mineral grains and pebbles, and filtered distant detail. These are procedural viewer materials, not surveyed land cover or baked GLB textures. Browser rendering and JavaScript syntax verified.\n',encoding='utf-8')
p=out/'verification.txt';p.write_text(p.read_text(encoding='utf-8')+'Ground shader refinement rendered without browser console errors. Geometry unchanged in this material-only update.\n',encoding='utf-8')
archive=out/'samagam-3d-package.zip'
with zipfile.ZipFile(archive) as z:names=z.namelist()
names=list(dict.fromkeys(names+['samagam-ground-finish.png','source/upgrade_earth.py','source/package_earth.py']))
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for name in names:
        p=root/'work'/name.removeprefix('source/') if name.startswith('source/') else out/name
        if p.exists():z.write(p,name)
print('Ground refinement packaged')
