import json, math, sys
from pathlib import Path
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

root = Path(r'c:\Users\HP\Documents\Codex\2026-10-18\79-th-nirankari-sant-samagam-bhodwal\smagam')
out_dir = root / 'outputs'
work_dir = root / 'work'

raw_table = '''
Other	Garound A , स्टोर कैंटीन एवं लंगर	29.185407,77.026083
Other	Garound A, main office 	29.185820,77.025965
Entry/exit gate	Garound A, gate no 3	29.185650,77.027322
Other	Graund A, ATM	29.185698,77.026135
Other	Graund A, मैंन ऑफिस से, पंडाल की तरफ जाने वाला रास्ता	29.184673,77.025929
Canteen	Graund A 	29.183434,77.026021
Langar	Graund A 	29.183435,77.025762
Machan - Watchtower	Graund A, A-13	29.182223,77.026758
Machan - Watchtower	Graund A 	29.182224,77.026008
Other	Graund A, SC parking 	29.182207,77.024781
Machan - Watchtower	C ground C1	29.179668,77.018170
Machan - Watchtower	C ground C2	29.180808,77.018381
Machan - Watchtower	B Block B1	29.180896,77.026905
Machan - Watchtower	C ground C3	29.180944,77.015251
Machan - Watchtower	C ground C4	29.182336,77.014651
Machan - Watchtower	C ground C5	29.182381,77.018259
Machan - Watchtower	Ground B B2	29.176435,77.030246
Machan - Watchtower	C ground C 6	29.184613,77.018476
Machan - Watchtower	C ground C7 गेट NO 10 के पास 	29.186234,77.020999
Machan - Watchtower	C ground C8	29.182334,77.020900
Machan - Watchtower	C ground C 9	29.178123,77.021995
Parking	Gate no 1। Parking no 2	29.076682,77.130634
Machan - Watchtower	Graund A 	29.182288,77.023968
Canteen	Ground B canteen no 4	29.135014,77.065292
Parking	Graund A 	29.182222,77.023162
Machan - Watchtower	Graund A , A-10	29.182329,77.022422
Canteen	Ground B canteen no 5	29.133640,77.062789
Outer cordon	Graund A, pandal back side	29.179504,77.022214
Machan - Watchtower	Grond B machan no 5	29.128256,77.059375
Morcha - Security post	Graund A, pandal back right corner 	29.177949,77.022298
Machan - Watchtower	Graund A, pandal right side	29.177741,77.023650
Machan - Watchtower	Grond B machan no 4	29.166559,77.027469
Entry/exit gate	Graund A, pandal rihgt side	29.178026,77.024734
Machan - Watchtower	Garaund A, watchtower with parking 	29.177655,77.026843
Entry/exit gate	Garaund A, front of pandal right 	29.177869,77.026924
Machan - Watchtower	Garaund A, A6	29.177952,77.029323
Foot-bridge	Garaund A 	29.177984,77.029219
Outer cordon	Garaund A, pandal front side	29.179316,77.028735
Machan - Watchtower	Garaund A, A5	29.180392,77.028536
Machan - Watchtower	Garaund A A4	29.182095,77.028101
Entry/exit gate	Garaund A , gate no 2	29.182409,77.028221
'''

# Transformation matrix M: [lon, lat, 1] @ M = [x, z]
M = np.array([
    [ 5.53456049e+04,  6.27126153e+03],
    [ 2.04433779e+03, -6.47985609e+04],
    [-4.32253675e+06,  1.40805118e+06]
])

parsed_points = []
for idx, line in enumerate(raw_table.strip().splitlines()):
    parts = line.split('\t')
    if len(parts) >= 3:
        cat = parts[0].strip()
        name = parts[1].strip()
        coords = [float(x.strip()) for x in parts[2].split(',')]
        lat, lon = coords[0], coords[1]
        model_pos = np.array([lon, lat, 1.0]) @ M
        x, z = round(float(model_pos[0]), 2), round(float(model_pos[1]), 2)
        parsed_points.append({
            'index': idx + 1,
            'cat': cat,
            'name': name,
            'lat': lat,
            'lon': lon,
            'x': x,
            'z': z,
            'gmaps_url': f'https://www.google.com/maps?q={lat},{lon}'
        })

