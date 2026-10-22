from pathlib import Path
from PIL import Image
import json,hashlib,shutil
root=Path(__file__).resolve().parents[1];out=root/'outputs';dest=out/'satellite-reference-1043';dest.mkdir(exist_ok=True)
observations=[
'Pavilion close-up: concentric terrace edges, central roof, surrounding planting and crossing paths. Dome height and petal geometry cannot be measured from this view.',
'Wide northeast context: large industrial roofs, solar arrays, fields and road. BAMC roof lettering visible; this does not establish campus ownership.',
'Wide southwest context: three adjoining roofed blocks, fields, tracks and the landscaped enclosure across the road. Ownership boundaries remain unverified.',
'Eastern industrial compound and diagonal rural road. Large BAMC roof lettering is visible; no new campus facade sign is established.',
'Approach road close-up: paved corridor, tree-lined edge, entrance opening and fields opposite the pavilion.',
'Road north/east of the core: individual access aprons and neighboring industrial forecourts. A phone volume overlay obscures part of the source.',
'Nearby industrial roofs and solar arrays, court access and the campus-adjacent blue roof. No affiliation inferred from proximity.',
'Fields across the approach road, visible tracks and planted edges. A dark rectangular ground feature has unknown use.',
'Southern building roof with multiple solar banks, narrow rear wing and adjacent field. Room divisions cannot be inferred from roof seams.',
'Blue-roof building close-up with two small panel banks, pavilion terraces, small red roof and garden paths.',
'Field between the southern campus block and eastern industry, roof arrays and light-colored garden stacks. Stack purpose/date unknown.'
]
files=sorted((root/'work/references-1043').glob('*.jpeg'));inventory=[]
for i,(p,obs) in enumerate(zip(files,observations),1):
 im=Image.open(p);shutil.copyfile(p,dest/p.name)
 inventory.append(dict(index=i,file=p.name,size=list(im.size),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),exifGPS=bool(im.getexif().get(34853)),observation=obs))
(out/'satellite-review-1043.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
text='# Additional satellite review — ZIP received 10:43 AM\n\nAll 11 JPEG screenshots were inspected at full resolution. There are no videos in this archive and no EXIF GPS tags. They show Google Earth with a printed coordinate grid, rotated views and phone controls. The phone screenshot time does not establish the satellite capture date.\n\n'
text+='\n\n'.join(f"{i['index']}. **{i['file']}** — {i['observation']}" for i in inventory)
text+='\n\n## Model changes and limits\n\nAdded visible concentric pavilion terrace edges and the small solar banks on the blue roof in the existing registered coordinate frame. The previous grid calibration remains the spatial reference; these screenshots were used as visual corroboration, not as newly measured survey controls. No extra gate, new interior room or measured height is established by this archive.\n\nThe industrial roof lettering is recorded as source evidence. It has not been repainted onto an approximate industrial mesh whose full footprint is not yet registered. Nearby roads, fields and industrial massing beyond the registered crop remain approximate. Ground photos/videos remain the source for gate shape, paint, facade names and hall interior.\n'
(out/'SATELLITE-REVIEW-1043.md').write_text(text,encoding='utf-8')
readme=out/'READ-ME.txt';s=readme.read_text(encoding='utf-8');s=s.replace('20 October 2026\n','20 October 2026\n\nREVISION 5: Reviewed all 11 screenshots in the 10:43 AM ZIP; pavilion\nterrace edges and blue-roof solar modules refined. No videos in this archive.\nSee SATELLITE-REVIEW-1043.md and satellite-review-1043.json.\n',1);readme.write_text(s,encoding='utf-8')
print('Reviewed and archived',len(inventory),'satellite screenshots')
