from pathlib import Path
import json,shutil,base64,io
from PIL import Image
root=Path(__file__).resolve().parents[1];out=root/'outputs'
scene=json.loads((root/'work/scene-inline.json').read_text(encoding='utf-8'))
names=list(dict.fromkeys(o['name'] for o in scene['objects'])); mats=list(scene['colors']);shapes=list(dict.fromkeys(o['shape'] for o in scene['objects']));groups=list(dict.fromkeys(o['group'] for o in scene['objects']))
rows=[[names.index(o['name'])]+[round(v,3) for v in o['p']+o['s']]+[mats.index(o['mat']),shapes.index(o['shape']),groups.index(o['group']),round(o['rot'],5),round(o.get('tilt',0),5)]+([round(o['rz'],5)] if o.get('rz') else []) for o in scene['objects']]
packed={k:v for k,v in scene.items() if k!='objects'};packed.update(names=names,mats=mats,shapes=shapes,groups=groups,rows=rows)
for mesh in packed.get('profiles',{}).get('lotusMeshes',{}).values():
    mesh['vertices']=[[round(v,4) for v in p] for p in mesh['vertices']]
for sign in packed['signs']:
    im=Image.open(out/'sign-textures'/f"{sign['key']}.png").convert('RGB');im.thumbnail((256 if sign['key'] in ['sign-pure','sign-yogi'] else 768,1600));buf=io.BytesIO();im.quantize(colors=64).save(buf,format='PNG',optimize=True)
    sign['image']='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
geo=packed['georeference'];import numpy as np
def pixel_local(u,v):
    lon,lat=np.array([u,v,1])@np.array(geo['pixelToLonLat']);return [(lon-geo['originLongitude'])*geo['eastMetresPerDegree'],(geo['originLatitude']-lat)*geo['northMetresPerDegree']]
