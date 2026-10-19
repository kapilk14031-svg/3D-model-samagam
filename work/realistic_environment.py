"""Realistic environment detailing for 79th Nirankari Sant Samagam venue:
- Organic 3D Trees (Broad Shade Trees, Columnar Ashoka Avenues, Royal Palms)
- High-Mast Stadium Floodlight Towers across parking and residential grounds
- Ceremonial Welcome Banners and Nirankari Flags
- Road Crossings and Avenue Lighting
"""
import math, random

# 1. Register geometric shapes for trees, towers and ceremonial elements
if 'treetrunk' not in extra_shapes:
    # 8-sided tapered trunk
    vv=[]; ff=[]
    for y, r in [(0, 0.55), (1, 0.35)]:
        for j in range(8):
            a = j * math.tau / 8
            vv.append([r * math.cos(a), y, r * math.sin(a)])
    for j in range(8):
        k = (j + 1) % 8
        ff.append([j, k, k + 8, j + 8])
    ff.extend([[7,6,5,4,3,2,1,0], [8,9,10,11,12,13,14,15]])
    extra_shapes['treetrunk'] = [vv, ff]

if 'foliagecrown' not in extra_shapes:
    # 12-sided organic ellipsoid crown
    vv=[]; ff=[]; rings=5; sides=10
    for r in range(rings+1):
        a = math.pi * r / rings
        for j in range(sides):
            t = math.tau * j / sides
            noise = 1.0 + 0.12 * math.sin(j * 3.1 + r * 2.3)
            vv.append([0.5 * math.sin(a) * math.cos(t) * noise, 0.5 + 0.5 * math.cos(a) * noise, 0.5 * math.sin(a) * math.sin(t) * noise])
    for r in range(rings):
        for j in range(sides):
            a = r * sides + j; b = r * sides + (j + 1) % sides; c = a + sides; d = b + sides
            if r == 0: ff.append([a, c, d])
            elif r == rings - 1: ff.append([a, c, b])
            else: ff.append([a, c, d, b])
    extra_shapes['foliagecrown'] = [vv, ff]

if 'ashokacrown' not in extra_shapes:
    # Slender vertical columnar crown for Ashoka trees with verified non-zero normals
    vv = [[0, 1, 0], [0, 0, 0]]; ff = []
    sides = 8; tiers = 4
    for tier in range(tiers):
        y = 0.15 + 0.7 * (tier / (tiers - 1))
        r = 0.45 * math.sin(math.pi * (0.1 + 0.8 * (tier / (tiers - 1))))
        for j in range(sides):
            a = j * math.tau / sides
            vv.append([r * math.cos(a), y, r * math.sin(a)])
    for j in range(sides):
        k = (j + 1) % sides; ff.append([1, 2 + k, 2 + j])
    for t in range(tiers - 1):
        r1 = 2 + t * sides; r2 = 2 + (t + 1) * sides
        for j in range(sides):
            k = (j + 1) % sides; ff.append([r1 + j, r1 + k, r2 + k, r2 + j])
    top_r = 2 + (tiers - 1) * sides
    for j in range(sides):
        k = (j + 1) % sides; ff.append([0, top_r + j, top_r + k])
    extra_shapes['ashokacrown'] = [vv, ff]

if 'palmcrown' not in extra_shapes:
    # Radiating palm fronds umbrella with verified non-zero normals
    vv = [[0, 0.5, 0]]; ff = []
    fronds = 10
    for j in range(fronds):
        a = j * math.tau / fronds
        left_a = a - 0.18; right_a = a + 0.18
        m1 = [1.2 * math.cos(left_a), 0.3, 1.2 * math.sin(left_a)]
        m2 = [1.2 * math.cos(right_a), 0.3, 1.2 * math.sin(right_a)]
        tip = [2.2 * math.cos(a), -0.5, 2.2 * math.sin(a)]
        b_idx = len(vv); vv.extend([m1, m2, tip])
        ff.append([0, b_idx, b_idx + 1])
        ff.append([b_idx, b_idx + 2, b_idx + 1])
    extra_shapes['palmcrown'] = [vv, ff]

