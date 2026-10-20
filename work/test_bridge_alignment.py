import json,math
from pathlib import Path
d=json.loads(Path('outputs/scene-data.json').read_text(encoding='utf-8'));b=d['meta']['s04_footbridge'];road=next(f for f in d['features'] if f['id']=='H01')['path'];a,bb=next((a,bb) for a,bb in zip(road,road[1:]) if a[0]<=855<=bb[0]);v=a[1]+(bb[1]-a[1])*(855-a[0])/(bb[0]-a[0]);assert math.dist(b['anchor'],[(v-760)*1.4,0,(1000-855)*1.4])<1e-8
angle=math.atan2(a[1]-bb[1],bb[0]-a[0]);assert abs(b['angle']-angle)<1e-8
assert b['span']/2-2.8>18 # stair inner edge stays outside 36-unit carriageway
assert b['span']/2+3<25.5-1.1 # landing outer edge stays clear of wall/pier
assert b['span']==42.5
print('PASS: 42.5-unit bridge centred on NH44; perpendicular to local road; stairs outside lanes and landing clear of frontage wall')