im=Image.open(root/'work/new-references/WhatsApp Image 2026-10-20 at 10.21.33 AM (1).jpeg').rotate(90,expand=True).crop((150,150,1370,700));im.save(out/'registered-satellite-reference.jpg',quality=72)
im.thumbnail((800,800));buf=io.BytesIO();im.save(buf,format='JPEG',quality=50)
geo['raster']={'image':'data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode(),'corners':[pixel_local(u,v) for u,v in [(150,150),(1370,150),(1370,700),(150,700)]],'source':'User-provided Google Earth screenshot, graticule calibrated; screen UI cropped outside the reference area.'}
for k in ['gridControlPoints','verticalGridFits','horizontalGridFits']:geo.pop(k,None)
fragment=(root/'work/viewer-fragment.html').read_text(encoding='utf-8').replace('__SCENE_DATA__',json.dumps(packed,ensure_ascii=False,separators=(',',':')))
viz=Path(r'C:\Users\HP\.codex\visualizations\2026\10\20\01a15786-1405-7681-bdee-4876e7a65935\gyan-mansarovar-3d.html')
viz.write_text(fragment,encoding='utf-8')
style='''<style>:root{--background:#f6f4ed;--foreground:#233b36;--card:#fff;--border:#d1d7cc;font-family:system-ui,sans-serif;color-scheme:light}body{margin:0 auto;max-width:1280px;padding:24px;background:var(--background);color:var(--foreground)}h2{font-weight:500}a{color:#356b68}.viz-controls,.viz-row{display:flex;gap:18px;align-items:center;flex-wrap:wrap}.form-label{display:flex;gap:8px;align-items:center}.form-select{font:inherit;padding:10px;background:#fff;color:#233b36;border:1px solid #c7cec4;border-radius:5px}.form-check{display:flex;align-items:center;gap:7px}.form-check-input{width:18px;height:18px}.text-small{font-size:13px}details{margin-top:16px}#gms-stage{height:650px!important}summary{cursor:pointer}.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px;margin-top:18px}.gallery img{width:100%;height:200px;object-fit:contain;background:#e3e4dc}.gallery figure{margin:0}.gallery figcaption{font-size:13px;padding-top:5px}@media(max-width:600px){body{padding:12px}#gms-stage{height:420px!important}}</style>'''
files=sorted((root/'work/references').glob('*.jpeg')); chosen=[(6,'Entrance and approach'),(18,'Scalloped hall frontage'),(25,'Building entrance portico'),(40,'Lawn and lotus pavilion'),(48,'Stage and green carpet stairs'),(56,'Hall seating and centre aisle'),(12,'CLASS ROOM — readable source lettering'),(20,'DADI PRAKASHMANI Residential Complex — source boards'),(64,'Dadi Chandermani Universal Peace Auditorium — entry plaque')]
gallery='<details><summary>Asli site reference photos (19 October 2026)</summary><div class="gallery">'
(out/'reference-photos').mkdir(exist_ok=True)
from PIL import Image,ImageOps
for index,label in chosen:
    dest=out/'reference-photos'/f'ref-{index+1}.jpg';im=Image.open(files[index]);im.thumbnail((1000,750));im.save(dest,quality=82)
    gallery+=f'<figure><img src="reference-photos/{dest.name}" alt="{label}" loading="lazy"><figcaption>{label}</figcaption></figure>'
gallery+='</div></details>'
video_gallery='<details><summary>Video analysis — source frames with timestamps</summary><div class="gallery">'
selected=[(1,'frame-002.jpg','V1 ~3s · large garden slabs and bollard lights'),(3,'frame-006.jpg','V3 ~11s · white barred entrance gates'),(3,'frame-031.jpg','V3 ~61s · scalloped frontage and window niches'),(3,'frame-049.jpg','V3 ~97s · building portico'),(5,'frame-001.jpg','V5 ~1s · stage stairs and fascia'),(7,'frame-004.jpg','V7 ~7s · chair frames, rounded backs and curtains'),(8,'start.jpg','V8 start · auditorium sign and entry'),(9,'frame-004.jpg','V9 ~7s · exterior steps and side entrance')]
(out/'video-reference-frames').mkdir(exist_ok=True)
for vid,filename,label in selected:
    src=root/'work/video-review'/f'video-{vid:02d}'/filename; dest=out/'video-reference-frames'/f'v{vid}-{filename}';shutil.copyfile(src,dest)
    video_gallery+=f'<figure><img src="video-reference-frames/{dest.name}" alt="{label}" loading="lazy"><figcaption>{label}</figcaption></figure>'
video_gallery+='</div></details>'
shutil.copyfile(root/'work/video-review/inventory.json',out/'video-review-inventory.json')
html='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gyan Mansarovar — 3D venue study</title>'+style+'<body>'+fragment+gallery+'</body></html>'
html=html.replace('</body>',video_gallery+'</body>')
satellite_gallery='<details><summary>Additional satellite references — 10:43 AM ZIP (11 screenshots)</summary><div class="gallery">'
for item in json.loads((out/'satellite-review-1043.json').read_text(encoding='utf-8')):
    satellite_gallery+=f'<figure><img src="satellite-reference-1043/{item["file"]}" alt="Satellite reference {item["index"]}" loading="lazy"><figcaption>{item["index"]}. {item["observation"]}</figcaption></figure>'
satellite_gallery+='</div></details>'
html=html.replace('</body>',satellite_gallery+'</body>')
lotus_gallery='<details><summary>Lotus pavilion — focused source comparison</summary><div class="gallery">'
for filename,label in [('v1-0.jpg','Video 1 start — dome, drum and illuminated finial'),('v4-0.jpg','Video 4 start — elevated petal rim and white drum'),('v4-27.jpg','Video 4 27 seconds — second pavilion view'),('photo-20.jpg','Photo 20 — pink dome springing motifs and garden context')]:
    lotus_gallery+=f'<figure><img src="lotus-reference-frames/{filename}" alt="{label}" loading="lazy"><figcaption>{label}</figcaption></figure>'
lotus_gallery+='</div></details>'
html=html.replace('</body>',lotus_gallery+'</body>')
architecture_gallery='<details><summary>New architecture references — 12 images and change notes</summary><div class="gallery">'
for item in json.loads((out/'architectural-photo-review.json').read_text(encoding='utf-8')):
    architecture_gallery+=f'<figure><img src="architectural-reference-photos/{item["file"]}" alt="{item["observation"]}" loading="lazy"><figcaption>{item["observation"]}<br>{item["action"]}</figcaption></figure>'
architecture_gallery+='</div><p><a href="ARCHITECTURAL-PHOTO-REVIEW.md">Detailed review and remaining uncertainties</a> · <a href="dadi-janki-health-centre-facade-study.glb">Health-centre facade study (location unverified)</a></p></details>'
html=html.replace('</body>',architecture_gallery+'</body>')
(out/'gyan-mansarovar-3d.html').write_text(html,encoding='utf-8')
print('Inline fragment bytes:',viz.stat().st_size,'; viewer:',len(html.encode()))