print(f'Parsed {len(parsed_points)} points.')

# 1. Update scene-data.json
scene_path = out_dir / 'scene-data.json'
scene = json.loads(scene_path.read_text(encoding='utf-8'))

# Store georeferencing info in metadata
scene['meta']['georeference'] = {
    'status': 'Calibrated with 41 live Google Maps ground points (October 2026)',
    'venue_anchor_lat_lon': [29.179636, 77.0261412],
    'gate3_gps': [29.185650, 77.027322],
    'gate2_gps': [29.182409, 77.028221],
    'affine_matrix_lon_lat_to_xz': M.tolist(),
    'inverse_affine_dx_dz': [4322536.75, 1408051.18],
    'inverse_matrix_2x2': [
        [1.8003920557812304e-05, 5.680079102573645e-07],
        [1.7424352148441684e-06, -1.5377469190734254e-05]
    ],
    'points_count': len(parsed_points)
}

# Add 3D representation objects for each venue point into scene['objects']
existing_objects = scene.get('objects', [])
# Remove previous GPS alignment objects if any
existing_objects = [o for o in existing_objects if not o.get('name', '').startswith('GPS ALIGNED / ')]

new_objects = []
new_labels = []

def add_box(name, x, y, z, w, h, d, color, layer='site'):
    new_objects.append({
        'name': f'GPS ALIGNED / {name}',
        'kind': 'box',
        'p': [round(x, 2), round(y, 2), round(z, 2)],
        's': [round(w, 2), round(h, 2), round(d, 2)],
        'color': color,
        'layer': layer,
        'ground': '',
        'status': 'Live Google Maps aligned position'
    })

def add_machan(pt):
    x, z = pt['x'], pt['z']
    name = pt['name']
    # 4 Corner Timber/Steel Posts
    for dx in [-2.2, 2.2]:
        for dz in [-2.2, 2.2]:
            add_box(f'{name} Post', x + dx, 3.8, z + dz, 0.45, 7.6, 0.45, '#3e4137', layer='security')
    # Cross braces
    add_box(f'{name} Platform Deck', x, 7.5, z, 5.4, 0.35, 5.4, '#9c825a', layer='security')
    # Railing
    for dx in [-2.6, 2.6]:
        add_box(f'{name} Railing X', x + dx, 8.2, z, 0.2, 1.0, 5.4, '#c2ab7b', layer='security')
    for dz in [-2.6, 2.6]:
        add_box(f'{name} Railing Z', x, 8.2, z + dz, 5.4, 1.0, 0.2, '#c2ab7b', layer='security')
    # Roof canopy
    add_box(f'{name} Canopy', x, 10.4, z, 6.0, 0.4, 6.0, '#354832', layer='security')
    # Roof apex
    add_box(f'{name} Eaves', x, 10.8, z, 3.2, 0.5, 3.2, '#485e44', layer='security')
    # Observation officer
    add_box(f'{name} Officer Body', x, 8.4, z, 0.8, 1.5, 0.55, '#867558', layer='security')
    add_box(f'{name} Officer Cap', x, 9.35, z, 0.7, 0.35, 0.7, '#243746', layer='security')
    # Searchlight beacon
    add_box(f'{name} Searchlight', x, 11.2, z, 0.6, 0.5, 0.6, '#f4d068', layer='security')
    # Sign board banner
    add_box(f'{name} Sign', x, 7.1, z + 2.75, 4.2, 0.7, 0.15, '#c93b2b', layer='security')