if 'hexplatform' not in extra_shapes:
    # Hexagonal maintenance platform for high-mast tower
    vv=[]; ff=[]
    for y in [0, 0.4]:
        for j in range(6):
            a = j * math.tau / 6
            vv.append([math.cos(a), y, math.sin(a)])
    for j in range(6):
        k = (j + 1) % 6
        ff.append([j, k, k + 6, j + 6])
    ff.extend([[5,4,3,2,1,0], [6,7,8,9,10,11]])
    extra_shapes['hexplatform'] = [vv, ff]

def add_tree_shade(x, z, height=9.0, spread=8.0, layer='context'):
    """Broad shade tree (Neem / Peepal) with trunk and multi-tier lush crown."""
    trunk_h = height * 0.45; trunk_w = spread * 0.16
    add('Tree trunk', 'treetrunk', x, 0, z, trunk_w, trunk_h, trunk_w, '#544131', layer)
    # 3 overlapping organic foliage spheres
    greens = ['#285929', '#326c33', '#3c7e3e', '#234e24']
    for idx, (dy, r_mult, c_idx) in enumerate([(0.35, 0.95, 0), (0.55, 0.85, 1), (0.75, 0.65, 2)]):
        cy = height * dy
        cw = spread * r_mult; ch = height * 0.45 * r_mult
        col = greens[c_idx % len(greens)]
        add(f'Tree foliage tier {idx+1}', 'foliagecrown', x, cy, z, cw, ch, cw, col, layer)

def add_tree_ashoka(x, z, height=11.0, layer='context'):
    """Tall slender Ashoka tree typical of ceremonial Indian avenues."""
    trunk_h = 2.0; trunk_w = 0.5
    add('Ashoka trunk', 'treetrunk', x, 0, z, trunk_w, trunk_h, trunk_w, '#4e3f32', layer)
    add('Ashoka columnar foliage', 'ashokacrown', x, trunk_h, z, 2.6, height - trunk_h, 2.6, '#1d4f26', layer)

def add_tree_palm(x, z, height=12.0, layer='context'):
    """Royal palm tree with slender trunk and radiating fronds."""
    trunk_w = 0.7
    add('Palm trunk', 'treetrunk', x, 0, z, trunk_w, height, trunk_w, '#695a49', layer)
    add('Palm fronds crown', 'palmcrown', x, height, z, 3.2, 1.8, 3.2, '#2e6b36', layer)

def add_high_mast(x, z, height=30.0, layer='utilities'):
    """30-meter high-mast stadium floodlight tower."""
    # Base plinth
    box('High-mast concrete foundation', x, z, 4.0, 4.0, 1.2, '#b8b9ad', 0, layer)
    # Tapered steel mast
    add('High-mast galvanized steel tower', 'treetrunk', x, 1.2, z, 1.8, height - 1.2, 1.8, '#9ba2a6', layer)
    # Hexagonal maintenance platform
    add('High-mast service ring', 'hexplatform', x, height - 2.5, z, 4.5, 0.4, 4.5, '#788085', layer)
    # Headframe luminaire ring
    add('High-mast headframe', 'hexplatform', x, height - 0.5, z, 5.0, 0.6, 5.0, '#5a6266', layer)
    # 12 high-power LED floodlight projectors pointing outward and down
    for j in range(12):
        a = j * math.tau / 12
        fx = x + 2.3 * math.cos(a); fz = z + 2.3 * math.sin(a); fy = height - 1.2
        box('High-mast LED floodlight housing', fx, fz, 0.9, 0.7, 0.8, '#41474a', fy, layer)
        # Glowing luminaire face (warm bright projector beam)
        box('High-mast LED emitter face', fx + 0.15*math.cos(a), fz + 0.15*math.sin(a), 0.8, 0.6, 0.7, '#fff5cb', fy + 0.05, layer)

