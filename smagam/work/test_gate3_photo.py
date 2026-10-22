from pathlib import Path
import json,math
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'outputs/scene-data.json').read_text(encoding='utf-8'))
f=next(f for f in d['features'] if f['id']=='G03');a=f['gateAlignment'];parts=[o for o in d['objects'] if o['featureId']=='G03']
assert all(o.get('photoGate3') for o in parts)
assert len([o for o in parts if o['name'].endswith('wood-tone gate leaf')])==4
assert any('raised name lettering' in o['name'] for o in parts)
assert len([o for o in parts if o['name'].endswith('cream outer pillar')])==2
assert any('long dark overhead beam' in o['name'] for o in parts)
assert any('round emblem blue face' in o['name'] for o in parts)
assert not any('arch' in o['name'].lower() for o in parts)
assert math.dist([f['world'][0],0,f['world'][2]],a['boundaryCentre'])<1e-7
assert abs(math.cos(a['angle'])*a['tangent'][1]+math.sin(a['angle'])*a['tangent'][0])<1e-7
assert all(abs(o['rotY']-a['angle'])<1e-7 for o in parts)
print('PASS: Gate 3 photo architecture, four wood leaves, raised lettering, central cabin/emblem, exact wall alignment;',len(parts),'parts')