def add_morcha(pt):
    x, z = pt['x'], pt['z']
    name = pt['name']
    # Sandbag horseshoe bunker
    add_box(f'{name} Sandbags North', x, 0.7, z - 1.8, 4.2, 1.4, 0.8, '#8e7a5c', layer='security')
    add_box(f'{name} Sandbags West', x - 1.8, 0.7, z, 0.8, 1.4, 4.2, '#8e7a5c', layer='security')
    add_box(f'{name} Sandbags East', x + 1.8, 0.7, z, 0.8, 1.4, 4.2, '#8e7a5c', layer='security')
    # Camouflage protective canopy
    add_box(f'{name} Camo Canopy', x, 2.5, z, 4.8, 0.25, 4.8, '#41523c', layer='security')
    # Steel support pillars
    for dx in [-2.0, 2.0]:
        for dz in [-2.0, 2.0]:
            add_box(f'{name} Pillar', x + dx, 1.3, z + dz, 0.25, 2.4, 0.25, '#292f25', layer='security')
    # Armed security guard
    add_box(f'{name} Commando', x, 1.3, z, 0.8, 1.6, 0.6, '#314436', layer='security')
    add_box(f'{name} Commando Helmet', x, 2.2, z, 0.7, 0.35, 0.7, '#1b261d', layer='security')

def add_gate_portal(pt):
    x, z = pt['x'], pt['z']
    name = pt['name']
    # Gate Pillars
    for dx in [-4.5, 4.5]:
        add_box(f'{name} Pillar', x + dx, 4.5, z, 1.4, 9.0, 1.4, '#e4dbc5', layer='gates')
        add_box(f'{name} Pier Cap', x + dx, 9.2, z, 1.8, 0.5, 1.8, '#c2ab7b', layer='gates')
        add_box(f'{name} Finial Urn', x + dx, 9.8, z, 0.9, 0.8, 0.9, '#a4382c', layer='gates')
    # Overhead lintel beam
    add_box(f'{name} Overhead Lintel', x, 8.8, z, 9.4, 0.8, 1.2, '#6d3928', layer='gates')
    # Gate banner sign
    add_box(f'{name} Nameboard', x, 9.7, z, 8.2, 0.9, 0.2, '#23445d', layer='gates')
    # Gate barrier / leaves
    add_box(f'{name} Barrier Left', x - 2.2, 1.5, z, 3.8, 2.6, 0.3, '#4d3023', layer='gates')
    add_box(f'{name} Barrier Right', x + 2.2, 1.5, z, 3.8, 2.6, 0.3, '#4d3023', layer='gates')
    # Security guard kiosk
    add_box(f'{name} Guard Kiosk', x + 5.8, 1.8, z, 2.2, 3.5, 2.2, '#d6cca9', layer='gates')

def add_canteen_pavilion(pt):
    x, z = pt['x'], pt['z']
    name = pt['name']
    # Main pavilion platform
    add_box(f'{name} Plinth', x, 0.3, z, 16.0, 0.6, 10.0, '#cfc7b0', layer='services')
    # Tent canopy roof
    add_box(f'{name} Canopy', x, 4.8, z, 16.5, 1.2, 10.5, '#ad4b3b', layer='services')
    add_box(f'{name} Valance', x, 4.0, z, 16.7, 0.5, 10.7, '#f7eed2', layer='services')
    # Serving counters
    add_box(f'{name} Counter', x, 1.2, z, 13.0, 1.1, 1.6, '#ded6bd', layer='services')
    # Columns
    for dx in [-7.5, 0, 7.5]:
        for dz in [-4.5, 4.5]:
            add_box(f'{name} Pole', x + dx, 2.4, z + dz, 0.3, 4.2, 0.3, '#6e6a5c', layer='services')
    # Signboard
    add_box(f'{name} Sign', x, 5.7, z + 5.3, 8.0, 0.8, 0.2, '#b23d2e', layer='services')

