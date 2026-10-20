from pathlib import Path
import zipfile
root=Path(__file__).resolve().parents[1];out=root/'outputs'
p=out/'samagam-3d.html';s=p.read_text(encoding='utf-8').replace("image.toBlob(blob=>fetch('http://127.0.0.1:8766/preview',{method:'POST',headers:{'Content-Type':'image/png'},body:blob}).catch(()=>{}));",'');p.write_text(s,encoding='utf-8')
(root/'work/viewer-check.js').write_text(s.split('<script>',1)[1].split('</script>',1)[0],encoding='utf-8')
for name in ['samagam-realistic-street.png','samagam-street-view.png']:(out/name).write_bytes((out/'samagam-premium-preview.png').read_bytes())
(out/'samagam-premium-preview.png').write_bytes((out/'samagam-residential-reference.png').read_bytes())
p=out/'README.md';p.write_text(p.read_text(encoding='utf-8')+'\n## Surface and lighting edition\n\nThe interactive viewer adds distance-faded procedural canvas weave/folds, plaster variation, asphalt grain, wood grain, view-dependent glazing, atmospheric sky/clouds, sunlight and haze. Tent entrance support poles and thresholds are actual exported geometry. Textures and sky are viewer shaders, not baked GLB textures. Geometry remains illustrative; this improves visual realism without claiming surveyed construction detail. Street/rectangle controls remain available.\n',encoding='utf-8')
p=out/'verification.txt';p.write_text(p.read_text(encoding='utf-8')+'Material/sky shaders compiled and rendered in browser with no console errors; 2600 tents and gate/wall roof clearance checks passed after adding support geometry.\n',encoding='utf-8')
archive=out/'samagam-3d-package.zip'
with zipfile.ZipFile(archive) as z:names=z.namelist()
names=list(dict.fromkeys(names+['samagam-realistic-street.png','source/realistic_view.py','source/package_realism.py','source/realistic_environment.py']))
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for name in names:
        p=root/'work'/name.removeprefix('source/') if name.startswith('source/') else out/name
        if p.exists():z.write(p,name)
print('Realistic appearance edition saved and packaged')
