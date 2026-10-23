import json
from pathlib import Path

ROOT = Path("79-th-nirankari-sant-samagam-bhodwal/smagam")
OUT = ROOT / 'outputs'

scene = json.loads((OUT / 'scene-data.json').read_text(encoding='utf-8'))
objects = scene['objects']
plan_routes = scene['routes']

old = (OUT / 'samagam-3d.html').read_text(encoding='utf-8')
shapes_str = old.split(',SHAPES=', 1)[1].split(';\nconst canvas', 1)[0]
shapes = json.loads(shapes_str)
extra_shapes = {k: v for k, v in shapes.items() if k not in ['box', 'roof', 'ramp']}

src = (ROOT / 'work/build_model.py').read_text(encoding='utf-8')
export = src[src.index('cubeV='):src.index('# A separate, recentered GLB')]
export = export.replace('doubleSided=True))', "doubleSided=True,emissiveFactor=([min(1,c*1.65+.06) for c in rgb] if color in {r['color'] for r in plan_routes} else [0,0,0])))")
export = export.replace('else [0,0,0]', "else ([.35,.19,.045] if color in ['#b78743','#c69a55'] else [0,0,0])")
export = export.replace('else [0,0,0]', "else ([.45,.13,.015] if color in ['#b94d18','#dc7b24','#f0a044'] else [0,0,0])")
export = export.replace("(OUT/'samagam-schematic.glb').write_bytes(glb)", "(ROOT/'work/updated-model.glb').write_bytes(glb); (ROOT/'work/updated-model.glb').replace(OUT/'samagam-schematic.glb')")

local_vars = {
    'ROOT': ROOT,
    'OUT': OUT,
    'scene': scene,
    'objects': objects,
    'plan_routes': plan_routes,
    'extra_shapes': extra_shapes
}
exec(export, local_vars)
glb = (OUT / 'samagam-schematic.glb').read_bytes()
print(f"GLB regenerated: {len(glb):,} bytes, containing {len(objects)} objects!")