def add_langar_hall(pt):
    x, z = pt['x'], pt['z']
    name = pt['name']
    # Large community dining hall plinth
    add_box(f'{name} Plinth', x, 0.3, z, 24.0, 0.6, 12.0, '#cfc7b0', layer='services')
    # Canopy roof
    add_box(f'{name} Canopy', x, 5.2, z, 24.5, 1.4, 12.5, '#3b6287', layer='services')
    add_box(f'{name} Trim', x, 4.3, z, 24.7, 0.5, 12.7, '#ecd9b2', layer='services')
    # Dining rows / mats
    for dz in [-3.5, 0, 3.5]:
        add_box(f'{name} Dining Row', x, 0.65, z + dz, 20.0, 0.1, 1.8, '#b88c56', layer='services')
    # Support pillars
    for dx in [-11.0, -5.5, 0, 5.5, 11.0]:
        for dz in [-5.5, 5.5]:
            add_box(f'{name} Pillar', x + dx, 2.6, z + dz, 0.35, 4.6, 0.35, '#5c646b', layer='services')
    # Sign
    add_box(f'{name} Sign', x, 6.2, z + 6.3, 10.0, 0.9, 0.2, '#21496b', layer='services')

def add_office_building(pt):
    x, z = pt['x'], pt['z']
    name = pt['name']
    # 2-Storey Administrative Office
    add_box(f'{name} Ground Floor', x, 2.2, z, 18.0, 4.4, 12.0, '#8d6849', layer='services')
    add_box(f'{name} Upper Floor', x, 6.2, z, 18.2, 3.8, 12.2, '#6b4c33', layer='services')
    add_box(f'{name} Roof Slab', x, 8.3, z, 19.0, 0.5, 13.0, '#baa286', layer='services')
    # Entrance portico
    add_box(f'{name} Portico', x, 2.2, z + 6.8, 6.0, 3.6, 2.5, '#baa286', layer='services')
    # Glass windows band
    add_box(f'{name} Windows Lower', x, 2.5, z + 6.05, 15.0, 1.5, 0.1, '#3a5f6e', layer='services')
    add_box(f'{name} Windows Upper', x, 6.3, z + 6.15, 15.0, 1.5, 0.1, '#3a5f6e', layer='services')
    # Flagpole
    add_box(f'{name} Mast', x + 8.0, 9.5, z + 6.5, 0.2, 6.0, 0.2, '#e0ded5', layer='services')
    add_box(f'{name} Flag', x + 8.6, 12.0, z + 6.5, 1.2, 0.7, 0.05, '#d95328', layer='services')

def add_atm_kiosk(pt):
    x, z = pt['x'], pt['z']
    name = pt['name']
    add_box(f'{name} Kiosk', x, 1.8, z, 3.2, 3.6, 3.2, '#ffffff', layer='services')
    add_box(f'{name} Blue Fascia', x, 3.4, z, 3.3, 0.8, 3.3, '#1a56a6', layer='services')
    add_box(f'{name} Glazing', x, 1.6, z + 1.62, 2.4, 2.2, 0.08, '#437d99', layer='services')
    add_box(f'{name} ATM Screen', x, 1.4, z + 1.2, 0.8, 0.8, 0.4, '#00b4d8', layer='services')

def add_cordon_marker(pt):
    x, z = pt['x'], pt['z']
    name = pt['name']
    # Outer security cordon fence / pylons
    for dx in [-15, -7.5, 0, 7.5, 15]:
        add_box(f'{name} Pylon', x + dx, 1.0, z, 0.35, 2.0, 0.35, '#d97706', layer='security')
        add_box(f'{name} Flash Lamp', x + dx, 2.1, z, 0.25, 0.25, 0.25, '#fbbf24', layer='security')
    # High-vis cordon ribbon
    add_box(f'{name} Ribbon Upper', x, 1.6, z, 31.0, 0.12, 0.08, '#f59e0b', layer='security')
    add_box(f'{name} Ribbon Lower', x, 0.9, z, 31.0, 0.12, 0.08, '#ef4444', layer='security')

def add_parking_node(pt):
    x, z = pt['x'], pt['z']
    name = pt['name']
    add_box(f'{name} Paved Bay', x, 0.15, z, 26.0, 0.3, 18.0, '#424d52', layer='parking')
    # Perimeter boundary curbs
    for dx in [-13.2, 13.2]:
        add_box(f'{name} Curb X', x + dx, 0.4, z, 0.4, 0.4, 18.0, '#c7c2b3', layer='parking')
    for dz in [-9.2, 9.2]:
        add_box(f'{name} Curb Z', x, 0.4, z + dz, 26.0, 0.4, 0.4, '#c7c2b3', layer='parking')
    # Signboard
    add_box(f'{name} Parking Sign', x - 12.0, 2.2, z + 9.5, 0.2, 3.8, 0.2, '#3b4347', layer='parking')
    add_box(f'{name} Sign Plate', x - 12.0, 3.8, z + 9.5, 0.1, 1.2, 1.2, '#1d4ed8', layer='parking')