def add_ceremonial_flagpole(x, z, height=14.0, layer='gates'):
    """Flagpole flying Nirankari peace flag / Indian tricolor."""
    box('Flagpole pedestal', x, z, 1.4, 1.4, 0.8, '#d4cebe', 0, layer)
    add('Stainless flagpole', 'treetrunk', x, 0.8, z, 0.25, height, 0.25, '#dbe2e6', layer)
    box('Flagpole gold finial', x, z, 0.6, 0.6, 0.6, '#d8b668', height + 0.8, layer)
    # Nirankari white flag with gold trim and emblem
    box('Nirankari ceremonial flag', x + 1.6, z, 3.2, 0.08, 1.8, '#fefefe', height - 1.2, layer)
    box('Flag emblem circle', x + 1.6, z + 0.05, 0.9, 0.04, 0.9, '#30628e', height - 1.2, layer)

print("Planting trees, landscaping, high-mast floodlights and ceremonial decor...")

# --- 2. High-Mast Floodlight Towers placement across the venue ---
floodlight_locations = [
    # Parking areas
    (200, 830, 'Parking P1 High-Mast South'),
    (370, 860, 'Parking P1 High-Mast North'),
    (20, 585, 'Parking P2 High-Mast West'),
    (200, 440, 'Parking P2 High-Mast East'),
    (-760, -180, 'Parking P3 High-Mast'),
    (-680, -220, 'Parking P3 Auxiliary Mast'),
    (60, -245, 'Parking P4 High-Mast'),
    (500, 250, 'Parking P5 High-Mast Opposite NH44'),
    # Residential Camp Grounds (Ground B, C, D)
    (-250, 680, 'Ground B Central High-Mast'),
    (-100, 780, 'Ground B North High-Mast'),
    (-380, 520, 'Ground B South High-Mast'),
    (40, 720, 'Ground C Central High-Mast'),
    (-80, 450, 'Ground C South High-Mast'),
    (80, 320, 'Ground C West High-Mast'),
    (-350, 220, 'Ground D North High-Mast'),
    (-200, 100, 'Ground D Central High-Mast'),
    (-480, 50, 'Ground D West High-Mast'),
    # Main Satsang Pandal Perimeter
    (140, 490, 'Pandal North Forecourt Mast'),
    (340, 480, 'Pandal North-East Mast'),
    (130, 140, 'Pandal South Forecourt Mast'),
    (350, 130, 'Pandal South-East Mast'),
    # Gate Plazas
    (385, 510, 'Delhi Gate 1 Plaza High-Mast'),
    (300, 155, 'Gate 2 Plaza High-Mast'),
    (430, 275, 'Gate 3 Flyover Plaza High-Mast'),
]

for fx, fz, fname in floodlight_locations:
    add_high_mast(fx, fz, height=28.0, layer='utilities')

# --- 3. Tree Lines along NH-44 Highway (Median & Outer Margins) ---
# NH44 path points from H01
nh44_raw = [[82, 1196], [335, 1139], [650, 1058], [905, 989], [1100, 950], [1320, 888], [1610, 824]]
nh44_pts = [planpoint(*p) for p in nh44_raw]

