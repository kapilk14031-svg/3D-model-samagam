def indian_oil_pump(f,x,z,w,d):
    """IndianOil-themed treatment requested by the user; not a verified operator record."""
    layer='services';name='IndianOil / PETROL PUMP'
    def pb(part,xx,zz,ww,dd,hh,color,y=0,roof=False):
        box(name+' / '+part,xx,zz,ww,dd,hh,color,y,layer)
        if roof:objects[-1]['part']='roof'
    pb('forecourt',x,z,w,d,.22,'#b5b9ae')
    pb('white service kiosk',x-w*.32,z,w*.28,d*.8,4.6,'#f2eee3',.22)
    pb('kiosk orange fascia',x-w*.32,z,w*.29,d*.81,.65,'#e8751b',4.3)
    pb('kiosk entrance glass',x-w*.175,z,.12,d*.25,2.7,'#587d85',.55)
    for off in [-.24,.24]:pb('kiosk windows',x-w*.175,z+d*off,.12,d*.16,1.7,'#6c9097',1.8)
    cx=x+w*.15;cw=w*.56;cd=d*.87
    for sx in [-1,1]:
        for sz in [-1,1]:pb('white canopy column',cx+sx*cw*.43,z+sz*cd*.43,.65,.65,6.4,'#eeece3',0)
    pb('white canopy soffit',cx,z,cw,cd,.32,'#f4f0e7',6.1,True)
    pb('orange canopy fascia',cx,z,cw,cd,.75,'#e8751b',6.42,True)
    pb('navy fascia line',cx,z,cw+.1,cd+.1,.14,'#243e71',6.42,True)
    for off in [-.22,.22]:
        zz=z+d*off
        pb('pump island',cx,zz,4.5,5.5,.25,'#dfd8c0',.22)
        pb('orange dispenser base',cx,zz,2.2,1.5,.7,'#e8751b',.5)
        pb('white fuel dispenser',cx,zz,2,1.45,1.6,'#efece1',1.2)
        pb('display panel',cx+1.03,zz,.08,.95,.7,'#183c4c',1.8)
        for side in [-1,1]:
            pts=[[cx+side*1.05,2.55,zz],[cx+side*1.55,1.25,zz],[cx+side*1.35,.85,zz]]
            for a,b in zip(pts,pts[1:]):beam3(name+' / fuel hose',a,b,.1,'#303c38',layer)
    sx=x+w*.41;sz=z+d*.35
    pb('white brand pylon',sx,sz,2.5,1.2,8.3,'#eee9dc',.25)
    pb('orange brand panel',sx,sz,3.6,1.4,3.5,'#e8751b',5.2)
    add(name+' / orange circular badge','ellipsoid',sx,7.9,sz,4,3.8,.6,'#ed7c1e',layer)
    pb('navy wordmark stripe',sx,sz+.36,3.8,.14,.8,'#213f75',9.2)
    for l in labels:
        if l.get('featureId')==f['id']:l['text']='IndianOil / PETROL PUMP';l['p']=[x,19,z]
    f['display_brand']='IndianOil — user-requested appearance, operator not verified'
