def four_floor_office(f,x,z,w,d):
    """User-requested four-floor appearance within the source S/D office block."""
    name='S/D OFFICE';layer='services';fh=3.4;plinth=.55;height=4*fh
    def ob(part,xx,zz,ww,dd,hh,color,y=0,roof=False):
        box(name+' / '+part,xx,zz,ww,dd,hh,color,y,layer)
        if roof:objects[-1]['part']='roof'
    ob('stone foundation',x,z,w,d,plinth,'#a18d74')
    ob('four-floor chocolate facade',x,z,w*.985,d*.985,height,'#593b2e',plinth)
    for floor in range(4):
        yy=plinth+floor*fh
        ob('floor '+str(floor+1)+' horizontal band',x,z,w,d,.22,'#a2805d',yy)
        for side in [-1,1]:
            count=max(4,int(w/7))
            for j in range(count):
                xx=x-w*.46+(j+.5)*w*.92/count;ww=w*.92/count-1.25;zz=z+side*d*.497
                ob('floor '+str(floor+1)+' window frame',xx,zz,ww+.35,.16,2.4,'#bda27b',yy+.6)
                ob('floor '+str(floor+1)+' glazing',xx,zz+side*.1,ww,.12,2.08,'#6f898a',yy+.76)
                ob('window mullion',xx,zz+side*.19,.13,.12,2.1,'#d2c4aa',yy+.75)
            count=max(4,int(d/7))
            for j in range(count):
                zz=z-d*.43+(j+.5)*d*.86/count;dd=d*.86/count-1.25;xx=x+side*w*.497
                ob('side floor '+str(floor+1)+' frame',xx,zz,.16,dd+.35,2.4,'#bda27b',yy+.6)
                ob('side floor '+str(floor+1)+' glass',xx+side*.1,zz,.12,dd,2.08,'#6f898a',yy+.76)
    top=plinth+height
    ob('flat chocolate roof',x,z,w*1.005,d*1.005,.4,'#432e26',top,True)
    for side in [-1,1]:
        ob('side parapet',x+side*w*.491,z,.65,d,.85,'#684836',top+.4,True)
        ob('front parapet',x,z+side*d*.491,w,.65,.85,'#684836',top+.4,True)
        ob('corner facade pier',x+side*w*.482,z,w*.018,d*.99,height,'#74543c',plinth)
    front=z+d*.498
    ob('recessed main entrance',x,front,w*.1,.35,3,'#302c29',plinth)
    ob('glass entrance doors',x,front+.2,w*.07,.12,2.65,'#8fa4a0',plinth+.1)
    ob('bronze entrance canopy',x,front-1.3,w*.17,4,.3,'#9c7954',plinth+3.1)
    for l in labels:
        if l.get('featureId')==f['id']:l['p'][1]=24
