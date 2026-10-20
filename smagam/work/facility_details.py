"""Illustrative architecture and vehicles within source-defined facility footprints."""
def beam3(name,a,b,width,color,layer='pandal'):
    d=[b[i]-a[i] for i in range(3)];length=math.sqrt(sum(v*v for v in d));dx,dy,dz=[v/length for v in d]
    q=[dz,0,-dx,1+dy];ql=math.sqrt(sum(v*v for v in q))
    if ql<.00001:q=[1,0,0,0]
    else:q=[v/ql for v in q]
    add(name,'box',*( (a[i]+b[i])/2 for i in range(3)),width,length,width,color,layer);objects[-1]['quaternion']=q

def detailed_facility(f,x,z,w,d,h):
    layer=f['layer'];name=f['name'];langar='LANGAR' in name;toilet=f['kind']=='toilets'
    if w<5 or d<5:return
    # All detailing stays inside the depicted block envelope.
    box(name+' plinth',x,z,w+.5,d+.5,.35,'#acaa96',0,layer)
    front=z+d/2+.08
    doorw=min(3.5,w*.22);doorh=min(3.8,h*.8)
    box(name+' entrance reveal',x,front,doorw+.7,.25,doorh+.3,'#9b977f',.3,layer)
    box(name+' entrance door',x,front+.15,doorw,.12,doorh,'#42686a',.35,layer)
    box(name+' canopy',x,front+.7,min(w*.55,8),1.5,.2,'#d8c5a0',doorh+.7,layer)
    if not toilet:
        n=max(1,min(14,int(w/8)))
        for j in range(n):
            xx=x-w/2+(j+.5)*w/n
            if abs(xx-x)<doorw:continue
            ww=min(3.5,w/n*.56)
            box(name+' window surround',xx,front,ww+.45,.22,2.45,'#e9e1cb',2,layer)
            box(name+' ventilation panel' if langar else name+' glazing',xx,front+.14,ww,.12,1.95,'#617c78' if langar else '#668b91',2.22,layer)
            box(name+' window mullion',xx,front+.24,.12,.14,2,'#d4ceb6',2.2,layer)
            if langar:
                for yy in [2.5,3,3.5]:box(name+' ventilation louvre',xx,front+.25,ww,.16,.1,'#bfc8b0',yy,layer)
        for off in [-w/2+.3,w/2-.3]:box(name+' corner trim',x+off,front,.45,.35,h,'#ded4bb',0,layer)
    for off in [-d/2,d/2]:box(name+' eave fascia',x,z+off,w+.8,.45,.4,'#bba985',h,layer)
    if langar or 'EXHIBITION' in name:
        for j in range(max(2,min(10,int(w/12)))):
            xx=x-w*.45+j*w*.9/max(1,min(10,int(w/12))-1)
            box(name+' front canopy post',xx,front+.9,.35,.35,h,'#b6aa8d',0,layer)
        box(name+' sheltered veranda',x,front+.65,w,1.7,.2,'#d8c8a4',h-.2,layer)

def parked_vehicle(f,px,pz,bus=False,bike=False,variant=0):
    vehicle_start=len(objects)
    layer='parking';name=f['id']+' representative '+('bus' if bus else 'two-wheeler' if bike else 'car')
    if bike:
        for zz in [-1.1,1.1]:add(name+' wheel','ellipsoid',px,.35,pz+zz,.7,1,.9,'#3c4947',layer)
        box(name+' frame',px,pz,.7,1.5,.6,'#7d9390',.7,layer);box(name+' seat',px,pz,.8,1,.2,'#3e4b47',1.3,layer)
        box(name+' handlebar',px,pz-.9,1.3,.15,.15,'#c2c8ba',1.5,layer);return
    vw,vd,vh=(6.8,17,4) if bus else (4.8,9.5,1.9)
    colors=['#e5e7df','#b9c6c6','#9caa9f','#c6bda8','#577377','#d3cec1']
    color=colors[variant%len(colors)]
    box(name+' lower body',px,pz,vw,vd,vh,color,.8,layer)
    box(name+' cabin',px,pz-.3,vw*.88,vd*.55,1.7,color,vh+.55,layer)
    for side in [-1,1]:
        box(name+' side glazing',px+side*vw*.448,pz-.3,.1,vd*.5,1.05,'#385d65',vh+.95,layer)
        for zz in [-vd*.31,vd*.31]:add(name+' tyre','ellipsoid',px+side*vw*.46,.35,pz+zz,.8,1.7,1.8,'#344543',layer)
        box(name+' headlight',px+side*vw*.32,pz-vd/2-.04,.65,.12,.35,'#f0dfb2',1.55,layer)
        box(name+' tail light',px+side*vw*.32,pz+vd/2+.04,.45,.12,.27,'#af6257',1.5,layer)
    for side in [-1,1]:box(name+' windscreen',px,pz-.3+side*vd*.277,vw*.77,.12,1.05,'#3e6771',vh+.95,layer)
    box(name+' registration plaque',px,pz-vd/2-.1,.9,.12,.28,'#e1dfc9',1.15,layer)
    if bus:
        for zz in range(-6,7,3):
            for side in [-1,1]:box(name+' window separator',px+side*vw*.46,pz+zz,.14,.17,1.7,color,vh+.55,layer)
        box(name+' roof vent',px,pz,2,3,.35,'#b2bbae',vh+2.25,layer)
    # Parking bay outlines are presentation details; not a capacity statement.
    bw,bd=vw+3,vd+4
    for side in [-1,1]:box(name+' bay side',px+side*bw/2,pz,.16,bd,.04,'#e7e2cb',.42,layer)
    box(name+' bay end',px,pz+bd/2,bw,.16,.04,'#e7e2cb',.42,layer)
    for o in objects[vehicle_start:]:o['parkingVehicleOrigin']=[px,pz]

def enhance_pandal(f,x,z,w,d):
    bw=w
    # Cross-bracing, interior ridge beams, paired trusses and guy lines.
    for n in range(1):
        xx=x-w/2+bw*(n+.5)
        for zz in [z-d*.32,z,z+d*.32]:
            pts=[]
            for j in range(33):
                q=j/32-.5;pts.append([xx+q*bw,19+15*math.sqrt(max(0,1-(2*q)**2)),zz])
            for a,b in zip(pts,pts[1:]):beam3('Illustrative curved tent truss',a,b,.38,'#c0b99f')
            beam3('Tent tie beam',[xx-bw/2,19,zz],[xx+bw/2,19,zz],.35,'#b9b39e')
        for zz in [z-d/2,z+d/2]:
            beam3('Tent stabilising guy line',[xx-bw/2,19,zz],[xx-bw/2,0,zz+(-3 if zz<z else 3)],.1,'#a2a38e')
        box('Canopy ridge seam',xx,z,.3,d,.18,'#d4c4a2',35,'pandal')
    # Carpet aisle connects the illustrated stage to the front section.
    box('Stage approach carpet aisle',x+w*.12,z,w*.68,8,.2,'#8e4e53',1.2,'pandal')
    for off in [-d*.43,d*.43]:
        box('Tent interior circulation carpet',x,z+off,w*.91,3,.18,'#d0b98b',1.15,'pandal')
