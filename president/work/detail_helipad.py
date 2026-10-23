"""Ultra-realistic VIP Helicopter and Circular Helipad matching user reference images with prominent 'H'."""
import json
import math
from pathlib import Path
import numpy as np

def add_helipad(objects, colors, geo):
    colors.update(
        padConcrete='#4b535d',        # Slate gray inner touchdown circle (TLOF core)
        padOuterRim='#cbd5e1',        # Light concrete border rim
        padAsphalt='#343a40',         # Dark gray asphalt ring & approach road
        padRoadCurb='#f8fafc',        # Crisp white road curb border
        padLineWhite='#ffffff',       # Brilliant pure white for 'H' and guide circles
        padLineDark='#1f2937',        # High-contrast border outline for 'H'
        padLineYellow='#facc15',      # Aviation yellow ring & stencils ('VIP', '12 t')
        padDashedRed='#ef4444',       # Dashed red/coral safety circle
        padLightTurquoise='#2dd4bf',  # Perimeter dome lights (turquoise glow)
        padLightMetal='#475569',      # Perimeter dome light bezel
        padPoleDark='#27272a',        # Floodlight tower dark mast
        padPoleYellow='#facc15',      # Floodlight top yellow box
        padWindsockOrange='#f97316',  # Windsock orange cone
        padWindsockWhite='#f8fafc',   # Windsock white cone
        # VIP Helicopter colors
        heliWhite='#f8fafc',          # Upper fuselage white
        heliBlue='#0d2b45',           # Deep navy blue lower hull & boom
        heliGlass='#16202c',          # Dark tinted panoramic windows
        heliMetal='#64748b',          # Rotor mechanics & landing gear struts
        heliDark='#181c22',           # Tires & cockpit anti-glare
        heliTirangaSaffron='#ff9933', # Indian flag top stripe
        heliTirangaWhite='#ffffff',   # Indian flag center stripe
        heliTirangaGreen='#138808',   # Indian flag bottom stripe
        heliTirangaNavy='#000080',    # Ashoka chakra dot
        redCarpet='#991b1b'           # Campus VIP red carpet runner
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
    # 1. CIRCULAR HELIPAD PLATFORM WITH EXACT Y-SURFACE ELEVATION
    # =========================================================================
    # Concentric Radii (in meters):
    # - R_outer_rim: 16.5m (Light concrete border rim)
    # - R_asphalt_ring: 15.0m (Dark asphalt circular ring)
    # - R_yellow_ring: 12.8m (Solid aviation yellow safety circle)
    # - R_white_ring: 11.2m (Concentric solid white guide circle)
    # - R_dashed_red: 8.6m (Broken dashed red/salmon warning circle)
    # - R_slate_core: 9.8m (Slate gray touchdown core surface)
    #
    # Surface Y-Hierarchy (zero z-fighting, full visibility):
    # - Platform base rim: y = 0.14, height = 0.28 (top surface at y = 0.28)
    # - Asphalt circle: y = 0.15, height = 0.30 (top surface at y = 0.30)
    # - Slate TLOF core: y = 0.16, height = 0.32 (top surface at y = 0.32)
    # - Ground markings ('H', rings, stencils): y = 0.345, height = 0.03 (top at y = 0.36)

    r_outer_rim = 16.5
    r_asphalt = 15.0
    r_slate_core = 9.8
    r_yellow_ring = 12.8
    r_white_ring = 11.2
    r_dashed_red = 8.6

    pad_surf_y = 0.320
    mark_y = 0.342

    # 1.1 Outer Light Concrete Border Rim (Raised platform disc)
    add('Helipad circular light concrete perimeter rim', [centre[0], 0.14, centre[1]], [r_outer_rim, 0.28, r_outer_rim], 'padOuterRim', 'cylinder')

    # 1.2 Dark Asphalt Circular Apron Ring
    add('Helipad dark asphalt circular apron', [centre[0], 0.15, centre[1]], [r_asphalt, 0.30, r_asphalt], 'padAsphalt', 'cylinder')

    # 1.3 Inner Slate Gray Touchdown Core (TLOF)
    add('Helipad TLOF slate touchdown core', [centre[0], 0.16, centre[1]], [r_slate_core, 0.32, r_slate_core], 'padConcrete', 'cylinder')

    # 1.4 Solid Yellow Safety Ring (64 smooth segments)
    n_yellow = 64
    seg_len_y = (2 * math.pi * r_yellow_ring) / n_yellow + 0.10
    for k in range(n_yellow):
        t = 2 * math.pi * k / n_yellow
        p = centre + r_yellow_ring * np.array([math.cos(t), math.sin(t)])
        add('Helipad yellow safety circle segment', [p[0], mark_y, p[1]], [seg_len_y, 0.024, 0.48], 'padLineYellow', rot=math.pi / 2 - t)

    # 1.5 Solid White Guide Ring (64 smooth segments)
    n_white = 64
    seg_len_w = (2 * math.pi * r_white_ring) / n_white + 0.08
    for k in range(n_white):
        t = 2 * math.pi * k / n_white
        p = centre + r_white_ring * np.array([math.cos(t), math.sin(t)])
        add('Helipad white guide circle segment', [p[0], mark_y + 0.002, p[1]], [seg_len_w, 0.024, 0.40], 'padLineWhite', rot=math.pi / 2 - t)

    # 1.6 Dashed Red / Coral Warning Ring (36 dashes, alternating on/off)
    n_dashed = 72
    seg_len_r = (2 * math.pi * r_dashed_red) / n_dashed + 0.03
    for k in range(0, n_dashed, 2):
        t = 2 * math.pi * k / n_dashed
        p = centre + r_dashed_red * np.array([math.cos(t), math.sin(t)])
        add('Helipad red dashed safety circle segment', [p[0], mark_y + 0.004, p[1]], [seg_len_r, 0.024, 0.32], 'padDashedRed', rot=math.pi / 2 - t)

    # 1.7 Perimeter Dome Lights along Outer Light Gray Rim (Turquoise/Green LEDs)
    n_lights = 28
    r_lights = 15.75
    for k in range(n_lights):
        t = 2 * math.pi * k / n_lights
        p = centre + r_lights * np.array([math.cos(t), math.sin(t)])
        add('Perimeter dome light bezel', [p[0], 0.29, p[1]], [0.34, 0.05, 0.34], 'padLightMetal', 'cylinder')
        add('Perimeter dome light turquoise lens', [p[0], 0.34, p[1]], [0.22, 0.08, 0.22], 'padLightTurquoise', 'cylinder')

    # =========================================================================
    # 2. PROMINENT, BOLD AVIATION 'H' MARKINGS (CLEARLY VISIBLE FROM AIR & 3D)
    # =========================================================================
    # Standard ICAO Large Aviation 'H':
    # - Length of parallel uprights: 8.6 m
    # - Total width between uprights: 5.6 m (spaced at -2.5m and +2.5m from center)
    # - Stroke thickness: 1.15 m
    # - Crossbar length: 5.0 m, stroke thickness: 1.15 m
    # - High-contrast black underlay backing: stroke 1.30m, makes 'H' pop vibrantly!

    h_upright_len = 8.6
    h_crossbar_len = 5.0
    h_stroke = 1.15
    h_sep = 2.50

    # 2.1 High-contrast outline borders underneath 'H'
    for x in [-h_sep, h_sep]:
        p = centre + u * x
        add('Helipad H contrast backing upright', [p[0], mark_y + 0.003, p[1]], [h_stroke + 0.16, 0.015, h_upright_len + 0.16], 'padLineDark', rot=angle)
    add('Helipad H contrast backing crossbar', [centre[0], mark_y + 0.003, centre[1]], [h_crossbar_len + 0.16, 0.015, h_stroke + 0.16], 'padLineDark', rot=angle)

    # 2.2 Brilliant Pure White 'H' Strokes
    for x in [-h_sep, h_sep]:
        p = centre + u * x
        add('Helipad H upright stroke', [p[0], mark_y + 0.008, p[1]], [h_stroke, 0.024, h_upright_len], 'padLineWhite', rot=angle)
    add('Helipad H crossbar stroke', [centre[0], mark_y + 0.008, centre[1]], [h_crossbar_len, 0.024, h_stroke], 'padLineWhite', rot=angle)

    # 2.3 Flight Approach Alignment Arrows (Prevailing inbound/outbound heading)
    for sign in [-1, 1]:
        p_arrow = centre + zaxis * (sign * 6.8)
        add('Approach alignment arrow shaft', [p_arrow[0], mark_y + 0.006, p_arrow[1]], [0.45, 0.02, 1.8], 'padLineWhite', rot=angle)
        p_head1 = p_arrow + zaxis * (sign * 0.7) - u * 0.45
        p_head2 = p_arrow + zaxis * (sign * 0.7) + u * 0.45
        add('Approach arrow chevron left', [p_head1[0], mark_y + 0.006, p_head1[1]], [0.35, 0.02, 0.9], 'padLineWhite', rot=angle + (0.45 * sign))
        add('Approach arrow chevron right', [p_head2[0], mark_y + 0.006, p_head2[1]], [0.35, 0.02, 0.9], 'padLineWhite', rot=angle - (0.45 * sign))

    # 2.4 Yellow Aviation Stencils: "VIP" and "12 t"
    # Helper to add bold stencil lettering at mark_y + 0.008
    def add_stencil(text, center_u, center_z, letter_spacing=1.35):
        cur_u = center_u
        for char in text:
            if char == 'V':
                add('Stencil V left', [centre[0] + u[0] * (cur_u - 0.28) + zaxis[0] * center_z, mark_y + 0.008, centre[1] + u[1] * (cur_u - 0.28) + zaxis[1] * center_z], [0.26, 0.02, 1.6], 'padLineYellow', rot=angle + 0.22)
                add('Stencil V right', [centre[0] + u[0] * (cur_u + 0.28) + zaxis[0] * center_z, mark_y + 0.008, centre[1] + u[1] * (cur_u + 0.28) + zaxis[1] * center_z], [0.26, 0.02, 1.6], 'padLineYellow', rot=angle - 0.22)
            elif char == 'I':
                add('Stencil I bar', [centre[0] + u[0] * cur_u + zaxis[0] * center_z, mark_y + 0.008, centre[1] + u[1] * cur_u + zaxis[1] * center_z], [0.28, 0.02, 1.6], 'padLineYellow', rot=angle)
            elif char == 'P':
                add('Stencil P stem', [centre[0] + u[0] * (cur_u - 0.35) + zaxis[0] * center_z, mark_y + 0.008, centre[1] + u[1] * (cur_u - 0.35) + zaxis[1] * center_z], [0.26, 0.02, 1.6], 'padLineYellow', rot=angle)
                add('Stencil P top', [centre[0] + u[0] * (cur_u + 0.05) + zaxis[0] * (center_z + 0.65), mark_y + 0.008, centre[1] + u[1] * (cur_u + 0.05) + zaxis[1] * (center_z + 0.65)], [0.75, 0.02, 0.26], 'padLineYellow', rot=angle)
                add('Stencil P mid', [centre[0] + u[0] * (cur_u + 0.05) + zaxis[0] * (center_z), mark_y + 0.008, centre[1] + u[1] * (cur_u + 0.05) + zaxis[1] * (center_z)], [0.75, 0.02, 0.26], 'padLineYellow', rot=angle)
                add('Stencil P loop', [centre[0] + u[0] * (cur_u + 0.42) + zaxis[0] * (center_z + 0.32), mark_y + 0.008, centre[1] + u[1] * (cur_u + 0.42) + zaxis[1] * (center_z + 0.32)], [0.26, 0.02, 0.7], 'padLineYellow', rot=angle)
            elif char == '1':
                add('Stencil 1 stem', [centre[0] + u[0] * cur_u + zaxis[0] * center_z, mark_y + 0.008, centre[1] + u[1] * cur_u + zaxis[1] * center_z], [0.28, 0.02, 1.6], 'padLineYellow', rot=angle)
                add('Stencil 1 serif', [centre[0] + u[0] * (cur_u - 0.22) + zaxis[0] * (center_z + 0.55), mark_y + 0.008, centre[1] + u[1] * (cur_u - 0.22) + zaxis[1] * (center_z + 0.55)], [0.4, 0.02, 0.26], 'padLineYellow', rot=angle + 0.4)
            elif char == '2':
                add('Stencil 2 top', [centre[0] + u[0] * cur_u + zaxis[0] * (center_z + 0.65), mark_y + 0.008, centre[1] + u[1] * cur_u + zaxis[1] * (center_z + 0.65)], [0.9, 0.02, 0.26], 'padLineYellow', rot=angle)
                add('Stencil 2 right', [centre[0] + u[0] * (cur_u + 0.35) + zaxis[0] * (center_z + 0.35), mark_y + 0.008, centre[1] + u[1] * (cur_u + 0.35) + zaxis[1] * (center_z + 0.35)], [0.26, 0.02, 0.7], 'padLineYellow', rot=angle)
                add('Stencil 2 mid', [centre[0] + u[0] * cur_u + zaxis[0] * center_z, mark_y + 0.008, centre[1] + u[1] * cur_u + zaxis[1] * center_z], [0.9, 0.02, 0.26], 'padLineYellow', rot=angle)
                add('Stencil 2 left', [centre[0] + u[0] * (cur_u - 0.35) + zaxis[0] * (center_z - 0.35), mark_y + 0.008, centre[1] + u[1] * (cur_u - 0.35) + zaxis[1] * (center_z - 0.35)], [0.26, 0.02, 0.7], 'padLineYellow', rot=angle)
                add('Stencil 2 bot', [centre[0] + u[0] * cur_u + zaxis[0] * (center_z - 0.65), mark_y + 0.008, centre[1] + u[1] * cur_u + zaxis[1] * (center_z - 0.65)], [0.95, 0.02, 0.26], 'padLineYellow', rot=angle)
            elif char == 't':
                add('Stencil t stem', [centre[0] + u[0] * cur_u + zaxis[0] * (center_z - 0.15), mark_y + 0.008, centre[1] + u[1] * cur_u + zaxis[1] * (center_z - 0.15)], [0.26, 0.02, 1.35], 'padLineYellow', rot=angle)
                add('Stencil t cross', [centre[0] + u[0] * cur_u + zaxis[0] * (center_z + 0.22), mark_y + 0.008, centre[1] + u[1] * cur_u + zaxis[1] * (center_z + 0.22)], [0.75, 0.02, 0.26], 'padLineYellow', rot=angle)
            cur_u += letter_spacing

    # Place "VIP" on upper-left quadrant and "12 t" on lower-right quadrant
    add_stencil("VIP", -5.5, 3.8, letter_spacing=1.2)
    add_stencil("12t", 3.8, -3.8, letter_spacing=1.1)

    # =========================================================================
    # 3. RADIAL APPROACH LINK ROAD ("MAIN GATE LINK ROAD")
    # =========================================================================
    # Seamless connection from circular helipad rim to main road near campus gate
    helicopter_scale = 1.45
    heli = centre.copy()

    # Road starts at circular rim (radius 15.0m) towards the gate
    road_start = centre - outward * (r_asphalt - 0.2)
    direction = gate - road_start
    direction /= np.linalg.norm(direction)
    side = np.array([direction[1], -direction[0]])
    road_edge = roadpoint + original_outward * (geo['roads'][0]['width'] / 2)

    def end_at_road(start):
        t = np.dot(road_edge - start, original_outward) / np.dot(direction, original_outward)
        return start + direction * t

    road_w = 5.5
    half_rw = road_w / 2
    ends = [end_at_road(road_start - side * half_rw), end_at_road(road_start + side * half_rw)]
    road_end = (ends[0] + ends[1]) / 2

    polygon = np.array([road_start - side * half_rw, ends[0], ends[1], road_start + side * half_rw])
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

    # 3.1 Asphalt road surface (flush with helipad asphalt at top = 0.30)
    add('Proposed vehicle access • stops at main road edge', [mid[0], 0.15, mid[1]], [span[0], 0.30, span[1]], 'padAsphalt', 'helipadAccessTrimmed')

    # 3.2 White raised curbs along left and right edges
    road_vector = road_end - road_start
    road_len = np.linalg.norm(road_vector)
    road_rot = math.atan2(direction[0], direction[1])

    curb_w = 0.32
    curb_h = 0.16
    for s_sign in [-1, 1]:
        curb_center = (road_start + road_end) / 2 + side * (s_sign * (half_rw - curb_w / 2))
        add('Link road white curb border', [curb_center[0], 0.38, curb_center[1]], [curb_w, curb_h, road_len], 'padRoadCurb', rot=road_rot)

    # 3.3 Dashed white centerline along the approach road
    dash_len = 2.0
    dash_gap = 2.0
    dash_period = dash_len + dash_gap
    num_dashes = int(road_len / dash_period)
    for i in range(1, num_dashes):
        d_pos = road_start + direction * (i * dash_period)
        add('Link road dashed white centerline', [d_pos[0], 0.32, d_pos[1]], [0.24, 0.02, dash_len], 'padLineWhite', rot=road_rot)

    drive = road_end - road_start
    def approach_distance(o):
        p = np.array([o['p'][0], o['p'][2]])
        t = np.clip(np.dot(p - road_start, drive) / np.dot(drive, drive), 0, 1)
        return np.linalg.norm(p - road_start - t * drive)

    # Current user layout performs its own road/wall clearance after registration.

    # =========================================================================
    # 4. PERIMETER FLOODLIGHT POLES & WINDSOCK
    # =========================================================================
    # 5 Tall Dark Mast Poles with Yellow Floodlight Box Heads
    # Spaced outside circular pad at radius ~21.5m, matching reference photos
    pole_angles = [
        0.50 * math.pi,    # Top / North
        0.12 * math.pi,    # Upper-right / East
        -0.28 * math.pi,   # Lower-right / Southeast
        -0.68 * math.pi,   # Lower-left / Southwest (near approach road)
        0.88 * math.pi     # Upper-left / West
    ]
    r_pole = 21.5
    for p_ang in pole_angles:
        p_pole = centre + r_pole * np.array([math.cos(p_ang), math.sin(p_ang)])
        # Skip floodlight if it falls in the approach road corridor
        if approach_distance(dict(p=[p_pole[0], 0, p_pole[1]])) < half_rw + 0.5:
            continue
        # Tall dark cylindrical mast
        add('Perimeter floodlight dark mast', [p_pole[0], 2.85, p_pole[1]], [0.14, 5.5, 0.14], 'padPoleDark', 'cylinder')
        # Distinct yellow floodlight box head
        add('Perimeter floodlight yellow head box', [p_pole[0], 5.65, p_pole[1]], [0.65, 0.48, 0.55], 'padPoleYellow', rot=p_ang + math.pi / 2)
        # White floodlight lamp face facing toward helipad center
        vec_to_center = centre - p_pole
        face_rot = math.atan2(vec_to_center[0], vec_to_center[1])
        add('Perimeter floodlight lamp reflector', [p_pole[0], 5.62, p_pole[1]], [0.55, 0.38, 0.05], 'heliWhite', rot=face_rot)

    # Slender Aviation Windsock (at ~10 o'clock near outer rim)
    wind_ang = 0.72 * math.pi
    p_wind = centre + 16.2 * np.array([math.cos(wind_ang), math.sin(wind_ang)])
    add('Windsock foundation collar', [p_wind[0], 0.32, p_wind[1]], [0.45, 0.20, 0.45], 'padConcrete', 'cylinder')
    add('Windsock slender mast', [p_wind[0], 2.65, p_wind[1]], [0.08, 4.8, 0.08], 'padPoleDark', 'cylinder')
    add('Windsock swivel frame hoop', [p_wind[0], 5.05, p_wind[1]], [0.35, 0.35, 0.05], 'padPoleYellow', 'torus', rot=math.pi / 2)
    wind_vec = np.array([0.8, 0.35])
    wind_vec /= np.linalg.norm(wind_vec)
    for i, w_mat in enumerate(['padWindsockOrange', 'padWindsockWhite', 'padWindsockOrange', 'padWindsockWhite']):
        p_cone = p_wind + wind_vec * (0.45 + i * 0.36)
        r_cone = 0.34 - i * 0.05
        add('Windsock cone fabric segment', [p_cone[0], 5.05 - i * 0.04, p_cone[1]], [r_cone, 0.36, r_cone], w_mat, 'cylinder', rot=angle + 0.3)

    # Campus VIP Red Carpet (inside campus: main gate to auditorium entrance)
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
    add('Auditorium entrance porch landing slab', [-18.75, 0.95, entry_z], [2.3, 0.22, 7.37], 'paving')
    add('Auditorium red-carpet entrance landing', [(top['p'][0] + door_x) / 2, top['p'][1] + top['s'][1] / 2 + 0.015, entry_z], [abs(top['p'][0] - door_x), 0.025, 2.4], 'redCarpet')
    carpet_route.append([door_x, entry_z])

    # =========================================================================
    # 5. ULTRA-REALISTIC VIP HELICOPTER WITH WHEELED GEAR & INDIAN FLAG
    # =========================================================================
    facing = -outward
    yaw = math.atan2(-facing[0], -facing[1])
    c, s = math.cos(yaw), math.sin(yaw)

    # Ground contact plane is exactly pad_surf_y = 0.320 m
    # Tires touch ground at 0.320m, rest of body is elevated accurately!
    def part(name, p, size, mat, shape='box', r=0, rot=0):
        rot_val = r if r != 0 else rot
        x, y, z = p
        x *= helicopter_scale
        z *= helicopter_scale
        y_world = pad_surf_y + y * helicopter_scale
        add('Parked helicopter • ' + name, [heli[0] + c * x + s * z, y_world, heli[1] - s * x + c * z], [v * helicopter_scale for v in size], mat, shape, yaw + rot_val)

    # 5.1 FUSELAGE: Royal Navy Blue Lower Hull & Gloss White Upper Cabin
    part('royal navy blue lower belly hull', [0, 1.35, 0.15], [1.38, 0.72, 3.8], 'heliBlue', 'sphereSmooth')
    part('gloss white upper VIP passenger cabin', [0, 2.05, 0.1], [1.36, 0.85, 3.6], 'heliWhite', 'sphereSmooth')

    # 5.2 COCKPIT CANOPY & NOSE
    part('cockpit panoramic windshield canopy', [0, 2.08, -2.25], [1.22, 0.78, 1.35], 'heliGlass', 'sphereSmooth')
    part('cockpit aerodynamic nose cone', [0, 1.52, -2.95], [1.05, 0.58, 0.95], 'heliBlue', 'sphereSmooth')
    part('cockpit centre windshield post', [0, 2.15, -2.65], [0.06, 0.85, 0.12], 'heliWhite')

    # 5.3 VIP PASSENGER CABIN WINDOWS (Row of side windows)
    for side_x in [-1, 1]:
        for win_z in [-0.95, -0.25, 0.45, 1.15]:
            part('VIP panoramic cabin passenger window', [side_x * 1.37, 2.05, win_z], [0.04, 0.44, 0.54], 'heliGlass', r=math.pi / 2)
            part('passenger window chrome frame', [side_x * 1.38, 2.05, win_z], [0.02, 0.48, 0.58], 'heliMetal', r=math.pi / 2)

    # 5.4 TWIN TURBINE ENGINES & EXHAUST HOUSING
    part('roof engine turbine housing cowl', [0, 2.68, 0.65], [0.95, 0.48, 2.2], 'heliWhite', 'sphereSmooth')
    part('turbine dual air intake mouth', [0, 2.72, -0.45], [0.82, 0.32, 0.25], 'heliDark')
    for side_x in [-1, 1]:
        part('titanium canted exhaust tailpipe', [side_x * 0.55, 2.65, 1.85], [0.25, 0.25, 0.55], 'heliMetal', 'cylinder', r=0.15 * side_x)

    # 5.5 TRICYCLE WHEELED LANDING GEAR (Tires resting firmly on touchdown surface)
    # Front Nose Gear: Tire diameter 0.44m (radius 0.22m, so center is at y = 0.22)
    part('nose gear rubber tire', [0, 0.22, -2.25], [0.14, 0.44, 0.44], 'heliDark', 'cylinder')
    part('nose gear chrome hub', [0, 0.22, -2.25], [0.15, 0.24, 0.24], 'heliMetal', 'cylinder')
    part('nose gear steering yoke', [0, 0.38, -2.25], [0.22, 0.16, 0.16], 'heliDark')
    part('nose landing gear oleo strut', [0, 0.72, -2.25], [0.08, 0.65, 0.08], 'heliMetal', 'cylinder')

    # Dual Rear Main Landing Gear: Tire diameter 0.54m (radius 0.27m, so center is at y = 0.27)
    for side_x in [-1, 1]:
        part('main gear heavy rubber tire', [side_x * 1.18, 0.27, 0.65], [0.18, 0.54, 0.54], 'heliDark', 'cylinder')
        part('main gear silver wheel hub cap', [side_x * 1.19, 0.27, 0.65], [0.19, 0.28, 0.28], 'heliMetal', 'cylinder')
        part('main gear angled shock strut', [side_x * 0.95, 0.75, 0.65], [0.12, 0.82, 0.12], 'heliMetal', r=0.25 * side_x)
        part('main gear retraction pivot link', [side_x * 0.75, 0.95, 0.65], [0.38, 0.12, 0.12], 'heliDark')

    # 5.6 TAIL BOOM & HORIZONTAL STABILIZER
    part('royal navy blue tapered tail boom', [0, 1.85, 4.4], [0.36, 0.36, 3.8], 'heliBlue', 'cylinder')
    part('horizontal stabilizer airfoil wing', [0, 1.95, 5.8], [2.6, 0.08, 0.55], 'heliWhite')
    for side_x in [-1, 1]:
        part('horizontal stabilizer winglet fin', [side_x * 1.30, 1.95, 5.8], [0.06, 0.45, 0.38], 'heliBlue')

    # 5.7 SWEPT VERTICAL TAIL FIN WITH INDIAN NATIONAL FLAG (TIRANGA)
    part('swept vertical tail fin', [0, 2.85, 6.6], [0.12, 2.1, 1.25], 'heliWhite')
    part('tail fin leading edge trim', [0, 2.85, 6.05], [0.13, 1.95, 0.15], 'heliBlue')

    # INDIAN FLAG (Tiranga) painted prominently on vertical tail fin (both sides)
    flag_h = 0.28
    flag_l = 0.85
    part('Indian Flag - Saffron top band', [0, 3.22, 6.6], [0.14, flag_h, flag_l], 'heliTirangaSaffron')
    part('Indian Flag - White middle band', [0, 2.94, 6.6], [0.142, flag_h, flag_l], 'heliTirangaWhite')
    part('Indian Flag - Ashoka Chakra dot', [0, 2.94, 6.6], [0.148, 0.14, 0.14], 'heliTirangaNavy', 'sphereSmooth')
    part('Indian Flag - Green bottom band', [0, 2.66, 6.6], [0.14, flag_h, flag_l], 'heliTirangaGreen')

    # Tail strike bumper skid
    part('tail rotor protective bumper', [0, 1.35, 6.65], [0.06, 0.45, 0.45], 'heliMetal', 'torus', r=math.pi / 2)

    # Tail Rotor Assembly
    part('tail rotor 90-degree gearbox', [0.26, 3.15, 6.8], [0.18, 0.22, 0.22], 'heliMetal', 'cylinder')
    part('tail rotor vertical blade', [0.28, 3.15, 6.8], [0.06, 1.8, 0.14], 'heliDark')
    part('tail rotor horizontal blade', [0.28, 3.15, 6.8], [0.06, 0.14, 1.8], 'heliDark')
    for ty, tz in [(3.85, 6.8), (2.45, 6.8), (3.15, 6.1), (3.15, 7.5)]:
        part('tail rotor yellow warning tip', [0.29, ty, tz], [0.07, 0.16, 0.16], 'padPoleYellow')

    # 5.8 5-BLADE MAIN ROTOR SYSTEM WITH YELLOW SAFETY TIPS
    part('main rotor mast shaft', [0, 3.25, 0.45], [0.14, 0.85, 0.14], 'heliMetal', 'cylinder')
    part('main rotor swashplate disc', [0, 3.15, 0.45], [0.46, 0.08, 0.46], 'heliMetal', 'cylinder')
    part('main rotor central hub casting', [0, 3.65, 0.45], [0.55, 0.16, 0.55], 'heliMetal', 'cylinder')
    part('rotor hub vibration dampener dome', [0, 3.78, 0.45], [0.32, 0.12, 0.32], 'heliDark', 'sphereSmooth')

    # 5 Main Rotor Blades (spaced at 72 degrees, exactly matching top-down photo)
    n_blades = 5
    blade_len = 6.2
    for k in range(n_blades):
        b_ang = k * (2 * math.pi / n_blades) + 0.35
        cos_b, sin_b = math.cos(b_ang), math.sin(b_ang)

        # Inner blade root cuff
        cuff_dist = 0.65
        part('rotor blade root pitch cuff', [cuff_dist * cos_b, 3.66, 0.45 + cuff_dist * sin_b], [0.65, 0.12, 0.18], 'heliMetal', r=-b_ang)

        # Titanium main aerofoil blade body
        body_dist = 3.3
        part('main rotor titanium blade airfoil', [body_dist * cos_b, 3.64, 0.45 + body_dist * sin_b], [blade_len * 0.85, 0.06, 0.24], 'heliMetal', r=-b_ang)

        # High-visibility bright yellow safety tip
        tip_dist = blade_len
        part('rotor blade aviation yellow safety tip', [tip_dist * cos_b, 3.62, 0.45 + tip_dist * sin_b], [0.65, 0.055, 0.24], 'padPoleYellow', r=-b_ang)

    # 5.9 External Beacons & Navigation Lights
    part('tail fin apex red anticollision beacon', [0, 3.95, 6.75], [0.12, 0.15, 0.12], 'padDashedRed', 'sphereSmooth')
    part('fuselage belly red anticollision beacon', [0, 0.95, 0.2], [0.12, 0.12, 0.12], 'padDashedRed', 'sphereSmooth')
    part('forward steerable landing searchlight', [0, 1.15, -2.65], [0.22, 0.16, 0.18], 'heliWhite', 'sphereSmooth')

    corners = [(centre + u * x + zaxis * z).tolist() for x, z in [(-r_outer_rim, -r_outer_rim), (r_outer_rim, -r_outer_rim), (r_outer_rim, r_outer_rim), (-r_outer_rim, r_outer_rim)]]
    proposal = dict(
        status='Circular VIP Helipad matching user aerial reference design with prominent H',
        gate=gate.tolist(),
        centre=centre.tolist(),
        gateToCentreMetres=float(np.linalg.norm(centre - gate)),
        rightShiftMetres=right_shift,
        rightShiftReference='Looking outward from main gate',
        originalOutwardAxis=original_outward.tolist(),
        originalRightAxis=original_right.tolist(),
        widthMetres=float(r_outer_rim * 2),
        depthMetres=float(r_outer_rim * 2),
        areaSquareMetres=float(math.pi * r_outer_rim**2),
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
        vehicleAccessWidthMetres=5.5
    )
    geo['helipadProposal'] = proposal
    from helipad_user_layout import apply_layout
    objects,colors,geo=apply_layout(objects,colors,geo)
    proposal=geo['helipadProposal']
    root = Path(__file__).resolve().parents[1]
    (root / 'outputs/helipad-proposal.json').write_text(json.dumps(proposal, indent=2), encoding='utf-8')
    (root / 'outputs/georeference.json').write_text(json.dumps(geo, indent=2), encoding='utf-8')
    return objects, colors, geo
