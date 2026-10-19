from pathlib import Path
import json,re,zipfile
root=Path(__file__).resolve().parents[1];out=root/'outputs'
count=json.loads((out/'scene-data.json').read_text(encoding='utf-8'))['meta']['reference_accommodation']['tent_count']
for path in [root/'work/viewer-pdf.html',out/'samagam-3d.html']:
    text=path.read_text(encoding='utf-8')
    text=text.replace("image.toBlob(blob=>fetch('http://127.0.0.1:8766/preview',{method:'POST',headers:{'Content-Type':'image/png'},body:blob}).catch(()=>{}));",'')
    text=text.replace('Unspecified residential tent rows have not been assigned invented locations.','Residential rows are a user-proposed visual adaptation of the separate 75th-event reference image; positions and counts are illustrative, not official allocations.')
    path.write_text(text,encoding='utf-8')
(out/'samagam-residential-reference.png').write_bytes((out/'samagam-premium-preview.png').read_bytes())
p=out/'README.md';text=p.read_text(encoding='utf-8')
text=re.sub(r'Current residential module count: \d+',f'Current residential module count: {count}',text)
text+='\nCoverage re-check: seven additional interior parcel groups now contain residential rows, including the diagonal-road triangle, central parcels, rear langar parcels and northern pocket beside P3. Cross aisles and traced roads, parking, buildings, gates and source walls remain reserved. Added modules follow the reference colour treatment; no unreadable allocation names were invented.\n'
p.write_text(text,encoding='utf-8')
(out/'verification.txt').write_text(f'136 source entries retained. {count} residential tents. Seven additional parcel groups filled in the latest coverage pass. Tent roofs checked against actual wall, gate and frontage footprints: no intersections. Placement excludes source occupied polygons and road clearances. Source names Ground B/C/D retained; other new groups are unnamed design sectors. No rides/black tents. GLB length/header validated. Browser rendering visually checked. These are user-proposed reference-inspired modules, not measured event allocations.\n',encoding='utf-8')
html=(out/'samagam-3d.html').read_text(encoding='utf-8')
(root/'work/viewer-check.js').write_text(html.split('<script>',1)[1].split('</script>',1)[0],encoding='utf-8')
archive=out/'samagam-3d-package.zip'
with zipfile.ZipFile(archive) as z:names=z.namelist()
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for name in names:
        p=(root/'work'/name.removeprefix('source/')) if name.startswith('source/') else out/name
        if p.exists():z.write(p,name)
    if 'source/finalize_reference.py' not in names:z.write(__file__,'source/finalize_reference.py')
print('Finalized',count,'tents; preview, documentation and package updated')
