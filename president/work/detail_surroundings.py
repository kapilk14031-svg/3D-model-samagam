import math

def detail(objects,colors):
    signs=[]
    def add(name,p,s,mat='stone',shape='box',group='campus',rot=0,tilt=0):
        objects.append(dict(name=name,p=p,s=s,mat=mat,shape=shape,group=group,rot=rot,tilt=tilt))
    def box(name,x,y,z,w,h,d,mat='stone',group='campus',rot=0):add(name,[x,y,z],[w,h,d],mat,group=group,rot=rot)
    def cyl(name,x,y,z,r,h,mat='stone',group='campus',tilt=0):add(name,[x,y,z],[r,h,r],mat,'cylinder',group,tilt=tilt)
    # The gate-to-residential sequence places the auditorium entry toward the
    # residential end of its frontage. Keep that inference explicit in metadata.
    for o in objects:
        x,y,z=o['p']
        if o['name'].startswith(('Garden bollard lamp','Garden lamp globe')):
            o['p'][0]=1.7 if x==-9 else 52.8 if x==55 else x
        if o['name'].startswith(('Landscape tree trunk','Landscape tree canopy')) and x==-5:o['p'][0]=2.5
        if o['name'].startswith(('Palm trunk','Palm frond')) and x<-6 and z>25:o['p'][0]-=8
        if -62<=x<=-18 and -45<=z<=24 and o['group'] in ['interior','seating','ceiling','shell']:
            o['p'][2]=-20-z;o['rot']=-o['rot'];o['tilt']=-o.get('tilt',0)
        elif o['name'].startswith(('External black entry step','Entrance stainless rail','Entrance handrail')):
            o['p'][2]=-20-z
        if o['name'].startswith('Side entrance metal jamb'):o['p'][2]=6.5 if o['p'][2]<8 else 10.5
        if o['name'].startswith('Open glazed door leaf'):o['p'][2]=6.6 if o['p'][2]<8 else 10.4
    box('Hall side doorway north infill',-19,5,5.25,.5,9,2.5,'white','shell')
    box('Hall side doorway south infill',-19,5,11.75,.5,9,2.5,'white','shell')
    # Replace the solid portico placeholder with columns and a real entrance void.
    objects[:]=[o for o in objects if not o['name'].startswith(('Central portico frame','South building ground floor','Upper gallery rail'))]
    colors.update({'pinkColumn':'#c5919b','fieldDry':'#a99473','fieldGreen':'#7c8860','fieldDark':'#766753','rail':'#635e56','roofMetal':'#a6b0ad','brick':'#a88e73'})
    box('Residential floor slab',0,.16,39,112,.32,17,'stone','shell')
    box('Residential back wall',0,2.3,47.5,112,4.6,.4,'white','shell')
    for x in [-31,31]:box('Residential frontage flanking entrance',x,2.3,30.5,50,4.6,.35,'white','shell')
    for x in [-56,56]:box('Residential side wall',x,2.3,39,.4,4.6,17,'white','shell')
    box('Residential portico roof • photo 21',0,9,25.7,15,.55,11,'white','roof')
    for x in [-6.5,6.5]:cyl('Pink circular portico column • photo 21',x,4.5,21.4,.38,9,'pinkColumn')
    for y in [9.6,10,10.4]:
        box('Portico terrace horizontal rail',0,y,21.6,14,.06,.06,'metal')
        for x in [-7,7]:box('Portico terrace side rail',x,y,26,.06,.06,9,'metal')
    for x in [-6.5,6.5]:box('Portico railing upright',x,10,21.6,.07,1.2,.07,'metal')
    for x in [-30.5,30.5]:box('Upper gallery side parapet • clear central name board',x,5.3,29.8,51,.8,.25,'stone')
    box('Residential lobby counter • visible behind doorway',0,.95,35,4,1.3,.8,'white')
    box('Residential counter green panel',0,.85,34.55,3.4,.8,.06,'skirt')
    for x in [-4.5,4.5]:
        cyl('Residential entry planter',x,.65,29,.45,1.2,'stone')
        add('Entry planter shrub',[x,1.6,29],[.65,.85,.65],'tree','sphereSmooth')
    for x in [-10,10]:
        box('Balcony AC condenser • photo reference',x,6.7,29.6,1.4,1,.65,'white')
        cyl('Condenser fan grille',x,6.7,29.2,.38,.06,'metal',tilt=math.pi/2)
        for y in [5.1,5.45,5.8]:box('Residential balcony metal rail',x,y,29,6,.05,.06,'metal')
    for x in range(-52,57,8):
        for y in [2,6.7]:
            for dx in [-1.6,1.6]:box('Residential window jamb',x+2+dx,y,30.15,.08,2.2,.1,'dark')
            box('Residential window sill',x+2,y-1.1,30.1,3.4,.1,.16,'stone')
    for x in [-15,15]:
        for z in [22,27]:box('Residential clipped hedge',x,1, z,7,1.5,1,'tree')
    # Classroom entry below the hall arcade; its exact bay is approximate.
    box('Classroom recessed entry • photo 13',-17.9,.65,-34,.15,1.8,4.2,'glass','shell')
    box('Classroom apron',-16.2,.06,-34,3.5,.08,4.5,'stone')
    for z in [-36,-32]:
        for x in [-17.5,-16]:cyl('Classroom entrance railing',x,.75,z,.035,1.2,'metal')
    # Forecourt joints, drainage edge, parapet caps and porch floodlights.
    for z in range(-56,27,6):box('Forecourt slab expansion joint',-9,.31,z,18,.012,.035,'dark')
    for x in [-17.3,-.8]:box('Forecourt drainage strip',x,.32,-14,.18,.04,84,'dark')
    for z in range(-36,24,8):
        box('Hall pink parapet cap',-18.4,8.6,z,1.1,.16,7.8,'pink')
        box('Hall facade floodlight bracket',-17.7,7.4,z,.5,.06,.06,'metal')
        box('Hall facade floodlight',-17.4,7.45,z,.15,.25,.36,'light')
    for x in [-61,61]:
        for z in range(-40,61,10):box('Compound wall pilaster',x,1.15,z,.9,2.3,.9,'stone')
        box('Compound wall coping',x,2.1,8,.75,.16,105,'white')
    # Signs are placed on facades, not camera-facing labels. Text follows photos.
    def sign(key,lines,p,size,rot,source,bg='#eee8d9',fg='#343544',group='campus'):
        colors[key]='#ffffff';signs.append(dict(key=key,lines=lines,p=p,size=size,rot=rot,source=source,bg=bg,fg=fg,placement='Relative facade position observed; metric coordinates estimated'))
        add('Observed sign: '+' / '.join(lines),p,[size[0],size[1],1],key,'sign',group,rot)
    sign('sign-gate',['ACADEMY FOR HOLISTIC EXCELLENCE','ज्ञान मानसरोवर'],[-13,5.55,-61.82],[16,1.5],math.pi,'Photo 6; video 3 opening gate','#d2b26f','#283650')
    sign('sign-residential',['DADI','PRAKASHMANI','Residential Complex'],[0,4.65,30.12],[9,2.1],math.pi,'Photo 21 / 26; video 3 ~97s','#735449','#f3dfad')
    box('Portico top name-board backing',0,10.45,20.3,16.5,2.5,.25,'stone')
    sign('sign-main-hindi',['प्रजापिता ब्रह्माकुमारी','ईश्वरीय विश्व विद्यालय','मुख्यालय माउण्ट आबू (राजस्थान)','ज्ञान मानसरोवर (पानीपत)'],[0,10.45,20.12],[14,2.3],math.pi,'Photo 21 / 26, portico top board','#ece5d2','#293d6e')
    sign('sign-pure',['पवित्र','बनो'],[7.9,10.45,20.12],[1.1,2],math.pi,'Photo 21, viewer-left side of portico board','#ece5d2','#293d6e')
    sign('sign-yogi',['योगी','बनो'],[-7.9,10.45,20.12],[1.1,2],math.pi,'Photo 21, viewer-right side of portico board','#ece5d2','#293d6e')
    sign('sign-auditorium',['Dadi','Chandermani','Universal','Peace','Auditorium'],[-17.77,3.4,15.5],[3.9,2.5],math.pi/2,'Photo 65; video 8 first frame','#41362f','#eee2bb','shell')
    sign('sign-classroom',['CLASS ROOM'],[-17.7,1.8,-34],[4.1,.5],math.pi/2,'Photo 13; photo 19 classroom near gate end','#e5dfcc','#622c33','shell')
    sign('sign-literature',['LITERATURE DEPARTMENT'],[-17.7,4.5,19],[5.5,.45],math.pi/2,'Photo 65 left of auditorium entry; only readable words reproduced','#e5dfcc','#3e3331','shell')
    # Immediate surrounding context, read visually from wider satellite view.
    # No physical facade names are invented for these off-campus structures.
    objects[:]=[o for o in objects if o['name']!='Context ground • extent illustrative']
    box('Surrounding agricultural ground • schematic satellite context',50,-1,30,1050,1.2,850,'fieldDry','context')
    plots=[(-260,180,100,180,'fieldGreen'),(-160,180,80,180,'fieldDark'),(-40,200,140,200,'fieldDry'),(90,210,90,210,'fieldDry'),(-335,-90,150,180,'fieldDry'),(-350,170,100,150,'fieldDark'),(-260,-220,90,110,'fieldDark'),(-110,-230,100,160,'fieldDry'),(30,-210,140,230,'fieldDry'),(370,240,190,180,'fieldDry')]
    for x,z,w,d,mat in plots:
        box('Satellite-visible agricultural parcel • approximate',x,-.24,z,w,.1,d,mat,'context')
        for zz in range(int(z-d/2),int(z+d/2),12):box('Agricultural furrow • contextual detail',x,-.16,zz,w,.015,.06,'soil','context')
    # Northern landscaped enclosure across Assan–Thirana Road.
    box('North landscaped lower enclosure • ownership unverified',-165,.01,-76,195,.25,108,'fieldDark','context')
    box('North enclosure upper stem • satellite',-229,.01,-193,70,.25,122,'fieldDark','context')
    box('North enclosure west arm • satellite',-296,.01,-160,65,.25,65,'fieldDark','context')
    box('North enclosure east arm • satellite',-133,.01,-150,130,.25,40,'fieldDark','context')
    for x in [-267,-65]:box('North lower enclosure perimeter wall',x,1,-76,.5,2,108,'context','context')
    box('North enclosure horizontal spine • satellite',-198,.23,-130,268,.1,4,'stone','context')
    box('North enclosure east perimeter path',-67,.23,-97,4,.1,150,'stone','context')
    for x in [-250,-211]:box('North upper stem longitudinal path',x,.23,-193,4,.1,122,'stone','context')
    for z in [-237,-200,-162]:box('North upper stem cross path',-229,.23,z,70,.1,4,'stone','context')
    for x in [-320,-290,-266]:box('North west-arm path',x,.23,-160,4,.1,62,'stone','context')
    for z in [-185,-160,-135]:box('North west-arm cross path',-296,.23,z,65,.1,4,'stone','context')
    for z in [-162,-139]:box('North east-arm path',-133,.23,z,130,.1,4,'stone','context')
    # East industrial roof massing (approximate footprints and unknown heights).
    industrial=[(201,37,60,230),(166,-29,41,84),(307,12,34,180),(352,-7,54,160),(169,137,53,76)]
    for x,z,w,d in industrial:
        box('Eastern industrial shed • satellite footprint; not campus',x,5,z,w,10,d,'context','context')
        box('Eastern industrial metal roof',x,10.3,z,w+1,.6,d+1,'roofMetal','context')
        for xx in range(int(x-w/2),int(x+w/2),4):box('Industrial roof seam',xx,10.65,z,.08,.035,d,'metal','context')
        for zz in range(int(z-d/2)+6,int(z+d/2),15):box('Industrial roof panel strip',x,10.66,zz,w*.8,.03,1.5,'glass','context')
    # Standard map view confirms the diagonal corridor is a road, not railway.
    for o in objects:
        if o['name'].startswith('Assan–Thirana Road'):
            o['p']=[15,.02,-71];o['s']=[1000,.15,9];o['rot']=.16
    for x,z in [(-265,120),(53,155)]:box('Rural access track • satellite',x,.04,z,4,.12,215,'paving','context')
    route=[(635,-152),(327,176),(355,300),(330,370)]
    for (x1,z1),(x2,z2) in zip(route,route[1:]):
        length=math.hypot(x2-x1,z2-z1);a=math.atan2(x2-x1,z2-z1)
        box('Eastern diagonal rural road • map confirmed', (x1+x2)/2,.08,(z1+z2)/2,6,.15,length,'road','context',a)
    # Entry and circulation pass. The concrete vehicle court and narrower
    # walking paths are distinct surfaces; no unobserved lane markings added.
    objects[:]=[o for o in objects if not o['name'].startswith(('Entrance white gate','Road marking'))]
    box('Main inner concrete approach • photo/video visible',-9,.26,-14,12,.16,94,'paving')
    box('Hall frontage pedestrian paving',-16.7,.34,-14,2.8,.13,94,'tile')
    box('Residential frontage turning court • satellite',21,.27,24,72,.16,7,'paving')
    box('East internal circulation strip • satellite',57,.26,-9,5,.15,113,'paving')
    box('North garden circulation strip • satellite',24,.26,-59,68,.15,3.4,'paving')
    for x in [-15.1,-2.9]:
        box('Inner approach low stone edge',x,.38,-14,.18,.18,94,'stone')
        for z in range(-57,32,3):box('Approach curb joint',x,.48,z,.2,.012,.025,'dark')
    for z in [20.4,27.6]:box('South court stone edge',21,.39,z,72,.18,.18,'stone')
    for x in [54.4,59.6]:box('East circulation stone edge',x,.38,-9,.15,.16,113,'stone')
    for z in range(-57,31,6):box('Inner concrete transverse joint',-9,.35,z,12,.012,.025,'dark')
    for z in range(-53,28,12):
        box('Edge drain grille • placement indicative',-15.2,.41,z,.35,.025,.8,'metal')
        for dz in [-.3,-.15,0,.15,.3]:box('Drain grille slat',-15.2,.44,z+dz,.34,.02,.025,'dark')
    # Open gate leaves, with modelled vertical bars, ornamental rings and fins.
    for hinge,direction,angle in [(-20,1,-math.radians(65)),(-6,-1,math.radians(65))]:
        def gp(u,y,v=0):return [hinge+math.cos(angle)*direction*u+math.sin(angle)*v,y,-61-math.sin(angle)*direction*u+math.cos(angle)*v]
        for h in [.65,1.2,2.8]:add('Open gate leaf horizontal rail',gp(3.1,h),[6.2,.1,.12],'white',rot=angle)
        for j in range(22):
            u=.12+j*.28;height=2.9+.8*math.sin(j/21*math.pi)
            add('Open gate white vertical bar',gp(u,.6+height/2),[.045,height,.06],'white',rot=angle)
            add('Gate bar pointed finial',gp(u,.6+height+.07),[.08,.15,.08],'white','petal',rot=angle)
        for u in [.55,1.4,2.25,3.1,3.95,4.8,5.65]:add('Gate ornamental circular ring',gp(u,2.9),[.27,.27,.07],'white','torus',rot=angle)
        for u in [.2,6.1]:add('Gate leaf end upright',gp(u,2),[.12,3.8,.16],'white',rot=angle)
        cyl('Gate hinge post',hinge,2,-61,.18,4,'white')
    box('Gate left side bay • visible exterior structure',-25,1.8,-61,6,3.6,5,'white')
    box('Gate-side bay roof',-25,3.7,-61,6.5,.2,5.5,'roof')
    box('Entrance threshold concrete apron',-13,.23,-65,17,.1,9,'paving')
    for x in [-20,-6]:
        for y in [2.9,3.6]:box('Gate hinge bracket',x,y,-60.9,.35,.12,.18,'metal')
    # Floodlights visible under the entry beam, not inferred control equipment.
    for x in [-19,-16,-13,-10,-7]:box('Entry beam downlight',x,4.88,-61.2,.28,.06,.22,'light')
    # Detailed sheds retain approximate massing and do not gain invented names.
    for centre_x,centre_z,w,d in industrial:
        for z in range(int(centre_z-d/2)+10,int(centre_z+d/2),18):
            for x in [centre_x-w/2-.1,centre_x+w/2+.1]:box('Industrial side wall pilaster',x,5,z,.18,10,.6,'stone','context')
    for x in [-94,-119]:
        for z in range(-22,55,12):box('West covered block roof rib',x,10,z,17 if x==-94 else 25,.12,.15,'metal','context')
    return objects,colors,signs
