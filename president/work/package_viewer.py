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

/* Deployed Asset Catalog & Lightbox Styles */
.dep-catalog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  background: #f8fafc;
  padding: 14px 18px;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  margin-bottom: 16px;
}
.dep-catalog-filter-bar {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.dep-filter-btn {
  padding: 6px 12px;
  font-size: 12.5px;
  font-weight: 600;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: #fff;
  color: var(--text-main);
  cursor: pointer;
  transition: all 0.15s ease;
}
.dep-filter-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}
.dep-filter-btn.active {
  background: #0284c7;
  color: #fff;
  border-color: #0284c7;
  box-shadow: 0 2px 6px rgba(2, 132, 199, 0.25);
}
.dep-total-badge {
  font-size: 13px;
  font-weight: 700;
  color: #0369a1;
  background: #e0f2fe;
  padding: 5px 12px;
  border-radius: 9999px;
  border: 1px solid #bae6fd;
}
.dep-asset-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}
.dep-asset-card {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.dep-asset-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.09);
  border-color: #cbd5e1;
}
.dep-asset-thumb-wrap {
  position: relative;
  background: #0f172a;
  height: 220px;
  overflow: hidden;
  cursor: pointer;
}
.dep-asset-thumb-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}
.dep-asset-card:hover .dep-asset-thumb-wrap img {
  transform: scale(1.03);
}
.dep-zoom-hint {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(15, 23, 42, 0.85);
  color: #fff;
  font-size: 11.5px;
  padding: 4px 9px;
  border-radius: 6px;
  backdrop-filter: blur(4px);
  pointer-events: none;
}
.dep-live-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  font-size: 11.5px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 9999px;
  backdrop-filter: blur(4px);
}
.dep-live-badge.badge-active {
  background: rgba(16, 185, 129, 0.9);
  color: #fff;
  box-shadow: 0 2px 6px rgba(16, 185, 129, 0.4);
}
.dep-live-badge.badge-zero {
  background: rgba(100, 116, 139, 0.85);
  color: #e2e8f0;
}
.dep-asset-body {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex-grow: 1;
}
.dep-asset-title-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}
.dep-asset-title {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: var(--text-main);
}
.dep-asset-hindi {
  font-size: 13px;
  font-weight: 600;
  color: #0284c7;
  margin-top: 2px;
}
.dep-asset-role-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
  background: #f1f5f9;
  color: #475569;
}
.dep-asset-desc {
  font-size: 12.5px;
  line-height: 1.5;
  color: #64748b;
  margin: 0;
}
.dep-asset-spec-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 11.5px;
  color: #334155;
  line-height: 1.5;
}
.dep-asset-spec-box b {
  color: #0f172a;
}
.dep-asset-actions {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.dep-asset-instances-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  max-height: 110px;
  overflow-y: auto;
  padding: 6px 0;
}
.dep-instance-jump-btn {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  color: #1d4ed8;
  font-size: 11.5px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.14s ease;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.dep-instance-jump-btn:hover {
  background: #dbeafe;
  border-color: #93c5fd;
  color: #1e40af;
}
/* Modal Lightbox */
.dep-lightbox-modal {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(6px);
  z-index: 10000;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.dep-lightbox-modal.show {
  display: flex;
  animation: fadeIn 0.2s ease;
}
.dep-lightbox-content {
  background: #fff;
  border-radius: 16px;
  max-width: 840px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 50px rgba(0,0,0,0.3);
  position: relative;
  display: flex;
  flex-direction: column;
}
.dep-lightbox-close {
  position: absolute;
  top: 14px;
  right: 16px;
  background: rgba(15, 23, 42, 0.7);
  color: #fff;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: background 0.15s ease;
}
.dep-lightbox-close:hover {
  background: #ef4444;
}
.dep-lightbox-img {
  width: 100%;
  max-height: 480px;
  object-fit: contain;
  background: #0f172a;
}
.dep-lightbox-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* Equipment Lightbox Media Modal */
.dep-lightbox-media-wrap {
  position: relative;
  background: radial-gradient(circle at 50% 50%, #1e293b 0%, #090d16 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 360px;
  max-height: 500px;
  overflow: hidden;
}
.dep-lightbox-img {
  width: 100%;
  max-height: 500px;
  object-fit: contain;
  display: block;
}
.dep-modal-nav-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(6px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: #fff;
  font-size: 28px;
  line-height: 40px;
  text-align: center;
  cursor: pointer;
  z-index: 10;
  transition: all 0.15s ease;
  user-select: none;
}
.dep-modal-nav-arrow:hover {
  background: #0284c7;
  border-color: #38bdf8;
  transform: translateY(-50%) scale(1.1);
}
.dep-modal-nav-arrow.left { left: 16px; }
.dep-modal-nav-arrow.right { right: 16px; }

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


# Catalog items for the Verification Hub deployment panel
catalog_items = [
    {
        "kind": "officer",
        "symbol": "👮",
        "name": "Police Duty Personnel",
        "hindi": "सुरक्षा कर्मी / पुलिस अधिकारी",
        "role": "Sector Security & VIP Cordon",
        "desc": "On-ground Haryana Police personnel stationed at main gates, auditorium entrances, perimeter cordons, and VIP movement routes.",
        "specs": "Khaki Uniform · Peak Cap · Leather Duty Belt · VHF Wireless · Direct Walk/Run/Jump Keyboard Driving Controls",
        "guideline": "Stationed in 8-hour tactical shifts across active venue sectors."
    },
    {
        "kind": "barricade",
        "symbol": "🚧",
        "name": "Heavy Crowd Barricade",
        "hindi": "सुरक्षा बैरिकेड / रोड ब्लॉकर",
        "role": "Crowd Segregation & Road Blocking",
        "desc": "Heavy-duty crowd restriction steel barricade with diagonal yellow/black retro-reflective caution stripes. Establishes sterile queues and vehicular road closures.",
        "specs": "Galvanized Tubular Steel · 2.0m x 1.2m · Retro-Reflective Hazard Banding · Interlocking Side Connectors",
        "guideline": "Deployed along approach roads, choke points, and main entrance corridors."
    },
    {
        "kind": "dfmd",
        "symbol": "🚪",
        "name": "Door Frame Metal Detector",
        "hindi": "DFMD सिक्योरिटी गेट",
        "role": "Walk-Through Pedestrian Screening",
        "desc": "Multi-zone walk-through archway metal detector with vertical LED zone lights and digital transit counter for primary screening at major venue entrances.",
        "specs": "Multi-Zone Detection Arch · Digital LCD Display · Visual/Audible Alarms · 1.8m Height",
        "guideline": "Mandatory at Main Gate and Auditorium entry points for zero-compromise security."
    },
    {
        "kind": "hhmd",
        "symbol": "🔍",
        "name": "Hand-Held Metal Detector",
        "hindi": "HHMD स्कैनर वैंड",
        "role": "Close-Contact Frisking Wand",
        "desc": "High-sensitivity manual frisking scanner wand with 360-degree detection coil, ergonomic ribbed grip, and multi-tone vibration/audio alarms.",
        "specs": "360° Search Loop · Audio & Haptic Vibration Alerts · Ferrous/Non-Ferrous Detection",
        "guideline": "Carried by frisking staff stationed adjacent to DFMD archways."
    },
    {
        "kind": "binocular",
        "symbol": "🔭",
        "name": "Rooftop Spotter Binoculars",
        "hindi": "दूरबीन / वॉचटावर पोस्ट",
        "role": "Elevated Long-Range Surveillance",
        "desc": "Military-grade 20x80 high-magnification optical binoculars mounted on heavy-duty aluminum tripod stands for perimeter overwatch from elevated roofs.",
        "specs": "20x80 Multi-Coated Optics · 360° Panoramic Fluid Tripod Head · Wide Field of View",
        "guideline": "Stationed on Universal Peace Auditorium roof and Lotus Pavilion elevated terraces."
    },
    {
        "kind": "radio",
        "symbol": "📻",
        "name": "VHF Police Wireless Radio",
        "hindi": "वायरलेस वॉकी-टॉकी सेट",
        "role": "Tactical Voice Communications",
        "desc": "Heavy-duty ruggedized handheld tactical VHF/UHF wireless transceiver connecting sector officers with the centralized police bandobast control room.",
        "specs": "5W VHF Output · Backlit LCD Screen · PTT Side Switch · IP67 Weatherproof",
        "guideline": "Issued to all sector officers and flying squad mobile patrols."
    },
    {
        "kind": "cone",
        "symbol": "⚠️",
        "name": "Reflective Traffic Cone",
        "hindi": "रिफ्लेक्टिव ट्रैफिक कोन",
        "role": "Lane Guidance & Hazard Marking",
        "desc": "Day-glo fluorescent orange traffic cones with dual micro-prismatic white retro-reflective collars and heavy anti-roll rubber bases for approach roads.",
        "specs": "750mm PVC Height · High-Tack Prismatic Collars · Heavy Recycled Rubber Base",
        "guideline": "Lined along Assan-Thirana road, parking approach, and emergency egress corridors."
    },
    {
        "kind": "cctv",
        "symbol": "📹",
        "name": "PTZ Surveillance CCTV Camera",
        "hindi": "360° सीसीटीवी कैमरा",
        "role": "24x7 Continuous Video Feed",
        "desc": "Weatherproof motorized pan-tilt-zoom security dome camera mounted on elevated masts, transmitting live high-definition video to the command monitoring center.",
        "specs": "4K Ultra-HD Resolution · 36x Optical Zoom · 100m Infrared Night Vision · IP66 Casing",
        "guideline": "Mounted at main gates, perimeter corners, central lawns, and stage surroundings."
    },
    {
        "kind": "light",
        "symbol": "💡",
        "name": "High-Intensity Floodlight Mast",
        "hindi": "फ्लड लाइट सर्चलाइट मस्तूल",
        "role": "Perimeter Night Illumination",
        "desc": "Portable telescopic lighting mast equipped with high-output quad-LED floodlight arrays on outrigger tripod legs for illumination of night routes and open grounds.",
        "specs": "4x 500W High-Lumen LED Array · 6m Telescopic Mast · 120° Beam Angle · Integrated Base",
        "guideline": "Stationed at parking zones, outer boundary roads, and dark spots across the complex."
    },
    {
        "kind": "ambulance",
        "symbol": "🚑",
        "name": "Emergency Medical Ambulance",
        "hindi": "आपातकालीन एम्बुलेंस (ALS)",
        "role": "Critical Life Support & Evacuation",
        "desc": "Advanced Life Support ambulance equipped with oxygen, defibrillator, emergency trauma kit, and stretcher dock on constant standby.",
        "specs": "Advanced Life Support · Stretcher Dock · Dual Siren/Beacon · Direct Highway Access",
        "guideline": "Stationed at Dadi Janki Health Centre portico and Main Gate standby zone."
    },
    {
        "kind": "firebrigade",
        "symbol": "🚒",
        "name": "Fire Rescue Tender Truck",
        "hindi": "अग्नि शमन वाहन / दमकल",
        "role": "Fire Suppression & Heavy Rescue",
        "desc": "High-capacity emergency fire rescue tender truck with high-pressure hose reels, water/foam monitor, and rescue extraction equipment.",
        "specs": "4500L Water/Foam Capacity · High-Pressure Hose Reel · Multi-Stage Heavy Pump · Roof Ladder",
        "guideline": "Positioned near Main Gate forecourt for rapid dispatch across venue sectors."
    },
    {
        "kind": "qbelt",
        "symbol": "🎗️",
        "name": "Retractable Q-Belt Barrier",
        "hindi": "क्यू-बेल्ट कतार बैरियर",
        "role": "Pedestrian Queue Channelization",
        "desc": "Stainless steel queue stanchion posts with high-tension red retractable nylon webbing belts for disciplined corridor movement.",
        "specs": "Stainless Steel Posts · 2.5m Red Woven Belt · Heavy Weighted Base · 4-Way Clip Heads",
        "guideline": "Arranged at registration desks, security gates, and auditorium foyer entrances."
    },
    {
        "kind": "square_box",
        "symbol": "📦",
        "name": "Security Checkpost Booth",
        "hindi": "सुरक्षा बूथ / चेकिंग काउंटर",
        "role": "Static Guard Sentry Post",
        "desc": "Modular weather-protected security cabin booth for duty sentries, pass verification, cloakroom baggage collection, and gate coordination.",
        "specs": "Weatherproof Insulated Enclosure · Observation Windows · Heavy Counter Desk · Cable Ports",
        "guideline": "Stationed at VIP reception gate and public parking entry barriers."
    }
]

dep_assets_dir = out / 'deployment-assets'
item_images_b64 = {}
catalog_json_map = {}
for it in catalog_items:
    k = it['kind']
    img_p = dep_assets_dir / f"{k}.png"
    if img_p.exists():
        item_images_b64[k] = "data:image/png;base64," + base64.b64encode(img_p.read_bytes()).decode('ascii')
    else:
        item_images_b64[k] = ""
    catalog_json_map[k] = {
        "kind": k,
        "name": it["name"],
        "hindi": it["hindi"],
        "symbol": it["symbol"],
        "role": it["role"],
        "desc": it["desc"],
        "specs": it["specs"],
        "guideline": it["guideline"],
        "img": item_images_b64[k]
    }

deployed_items_html = '''
<div class="dep-catalog-header">
  <div class="dep-catalog-filter-bar" id="dep-catalog-filters">
    <button type="button" class="dep-filter-btn active" data-filter="all">🌟 All Items (13 Types)</button>
    <button type="button" class="dep-filter-btn" data-filter="officer">👮 Officers</button>
    <button type="button" class="dep-filter-btn" data-filter="barricade">🚧 Barricades</button>
    <button type="button" class="dep-filter-btn" data-filter="dfmd">🚪 DFMD Gates</button>
    <button type="button" class="dep-filter-btn" data-filter="hhmd">🔍 HHMD Wands</button>
    <button type="button" class="dep-filter-btn" data-filter="binocular">🔭 Binoculars</button>
    <button type="button" class="dep-filter-btn" data-filter="radio">📻 Radios</button>
    <button type="button" class="dep-filter-btn" data-filter="cone">⚠️ Cones</button>
    <button type="button" class="dep-filter-btn" data-filter="cctv">📹 CCTV Cameras</button>
    <button type="button" class="dep-filter-btn" data-filter="light">💡 Floodlights</button>
    <button type="button" class="dep-filter-btn" data-filter="ambulance">🚑 Ambulance</button>
    <button type="button" class="dep-filter-btn" data-filter="firebrigade">🚒 Fire Brigade</button>
    <button type="button" class="dep-filter-btn" data-filter="qbelt">🎗️ Q-Belt</button>
    <button type="button" class="dep-filter-btn" data-filter="square_box">📦 Checkpost</button>
  </div>
  <div class="dep-total-badge" id="dep-catalog-total-badge">
    ⚡ Synchronizing with 3D Map...
  </div>
</div>
<div class="dep-asset-grid" id="dep-asset-grid">
'''

for it in catalog_items:
    k = it['kind']
    img_src = item_images_b64.get(k, '')
    deployed_items_html += f'''
  <div class="dep-asset-card" data-kind="{k}">
    <div class="dep-asset-thumb-wrap" onclick="openDepLightbox('{k}');" title="Click to view full high-res photo &amp; specifications">
      <img src="{img_src}" alt="{it['name']}" loading="lazy">
      <span class="dep-live-badge badge-zero" data-kind="{k}">Checking...</span>
      <span class="dep-zoom-hint">🔍 View Photo &amp; Specs (बड़ा करके देखें)</span>
    </div>
    <div class="dep-asset-body">
      <div class="dep-asset-title-row">
        <div>
          <h4 class="dep-asset-title">{it['symbol']} {it['name']}</h4>
          <div class="dep-asset-hindi">{it['hindi']}</div>
        </div>
        <span class="dep-asset-role-badge">{it['role']}</span>
      </div>
      <p class="dep-asset-desc">{it['desc']}</p>
      <div class="dep-asset-spec-box">
        <b>Technical Specs:</b> {it['specs']}<br>
        <span style="color:#0369a1;font-weight:600;margin-top:4px;display:inline-block;">Deployment Role: {it['guideline']}</span>
      </div>
      <div class="dep-asset-actions">
        <div style="font-size:12px;font-weight:700;color:#1e293b;display:flex;justify-content:space-between;align-items:center;">
          <span>📍 Deployed on Map:</span>
          <div style="display:flex;gap:4px;">
            <button type="button" class="btn btn-sm btn-primary" style="padding:2px 8px;font-size:11px;font-weight:700;display:inline-flex;align-items:center;gap:3px;" onclick="selectShowroomItem('{k}'); openDepLightbox('{k}');">🔄 Rotate 3D</button>
            <button type="button" class="btn btn-sm btn-outline" style="padding:2px 8px;font-size:11px;" onclick="selectShowroomItem('{k}');">Showroom</button>
          </div>
        </div>
        <div class="dep-asset-instances-list" data-kind="{k}">
          <span style="color:#94a3b8;font-size:12px;">Loading deployed items...</span>
        </div>
      </div>
    </div>
  </div>
'''

deployed_items_html += '''
</div>
<div id="dep-lightbox-modal" class="dep-lightbox-modal" onclick="if(event.target===this)closeDepLightbox();">
  <div class="dep-lightbox-content">
    <button type="button" class="dep-lightbox-close" onclick="closeDepLightbox()" title="Close (ESC)">✕</button>
    <div class="dep-lightbox-media-wrap">
      <button type="button" class="dep-modal-nav-arrow left" onclick="stepDepModal(-1)" title="Previous Equipment (‹)">‹</button>
      <img id="dep-lightbox-img" class="dep-lightbox-img" src="" alt="Equipment Photo">
      <button type="button" class="dep-modal-nav-arrow right" onclick="stepDepModal(1)" title="Next Equipment (›)">›</button>
    </div>
    <div class="dep-lightbox-body">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
        <div>
          <h2 id="dep-lightbox-title" style="margin:0;font-size:22px;color:#0f172a;">Equipment Name</h2>
          <div id="dep-lightbox-hindi" style="font-size:15px;color:#0284c7;font-weight:600;margin-top:2px;">Hindi Subtitle</div>
        </div>
        <span id="dep-lightbox-badge" class="ref-badge" style="font-size:13px;padding:6px 12px;">Category</span>
      </div>
      <p id="dep-lightbox-desc" style="font-size:14px;color:#475569;line-height:1.6;margin:0;"></p>
      <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:12px 16px;font-size:13px;color:#334155;line-height:1.6;">
        <div id="dep-lightbox-specs"><b>Specs:</b> ...</div>
        <div id="dep-lightbox-guideline" style="margin-top:6px;color:#0369a1;font-weight:600;"><b>Guidelines:</b> ...</div>
      </div>
    </div>
  </div>
</div>
'''
catalog_data_json = json.dumps(catalog_json_map, ensure_ascii=False)

ref_hub = f'''
<section class="ref-hub-card">
  <div class="ref-hub-header">
    <div class="ref-hub-title-wrap">
      <span class="ref-badge">📚 Verification Hub</span>
      <h3 class="ref-hub-title">Reference Imagery &amp; Audit Logs</h3>
    </div>
    <div class="ref-tabs-nav" id="ref-tabs">
      <button type="button" class="ref-tab-btn active" data-tab="tab-deployment-items">🛡️ Deployed Equipment (13 Types)</button>
      <button type="button" class="ref-tab-btn" data-tab="tab-photos">📸 Site Photos (9)</button>
      <button type="button" class="ref-tab-btn" data-tab="tab-videos">🎥 Video Frames (8)</button>
      <button type="button" class="ref-tab-btn" data-tab="tab-satellite">🛰️ Satellite GIS (11)</button>
      <button type="button" class="ref-tab-btn" data-tab="tab-lotus">🪷 Lotus Pavilion (4)</button>
      <button type="button" class="ref-tab-btn" data-tab="tab-arch">🏛️ Architecture (12)</button>
      <button type="button" class="ref-tab-btn" data-tab="tab-notes">📋 Audit &amp; Accuracy</button>
    </div>
  </div>
  <div id="tab-deployment-items" class="ref-tab-pane active">{deployed_items_html}</div>
  <div id="tab-photos" class="ref-tab-pane">{photos_html}</div>
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

// Deployed catalog filtering
document.querySelectorAll('#dep-catalog-filters .dep-filter-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('#dep-catalog-filters .dep-filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.dataset.filter;
    document.querySelectorAll('#dep-asset-grid .dep-asset-card').forEach(card => {{
      if (filter === 'all' || card.dataset.kind === filter) {{
        card.style.display = 'flex';
      }} else {{
        card.style.display = 'none';
      }}
    }});
  }});
}});

// Update catalog counts & instances
function updateDeployedCatalogCounts() {{
  if (typeof depItems === 'undefined' || !Array.isArray(depItems)) return;
  const counts = {{}};
  for (const it of depItems) {{
    if (it && it.kind) counts[it.kind] = (counts[it.kind] || 0) + 1;
  }}
  const total = depItems.length;
  const totalBadge = document.getElementById('dep-catalog-total-badge');
  if (totalBadge) {{
    totalBadge.textContent = `⚡ ${{total}} Items Deployed Across Gyan Mansarovar`;
  }}
  document.querySelectorAll('.dep-live-badge[data-kind]').forEach(el => {{
    const kind = el.dataset.kind;
    const c = counts[kind] || 0;
    el.textContent = c > 0 ? `${{c}} Deployed` : '0 Placed';
    el.className = 'dep-live-badge ' + (c > 0 ? 'badge-active' : 'badge-zero');
  }});
  document.querySelectorAll('.dep-asset-instances-list[data-kind]').forEach(el => {{
    const kind = el.dataset.kind;
    const instances = depItems.filter(it => it.kind === kind);
    if (instances.length === 0) {{
      el.innerHTML = '<span style="color:#94a3b8;font-size:12px;font-style:italic;">None placed on map yet.</span>';
      return;
    }}
    el.innerHTML = instances.map(it => `
      <button type="button" class="dep-instance-jump-btn" data-id="${{it.id}}" title="Click to inspect & control ${{it.name}} in 3D">
        📍 ${{it.name}} <small style="opacity:0.85;">(${{it.duty || 'General'}})</small>
      </button>
    `).join('');
  }});
}}
window.updateDeployedCatalogCounts = updateDeployedCatalogCounts;

// =========================================================================
// EQUIPMENT PHOTO LIGHTBOX MODAL
// =========================================================================
const depCatalogKinds = ['officer','barricade','dfmd','hhmd','binocular','radio','cone','cctv','light','ambulance','firebrigade','qbelt','square_box'];
const depCatalogData = {catalog_data_json};
let modalCurrentKind = 'officer';

window.openDepLightbox = function(kind) {{
  modalCurrentKind = kind;
  const data = depCatalogData[kind];
  if (!data) return;
  const modal = document.getElementById('dep-lightbox-modal');
  if (!modal) return;
  const imgEl = document.getElementById('dep-lightbox-img');
  if (imgEl) imgEl.src = data.img;
  document.getElementById('dep-lightbox-title').textContent = data.symbol + ' ' + data.name;
  document.getElementById('dep-lightbox-hindi').textContent = data.hindi;
  document.getElementById('dep-lightbox-badge').textContent = data.role;
  document.getElementById('dep-lightbox-desc').textContent = data.desc;
  document.getElementById('dep-lightbox-specs').innerHTML = '<b>Technical Specs:</b> ' + data.specs;
  document.getElementById('dep-lightbox-guideline').innerHTML = '<b>Deployment Role:</b> ' + data.guideline;
  modal.classList.add('show');
}};

window.closeDepLightbox = function() {{
  const modal = document.getElementById('dep-lightbox-modal');
  if (modal) modal.classList.remove('show');
}};

window.stepDepModal = function(delta) {{
  const idx = depCatalogKinds.indexOf(modalCurrentKind);
  const nextIdx = (idx + delta + depCatalogKinds.length) % depCatalogKinds.length;
  window.openDepLightbox(depCatalogKinds[nextIdx]);
}};

document.addEventListener('keydown', e => {{
  if (e.key === 'Escape') window.closeDepLightbox();
  const modal = document.getElementById('dep-lightbox-modal');
  if (modal && modal.classList.contains('show')) {{
    if (e.key === 'ArrowRight') window.stepDepModal(1);
    if (e.key === 'ArrowLeft') window.stepDepModal(-1);
  }}
}});

// Jump button click listener
document.addEventListener('click', e => {{
  const btn = e.target.closest('.dep-instance-jump-btn');
  if (btn && btn.dataset.id) {{
    const id = btn.dataset.id;
    if (typeof depChoose === 'function') {{
      depChoose(id, true);
      const appEl = document.querySelector('#app') || document.querySelector('canvas');
      if (appEl) appEl.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
    }}
  }}
}});

setTimeout(updateDeployedCatalogCounts, 600);

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
