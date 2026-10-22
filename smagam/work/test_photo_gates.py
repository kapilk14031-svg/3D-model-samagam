from pathlib import Path
import json,math
d=json.loads(Path('outputs/scene-data.json').read_text(encoding='utf-8'))
for gate_id in ['G01','G02']:
 f=next(v for v in d['features'] if v['id']==gate_id);parts=[v for v in d['objects'] if v['featureId']==gate_id];assert all(v.get('photoGate') for v in parts)
 assert not any('arch' in v['name'].lower() or 'finial' in v['name'].lower() for v in parts)
 leaves=[v for v in parts if 'ribbed dark-brown steel gate leaf' in v['name']];assert len(leaves)==4
 assert all(v['color']=='#47372f' and 'photoLeaf' in v for v in leaves)
 assert len([v for v in parts if 'outer cream pier' in v['name']])==2
 assert any('guard-room flat roof' in v['name'] for v in parts);assert any('upper entrance door window glass' in v['name'] for v in parts)
 assert len([v for v in parts if v['name'].endswith('palm planter')])==2
 def contains(o,p):
  a=o.get('rotY',0);dx=p[0]-o['p'][0];dz=p[2]-o['p'][2];return abs(dx*math.cos(a)-dz*math.sin(a))<=o['s'][0]/2 and abs(dx*math.sin(a)+dz*math.cos(a))<=o['s'][2]/2
 for side in [-1,1]:
  # Local X is tangent to the frontage; local Z is inward from the road.
  a=f.get('gateAlignment',{}).get('angle',-math.pi/2);p=[f['world'][0]+math.cos(a)*side*15,0,f['world'][2]-math.sin(a)*side*15]
  assert any(contains(o,p) for o in leaves)
  opened=[]
  for o in leaves:
   leaf=o['photoLeaf'];a=leaf['turn'];c=math.cos(a);s=math.sin(a);px,_,pz=leaf['pivot'];dx=o['p'][0]-px;dz=o['p'][2]-pz
   opened.append({**o,'p':[px+dx*c+dz*s,o['p'][1],pz-dx*s+dz*c],'rotY':o['rotY']+a})
  assert not any(contains(o,p) for o in opened)
assert any(o['featureId']=='G03' and o.get('photoGate3') for o in d['objects'])
print('PASS: both photo gates; four brown leaves, cream piers, guard room, palms; closed blocks / open clears both portals; Gate 3 retained')
