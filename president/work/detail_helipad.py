"""Ultra-realistic VIP Helicopter and International ICAO-compliant Helipad."""
import json
import math
from pathlib import Path
import numpy as np

def add_helipad(objects, colors, geo):
    colors.update(
        helipadSurface='#383d42',     # Dark asphalt safety apron
        helipadEdge='#e2e8f0',        # White safety perimeter trim
        padConcrete='#2c3136',        # Textured non-slip landing core
        padChevronRed='#b91c1c',      # ICAO safety perimeter chevron red
        padChevronWhite='#f8fafc',    # ICAO safety perimeter chevron white
        padLightGreen='#10b981',      # Elevated green landing light lens
        padLightRed='#ef4444',        # Obstruction red warning beacon
        padWindsockOrange='#ea580c',  # Aviation windsock day-glo orange
        padWindsockWhite='#f8fafc',   # Aviation windsock white
        heliWhite='#f8fafc',          # High-gloss aviation white fuselage
        heliBlue='#10385c',           # Deep royal navy blue lower hull
        heliGold='#c99a3e',           # VIP metallic gold cheatline stripe
        heliGlass='#162f40',          # Transparent tinted cockpit canopy
        heliMetal='#64748b',          # Titanium & aluminum rotor mechanism
        heliDark='#181c22',           # Anti-glare shield & cockpit interior
        heliNavRed='#ef4444',         # Port navigation light & beacon
        heliNavGreen='#10b981',       # Starboard navigation light
        heliYellow='#fbbf24',         # Safety yellow rotor tips & stencils
        redCarpet='#991b1b'           # VIP red carpet runner
    )

    def add(name, p, s, mat, shape='box', rot=0):
        objects.append(dict(name=name, p=list(map(float, p)), s=list(map(float, s)), mat=mat, shape=shape, group='helipad', rot=float(rot)))

    g = np.array([-13., 1., -61.])
    m = np.array(geo['globalPlanTransform'])
    gate = np.array([g[0], g[2], 1]) @ m
    gate += np.array(geo['gateDelta'])
    road = np.array(geo['roads'][0]['points'])
    candidates = []
    for a, b in zip(road, road[1:]):
        v = b - a
        t = np.clip(np.dot(gate - a, v) / np.dot(v, v), 0, 1)
        p = a + t * v
        candidates.append((np.linalg.norm(p - gate), p, v / np.linalg.norm(v)))
    _, roadpoint, u = min(candidates, key=lambda x: x[0])
    outward = roadpoint - gate
    outward /= np.linalg.norm(outward)
    right_shift = 8.0
    original_outward = outward.copy()
    original_right = u.copy()
    centre = gate + outward * math.sqrt(100**2 - right_shift**2) + u * right_shift
    outward = (centre - gate) / 100
    u = np.array([-outward[1], outward[0]])
    lawn = np.array(next(f['points'] for f in geo['footprints'] if f['id'] == 'garden'))
    width = np.linalg.norm(lawn[1] - lawn[0])
    depth = np.linalg.norm(lawn[3] - lawn[0])
    v1 = lawn[1] - lawn[0]
    v2 = lawn[3] - lawn[0]
    area = abs(v1[0] * v2[1] - v1[1] * v2[0])
    depth = area / width

    zaxis = -outward
    angle = math.atan2(-u[1], u[0])

    # =========================================================================
    # 1. HELIPAD GROUND APRON & TLOF (TOUCHDOWN & LIFT-OFF) SURFACE
    # =========================================================================
    # Main asphalt safety apron
    add('Helipad safety apron slab', [centre[0], 0.22, centre[1]], [width, 0.22, depth], 'helipadSurface', rot=angle)

    # Circular non-slip touchdown core (TLOF)
    pad_radius = min(width, depth) * 0.38
    add('Helipad TLOF asphalt landing core', [centre[0], 0.25, centre[1]], [pad_radius * 2, 0.05, pad_radius * 2], 'padConcrete', 'cylinder')

    # Alternating Red & White ICAO Safety Perimeter Border Kerbs
    half_w, half_d = width / 2, depth / 2
    for x_step in np.linspace(-half_w + 1.0, half_w - 1.0, int(width / 2.2)):
        mat = 'padChevronRed' if int(x_step) % 2 == 0 else 'padChevronWhite'
        p1 = centre + u * x_step + zaxis * half_d
        p2 = centre + u * x_step - zaxis * half_d
        add('Helipad perimeter kerb block', [p1[0], 0.36, p1[1]], [1.8, 0.06, 0.28], mat, rot=angle)
        add('Helipad perimeter kerb block', [p2[0], 0.36, p2[1]], [1.8, 0.06, 0.28], mat, rot=angle)
    for z_step in np.linspace(-half_d + 1.0, half_d - 1.0, int(depth / 2.2)):
        mat = 'padChevronWhite' if int(z_step) % 2 == 0 else 'padChevronRed'
        p1 = centre + u * half_w + zaxis * z_step
        p2 = centre - u * half_w + zaxis * z_step
        add('Helipad perimeter kerb block', [p1[0], 0.36, p1[1]], [0.28, 0.06, 1.8], mat, rot=angle)
        add('Helipad perimeter kerb block', [p2[0], 0.36, p2[1]], [0.28, 0.06, 1.8], mat, rot=angle)

    # Touchdown guide ring: outer yellow safety ring & inner white ring
    inner_ring_radius = pad_radius * 0.82
    for k in range(48):
        t = 2 * math.pi * k / 48
        # Outer yellow ring
        p_out = centre + pad_radius * np.array([math.cos(t), math.sin(t)])
        add('Helipad yellow safety circle segment', [p_out[0], 0.275, p_out[1]], [pad_radius * 2 * math.pi / 48 + 0.08, 0.02, 0.40], 'heliYellow', rot=math.pi / 2 - t)
        # Inner white touchdown circle
        p_in = centre + inner_ring_radius * np.array([math.cos(t), math.sin(t)])
        add('Helipad white touchdown ring segment', [p_in[0], 0.28, p_in[1]], [inner_ring_radius * 2 * math.pi / 48 + 0.05, 0.02, 0.35], 'heliWhite', rot=math.pi / 2 - t)

    # Standard Aviation 'H' Identification Mark (Crisp white with safety yellow bevel)
    h_upright_len = 7.5
    h_crossbar_len = 5.6
    h_stroke = 0.95
    for x in [-2.35, 2.35]:
        p = centre + u * x
        add('Helipad H upright stroke', [p[0], 0.29, p[1]], [h_stroke, 0.025, h_upright_len], 'heliWhite', rot=angle)
    add('Helipad H crossbar stroke', [centre[0], 0.29, centre[1]], [h_crossbar_len, 0.025, h_stroke], 'heliWhite', rot=angle)

    # Helipad Stencil Markings: MTOW (12 t) & Max D-Value (22 m)
    p_t = centre + zaxis * 5.2 - u * 3.8
    add('Helipad MTOW weight rating stencil', [p_t[0], 0.285, p_t[1]], [2.4, 0.02, 1.2], 'heliWhite', rot=angle)
    p_d = centre - zaxis * 5.2 + u * 3.8
    add('Helipad D-value rating stencil', [p_d[0], 0.285, p_d[1]], [2.4, 0.02, 1.2], 'heliWhite', rot=angle)

    # Flight Approach & Departure Guidance Arrows
    for fwd in [-1, 1]:
        p_arr = centre + zaxis * (fwd * (inner_ring_radius + 1.8))
        add('Flight corridor approach arrow shaft', [p_arr[0], 0.28, p_arr[1]], [0.65, 0.02, 3.2], 'heliYellow', rot=angle)
        p_head = p_arr + zaxis * (fwd * 1.8)
        add('Flight corridor approach arrowhead', [p_head[0], 0.282, p_head[1]], [1.8, 0.02, 0.75], 'heliYellow', rot=angle)

    # =========================================================================
    # 2. HELIPAD PERIMETER LIGHTING & AVIATION WINDSOCK
    # =========================================================================
    # 24 Elevated Green Perimeter Landing Lights (ICAO Omnidirectional Green LEDs)
    for k in range(24):
        t = 2 * math.pi * k / 24
        p_light = centre + (pad_radius + 0.65) * np.array([math.cos(t), math.sin(t)])
        add('Perimeter light base flange', [p_light[0], 0.28, p_light[1]], [0.22, 0.05, 0.22], 'heliYellow', 'cylinder')
        add('Perimeter light elevated pole', [p_light[0], 0.40, p_light[1]], [0.08, 0.22, 0.08], 'heliYellow', 'cylinder')
        add('Perimeter light green LED lens', [p_light[0], 0.54, p_light[1]], [0.12, 0.12, 0.12], 'padLightGreen', 'sphereSmooth')

    # 4 Corner Floodlight Towers with Red Obstruction Beacons
    corner_coords = [
        (-half_w + 2.5, -half_d + 2.5),
        (half_w - 2.5, -half_d + 2.5),
        (half_w - 2.5, half_d - 2.5),
        (-half_w + 2.5, half_d - 2.5)
    ]
    for cx, cz in corner_coords:
        p_tower = centre + u * cx + zaxis * cz
        add('Helipad floodlight concrete pedestal', [p_tower[0], 0.35, p_tower[1]], [0.75, 0.30, 0.75], 'padConcrete')
        add('Helipad floodlight mast pole', [p_tower[0], 2.55, p_tower[1]], [0.12, 4.2, 0.12], 'heliMetal', 'cylinder')
        add('Helipad floodlight fixture head', [p_tower[0], 4.60, p_tower[1]], [0.55, 0.25, 0.35], 'heliDark', rot=angle)
        add('Helipad floodlight lens face', [p_tower[0], 4.58, p_tower[1]], [0.48, 0.20, 0.05], 'heliWhite', rot=angle)
        add('Helipad corner red obstruction light', [p_tower[0], 4.85, p_tower[1]], [0.15, 0.16, 0.15], 'padLightRed', 'sphereSmooth')

    # Illuminated Aviation Windsock Assembly
    p_wind = centre + u * (-half_w + 4.2) + zaxis * (-half_d + 4.2)
    add('Windsock foundation pedestal', [p_wind[0], 0.35, p_wind[1]], [0.9, 0.25, 0.9], 'padConcrete', 'cylinder')
    add('Windsock steel tilt mast', [p_wind[0], 2.50, p_wind[1]], [0.08, 4.2, 0.08], 'heliMetal', 'cylinder')
    p_hoop = p_wind + np.array([0.45, 4.45])
    add('Windsock swivel frame hoop', [p_hoop[0], 4.50, p_wind[1]], [0.48, 0.48, 0.05], 'heliYellow', 'torus', rot=math.pi / 2)
    wind_dir = np.array([0.85, 0.25])
    wind_dir /= np.linalg.norm(wind_dir)
    for i, w_mat in enumerate(['padWindsockOrange', 'padWindsockWhite', 'padWindsockOrange', 'padWindsockWhite', 'padWindsockOrange']):
        p_cone = p_wind + wind_dir * (0.65 + i * 0.42)
        r_cone = 0.42 - i * 0.055
        add('Windsock cone fabric segment', [p_cone[0], 4.48 - i * 0.04, p_cone[1]], [r_cone, 0.44, r_cone], w_mat, 'cylinder', rot=angle + 0.3)
    add('Windsock mast top red beacon', [p_wind[0], 4.82, p_wind[1]], [0.14, 0.15, 0.14], 'padLightRed', 'sphereSmooth')

    # Mobile Fire Extinguisher Station (Twin-cylinder foam/powder unit)
    p_fire = centre + u * (half_w - 3.8) + zaxis * (-half_d + 4.5)
    add('Fire station yellow base plate', [p_fire[0], 0.35, p_fire[1]], [1.2, 0.06, 0.9], 'heliYellow')
    for fx in [-0.22, 0.22]:
        p_cyl = p_fire + u * fx
        add('Emergency fire foam cylinder', [p_cyl[0], 0.85, p_cyl[1]], [0.34, 0.92, 0.34], 'heliNavRed', 'cylinder')
        add('Cylinder chrome pressure valve', [p_cyl[0], 1.35, p_cyl[1]], [0.10, 0.12, 0.10], 'heliMetal', 'cylinder')
    add('Fire cart push handle', [p_fire[0], 1.15, p_fire[1] + 0.35], [0.65, 0.04, 0.04], 'heliMetal')
    add('Fire cart rubber wheel', [p_fire[0] - 0.45, 0.48, p_fire[1] + 0.35], [0.08, 0.30, 0.30], 'heliDark', 'cylinder')
    add('Fire cart rubber wheel', [p_fire[0] + 0.45, 0.48, p_fire[1] + 0.35], [0.08, 0.30, 0.30], 'heliDark', 'cylinder')

    # =========================================================================
    # 3. VEHICLE CONNECTOR & RED CARPET PASSAGEWAYS
    # =========================================================================
    helicopter_scale = 1.45
    heli = centre + outward * 4 - u * (1.9 * helicopter_scale)
    road_start = centre - outward * (depth / 2 - 1)
    direction = gate - road_start
    direction /= np.linalg.norm(direction)
    side = np.array([direction[1], -direction[0]])
    road_edge = roadpoint + original_outward * (geo['roads'][0]['width'] / 2)

    def end_at_road(start):
        t = np.dot(road_edge - start, original_outward) / np.dot(direction, original_outward)
        return start + direction * t

    ends = [end_at_road(road_start - side * 2.75), end_at_road(road_start + side * 2.75)]
    road_end = (ends[0] + ends[1]) / 2
    polygon = np.array([road_start - side * 2.75, ends[0], ends[1], road_start + side * 2.75])
    signed = sum(polygon[i, 0] * polygon[(i + 1) % 4, 1] - polygon[(i + 1) % 4, 0] * polygon[i, 1] for i in range(4))
    if signed < 0:
        polygon = polygon[::-1]
    lo = polygon.min(axis=0)
    hi = polygon.max(axis=0)
    mid = (lo + hi) / 2
    span = hi - lo
    vertices = [[float((x - mid[0]) / span[0]), y, float((z - mid[1]) / span[1])] for y in [-0.5, 0.5] for x, z in polygon]
    faces = [[0, 1, 2], [0, 2, 3], [4, 6, 5], [4, 7, 6]]
    for i in range(4):
        j = (i + 1) % 4
        faces.extend([[i, j, j + 4], [i, j + 4, i + 4]])
    from detail_lotus_v8 import MESHES
    MESHES['helipadAccessTrimmed'] = {'vertices': vertices, 'faces': faces}
    add('Proposed vehicle access • stops at main road edge', [mid[0], 0.30, mid[1]], [span[0], 0.12, span[1]], 'paving', 'helipadAccessTrimmed')

    drive = road_end - road_start
    def approach_distance(o):
        p = np.array([o['p'][0], o['p'][2]])
        t = np.clip(np.dot(p - road_start, drive) / np.dot(drive, drive), 0, 1)
        return np.linalg.norm(p - road_start - t * drive)

    objects[:] = [o for o in objects if not (o['name'].startswith('Northern enclosure wall') and approach_distance(o) < 3.4)]

    # Boarding red carpet
    helicopter_exit = heli + u * (1.9 * helicopter_scale)
    road_normal = np.array([drive[1], -drive[0]]) / np.linalg.norm(drive)
    if np.dot(road_normal, u) < 0:
        road_normal = -road_normal
    boarding_end = road_start.copy()
    boarding_delta = boarding_end - helicopter_exit
    boarding_centre = (helicopter_exit + boarding_end) / 2
    add('Short red carpet • helicopter to vehicle road only', [boarding_centre[0], 0.36, boarding_centre[1]], [2.4, 0.025, np.linalg.norm(boarding_delta)], 'redCarpet', rot=math.atan2(boarding_delta[0], boarding_delta[1]))

    steps = sorted([o for o in objects if o['name'].startswith('External black entry step')], key=lambda o: o['p'][1])
    entry_z = steps[0]['p'][2]
    turn = np.array([gate[0], entry_z])
    foot = np.array([steps[0]['p'][0] + steps[0]['s'][0] / 2, entry_z])
    carpet_route = [gate.tolist(), turn.tolist(), foot.tolist()]
    for a, b in [(gate, turn), (turn, foot)]:
        d = b - a
        c = (a + b) / 2
        add('Proposed red carpet • main gate to auditorium', [c[0], 0.38, c[1]], [2.4, 0.025, np.linalg.norm(d)], 'redCarpet', rot=math.atan2(d[0], d[1]))
    for step in steps:
        p = step['p']
        add('Auditorium red-carpet stair tread', [p[0], p[1] + step['s'][1] / 2 + 0.015, p[2]], [step['s'][0], 0.025, 2.4], 'redCarpet', rot=step['rot'])
    top = steps[-1]
    jambs = [o for o in objects if o['name'].startswith('Side entrance metal jamb')]
    door_x = sum(o['p'][0] for o in jambs) / len(jambs)
    add('Auditorium red-carpet entrance landing', [(top['p'][0] + door_x) / 2, top['p'][1] + top['s'][1] / 2 + 0.015, entry_z], [abs(top['p'][0] - door_x), 0.025, 2.4], 'redCarpet')
    carpet_route.append([door_x, entry_z])

    # =========================================================================
    # 4. ULTRA-REALISTIC VIP TWIN-TURBINE HELICOPTER
    # =========================================================================
    facing = -outward
    yaw = math.atan2(-facing[0], -facing[1])
    c, s = math.cos(yaw), math.sin(yaw)

    def part(name, p, size, mat, shape='box', r=0):
        x, y, z = p
        x *= helicopter_scale
        z *= helicopter_scale
        y = 0.33 + (y - 0.54) * helicopter_scale
        add('Parked helicopter • ' + name, [heli[0] + c * x + s * z, y, heli[1] - s * x + c * z], [v * helicopter_scale for v in size], mat, shape, yaw + r)

    # 4.1 FUSELAGE & MAIN AERO SHELL
    part('aerodynamic main fuselage', [0, 2.22, 0.05], [1.38, 1.25, 3.45], 'heliWhite', 'sphereSmooth')
    part('royal navy blue lower hull', [0, 1.55, 0.15], [1.25, 0.58, 3.05], 'heliBlue', 'sphereSmooth')
    # Metallic gold cheatline separating white top and blue bottom
    for side in [-1, 1]:
        part('metallic gold cheatline stripe', [side * 1.37, 1.82, 0.15], [0.03, 0.08, 3.15], 'heliGold')

    # 4.2 NOSE CONE & WEATHER RADOME
    part('nose radome cone', [0, 1.95, -3.35], [0.65, 0.55, 0.65], 'heliWhite', 'sphereSmooth')
    part('radome front tip', [0, 1.95, -3.72], [0.22, 0.22, 0.22], 'heliDark', 'sphereSmooth')
    for side in [-1, 1]:
        part('pitot static probe', [side * 0.48, 1.95, -3.65], [0.018, 0.018, 0.45], 'heliMetal', 'cylinder')

    # 4.3 COCKPIT CANOPY GLAZING & WIRE CUTTERS
    part('cockpit panoramic windshield', [0, 2.45, -2.4], [1.16, 0.82, 1.25], 'heliGlass', 'sphereSmooth')
    part('cockpit centre windshield divider', [0, 2.45, -3.61], [0.055, 1.25, 0.06], 'heliWhite')
    for side in [-1, 1]:
        part('lower chin observation glass', [side * 0.42, 1.62, -2.85], [0.38, 0.48, 0.38], 'heliGlass', 'sphereSmooth')
        part('overhead green tinted skylight window', [side * 0.45, 2.92, -2.05], [0.38, 0.06, 0.55], 'heliGlass')
        part('windshield articulated wiper', [side * 0.38, 1.78, -3.15], [0.014, 0.45, 0.014], 'heliDark', r=0.25 * side)

    # Wire Strike Protection System (WSPS) cable cutters
    part('upper WSPS wire cutter blade', [0, 3.12, -2.35], [0.045, 0.35, 0.22], 'heliMetal')
    part('lower WSPS wire cutter blade', [0, 1.48, -3.15], [0.045, 0.28, 0.18], 'heliMetal')

    # 4.4 COCKPIT & VIP CABIN INTERIOR
    part('cockpit glare shield', [0, 2.38, -2.75], [1.05, 0.10, 0.55], 'heliDark')
    for side in [-1, 1]:
        part('glass cockpit MFD screen', [side * 0.28, 2.32, -2.82], [0.24, 0.16, 0.02], 'padLightGreen')
    part('centre avionics pedestal', [0, 1.85, -2.45], [0.26, 0.45, 0.75], 'heliDark')
    for side in [-1, 1]:
        part('pilot leather bucket seat', [side * 0.35, 1.95, -2.10], [0.38, 0.55, 0.38], 'heliDark')
        part('pilot seat headrest', [side * 0.35, 2.32, -1.95], [0.22, 0.18, 0.14], 'heliDark')
        part('cyclic flight control stick', [side * 0.35, 1.85, -2.45], [0.02, 0.35, 0.02], 'heliMetal', 'cylinder')
    for side in [-1, 1]:
        part('VIP executive club chair', [side * 0.45, 1.95, 0.25], [0.44, 0.55, 0.44], 'heliDark')
        part('VIP executive club chair', [side * 0.45, 1.95, 0.95], [0.44, 0.55, 0.44], 'heliDark')

    # 4.5 CABIN DOORS & PANORAMIC SIDE WINDOWS
    for side in [-1, 1]:
        for z in [-0.5, 1.05]:
            part('side cabin panoramic window', [side * 1.40, 2.55, z], [1.25, 0.65, 0.035], 'heliGlass', 'rounded', math.pi / 2)
        part('flush chrome door handle', [side * 1.45, 1.95, 0.55], [0.04, 0.05, 0.32], 'heliMetal')
        for z in [-1.23, 1.82]:
            part('sliding door rubber seal', [side * 1.41, 2.2, z], [0.045, 1.5, 0.045], 'heliDark')
        for y in [1.47, 2.96]:
            part('stainless steel door guide track', [side * 1.41, y, 0.3], [0.055, 0.045, 3.05], 'heliMetal')

    # 4.6 TWIN TURBOSHAFT ENGINES & EXHAUST
    part('twin turbine engine fairing cowl', [0, 3.32, 1.05], [0.92, 0.48, 1.85], 'heliBlue', 'sphereSmooth')
    for side in [-1, 1]:
        part('turbine air intake mesh grille', [side * 0.34, 3.35, 0.12], [0.28, 0.22, 0.16], 'heliDark')
        part('engine oil cooler louvers', [side * 0.83, 3.42, 1.05], [0.035, 0.22, 0.85], 'heliDark')
    for side in [-1, 1]:
        part('titanium canted exhaust tailpipe', [side * 0.72, 3.25, 2.05], [0.26, 0.24, 0.65], 'heliMetal', 'sphereSmooth')
        part('exhaust heat shield lip', [side * 0.72, 3.25, 2.38], [0.28, 0.26, 0.08], 'heliDark', 'cylinder')

    # 4.7 MAIN ROTOR MAST, DETAILED SWASHPLATE & DROOPED BLADES
    part('main rotor mast shaft', [0, 3.95, 0.25], [0.14, 1.15, 0.14], 'heliMetal', 'cylinder')
    part('stationary lower swashplate', [0, 3.82, 0.25], [0.44, 0.07, 0.44], 'heliMetal', 'cylinder')
    part('rotating upper swashplate', [0, 3.96, 0.25], [0.42, 0.07, 0.42], 'heliMetal', 'cylinder')
    for rod_ang in [0.8, 2.9, 4.9]:
        rx, rz = math.cos(rod_ang) * 0.26, math.sin(rod_ang) * 0.26
        part('hydraulic pitch actuator rod', [rx, 3.95, 0.25 + rz], [0.03, 0.75, 0.03], 'heliMetal', 'cylinder')

    part('main rotor hub casting', [0, 4.49, 0.25], [0.52, 0.18, 0.52], 'heliMetal', 'cylinder')
    part('pendulum vibration absorber cap', [0, 4.62, 0.25], [0.32, 0.12, 0.32], 'heliDark', 'sphereSmooth')

    for k in range(4):
        a = k * math.pi / 2 + 0.2
        cos_a, sin_a = math.cos(a), math.sin(a)
        gx, gz = 0.55 * cos_a, 0.25 + 0.55 * sin_a
        part('rotor blade pitch cuff', [gx, 4.52, gz], [0.72, 0.16, 0.22], 'heliMetal', r=-a)

        m1_dist = 2.4
        part('main rotor blade inner airfoil', [m1_dist * cos_a, 4.53, 0.25 + m1_dist * sin_a], [3.2, 0.07, 0.28], 'heliMetal', r=-a)

        m2_dist = 5.2
        part('main rotor blade droop aerofoil', [m2_dist * cos_a, 4.45, 0.25 + m2_dist * sin_a], [3.2, 0.065, 0.26], 'heliMetal', r=-a)

        tip_dist = 6.85
        part('rotor blade yellow hazard tip', [tip_dist * cos_a, 4.38, 0.25 + tip_dist * sin_a], [0.55, 0.05, 0.26], 'heliYellow', r=-a)
        part('rotor blade white accent stripe', [(tip_dist - 0.32) * cos_a, 4.40, 0.25 + (tip_dist - 0.32) * sin_a], [0.18, 0.052, 0.26], 'heliWhite', r=-a)

        for step in [2.0, 4.0, 6.0]:
            part('blade stainless erosion strip', [step * cos_a, 4.50 - (step / 6.0) * 0.12, 0.25 + step * sin_a], [0.03, 0.03, 0.03], 'heliWhite', 'sphereSmooth')

    # 4.8 TAIL BOOM, STABILIZERS & TAIL ROTOR
    part('tapered tail boom', [0, 2.30, 5.6], [0.34, 0.36, 3.6], 'heliWhite', 'sphereSmooth')
    part('drive shaft dorsal spine fairing', [0, 2.50, 5.5], [0.14, 0.08, 3.4], 'heliBlue')

    part('horizontal stabilizer wing', [0, 2.32, 7.7], [2.85, 0.12, 0.68], 'heliWhite')
    for side in [-1, 1]:
        part('horizontal stabilizer finlet', [side * 1.42, 2.32, 7.7], [0.08, 0.65, 0.45], 'heliBlue')
        nav_mat = 'heliNavRed' if side < 0 else 'heliNavGreen'
        part('winglet navigation light', [side * 1.48, 2.32, 7.7], [0.09, 0.09, 0.12], nav_mat, 'sphereSmooth')

    part('swept vertical tail fin', [0, 3.10, 8.55], [0.18, 2.35, 1.45], 'heliBlue')
    part('tail strike bumper skid', [0, 1.82, 8.4], [0.06, 0.65, 0.55], 'heliMetal', 'torus', r=math.pi / 2)

    part('tail rotor 90-deg gearbox', [0.35, 3.02, 8.55], [0.16, 0.24, 0.24], 'heliMetal', 'cylinder')
    part('tail rotor pitch slider hub', [0.44, 3.02, 8.55], [0.12, 0.22, 0.22], 'heliWhite', 'sphereSmooth')
    part('tail rotor vertical blade', [0.36, 3.02, 8.55], [0.08, 2.5, 0.16], 'heliMetal')
    part('tail rotor horizontal blade', [0.36, 3.02, 8.55], [0.08, 0.16, 2.5], 'heliMetal')
    for ty, tz in [(4.25, 8.55), (1.79, 8.55), (3.02, 7.32), (3.02, 9.78)]:
        part('tail rotor safety warning tip', [0.37, ty, tz], [0.10, 0.22, 0.22], 'heliYellow')
        part('tail rotor black stripe', [0.37, ty, tz], [0.105, 0.08, 0.08], 'heliDark')

    # 4.9 AVIONICS, ANTENNAS & STROBE LIGHTING
    part('VHF communications blade antenna', [0, 2.68, 4.8], [0.03, 0.45, 0.18], 'heliMetal')
    part('ATC transponder blade antenna', [0, 2.62, 6.4], [0.025, 0.35, 0.14], 'heliMetal')
    part('GPS satellite mushroom antenna dome', [0, 3.78, 1.6], [0.18, 0.09, 0.18], 'heliWhite', 'sphereSmooth')

    part('vertical fin apex red strobe beacon', [0, 4.35, 8.7], [0.14, 0.16, 0.14], 'padLightRed', 'sphereSmooth')
    part('fuselage lower belly red beacon', [0, 1.24, 0.2], [0.14, 0.14, 0.14], 'padLightRed', 'sphereSmooth')
    part('tail cone aft white position light', [0, 2.35, 9.4], [0.08, 0.08, 0.12], 'heliWhite', 'sphereSmooth')

    for side in [-1, 1]:
        part('nose steerable landing searchlight', [side * 0.26, 1.45, -3.05], [0.22, 0.16, 0.18], 'heliWhite', 'sphereSmooth')

    # 4.10 HEAVY-DUTY TUBULAR SKIDS & BOARDING FOOTBOARDS
    for side in [-1, 1]:
        part('heavy-duty tubular landing skid', [side * 1.52, 0.62, 0.2], [0.12, 0.12, 6.2], 'heliMetal', 'rounded')
        part('skid upturned nose curve', [side * 1.52, 0.78, -2.85], [0.10, 0.24, 0.45], 'heliMetal', 'sphereSmooth')
        part('skid rear protective end cap', [side * 1.52, 0.62, 3.3], [0.13, 0.13, 0.15], 'heliDark', 'sphereSmooth')
        for z in [-1.5, 1.5]:
            part('cross-tube gear saddle arch', [side * 1.12, 1.02, z], [0.12, 0.88, 0.12], 'heliMetal')
            part('hydraulic oleo damper collar', [side * 1.12, 0.95, z], [0.16, 0.22, 0.16], 'heliDark')
        part('passenger boarding footboard', [side * 1.68, 0.98, 0.1], [0.42, 0.12, 1.6], 'heliMetal', 'rounded')
        for z in [-0.5, -0.2, 0.1, 0.4, 0.7]:
            part('footboard anti-slip grip rib', [side * 1.68, 1.05, z], [0.40, 0.025, 0.035], 'heliDark')
        part('ground handling wheel tire', [side * 1.64, 0.62, 2.2], [0.12, 0.36, 0.36], 'heliDark', 'cylinder')
        part('ground handling wheel hub', [side * 1.64, 0.62, 2.2], [0.13, 0.20, 0.20], 'heliMetal', 'cylinder')

    corners = [(centre + u * x + zaxis * z).tolist() for x, z in [(-width / 2, -depth / 2), (width / 2, -depth / 2), (width / 2, depth / 2), (-width / 2, depth / 2)]]
    proposal = dict(
        status='Proposed visual arrangement; site/flight suitability not verified',
        gate=gate.tolist(),
        centre=centre.tolist(),
        gateToCentreMetres=float(np.linalg.norm(centre - gate)),
        rightShiftMetres=right_shift,
        rightShiftReference='Looking outward from main gate',
        originalOutwardAxis=original_outward.tolist(),
        originalRightAxis=original_right.tolist(),
        widthMetres=float(width),
        depthMetres=float(depth),
        areaSquareMetres=float(area),
        corners=corners,
        helicopterCentre=heli.tolist(),
        helicopterDisplayScale=helicopter_scale,
        alignmentAxis=outward.tolist(),
        carpet=carpet_route,
        carpetDestination='Auditorium side entrance',
        vehicleAccess=[road_start.tolist(), road_end.tolist()],
        vehicleAccessEnd='Main road field-side edge',
        vehicleAccessPolygon=polygon.tolist(),
        mainRoadJoinEdge=[ends[0].tolist(), ends[1].tolist()],
        vehicleAccessWidthMetres=5.5,
        helipadBoardingCarpet=[helicopter_exit.tolist(), boarding_end.tolist()]
    )
    geo['helipadProposal'] = proposal
    root = Path(__file__).resolve().parents[1]
    (root / 'outputs/helipad-proposal.json').write_text(json.dumps(proposal, indent=2), encoding='utf-8')
    (root / 'outputs/georeference.json').write_text(json.dumps(geo, indent=2), encoding='utf-8')
    return objects, colors, geo