# Generate 3D objects for all points that are within venue bounds (lat > 29.17)
for pt in parsed_points:
    cat = pt['cat'].lower()
    name = pt['name']
    x, z = pt['x'], pt['z']
    
    # Add high-visibility floating GPS Pin marker
    add_box(f'{name} GPS PIN', x, 13.5, z, 1.0, 2.0, 1.0, '#e11d48', layer='gps_alignment')
    add_box(f'{name} GPS PULSE', x, 14.8, z, 2.2, 0.4, 2.2, '#fb7185', layer='gps_alignment')
    
    # Add textual label for interactive search
    new_labels.append({
        'text': f"📍 {pt['name']} ({pt['lat']:.5f}, {pt['lon']:.5f})",
        'p': [x, 16.0, z],
        'layer': 'gps_alignment',
        'featureId': f"GPS-{pt['index']}"
    })
    
    if pt['lat'] < 29.17:
        continue # remote points get pin/label only
    
    if 'machan' in cat or 'watchtower' in cat or 'machan' in name.lower() or 'watchtower' in name.lower():
        add_machan(pt)
    elif 'morcha' in cat or 'security post' in cat or 'morcha' in name.lower():
        add_morcha(pt)
    elif 'gate' in cat or 'entry/exit' in cat or 'gate' in name.lower():
        add_gate_portal(pt)
    elif 'canteen' in cat or 'canteen' in name.lower():
        add_canteen_pavilion(pt)
    elif 'langar' in cat or 'langar' in name.lower():
        add_langar_hall(pt)
    elif 'main office' in name.lower():
        add_office_building(pt)
    elif 'atm' in name.lower():
        add_atm_kiosk(pt)
    elif 'cordon' in cat or 'cordon' in name.lower():
        add_cordon_marker(pt)
    elif 'parking' in cat or 'parking' in name.lower():
        add_parking_node(pt)
    elif 'foot-bridge' in cat or 'footbridge' in name.lower() or 'foot-bridge' in name.lower():
        # High quality footbridge portal marker
        add_box(f'{name} Tower Left', x - 4.0, 6.0, z, 1.6, 12.0, 1.6, '#475569', layer='bridges')
        add_box(f'{name} Tower Right', x + 4.0, 6.0, z, 1.6, 12.0, 1.6, '#475569', layer='bridges')
        add_box(f'{name} Span Truss', x, 11.5, z, 10.0, 1.5, 3.2, '#e2e8f0', layer='bridges')
    else:
        # Service depot / default structure
        add_box(f'{name} Facility Block', x, 2.5, z, 10.0, 5.0, 6.0, '#94a3b8', layer='services')

scene['objects'] = existing_objects + new_objects
scene['labels'] = scene.get('labels', []) + new_labels
scene_path.write_text(json.dumps(scene, indent=2), encoding='utf-8')
print(f'Updated scene-data.json: {len(scene["objects"])} objects (+{len(new_objects)} GPS aligned 3D objects).')

# 2. Update samagam-duty-deployment.json
deploy_path = out_dir / 'samagam-duty-deployment.json'
deploy_data = json.loads(deploy_path.read_text(encoding='utf-8'))
units = deploy_data.get('units', [])

# Map of title keywords to existing unit IDs
title_to_id = {
    'A-13': 'A-M-13',
    'A-10': 'A-M-10',
    'A6': 'A-M-6',
    'A5': 'A-M-5',
    'A4': 'A-M-4',
    'C1': 'C-M-1',
    'C2': 'C-M-2',
    'C3': 'C-M-3',
    'C4': 'C-M-4',
    'C5': 'C-M-5',
    'C 6': 'C-M-6',
    'C7': 'C-M-7',
    'C8': 'C-M-8',
    'C 9': 'C-M-9',
    'B1': 'B-M-1',
    'B2': 'B-M-2',
    'gate no 3': 'OUT-M3',
    'gate no 2': 'OUT-M2',
    'pandal back right corner': 'A-MO-1',
}