# Plant trees along NH-44 median and highway road margins
rnd = random.Random(42)
for i in range(len(nh44_pts) - 1):
    p1 = nh44_pts[i]; p2 = nh44_pts[i+1]
    dx = p2[0] - p1[0]; dz = p2[2] - p1[2]
    seg_len = math.hypot(dx, dz)
    nx = -dz / seg_len; nz = dx / seg_len
    steps = int(seg_len / 22.0)
    for s in range(1, steps):
        t = s / steps
        cx = p1[0] + dx * t; cz = p1[2] + dz * t
        # Median Ashoka trees (slender, safe for median divider)
        if s % 2 == 0:
            add_tree_ashoka(cx, cz, height=8.5, layer='context')
        # Venue-side highway margin: Alternate broad shade trees and Royal palms
        off_venue = -22.0
        vx = cx + nx * off_venue; vz = cz + nz * off_venue
        if s % 3 == 0:
            add_tree_palm(vx, vz, height=13.0, layer='context')
        elif s % 3 == 1:
            add_tree_shade(vx, vz, height=10.0, spread=9.0, layer='context')
        else:
            add_tree_ashoka(vx, vz, height=11.0, layer='context')
        # Opposite highway margin (P5 side)
        off_opp = 24.0
        ox = cx + nx * off_opp; oz = cz + nz * off_opp
        if s % 2 == 0:
            add_tree_shade(ox, oz, height=9.5, spread=8.5, layer='context')

# --- 4. Main Avenues & Boulevards (Processional tree lines) ---
# Pandal perimeter avenues & VIP approach
for z in range(130, 480, 28):
    # East flank of Pandal
    add_tree_palm(345, z, height=12.5, layer='pandal')
    add_tree_ashoka(352, z, height=10.5, layer='pandal')
    # West flank of Pandal (towards Langar and Offices)
    add_tree_shade(125, z, height=9.0, spread=8.0, layer='pandal')

# Road R03 / R04 corridors (Ground B & C connecting avenues)
for x in range(-50, 300, 32):
    add_tree_ashoka(x, 620, height=9.5, layer='context')
    add_tree_shade(x + 16, 632, height=8.5, spread=7.5, layer='context')

for x in range(-200, 200, 36):
    add_tree_shade(x, 480, height=9.5, spread=8.5, layer='context')
    add_tree_ashoka(x + 18, 470, height=10.0, layer='context')

# SNCF Nursery (B20) zone lush greenery
for nx in range(25, 95, 14):
    for nz in range(-280, -220, 16):
        add_tree_shade(nx, nz, height=8.0 + rnd.random()*3.0, spread=7.0 + rnd.random()*2.5, layer='services')
        if rnd.random() > 0.5:
            add_tree_palm(nx + 6, nz + 7, height=11.5, layer='services')

# --- 5. Ceremonial Nirankari Peace Flags & Entrance Grandeur ---
# Gate 1 ceremonial avenue
for off in range(-36, 40, 12):
    add_ceremonial_flagpole(388 + off * 0.4, 488 + off * 0.9, height=13.0, layer='gates')

# Gate 2 ceremonial avenue
for off in range(-30, 35, 12):
    add_ceremonial_flagpole(302 + off * 0.3, 136 + off * 0.9, height=13.0, layer='gates')

# Pandal entrance forecourt flags
for fx in [185, 235, 285, 335, 385, 435]:
    add_ceremonial_flagpole(fx, 492, height=14.0, layer='pandal')

# --- 6. Authentic Regal Colors for Ceremonial Gates (Restoring ivory marble and lustrous gold) ---
for o in objects:
    if o['layer'] == 'gates':
        # Revert harsh burnt-orange overrides to regal ivory marble, gold leaf, and deep wine velvet
        if o['color'] == '#b94d18':
            o['color'] = '#f3ede0' # Pristine ivory marble
        elif o['color'] == '#dc7b24':
            o['color'] = '#d6b268' # Rich lustrous gold trim
        elif o['color'] == '#6c2c15':
            o['color'] = '#782836' # Deep ceremonial wine velvet
        elif o['color'] == '#8f3a16':
            o['color'] = '#b8a992' # Carved stone plinth
        elif o['color'] == '#f0a044':
            o['color'] = '#fff2cd' # Warm lantern illumination

print(f"Realistic environment added: High-mast floodlight towers, tree lines, palms, flags and restored regal gate architecture.")
