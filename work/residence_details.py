"""Illustrative modern facade; source supplies a relative block, not an architectural plan."""
def modern_residence(f,x,z,w,d):
    layer='services';name='SPECIAL RESIDENCE'
    def rb(part,xx,zz,ww,dd,hh,color,y=0,roof=False):
        box(name+' / '+part,xx,zz,ww,dd,hh,color,y,layer)
        if roof:objects[-1]['part']='roof'
    rb('recessed stone plinth',x,z,w,d,.65,'#a9aaa0')
    rb('modern ivory building',x,z,w*.98,d*.98,7.55,'#e8e5db',.65)
    for yy in [3.9,7.8]:rb('horizontal limestone floor band',x,z,w,d,.3,'#f5f0e3',yy)
    # Recessed glazing on all four elevations, without implying an approved room plan.
    for floor in [0,1]:
        y=1.05+floor*3.85
        count=max(3,int(w/7))
        for j in range(count):
            xx=x-w*.44+(j+.5)*w*.88/count;ww=w*.88/count-1.0
            for side in [-1,1]:
                zz=z+side*d*.492
                rb('recessed blue glass window',xx,zz,ww,.18,2.45,'#4b7581',y)
                rb('slender aluminium mullion',xx,zz+side*.12,.12,.18,2.5,'#b7c4c0',y)
                rb('window sill',xx,zz+side*.17,ww+.3,.35,.14,'#d3d4c9',y-.08)
        count=max(3,int(d/8))
        for j in range(count):
            zz=z-d*.43+(j+.5)*d*.86/count;dd=d*.86/count-1.1
            for side in [-1,1]:
                xx=x+side*w*.492
                rb('side curtain-wall glass',xx,zz,.18,dd,2.45,'#527d89',y)
                rb('side window mullion',xx+side*.12,zz,.18,.12,2.5,'#bcc8c2',y)
    # Shaded entrance stays within the block rather than taking the access road.
    front=z+d*.493
    rb('entry stone portal',x,front,w*.18,.8,6.8,'#3e565a',.65)
    rb('double height entrance glass',x,front+.46,w*.13,.16,5.9,'#6a959f',.8)
    for dx in [-w*.032,w*.032]:rb('entrance door stile',x+dx,front+.6,.18,.15,3.2,'#d7dfd6',.8)
    rb('floating entrance canopy',x,front-2.1,w*.28,5.2,.35,'#d8d3c4',4.1)
    rb('entrance soffit light',x,front-.2,w*.22,.18,.09,'#e8d2a2',4.02)
    # Roof slab, low parapets and glazed terrace rails.
    rb('flat roof slab',x,z,w*1.01,d*1.01,.45,'#d6d5c8',8.1,True)
    rb('terrace surface',x,z,w*.92,d*.92,.1,'#bfc3b0',8.56,True)
    for side in [-1,1]:
        rb('terrace parapet',x+side*w*.49,z,.65,d,1,'#eeeadc',8.55,True)
        rb('glass terrace railing',x,z+side*d*.49,w*.97,.25,.85,'#9eb8b6',8.68,True)
        rb('terrace top rail',x,z+side*d*.49,w,.3,.13,'#c7cfc6',9.5,True)
    # A smaller terrace lounge/pergola breaks up the original blank pitched roof.
    px=x-w*.24;pz=z-d*.2;pw=w*.32;pd=d*.3
    for sx in [-1,1]:
        for sz in [-1,1]:rb('terrace pergola post',px+sx*pw/2,pz+sz*pd/2,.4,.4,2.5,'#777f73',8.65,True)
    for j in range(9):rb('slatted terrace pergola',px-pw/2+j*pw/8,pz,.8,pd+1,.25,'#ad9d7c',11.05,True)
    rb('roof plant screen',x+w*.25,z-d*.26,w*.22,d*.15,1.8,'#8f9c90',8.65,True)
    for side in [-1,1]:
        for j in range(5):
            px=x-w*.35+j*w*.175;pz=z+side*d*.37
            rb('terrace planter',px,pz,4,2.2,.7,'#a09c88',8.65,True)
            add(name+' / terrace planting','ellipsoid',px,9.3,pz,4.4,1.2,2.6,'#628266',layer);objects[-1]['part']='roof'
    for j in range(5):
        px=x-w*.35+j*w*.175
        rb('vertical facade sunshade',px,front+.22,.38,.7,7.5,'#c5b79b',.7)
