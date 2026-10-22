import math

# Unit-radius roof meridian: eave to crown. Height/radius remain inferred.
DOME=[(0,0),(1,0),(1,.035),(.994,.10),(.975,.20),(.94,.31),(.89,.42),(.82,.53),(.73,.64),(.62,.74),(.49,.83),(.34,.90),(.19,.96),(0,1)]

def refine_lotus(objects,colors):
    objects[:]=[o for o in objects if not o['name'].startswith(('Lotus ','Meditation pavilion','Pavilion '))]
    colors.update(lotusIvory='#eeeae2',lotusPink='#cda8ab',lotusGlass='#c7d9d9',lotusFinial='#f8ad36')
    def add(name,p,s,mat='lotusIvory',shape='box',rot=0):
        objects.append(dict(name='Pavilion '+name,p=[28+p[0],p[1],-45+p[2]],s=s,mat=mat,shape=shape,group='campus',rot=rot))
    def cyl(name,r,y,h,mat='lotusIvory'):add(name,[0,y,0],[r,h,r],mat,'cylinder')
    for r,y,h in [(11.2,.32,.3),(10.5,.56,.18),(9.8,.76,.18),(9.1,.95,.2)]:cyl('concentric terrace tread • satellite reference',r,y,h)
    # Circular pedestal and flared lotus cup; no invented internal floor plan.
    cyl('lower pedestal',5.6,1.6,1.15)
    for i in range(18):
        t=i/17;cyl('flared lotus cup band',5.6+2.4*t,2.14+1.64*t,.11,'lotusPink' if i<3 else 'lotusIvory')
    # Small rim petals replace the former tall ground-level spikes.
    for i in range(40):
        a=math.tau*i/40
        add('small pointed rim petal • count inferred',[7.82*math.cos(a),4.0,7.82*math.sin(a)],[1.19,.62,.18],'lotusPink','petal',math.pi/2-a)
        add('ivory inner petal face',[7.69*math.cos(a),4.12,7.69*math.sin(a)],[.92,.42,.12],'lotusIvory','petal',math.pi/2-a)
    cyl('white cylindrical drum',5.87,5.5,3)
    for i in range(20):
        a=math.tau*i/20
        mat='lotusGlass' if i%4!=0 else 'lotusPink'
        add('drum panel • visible rhythm; rear layout inferred',[5.9*math.cos(a),5.62,5.9*math.sin(a)],[1.25,2.35,.09],mat,rot=math.pi/2-a)
        add('white drum mullion',[5.98*math.cos(a),5.62,5.98*math.sin(a)],[.11,2.45,.13],rot=math.pi/2-a)
        if i%5==0:add('small dark upper drum opening',[6.01*math.cos(a),6.2,6.01*math.sin(a)],[.35,.42,.1],'dark',rot=math.pi/2-a)
    cyl('projecting white eave fascia',6.65,7.14,.25)
    cyl('eave lower shadow reveal',6.42,6.96,.1,'stone')
    add('curved dome • video silhouette',[0,7.25,0],[6.35,5,6.35],'lotusIvory','lotusDome')
    # Low pink decoration is visible at the dome springing in the ground photo.
    for i in range(48):
        a=math.tau*i/48
        add('dome springing small pink motif',[6.25*math.cos(a),7.38,6.25*math.sin(a)],[.6,.23,.08],'lotusPink','petal',math.pi/2-a)
    for r,y,h in [(.65,12.27,.2),(.47,12.48,.22),(.38,12.68,.17)]:cyl('finial pedestal collar',r,y,h,'lotusPink')
    add('amber illuminated finial',[0,13.19,0],[.26,.48,.26],'lotusFinial','sphereSmooth')
    # Short terrace joints and planting beds read from the overhead source.
    for i in range(32):
        a=math.tau*i/32
        add('terrace radial paving joint',[10.55*math.cos(a),.73,10.55*math.sin(a)],[.018,.015,1.1],'stone',rot=math.pi/2-a)
    return objects,colors