# Update existing units or create new units for all 41 points
units_by_id = {u['id']: u for u in units}

for pt in parsed_points:
    matched_id = None
    for kw, uid in title_to_id.items():
        if kw.lower() in pt['name'].lower():
            if uid in units_by_id:
                matched_id = uid
                break
    
    uid = matched_id or f"GPS-{pt['index']:02d}"
    
    unit_type = 'machan' if ('machan' in pt['cat'].lower() or 'watchtower' in pt['cat'].lower() or 'machan' in pt['name'].lower()) else \
                'morcha' if ('morcha' in pt['cat'].lower() or 'morcha' in pt['name'].lower()) else \
                'parking' if ('parking' in pt['cat'].lower() or 'parking' in pt['name'].lower()) else \
                'canteen' if ('canteen' in pt['cat'].lower() or 'canteen' in pt['name'].lower()) else \
                'langar' if ('langar' in pt['cat'].lower() or 'langar' in pt['name'].lower()) else \
                'gate' if ('gate' in pt['cat'].lower() or 'entry/exit' in pt['cat'].lower()) else \
                'barricade' if ('cordon' in pt['cat'].lower()) else 'officer'
    
    pos = [pt['x'], 0.3, pt['z']]
    
    if uid in units_by_id:
        u = units_by_id[uid]
        u['position'] = pos
        u['enabled'] = True
        u['gps'] = [pt['lat'], pt['lon']]
        u['notes'] = (u.get('notes', '') + f" | Live Google Maps: {pt['lat']}, {pt['lon']} ({pt['name']})").strip(' |')
    else:
        new_u = {
            'id': uid,
            'title': f"{pt['name']}",
            'type': unit_type,
            'anchorId': None,
            'ground': 'Ground A' if 'ground a' in pt['name'].lower() else 'Ground C' if 'ground c' in pt['name'].lower() else 'Ground B',
            'position': pos,
            'rotation': 0,
            'scale': 1.0,
            'enabled': True,
            'speed': 7,
            'route': [],
            'routeMode': 'pingpong',
            'personnel': [],
            'gps': [pt['lat'], pt['lon']],
            'notes': f"Live Google Maps Aligned Point #{pt['index']} | Category: {pt['cat']} | Lat: {pt['lat']}, Lon: {pt['lon']} | Link: {pt['gmaps_url']}",
            'shifts': {
                'day': {'force': 2, 'female': None, 'incharge': 1, 'extra': 0, 'inchargeText': 'Duty Incharge', 'extraText': '', 'notes': '', 'start': '06:00', 'end': '18:00'},
                'night': {'force': 2, 'female': None, 'incharge': 1, 'extra': 0, 'inchargeText': 'Duty Incharge', 'extraText': '', 'notes': '', 'start': '18:00', 'end': '06:00'}
            }
        }
        units.append(new_u)
        units_by_id[uid] = new_u

deploy_data['version'] = 2
deploy_data['units'] = units
deploy_data['note'] = 'Aligned with 41 live Google Maps latitude & longitude survey coordinates (October 2026).'
deploy_path.write_text(json.dumps(deploy_data, indent=2), encoding='utf-8')
print(f'Updated samagam-duty-deployment.json: {len(units)} units total.')

# Write points CSV for reference
csv_path = out_dir / 'google-maps-aligned-points.csv'
import csv
with csv_path.open('w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['Index', 'Category', 'Name', 'Latitude', 'Longitude', 'Model_X', 'Model_Z', 'Google_Maps_URL'])
    for pt in parsed_points:
        writer.writerow([pt['index'], pt['cat'], pt['name'], pt['lat'], pt['lon'], pt['x'], pt['z'], pt['gmaps_url']])
print(f'Saved reference CSV to {csv_path.name}')
