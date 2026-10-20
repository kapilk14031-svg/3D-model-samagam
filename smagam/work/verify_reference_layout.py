from pathlib import Path
import json,math,struct
root=Path(__file__).resolve().parents[1]
s=json.loads((root/'outputs/scene-data.json').read_text(encoding='utf-8'))
t=json.loads((root/'outputs/sleeping-tent-layout.json').read_text(encoding='utf-8'))
assert len(t)==s['meta']['reference_accommodation']['tent_count']
assert len(s['features'])==len({f['id'] for f in s['features']})==136
assert not any('Black sleeping tent' in o['name'] or 'JHULA ZONE' in o['name'] for o in s['objects'])
assert all(any(l['text']=='GROUND-'+g for l in s['labels']) for g in ['B','C','D'])
assert abs(s['meta']['highway_boundary']['height']*2-s['meta']['highway_boundary']['main_gate_height'])<1e-5
assert len(s['meta']['highway_boundary']['openings'])==8
assert all(o['color'] in ['#493025','#38291f'] for o in s['objects'] if o['featureId']=='H06')
assert all(all(math.isfinite(v) for v in o['p']+o['s']) for o in s['objects'])
def overlap(a,b):
    for poly in [a,b]:
        for p,q in zip(poly,poly[1:]+poly[:1]):
            nx=q[1]-p[1];nz=p[0]-q[0]
            aa=[x*nx+z*nz for x,z in a];bb=[x*nx+z*nz for x,z in b]
            if max(aa)<=min(bb) or max(bb)<=min(aa):return False
    return True
walls=[]
for o in s['objects']:
    if o['kind']!='box' or not(o['layer'] in ['gates','frontage'] or o['featureId'].startswith('W')):continue
    ca=math.cos(o.get('rotY',0));sa=math.sin(o.get('rotY',0));p=[]
    for u,v in [[-.5,-.5],[.5,-.5],[.5,.5],[-.5,.5]]:
        x=u*o['s'][0];z=v*o['s'][2];p.append((o['p'][0]+x*ca+z*sa,o['p'][2]-x*sa+z*ca))
    walls.append((p,min(x for x,z in p),max(x for x,z in p),min(z for x,z in p),max(z for x,z in p)))
for tent in t:
    x,_,z=tent['p'];roof=[(x-3.4,z-4.5),(x+3.4,z-4.5),(x+3.4,z+4.5),(x-3.4,z+4.5)]
    for poly,x0,x1,z0,z1 in walls:
        if x+3.4<x0 or x-3.4>x1 or z+4.5<z0 or z-4.5>z1:continue
        assert not overlap(roof,poly),tent
blob=(root/'outputs/samagam-schematic.glb').read_bytes()
assert struct.unpack_from('<III',blob)==(0x46546c67,2,len(blob))
print(len(t),'reference tent roofs clear of gates/walls; no rides/black tents; names, frontage height/openings, railway colours and GLB validated')
