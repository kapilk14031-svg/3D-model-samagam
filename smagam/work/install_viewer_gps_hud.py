import json
import csv
from pathlib import Path

smagam_dir = Path("79-th-nirankari-sant-samagam-bhodwal/smagam")
points_csv = smagam_dir / "outputs/google-maps-aligned-points.csv"
dep_json = smagam_dir / "outputs/samagam-duty-deployment.json"
viewer_html = smagam_dir / "work/viewer-pdf.html"
bak = smagam_dir / "work/viewer-pdf.html.bak"

# 1. Load 41 GPS points
with open(points_csv, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    pts = []
    for r in reader:
        pts.append({
            "index": int(r.get("\ufeffIndex") or r.get("Index")),
            "category": r["Category"],
            "name": r["Name"],
            "lat": float(r["Latitude"]),
            "lon": float(r["Longitude"]),
            "x": round(float(r["Model_X"]), 2),
            "z": round(float(r["Model_Z"]), 2),
            "url": r["Google_Maps_URL"]
        })

# 2. Load deployment
with open(dep_json, "r", encoding="utf-8") as f:
    deployment = json.load(f)

# 3. Read fresh from backup
html = bak.read_text(encoding="utf-8")

# CSS to inject
css_to_add = """
/* === LIVE GOOGLE MAPS GPS ALIGNMENT HUD & CONTROLS === */
.gps-hud {
  position: absolute;
  top: 18px;
  right: 18px;
  background: rgba(15, 34, 38, 0.94);
  backdrop-filter: blur(8px);
  border: 1px solid #3d6e73;
  border-radius: 8px;
  padding: 10px 14px;
  color: #e5edea;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  z-index: 10;
  box-shadow: 0 4px 18px rgba(0,0,0,0.45);
  min-width: 275px;
  pointer-events: auto;
}
.gps-hud .gps-title {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.8px;
  color: #ffcc66;
  text-transform: uppercase;
  margin-bottom: 5px;
}
.gps-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #39e68d;
  box-shadow: 0 0 6px #39e68d;
  animation: gpsPulse 2s infinite;
}
@keyframes gpsPulse {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(57, 230, 141, 0.8); }
  70% { transform: scale(1.1); box-shadow: 0 0 0 6px rgba(57, 230, 141, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(57, 230, 141, 0); }
}
.gps-hud .gps-coords {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 13px;
  font-weight: 600;
  color: #ffffff;
  letter-spacing: 0.3px;
  margin-bottom: 4px;
}
.gps-hud .gps-location-name {
  font-size: 11px;
  color: #8ed6cf;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 290px;
  margin-bottom: 6px;
  font-weight: 500;
}
.gps-hud .gps-actions {
  display: flex;
  gap: 8px;
  align-items: center;
  border-top: 1px solid #284c51;
  padding-top: 6px;
}
.gps-hud .gps-actions a, .gps-hud .gps-actions button {
  font-size: 10px;
  color: #ffde8a;
  text-decoration: none;
  background: #1c3d42;
  border: 1px solid #3c6569;
  border-radius: 4px;
  padding: 4px 8px;
  cursor: pointer;
  transition: all .15s ease;
}
.gps-hud .gps-actions a:hover, .gps-hud .gps-actions button:hover {
  background: #2b5b62;
  color: #ffffff;
}
.gps-jump-wrap {
  margin: 10px 0 6px;
  padding: 8px 10px;
  background: #153439;
  border: 1px solid #2d555c;
  border-radius: 7px;
}
.gps-jump-wrap label {
  display: block;
  font-size: 10px;
  font-weight: 700;
  color: #ffcc66;
  margin-bottom: 5px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.gps-jump-select {
  width: 100%;
  padding: 6px 8px;
  border-radius: 5px;
  border: 1px solid #3c666c;
  background: #0f272b;
  color: #fff4d9;
  font-size: 11px;
  cursor: pointer;
  outline: none;
}
.gps-jump-select optgroup {
  background: #0b1d21;
  color: #8ed6cf;
  font-weight: bold;
}
.gps-jump-select option {
  background: #112d32;
  color: #ffffff;
}
"""

if css_to_add.strip() not in html:
    html = html.replace("</style>", css_to_add + "\n</style>", 1)

# Inject Jump selector in <aside> after <div class="views">
jump_html = """<div class="divider"></div><div class="gps-jump-wrap"><label for="gpsSelect">📍 Google Maps Jump (41 Points)</label><select id="gpsSelect" class="gps-jump-select"><option value="">Jump to live GPS location…</option></select></div>"""
if 'id="gpsSelect"' not in html:
    html = html.replace('</div><div class="divider"></div><div class="side-layers">', '</div>' + jump_html + '<div class="divider"></div><div class="side-layers">', 1)

# Inject layer checkboxes in side-layers
layer_checkboxes = """<label class="layer"><span>📍 Live GPS Pins (41)</span><input type="checkbox" data-layer="gps_alignment" checked></label><label class="layer"><span>🛡️ Watchtowers / Machan</span><input type="checkbox" data-layer="security" checked></label>"""
if 'data-layer="gps_alignment"' not in html:
    html = html.replace('<label class="layer"><span>Highway boundary</span><input type="checkbox" data-layer="frontage" checked></label>', '<label class="layer"><span>Highway boundary</span><input type="checkbox" data-layer="frontage" checked></label>' + layer_checkboxes, 1)

# Inject GPS HUD in scene section
gps_hud_html = """<div id="gpsHud" class="gps-hud"><div class="gps-title"><span class="gps-dot"></span> LIVE GOOGLE MAPS ALIGNMENT</div><div class="gps-coords" id="gpsLatLon">Lat: 29.185650, Lon: 77.027322</div><div class="gps-location-name" id="gpsFeatureName">Ground A, Gate 3 (Control Point)</div><div class="gps-actions"><a id="gpsMapsLink" href="https://www.google.com/maps?q=29.185650,77.027322" target="_blank" rel="noopener">Open Google Maps ↗</a><button id="gpsWalkBtn" type="button">Explore with AK 🚶</button></div></div>"""
if 'id="gpsHud"' not in html:
    html = html.replace('<canvas id="model"', gps_hud_html + '<canvas id="model"', 1)

# Replace DEPLOYMENT_SEED by replacing only line 624 (where line starts with const DEPLOYMENT_SEED=)
dep_json_str = json.dumps(deployment, separators=(',', ':'))
lines = html.splitlines()
found_seed = False
for idx, line in enumerate(lines):
    if line.startswith('const DEPLOYMENT_SEED='):
        lines[idx] = f"const DEPLOYMENT_SEED={dep_json_str};"
        found_seed = True
        break

assert found_seed, "Could not find DEPLOYMENT_SEED line"
html = "\n".join(lines)

# Bump DEP_KEY to v2
html = html.replace("const DEP_KEY='samagam-duty-deployment-v1';", "const DEP_KEY='samagam-duty-deployment-v2';")

# Inject JavaScript helper functions and data
js_gps_data = json.dumps(pts, separators=(',', ':'))
js_injection = """
// === LIVE GOOGLE MAPS ALIGNMENT (41 POINTS & REAL-TIME GPS) ===
const GPS_POINTS = __GPS_POINTS_DATA__;
const GPS_AFFINE_INVERSE = {
  cx: 4322536.75,
  cz: -1408051.18,
  m00: 1.80039205578e-05,
  m01: 5.68007910257e-07,
  m10: 1.74243521484e-06,
  m11: -1.53774691907e-05
};
function modelToGPS(x, z) {
  const dx = x + GPS_AFFINE_INVERSE.cx;
  const dz = z + GPS_AFFINE_INVERSE.cz;
  const lon = GPS_AFFINE_INVERSE.m00 * dx + GPS_AFFINE_INVERSE.m01 * dz;
  const lat = GPS_AFFINE_INVERSE.m10 * dx + GPS_AFFINE_INVERSE.m11 * dz;
  return { lat: +lat.toFixed(6), lon: +lon.toFixed(6) };
}
let currentGpsFocus = GPS_POINTS[2]; // Default Gate 3
function updateGPSHud(lat, lon, labelText, ptObj) {
  const latEl = document.getElementById('gpsLatLon');
  const nameEl = document.getElementById('gpsFeatureName');
  const mapLink = document.getElementById('gpsMapsLink');
  if (latEl) latEl.textContent = 'Lat: ' + lat.toFixed(6) + ', Lon: ' + lon.toFixed(6);
  if (nameEl && labelText) nameEl.textContent = labelText;
  if (mapLink) mapLink.href = 'https://www.google.com/maps?q=' + lat.toFixed(6) + ',' + lon.toFixed(6);
  if (ptObj) currentGpsFocus = ptObj;
}
function flyToGPSPoint(pt) {
  if (!pt) return;
  currentGpsFocus = pt;
  pandalInterior = false;
  setConcept(false);
  exitNavigation();
  target = [pt.x, 0, pt.z];
  yaw = 0.65;
  elevation = 0.52;
  distance = 230;
  topView = false;
  anim = null;
  orbit = false;
  dirty = true;
  updateGPSHud(pt.lat, pt.lon, '[' + pt.category + '] ' + pt.name, pt);
  const sel = document.getElementById('gpsSelect');
  if (sel) sel.value = String(pt.index);
  const navMsg = document.getElementById('navMessage');
  if (navMsg) {
    navMsg.hidden = false;
    navMsg.textContent = '📍 Focused: ' + pt.name + ' (' + pt.lat.toFixed(6) + ', ' + pt.lon.toFixed(6) + ')';
    setTimeout(() => { if (!streetMode && !boxMode) navMsg.hidden = true; }, 4000);
  }
  sceneEl.scrollIntoView({ block: 'start' });
}
function initGPSJumpDropdown() {
  const sel = document.getElementById('gpsSelect');
  if (!sel) return;
  const groups = {
    'Machan - Watchtower': '🗼 Machan / Watchtowers (' + GPS_POINTS.filter(p => p.category === 'Machan - Watchtower').length + ')',
    'Entry/exit gate': '🚪 Entry & Exit Gates (' + GPS_POINTS.filter(p => p.category === 'Entry/exit gate').length + ')',
    'Canteen': '☕ Canteens (' + GPS_POINTS.filter(p => p.category === 'Canteen').length + ')',
    'Langar': '🍲 Langar (' + GPS_POINTS.filter(p => p.category === 'Langar').length + ')',
    'Morcha - Security post': '🛡️ Morcha & Security (' + GPS_POINTS.filter(p => p.category === 'Morcha - Security post').length + ')',
    'Outer cordon': '🚧 Outer Cordon (' + GPS_POINTS.filter(p => p.category === 'Outer cordon').length + ')',
    'Parking': '🚗 Parking Areas (' + GPS_POINTS.filter(p => p.category === 'Parking').length + ')',
    'Foot-bridge': '🌉 Footbridge (' + GPS_POINTS.filter(p => p.category === 'Foot-bridge').length + ')',
    'Other': '🏢 Admin & Other Services (' + GPS_POINTS.filter(p => p.category === 'Other').length + ')'
  };
  for (const [cat, grpLabel] of Object.entries(groups)) {
    const ptsInCat = GPS_POINTS.filter(p => p.category === cat);
    if (!ptsInCat.length) continue;
    const optgroup = document.createElement('optgroup');
    optgroup.label = grpLabel;
    for (const pt of ptsInCat) {
      const opt = document.createElement('option');
      opt.value = String(pt.index);
      opt.textContent = pt.name + ' (' + pt.lat.toFixed(4) + ', ' + pt.lon.toFixed(4) + ')';
      optgroup.appendChild(opt);
    }
    sel.appendChild(optgroup);
  }
  sel.onchange = () => {
    const idx = parseInt(sel.value, 10);
    const pt = GPS_POINTS.find(p => p.index === idx);
    if (pt) flyToGPSPoint(pt);
  };
  const walkBtn = document.getElementById('gpsWalkBtn');
  if (walkBtn) {
    walkBtn.onclick = () => {
      if (currentGpsFocus) {
        enterStreet([currentGpsFocus.x, 0.5, currentGpsFocus.z]);
      }
    };
  }
}
setTimeout(initGPSJumpDropdown, 50);
""".replace("__GPS_POINTS_DATA__", js_gps_data)

if 'const GPS_POINTS =' not in html:
    html = html.replace('const DATA=__SCENE__,SHAPES=__SHAPES__;', 'const DATA=__SCENE__,SHAPES=__SHAPES__;\n' + js_injection, 1)

viewer_html.write_text(html, encoding="utf-8")
print(f"Updated {viewer_html} successfully!")
