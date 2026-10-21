from pathlib import Path
import json,shutil,base64,io
from PIL import Image

root = Path(__file__).resolve().parents[1]
out = root / 'outputs'

scene = json.loads((root / 'work/scene-inline.json').read_text(encoding='utf-8'))
names = list(dict.fromkeys(o['name'] for o in scene['objects']))
mats = list(scene['colors'])
shapes = list(dict.fromkeys(o['shape'] for o in scene['objects']))
groups = list(dict.fromkeys(o['group'] for o in scene['objects']))

rows = [
    [names.index(o['name'])]
    + [round(v, 2) for v in o['p']]
    + [round(v, 3) for v in o['s']]
    + [mats.index(o['mat']), shapes.index(o['shape']), groups.index(o['group']), round(o['rot'], 5), round(o.get('tilt', 0), 5)]
    + ([round(o['rz'], 5)] if o.get('rz') else [])
    for o in scene['objects']
]
for row in rows:
    while len(row) > 10 and row[-1] == 0:
        row.pop()

packed = {k: v for k, v in scene.items() if k != 'objects'}
packed.update(names=names, mats=mats, shapes=shapes, groups=groups, rows=rows)

for mesh in packed.get('profiles', {}).get('lotusMeshes', {}).values():
    mesh['vertices'] = [[round(v, 4) for v in p] for p in mesh['vertices']]

for sign in packed['signs']:
    im = Image.open(out / 'sign-textures' / f"{sign['key']}.png").convert('RGB')
    im.thumbnail((256 if sign['key'] in ['sign-pure', 'sign-yogi'] else 768, 1600))
    buf = io.BytesIO()
    im.quantize(colors=64).save(buf, format='PNG', optimize=True)
    sign['image'] = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

geo = packed['georeference']
import numpy as np

def pixel_local(u, v):
    lon, lat = np.array([u, v, 1]) @ np.array(geo['pixelToLonLat'])
    return [(lon - geo['originLongitude']) * geo['eastMetresPerDegree'], (geo['originLatitude'] - lat) * geo['northMetresPerDegree']]

im = Image.open(root / 'work/new-references/WhatsApp Image 2026-10-20 at 10.21.33 AM (1).jpeg').rotate(90, expand=True).crop((150, 150, 1370, 700))
im.save(out / 'registered-satellite-reference.jpg', quality=72)
im.thumbnail((600, 600))
buf = io.BytesIO()
im.save(buf, format='JPEG', quality=42)
geo['raster'] = {
    'image': 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode(),
    'corners': [pixel_local(u, v) for u, v in [(150, 150), (1370, 150), (1370, 700), (150, 700)]],
    'source': 'User-provided Google Earth screenshot, graticule calibrated; screen UI cropped outside the reference area.'
}
for k in ['gridControlPoints', 'verticalGridFits', 'horizontalGridFits']:
    geo.pop(k, None)

fragment = (
    (root / 'work/viewer-fragment.html')
    .read_text(encoding='utf-8')
    .replace('__DEPLOYMENT_PANEL__', (root / 'work/deployment-panel.html').read_text(encoding='utf-8'))
    .replace('__DEPLOYMENT_JS__', (root / 'work/deployment.js').read_text(encoding='utf-8'))
    .replace('__SCENE_DATA__', json.dumps(packed, ensure_ascii=False, separators=(',', ':')))
)

viz = Path(r'C:\Users\HP\.codex\visualizations\2026\10\20\01a15786-1405-7681-bdee-4876e7a65935\gyan-mansarovar-3d.html')
if viz.parent.exists():
    inline_fragment = fragment
    if len(inline_fragment.encode('utf-8')) > 1000000:
        import gzip
        payload = json.dumps(packed, ensure_ascii=False, separators=(',', ':'))
        zipped = base64.b64encode(gzip.compress(payload.encode('utf-8'), mtime=0)).decode('ascii')
        expression = "await new Response(new Blob([Uint8Array.from(atob('" + zipped + "'),c=>c.charCodeAt(0))]).stream().pipeThrough(new DecompressionStream('gzip'))).json()"
        inline_fragment = inline_fragment.replace('(()=>{', '(async()=>{', 1).replace('const data='+payload+';', 'const data='+expression+';', 1)
    assert len(inline_fragment.encode('utf-8')) < 1000000
    viz.write_text(inline_fragment, encoding='utf-8')

