"""Readable highway portals, open transverse road and continuous elevated NH44 approaches."""
underpass_nav=[]
def corrected_underpass(f,x,z,w,d):
    angle=.264;ca=math.cos(angle);sa=math.sin(angle)
    def point(xx,yy,zz):return[x+xx*ca+zz*sa,yy,z-xx*sa+zz*ca]
    def ub(name,xx,zz,ww,dd,hh,color,y=0):
        px,py,pz=point(xx,y,zz);box(f['id']+' UNDERPASS / '+name,px,pz,ww,dd,hh,color,py,'bridges');objects[-1]['rotY']=angle
    ub('open lower road',0,0,100,18,.15,'#303b3d',.65)
    for side in [-1,1]:
        ub('retaining side wall',0,side*10.5,50,1.5,8.3,'#aaa996',.8)
        ub('pedestrian kerb',0,side*8.3,94,1,.3,'#c6bda6',.8)
        ub('roof edge beam',0,side*11,50,1,1.8,'#bdb9a8',9.1)
    ub('highway bridge slab',0,0,48,24,1.8,'#888e87',9.1)
    for xx in [-24,24]:
        for zz in [-10.5,10.5]:ub('portal concrete column',xx,zz,1.8,2.1,8.3,'#a5a998',.8)
        for zz in [-10.5,10.5]:
            ub('hazard marker',xx,zz,1.9,.18,1.6,'#dbb64b',1)
    for xx in range(-44,45,10):ub('lower road centre dash',xx,0,4,.2,.04,'#e8d8aa',.82)
    underpass_nav.append(dict(id=f['id'],anchor=[x,0,z],angle=angle,half_width=9,road_half_length=50,clear_height=8.3,highway_height=11,approach_run=75))

def raise_highway_at_underpasses():
    for o in objects:
        if o['featureId']!='H01':continue
        def lift(px,pz):
            best=0
            for u in underpass_nav:
                dx=px-u['anchor'][0];dz=pz-u['anchor'][2];along=dx*math.sin(u['angle'])+dz*math.cos(u['angle'])
                best=max(best,9.9*max(0,min(1,(90-abs(along))/75)))
            return best
        if o['kind'] in extra_shapes:
            vv,ff=extra_shapes[o['kind']]
            # Road ribbons use absolute-world vertices.
            extra_shapes[o['kind']]=[[[v[0],v[1]+lift(v[0],v[2]),v[2]] for v in vv],ff]
        else:o['p'][1]+=lift(o['p'][0],o['p'][2])
