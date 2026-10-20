from pathlib import Path
from PIL import Image
import shutil,json
root=Path(__file__).resolve().parents[1];out=root/'outputs';dest=out/'architectural-reference-photos';dest.mkdir(exist_ok=True)
rows=[
('110115','Side-on lotus detail: rounded upper petals; long lower inverted petal flutes; thin narrow windows; white eave and serrated pink dome band.','Rebuilt sculpted pink upper/lower petal meshes and sparse windows.'),
('110133','Frontal lotus: central break in petal ring, glazed entrance, broad curved dark stair, light nosings, side pots, raised front bed and globe lights.','Opened the petal rim and drum; added fan-shaped stair, door frames, pots, flower bed and lights.'),
('110153','May 2018: long two-storey residential facade, horizontal metal balcony/roof rails and solar array; white historic portico.','Added gallery/roof rails and roof service masses. Retained latest 2026 signboard and pink portico rather than overwriting it with 2018 appearance.'),
('110207','March 2022: pavilion side form, lawns, paths, trees and edge fencing.','Used as contextual silhouette check; foreground people are not venue geometry.'),
('110220','Hall and pavilion relationship; clipped shrubs, palms, garden path, low lamps; partial Hindi hall fascia lettering.','Checked landscape relationships. Cropped words were not invented as a complete inscription.'),
('110234','July 2016: lawn and historic gate appearance.','Recorded as historical evidence; no temporary sports furniture or people treated as fixed infrastructure.'),
('110248','January 2022: Dadi Janki Positive Health Care Centre, single-storey white facade, central glazed doors, side windows, Hindi/English signboards.','Created a separate facade-study GLB. Exact campus footprint and current state are unconfirmed; no geographic placement assigned.'),
('110303','January 2022: residential portico, metal gallery rails, rooftop array, landscaping, parking/turning markings and circular ground feature.','Refined rails and roof masses; older parking paint, banners and ground feature are recorded but not asserted as verified 2026 details.'),
('110314','December 2022: red तपस्या धाम label, narrow barred windows, tall glazed door, curved stair and planted raised bed.','Added the readable entrance label and refined door/window and front planting details. Exact rear text is unknown.'),
('110332','Earlier unfinished facade with exposed upper reinforcement, open gallery, roof rails and temporary banner.','Historic construction state recorded; 2026 photos take precedence for finish and current banner.'),
('110902','Current night gate: two pedestrian side openings with closed ornamental leaves; large open main leaves; four piers; full upper beam and lighting.','Added both small side gates with bars, rings, curved tops, finials/latches, outer piers and soffits; widened beam/sign and moved frontage returns to outer piers.'),
]
inventory=[]
for suffix,observation,change in rows:
 p=Path(f'C:/Users/HP/Pictures/Screenshots/Screenshot 2026-10-20 {suffix}.png');shutil.copyfile(p,dest/p.name)
 inventory.append(dict(file=p.name,dimensions=list(Image.open(p).size),observation=observation,action=change))
p=Path('C:/Users/HP/Downloads/Retreat-centre-Panipat-5.jpg');shutil.copyfile(p,dest/p.name)
inventory.append(dict(file=p.name,dimensions=list(Image.open(p).size),observation='Wide frontal pavilion view: straight broad walkway, paired fan palms, globe-post rows, yellow/green planting borders, front flower bed, stair and entrance; parking paint in foreground.',action='Added straight pavilion walkway, lamp rows and paired fan palms. Parking marking age/location is not established as current.'))
(out/'architectural-photo-review.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf8')
text='# Architectural reference review — 12 new images\n\nEvery newly supplied image was inspected. Several Google Maps photos are explicitly dated 2016–2022; the photo upload/screenshot date is not necessarily the image capture date. The 2026 ground photos take precedence where finishes/signboards differ.\n\n'
for i,r in enumerate(inventory,1):text+=f"## {i}. {r['file']}\n\n{r['observation']}\n\n**Action:** {r['action']}\n\n"
text+='## Remaining limits\n\nSource coverage is much better, but the reconstruction is not a survey or an exact photogrammetric replica. Metric dimensions, petal/step/window counts and detailed placement are estimated. The full finial emblem, tiny painted words, exact curved ornament, rear faces and interior of the lotus pavilion are not completely resolved. No guarantee that every hidden feature has been recorded is supported by these images. The historical health-centre facade is a separate study; assigning it to a guessed campus roof would create false location information.\n'
(out/'ARCHITECTURAL-PHOTO-REVIEW.md').write_text(text,encoding='utf8')
p=out/'READ-ME.txt';s=p.read_text(encoding='utf8');s=s.replace('20 October 2026\n','20 October 2026\n\nREVISION 8: 12 additional architectural references reviewed. Sculpted pink\nlotus petal courses, open entrance, curved dark steps, pots, windows,\nname, broad walkway, lights, palms; residential rails; BOTH side gates.\nSee ARCHITECTURAL-PHOTO-REVIEW.md. A separate health-centre facade study\nis supplied without geographic placement. Historical views are documented.\n',1);p.write_text(s,encoding='utf8')
print('Archived and documented',len(inventory),'new architectural references')
