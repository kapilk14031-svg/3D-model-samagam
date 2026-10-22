"""Gate 1/2 reference: cream piers, brown ribbed steel leaves, central guard room."""
def photo_gate(f,x,z,w,d):
    start=len(objects);angle=-math.pi/2;layer='gates';name=f['name'];room=11.4;outer=27.5
    def gb(part,xx,zz,ww,dd,hh,col,y=0,leaf=None):
        box(name+' / PHOTO '+part,xx,zz,ww,dd,hh,col,y,layer)
        if leaf:objects[-1]['photoLeafLocal']=leaf
    def shape(part,kind,xx,yy,zz,ww,hh,dd,col):add(name+' / PHOTO '+part,kind,xx,yy,zz,ww,hh,dd,col,layer)
    cream='#d4c7ac';edge='#b7a88e';brown='#47372f';steel='#272b29'
    # Wide rectangular composition, without a ceremonial arch or finials.
    for side in [-1,1]:
        gb('outer cream pier',side*outer,0,2.8,3.7,13.7,cream)
        gb('pier top coping',side*outer,0,2.95,3.9,.3,'#c6b99d',13.7)
        gb('outer boundary return',side*(outer+3.2),.5,3.6,1.3,11.8,cream)
    gb('guard-room foundation',0,0,12.3,8.8,.55,'#ae9a7b')
    # Front face includes an actual door opening with a dark glazed door.
    gb('guard-room rear wall',0,3.65,room,.7,16.8,cream,.5)
    for side in [-1,1]:
        gb('guard-room side wall',side*5.35,0,.7,7.6,16.8,cream,.5)
        gb('guard-room front jamb',side*3.75,-3.65,3.9,.7,16.8,cream,.5)
    gb('door header',0,-3.65,3.6,.7,8,cream,9.3)
    gb('guard-room flat roof',0,0,12,8.3,.55,'#c1b598',17.3)
    gb('tall centre facade panel',0,2.8,10.8,1.4,7.3,'#ded3bb',17.7)
    gb('door dark frame',0,-4.03,3.7,.22,8.6,steel,.65)
    gb('brown lower entrance door',0,-4.17,3.15,.12,3.3,'#4f352c',.9)
    gb('upper entrance door window glass',0,-4.18,3.15,.12,4.25,'#9eafb0',4.25)
    for xx in [-1.65,1.65]:gb('door black stile',xx,-4.27,.13,.1,8.1,steel,.9)
    for yy in [4.1,8.5]:gb('door black cross rail',0,-4.28,3.4,.1,.15,steel,yy)
    gb('door handle',1.2,-4.38,.12,.12,.8,'#9c9e93',3.5)
    for i in range(3):gb('front step',0,-4.8-i*.65,4.1,.75,.22,'#b5a085',.1+(2-i)*.22)
    gb('burgundy entrance mat',0,-6.3,3.7,2.1,.07,'#723c40',.04)
    # Two vehicle portals, each with a pair of closed steel leaves.
    inner=room/2+.35;outside=outer-1.5;portal=outside-inner;lw=portal/2
    for side in [-1,1]:
        lo,hi=(inner,outside) if side>0 else (-outside,-inner)
        for half in [0,1]:
            mid=lo+lw*(half+.5);pivot=lo if half==0 else hi;turn=math.radians(82)*(-1 if half==0 else 1)
            leaf={'pivot':[pivot,0,0],'turn':turn}
            gb('ribbed dark-brown steel gate leaf',mid,0,lw-.12,.48,11.8,brown,.4,leaf)
            for j in range(1,10):gb('vertical steel panel seam',mid-lw/2+lw*j/10,-.3,.065,.08,11.45,'#382e29',.58,leaf)
            for yy in [.45,11.95]:gb('gate leaf perimeter frame',mid,-.05,lw,.65,.16,steel,yy,leaf)
            for xx in [mid-lw/2+.08,mid+lw/2-.08]:gb('gate leaf edge frame',xx,-.05,.16,.65,11.7,steel,.45,leaf)
            gb('horizontal lock strap',mid,-.42,lw*.78,.14,.14,'#222625',4.6,leaf)
            gb('drop bolt',mid+(lw/2-.35)*(1 if half==0 else -1),-.49,.14,.14,1.8,steel,.4,leaf)
            for yy in [1.2,6.1,10.9]:gb('visible hinge',pivot,-.06,.3,.8,.48,'#202625',yy,leaf)
    # Photo-like potted palms and wall-mounted floodlights.
    for side in [-1,1]:
        xx=side*4.4;zz=-5.35
        shape('palm planter','cylinder',xx,.15,zz,1.65,1.7,1.65,'#c9bca2')
        shape('planter rim','cylinder',xx,1.63,zz,1.85,.18,1.85,'#e0d6bd')
        gb('palm stem',xx,zz,.14,.14,3.6,'#756347',1)
        for j in range(9):
            a=j*math.tau/9;verts=[]
            for r,yy,ww in [(0,0,.04),(.75,.65,.16),(1.5,.42,.22),(2.05,-.35,.025)]:
                for sidewidth in [-ww,ww]:verts.append([math.cos(a)*r-math.sin(a)*sidewidth,yy,math.sin(a)*r+math.cos(a)*sidewidth])
            key='photoPalmLeaf'+str(len(extra_shapes));extra_shapes[key]=[verts,[[i,i+1,i+3,i+2] for i in [0,2,4]]]
            shape('potted palm foliage',key,xx,4.2,zz,1,1,1,'#456d4e')
    for xx,yy in [(-outer,14.4),(0,25.1),(outer,14.4)]:
        gb('floodlight bracket',xx,-.8,.22,2,.25,'#2b302e',yy)
        gb('floodlight black housing',xx,-1.7,2.3,.5,.85,'#303c3c',yy+.3)
        gb('floodlight diffuser',xx,-2.0,2,.08,.65,'#fff5d6',yy+.4)
    ca=math.cos(angle);sa=math.sin(angle)
    for o in objects[start:]:
        ox,oy,oz=o['p'];o['p']=[x+ox*ca+oz*sa,oy,z-ox*sa+oz*ca];o['rotY']=angle;o['photoGate']=True
        leaf=o.pop('photoLeafLocal',None)
        if leaf:
            px,py,pz=leaf['pivot'];o['photoLeaf']={'pivot':[x+px*ca+pz*sa,py,z-px*sa+pz*ca],'turn':leaf['turn']}
        o['status']='Gate 1/2 appearance follows supplied Amar Singh photograph; PDF position retained; dimensions illustrative'
    f['gate_style']='Photo reference: cream pillars, brown metal leaves, central guard room, potted palms'
    f['representation']='Photo-informed gate 1/2 with central guard room and two steel vehicle portals'
    for label in labels:
        if label.get('featureId')==f['id']:label['p']=[x,28,z];label['layer']='gates'
