"""Gate 3 permanent entrance, based on the supplied daytime photograph."""
def gate3_photo(f,x,z,w,d):
    from PIL import Image,ImageDraw,ImageFont
    start=len(objects);name=f['name'];angle=-math.pi/2
    def b(part,xx,zz,ww,dd,hh,col,y=0,leaf=None):
        box(name+' / PHOTO3 '+part,xx,zz,ww,dd,hh,col,y,'gates')
        if leaf:objects[-1]['photoLeafLocal']=leaf
    def shape(part,kind,xx,yy,zz,ww,hh,dd,col):add(name+' / PHOTO3 '+part,kind,xx,yy,zz,ww,hh,dd,col,'gates')
    cream='#dbd5c7';sand='#c4b59a';dark='#30302e';wood='#8b704e'
    for side in [-1,1]:
        xx=side*25
        b('cream outer pillar',xx,0,3.1,3.9,24,cream)
        b('pillar cap',xx,0,4.5,5,.65,dark,24)
        b('boundary return',side*28,.35,3,1.3,18.825,'#a58b65')
        for yy in [3,6,9,12,15,18,21]:b('pillar stone joint',xx,-2,3.05,.045,.055,'#b2a994',yy)
    b('long dark overhead beam',0,0,53,1.6,1.15,dark,22.8)
    # The letters are actual slim 3D strokes, visible from orbit and exported GLB.
    title='SANT NIRANKARI ADHYATMIK STHAL'
    font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',20)
    bb=font.getbbox(title);im=Image.new('L',(bb[2]-bb[0]+2,bb[3]-bb[1]+2));ImageDraw.Draw(im).text((1-bb[0],1-bb[1]),title,font=font,fill=255)
    unit=49/im.width
    for yy in range(im.height):
        row=[im.getpixel((xx,yy))>100 for xx in range(im.width)]+[False];begin=None
        for xx,on in enumerate(row):
            if on and begin is None:begin=xx
            if not on and begin is not None:
                b('raised name lettering',24.5-(begin+xx)*unit/2,-.3,(xx-begin)*unit,.25,unit,'#e1ddd2',24.1+(im.height-yy-1)*unit);begin=None
    # Tall central cream guard cabin, taupe inset and blue/gold emblem.
    b('guard cabin rear',0,3.3,8.8,.6,21,cream)
    for side in [-1,1]:b('guard cabin side',side*4.1,0,.6,7.2,21,cream)
    b('guard cabin front',0,-3.3,8.8,.6,21,cream)
    b('cabin inset taupe panel',.5,-3.65,4.1,.14,17,'#b4a38a',1)
    b('guard cabin roof',0,0,10.2,8.5,.8,'#b9a98d',21)
    b('glazed lower cabin door',.5,-3.8,3.2,.12,5.7,'#62716b',.3)
    for xx in [-1.18,2.18]:b('door dark stile',xx,-3.9,.15,.1,5.9,dark,.25)
    b('side inspection window',-4.45,-.7,.12,2,4,'#59564e',13)
    shape('round emblem gold rim','ellipsoid',.5,11.9,-3.85,3.4,3.4,.24,'#beaa6b')
    shape('round emblem blue face','ellipsoid',.5,11.9,-4.01,2.95,2.95,.13,'#255475')
    shape('emblem central motif','ellipsoid',.5,11.9,-4.09,1.2,1.2,.08,'#e4dfcc')
    # Two wood-tone vehicle portals with separate hinge pivots.
    inside=4.7;outside=23.35;half=(outside-inside)/2
    for side in [-1,1]:
        lo,hi=(inside,outside) if side>0 else (-outside,-inside)
        for i in [0,1]:
            mid=lo+half*(i+.5);pivot=lo if i==0 else hi;leaf={'pivot':[pivot,0,0],'turn':math.radians(82)*(-1 if i==0 else 1)}
            b('wood-tone gate leaf',mid,0,half-.1,.38,10.4,wood,.35,leaf)
            for j in range(1,12):b('wood vertical slat',mid-half/2+half*j/12,-.24,.055,.08,10.15,'#66573f',.5,leaf)
            for y in [.4,10.65]:b('gate dark perimeter',mid,-.1,half,.5,.14,dark,y,leaf)
            b('gate recessed handle',mid,-.32,1.1,.1,.18,dark,4.4,leaf)
    for side in [-1,1]:
        for j in range(5):
            xx=side*(5.8+j*1.5);zz=-3.6
            shape('white plant pot','cylinder',xx,.08,zz,.95,1.1,.95,'#ded9c8')
            shape('potted shrub','ellipsoid',xx,1.9,zz,1.25,1.6,1.2,'#416548')
    for xx in [-24,-9,9,24]:
        b('beam floodlight',xx,-1.05,1.1,.5,.65,dark,23.7)
        b('floodlight face',xx,-1.34,1,.06,.5,'#dedecb',23.8)
    ca=math.cos(angle);sa=math.sin(angle)
    for o in objects[start:]:
        ox,oy,oz=o['p'];o['p']=[x+ox*ca+oz*sa,oy,z-ox*sa+oz*ca];o['rotY']=angle;o['photoGate']=True;o['photoGate3']=True
        leaf=o.pop('photoLeafLocal',None)
        if leaf:
            px,py,pz=leaf['pivot'];o['photoLeaf']={'pivot':[x+px*ca+pz*sa,py,z-px*sa+pz*ca],'turn':leaf['turn']}
        o['status']='Gate 3 based on supplied daytime Amar Singh photo; dimensions illustrative'
    f['gate_style']='Photo reference: cream pillars, dark overhead beam, raised SANT NIRANKARI ADHYATMIK STHAL lettering, central guard cabin, wood-tone gates'
    f['representation']='Permanent photo-informed Gate 3, aligned to highway boundary'
    for label in labels:
        if label.get('featureId')==f['id']:label['p']=[x,29,z];label['layer']='gates'
