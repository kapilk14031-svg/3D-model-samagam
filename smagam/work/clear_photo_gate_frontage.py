"""Keep existing landscaping outside the two photo-reference vehicle portals."""
for gate_id in ['G01','G02','G03']:
    gate=next(f for f in features if f['id']==gate_id);gx,_,gz=gate['world']
    for o in objects:
        if not o.get('photoGate') and any(k in o['name'].lower() for k in ['high-mast','flagpole','ceremonial flag']):
            if abs(o['p'][0]-gx)<30 and abs(o['p'][2]-gz)<36:o['p'][2]+=45 if o['p'][2]>=gz else -45
        if o.get('photoGate') or not any(k in o['name'].lower() for k in ['tree trunk','tree foliage','palm trunk','palm fronds']):continue
        if abs(o['p'][0]-gx)<15 and abs(o['p'][2]-gz)<33:
            o['p'][2]=gz+(39 if o['p'][2]>=gz else -39)
