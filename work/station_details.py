def detailed_station(f,x,z,w,d):
    """Dark-brown station architecture inside the source station block; design illustrative."""
    layer='context';name='BHODWAL MAJRI RAILWAY STATION'
    def sb(part,xx,zz,ww,dd,hh,color,y=0,roof=False):
        box(name+' / '+part,xx,zz,ww,dd,hh,color,y,layer)
        if roof:objects[-1]['part']='roof'
    sb('station forecourt',x,z,w,d,.3,'#b4ad94')
    bw=w*.74;bd=d*.83
    sb('stone plinth',x-w*.07,z,bw+1,bd+1,.65,'#9a876a',.3)
    sb('dark brown facade',x-w*.07,z,bw,bd,6.2,'#513a2b',.95)
    add(name+' / dark brown pitched roof','roof',x-w*.07,7.15,z,bw+2,3.5,bd+2,'#342b24',layer);objects[-1]['part']='roof'
    for side in [-1,1]:
        side_x=x-w*.07+side*bw/2
        sb('cream eave fascia',side_x,z,.4,bd+2,.3,'#cfbd96',7.15)
        for j in range(15):
            zz=z-bd*.45+j*bd*.9/14
            if abs(zz-z)<12:continue
            sb('window stone surround',side_x+side*.12,zz,.28,5.2,2.8,'#beaa82',2.5)
            sb('blue grey window glazing',side_x+side*.3,zz,.1,4.5,2.2,'#587c80',2.8)
            sb('window central mullion',side_x+side*.4,zz,.15,.18,2.3,'#dbd2b9',2.75)
        sb('central entrance frame',side_x+side*.2,z,.5,12,5.1,'#ac916a',.95)
        sb('central entrance glass',side_x+side*.49,z,.16,9.5,4.3,'#354b4b',1.05)
        sb('entrance door mullion',side_x+side*.61,z,.15,.25,4.3,'#ded3b8',1.05)
    # Covered concourse faces the existing rail corridor, without moving the track.
    px=x+w*.435
    sb('platform edge within station block',px,z,w*.12,d,.5,'#c0b99e',.3)
    sb('platform safety stripe',px+w*.055,z,.3,d,.04,'#d8bd6a',.82)
    for j in range(13):
        zz=z-d*.45+j*d*.9/12
        sb('platform canopy column',x+w*.37,zz,.42,.42,5.5,'#c1b69a',.8)
        sb('canopy bracket',x+w*.33,zz,w*.18,.35,.3,'#947f5c',5.95)
    sb('platform canopy',x+w*.31,z,w*.3,d*.98,.35,'#655440',6.3,True)
    for j in range(7):
        zz=z-d*.39+j*d*.78/6
        sb('platform bench seat',x+w*.38,zz,1.1,5,.35,'#7c6a50',1.4)
        for off in [-1.8,1.8]:sb('bench support',x+w*.38,zz+off,.55,.4,.5,'#666e61',.85)
    # Both end boards follow the familiar station-nameboard silhouette; text remains accessible in labels.
    for side in [-1,1]:
        zz=z+side*d*.39
        for off in [-4,4]:sb('nameboard post',x+w*.41,zz+off,.35,.35,4.7,'#726b52',.8)
        sb('yellow station nameboard',x+w*.41,zz,.35,10,2.2,'#c5a13f',3.6)
    sb('entrance nameboard fascia',x+w*.324,z,.45,22,2.1,'#c4a260',5.25)
    for l in labels:
        if l.get('featureId')==f['id']:l['text']='BHODWAL MAJRI / RAILWAY STATION';l['p']=[x,17,z];l['layer']='context'
