import math

def improve_gate(objects):
    objects[:]=[o for o in objects if not o['name'].startswith(('Gate left side bay','Gate-side bay roof'))]
    for o in objects:
        if o['name'].startswith('Entry beam •'):
            o['s'][0]=22.5
        if o['mat']=='sign-gate':o['s'][0]=21.5
    def add(n,p,s,shape='box',rot=0):
        objects.append(dict(name=n,p=p,s=s,mat='white',shape=shape,group='campus',rot=rot))
    for side in [-1,1]:
        centre=-22.1 if side<0 else -3.9
        outer=-23.8 if side<0 else -2.2
        add('Gate outer pedestrian pier',[outer,2.6,-61],[.65,5.2,.8])
        add('Gate side opening soffit',[centre,4.92,-61],[3.8,.18,1.3])
        # Closed side leaves flank the open main gates in screenshot 110902.
        width=2.6
        def crown(x):return 2.6+.55*math.cos((x-centre)/width*math.pi)
        for y in [.4,.85,1.1,2.0]:add('Gate pedestrian leaf horizontal rail',[centre,y,-61],[width,.07,.10])
        for j in range(13):
            x=centre-width/2+j*width/12;top=crown(x)
            add('Gate pedestrian leaf vertical bar',[x,(top+.4)/2,-61],[.04,top-.4,.055])
            add('Gate pedestrian finial',[x,top+.10,-61],[.075,.18,.075],'petal')
        for j in range(12):
            x1=centre-width/2+j*width/12;x2=x1+width/12;y1=crown(x1);y2=crown(x2)
            length=math.hypot(x2-x1,y2-y1)
            add('Gate pedestrian curved crown segment',[(x1+x2)/2,(y1+y2)/2,-61],[length,.075,.09])
            # Small slope in the XY plane (the gate face).
            objects[-1]['rz']=math.atan2(y2-y1,x2-x1)
        for x in [centre-1.05,centre-.52,centre,centre+.52,centre+1.05]:
            add('Gate pedestrian decorative upper ring',[x,2.38,-61],[.19,.23,.06],'torus')
            add('Gate pedestrian lower diamond',[x,.67,-61],[.10,.15,.035],'petal')
        for x in [centre-width/2,centre+width/2]:add('Gate pedestrian end upright',[x,1.65,-61],[.10,2.65,.12])
        add('Gate pedestrian latch',[centre,1.45,-61.1],[.35,.035,.06])
    return objects