style = '''<style>
:root {
  --bg-page: #0f172a;
  --bg-container: #ffffff;
  --text-main: #0f172a;
  --text-muted: #64748b;
  --border-color: #e2e8f0;
  --primary: #0284c7;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color-scheme: light;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  padding: 20px 16px;
  background: #f1f5f9;
  color: var(--text-main);
  min-height: 100vh;
}
.app-wrapper {
  max-width: 1360px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
/* Modern Reference Hub */
.ref-hub-card {
  background: #ffffff;
  border-radius: 14px;
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 14px rgba(0,0,0,0.06);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.ref-hub-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border-color);
}
.ref-hub-title-wrap { display: flex; align-items: center; gap: 10px; }
.ref-badge {
  background: #e0f2fe;
  color: #0369a1;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 9px;
  border-radius: 9999px;
}
.ref-hub-title { margin: 0; font-size: 18px; font-weight: 700; color: var(--text-main); }
.ref-tabs-nav {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
.ref-tab-btn {
  padding: 7px 14px;
  font-size: 13px;
  font-weight: 600;
  background: #f8fafc;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.16s ease;
}
.ref-tab-btn:hover { background: #f1f5f9; color: var(--text-main); }
.ref-tab-btn.active {
  background: #0284c7;
  border-color: #0284c7;
  color: #fff;
  box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3);
}

.ref-tab-pane { display: none; }
.ref-tab-pane.active { display: block; animation: fadeIn 0.2s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(3px); } to { opacity: 1; transform: translateY(0); } }

.ref-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}
.ref-card {
  margin: 0;
  background: #f8fafc;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.ref-card img {
  width: 100%;
  height: 190px;
  object-fit: cover;
  background: #e2e8f0;
  transition: transform 0.2s ease;
}
.ref-card:hover img { transform: scale(1.02); }
.ref-card figcaption {
  padding: 10px 12px;
  font-size: 12.5px;
  font-weight: 500;
  color: var(--text-main);
  background: #fff;
  border-top: 1px solid var(--border-color);
  flex-grow: 1;
}

.audit-notes-card {
  background: #f8fafc;
  padding: 16px;
  border-radius: 10px;
  border: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  gap: 10px;
  font-size: 13px;
  line-height: 1.6;
}
.audit-links-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 6px;
}
.audit-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  font-size: 12.5px;
  font-weight: 600;
  color: #0369a1;
  background: #e0f2fe;
  border-radius: 6px;
  text-decoration: none;
  transition: all 0.16s ease;
}
.audit-link:hover { background: #bae6fd; }
</style>'''

files = sorted((root / 'work/references').glob('*.jpeg'))
chosen = [
    (6, 'Entrance and approach'),
    (18, 'Scalloped hall frontage'),
    (25, 'Building entrance portico'),
    (40, 'Lawn and lotus pavilion'),
    (48, 'Stage and green carpet stairs'),
    (56, 'Hall seating and centre aisle'),
    (12, 'CLASS ROOM — readable source lettering'),
    (20, 'DADI PRAKASHMANI Residential Complex — source boards'),
    (64, 'Dadi Chandermani Universal Peace Auditorium — entry plaque'),
]
(out / 'reference-photos').mkdir(exist_ok=True)
photos_html = '<div class="ref-grid">'
for index, label in chosen:
    dest = out / 'reference-photos' / f'ref-{index+1}.jpg'
    im = Image.open(files[index])
    im.thumbnail((1000, 750))
    im.save(dest, quality=82)
    photos_html += f'<figure class="ref-card"><img src="reference-photos/{dest.name}" alt="{label}" loading="lazy"><figcaption>{label}</figcaption></figure>'
photos_html += '</div>'

selected_videos = [
    (1, 'frame-002.jpg', 'V1 ~3s · large garden slabs and bollard lights'),
    (3, 'frame-006.jpg', 'V3 ~11s · white barred entrance gates'),
    (3, 'frame-031.jpg', 'V3 ~61s · scalloped frontage and window niches'),
    (3, 'frame-049.jpg', 'V3 ~97s · building portico'),
    (5, 'frame-001.jpg', 'V5 ~1s · stage stairs and fascia'),
    (7, 'frame-004.jpg', 'V7 ~7s · chair frames, rounded backs and curtains'),
    (8, 'start.jpg', 'V8 start · auditorium sign and entry'),
    (9, 'frame-004.jpg', 'V9 ~7s · exterior steps and side entrance'),
]
(out / 'video-reference-frames').mkdir(exist_ok=True)
video_html = '<div class="ref-grid">'
for vid, filename, label in selected_videos:
    src = root / 'work/video-review' / f'video-{vid:02d}' / filename
    dest = out / 'video-reference-frames' / f'v{vid}-{filename}'
    shutil.copyfile(src, dest)
    video_html += f'<figure class="ref-card"><img src="video-reference-frames/{dest.name}" alt="{label}" loading="lazy"><figcaption>{label}</figcaption></figure>'
video_html += '</div>'
shutil.copyfile(root / 'work/video-review/inventory.json', out / 'video-review-inventory.json')

satellite_html = '<div class="ref-grid">'
for item in json.loads((out / 'satellite-review-1043.json').read_text(encoding='utf-8')):
    satellite_html += f'<figure class="ref-card"><img src="satellite-reference-1043/{item["file"]}" alt="Satellite reference {item["index"]}" loading="lazy"><figcaption><b>Ref #{item["index"]}</b> · {item["observation"]}</figcaption></figure>'
satellite_html += '</div>'

