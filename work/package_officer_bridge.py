from pathlib import Path
import zipfile
root=Path(__file__).resolve().parents[1];out=root/'outputs';work=root/'work'
s=(work/'viewer-pdf.html').read_text(encoding='utf-8')
a=s.index('// Details for both deployed personnel');b=s.index('function depOfficerModelHit',a)
(work/'officer_details.js').write_text(s[a:b],encoding='utf-8')
notes='''\n## Officer click and bridge alignment — 20 October 2026\nOriginal deployment icons retained; no extra officer-icon overlay. Directly click an officer body at Morcha, parking, Naka, gate, chowki, traffic or other deployed duty to open information. The card shows duty location, point, type, work, shift, name, rank and mobile. Unprovided names and numbers remain Not assigned. Name, rank, mobile, work and location are editable; existing illustrative officers have a separate local identity record, included in JSON export/import, without increasing planned force counts.\n\nS04 footbridge is perpendicular to the local NH44 segment and centred on its axis. Span reduced from 60 to 42.5 illustrative model units, stair landings narrowed to 6 units. Stairs stay outside the 36-unit carriageway; the venue-side landing stays within the frontage wall clearance. Bridge/stair elevations and AK walking remain coordinated. Static GLB and interactive scene rebuilt.\n\nVerified in native browser: no duplicate officer icons, Morcha officer body click, saved name/mobile/work shown in the card (test data undone), editable fields, corrected bridge view, no console errors. Geometry checks verify centre/orientation/lane/wall clearance; AK stair and full-crossing tests pass.\n'''
for name in ['deployment-guide.md','README.md']:
 p=out/name;p.write_text(p.read_text(encoding='utf-8')+notes,encoding='utf-8')
with (out/'verification.txt').open('a',encoding='utf-8') as f:f.write(notes)
archive=out/'samagam-3d-package.zip'
with zipfile.ZipFile(archive) as z:names=z.namelist()
names+=['samagam-officer-click-info.jpg','samagam-footbridge-adjusted.jpg']+['source/'+n for n in ['officer_details.js','officer_body_click.js','test_officer_details.py','test-officer-details.cjs','test_bridge_alignment.py']]
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for name in dict.fromkeys(names):
  p=work/name[7:] if name.startswith('source/') else out/name
  if p.is_file():z.write(p,name)
print('Updated package: original icons, body-click information, corrected bridge')