lotus_html = '<div class="ref-grid">'
for filename, label in [
    ('v1-0.jpg', 'Video 1 start — dome, drum and illuminated finial'),
    ('v4-0.jpg', 'Video 4 start — elevated petal rim and white drum'),
    ('v4-27.jpg', 'Video 4 27 seconds — second pavilion view'),
    ('photo-20.jpg', 'Photo 20 — pink dome springing motifs and garden context'),
]:
    lotus_html += f'<figure class="ref-card"><img src="lotus-reference-frames/{filename}" alt="{label}" loading="lazy"><figcaption>{label}</figcaption></figure>'
lotus_html += '</div>'

arch_html = '<div class="ref-grid">'
for item in json.loads((out / 'architectural-photo-review.json').read_text(encoding='utf-8')):
    arch_html += f'<figure class="ref-card"><img src="architectural-reference-photos/{item["file"]}" alt="{item["observation"]}" loading="lazy"><figcaption><b>Observation:</b> {item["observation"]}<br><b>Model Action:</b> {item["action"]}</figcaption></figure>'
arch_html += '</div><div class="audit-links-row" style="margin-top:12px;"><a class="audit-link" href="ARCHITECTURAL-PHOTO-REVIEW.md" target="_blank">📄 Read Full Architectural Review Report</a><a class="audit-link" href="dadi-janki-health-centre-facade-study.glb" target="_blank">📦 Download Health-Centre Facade GLB</a></div>'

notes_html = '''<div class="audit-notes-card">
  <p><b>References Reviewed:</b> 65 ground photos, 147 video frames, and WGS84 graticule calibrated Google Earth satellite captures. All heights, bay counts, non-visible room layouts, and chair counts (~840) are schematic estimates.</p>
  <p><b>YouTube Audit:</b> Campus walkthroughs and garden reels cross-verified for stage materials, carpet patterns, side stair locations, and light fixtures.</p>
  <div class="audit-links-row">
    <a class="audit-link" href="READ-ME.txt" target="_blank">📄 Read-Me (Revisions 1–15)</a>
    <a class="audit-link" href="DEPLOYMENT-GUIDE.md" target="_blank">👮 Police Deployment Guide</a>
    <a class="audit-link" href="STAGE-ACCESS-CORRECTION.md" target="_blank">🪜 Stage Access Correction</a>
    <a class="audit-link" href="NAME-CORRECTIONS.md" target="_blank">🏷️ Verified Map Pins</a>
    <a class="audit-link" href="YOUTUBE-DETAIL-REVIEW.md" target="_blank">▶️ YouTube Detail Review</a>
    <a class="audit-link" href="https://maps.app.goo.gl/JG881XSsXu1Vi61L9?g_st=aw" target="_blank" rel="noopener">🗺️ Google Maps Location</a>
    <a class="audit-link" href="https://panipat.bk.ooo/?p=2036" target="_blank" rel="noopener">🌐 Official Venue Report</a>
  </div>
</div>'''

ref_hub = f'''
<section class="ref-hub-card">
  <div class="ref-hub-header">
    <div class="ref-hub-title-wrap">
      <span class="ref-badge">📚 Verification Hub</span>
      <h3 class="ref-hub-title">Reference Imagery &amp; Audit Logs</h3>
    </div>
    <div class="ref-tabs-nav" id="ref-tabs">
      <button type="button" class="ref-tab-btn active" data-tab="tab-photos">📸 Site Photos (9)</button>
      <button type="button" class="ref-tab-btn" data-tab="tab-videos">🎥 Video Frames (8)</button>
      <button type="button" class="ref-tab-btn" data-tab="tab-satellite">🛰️ Satellite GIS (11)</button>
      <button type="button" class="ref-tab-btn" data-tab="tab-lotus">🪷 Lotus Pavilion (4)</button>
      <button type="button" class="ref-tab-btn" data-tab="tab-arch">🏛️ Architecture (12)</button>
      <button type="button" class="ref-tab-btn" data-tab="tab-notes">📋 Audit &amp; Accuracy</button>
    </div>
  </div>
  <div id="tab-photos" class="ref-tab-pane active">{photos_html}</div>
  <div id="tab-videos" class="ref-tab-pane">{video_html}</div>
  <div id="tab-satellite" class="ref-tab-pane">{satellite_html}</div>
  <div id="tab-lotus" class="ref-tab-pane">{lotus_html}</div>
  <div id="tab-arch" class="ref-tab-pane">{arch_html}</div>
  <div id="tab-notes" class="ref-tab-pane">{notes_html}</div>
</section>
<script>
document.querySelectorAll('#ref-tabs .ref-tab-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('#ref-tabs .ref-tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.ref-tab-pane').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    const target = document.getElementById(btn.dataset.tab);
    if(target) target.classList.add('active');
  }});
}});
</script>
'''

full_html = (
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Gyan Mansarovar — Interactive 3D Study &amp; Deployment</title>'
    + style
    + '</head><body><div class="app-wrapper">'
    + fragment
    + ref_hub
    + '</div></body></html>'
)

(out / 'gyan-mansarovar-3d.html').write_text(full_html, encoding='utf-8')
print('Successfully generated clean modern viewer: bytes =', len(full_html.encode()))
