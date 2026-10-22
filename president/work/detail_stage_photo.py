"""Current user photo stage treatment and a proposed clear D duty apron."""
import math
from pathlib import Path
from PIL import Image
from detail_lotus_v8 import MESHES
from geometry_profiles import extruded_polygon
ROOT=Path(__file__).resolve().parents[1]
def improve(objects,colors,signs):
    remove=('Hall front-row sofa','Stage left side railing','Stage right side railing','Stage left side sloping','Stage right side sloping','Fascia garland loop','Gold fascia trim','Central emblem backing','Meditation focal point','Stage flower planter','Stage floral arrangement')
    objects[:]=[o for o in objects if not o['name'].startswith(remove)]
    colors.update(stageMarigold='#ef9b29',stageBell='#d3b777',stageDuty='#b69978',stageDutyLine='#e6ce88',stageSilver='#b7bab5',stageBackdrop='#c9aaa9')
    def add(n,p,s,mat,shape='box',rot=0):objects.append(dict(name=n,p=[p[0],p[1],-20-p[2]],s=s,mat=mat,shape=shape,group='interior',rot=-rot,tilt=0))
    # Photo shows a green fascia, polished railing, floral chains and bells.
    for x in [-56+i*2 for i in range(17)]:
        add('Stage front stainless railing upright',[x,2.62,-30.02],[.045,1.04,.045],'stageSilver')
    for y in [2.36,2.72,3.12]:add('Stage front stainless horizontal railing',[-40,y,-30.02],[33.8,.045,.045],'stageSilver')
    for x in [-56+i*.22 for i in range(147)]:
        y=1.92-.14*abs(math.sin((x+56)*math.pi/3))
        add('Stage fascia orange floral scallop',[x,y,-29.79],[.075,.075,.06],'stageMarigold','sphereSmooth')
    for x in [-55+i*3 for i in range(11)]:
        for y in [1.12+j*.15 for j in range(6)]:add('Stage fascia hanging flower chain',[x,y,-29.77],[.065,.075,.06],'stageMarigold','sphereSmooth')
        add('Stage fascia brass hanging bell',[x,1.08,-29.76],[.11,.14,.11],'stageBell','cylinder')
    for x in [-53,-46.5,-40,-33.5,-27]:
        for a in [i*math.tau/24 for i in range(24)]:add('Stage fascia floral circular wreath',[x+.62*math.cos(a),1.51+.35*math.sin(a),-29.76],[.045,.045,.035],'stageMarigold','sphereSmooth')
    for o in objects:
        if o['name']=='Central backdrop panel':o['s']=[11,4.6,.1];o['p'][1]=4.6;o['mat']='stageBackdrop'
    # Real event banner imagery from this supplied photograph, no invented wording.
    key='sign-stage-photo-banner';colors[key]='#ffffff'
    signs.append(dict(key=key,lines=[''],p=[-40,4.3,-38.95],size=[10,4.9],rot=0,source='User supplied IMG20261021165204 - Rajesh Malik.jpg; cropped original event banner',bg='#ffffff',fg='#333333',image='sign-textures/'+key+'.png'))
    add('Stage original photographed event banner',[-40,4.3,-38.95],[10,4.9,1],key,'sign',rot=math.pi)
    for x in [-55,-25]:
        for j in range(16):
            a=j*math.pi/15
            add('Stage side decorative floral arch',[x+2.0*math.cos(a),3.25+1.8*math.sin(a),-36.9],[.095,.095,.09],'stageMarigold','sphereSmooth')
        for dx in [-2,2]:add('Stage floral arch stem',[x+dx,2.8,-36.9],[.1,1.0,.1],'stageMarigold')
    # Flat, unobstructed D outline: straight side at stage, curved side toward chairs.
    pts=[[-13,0],[13,0]]+[[13*math.cos(a),7*math.sin(a)] for a in [i*math.pi/64 for i in range(1,64)]]
    m=extruded_polygon(pts);v=m.vertices[:,[0,2,1]].copy();v[:,2]*=-1;MESHES['stageDutyApron']={'vertices':v.tolist(),'faces':m.faces.tolist()}
    add('Stage D-shaped clear duty apron',[-40,1.012,-29.4],[1,.018,1],'stageDuty','stageDutyApron')
    for a,b in zip(pts,pts[1:]+pts[:1]):
        dx,dz=b[0]-a[0],b[1]-a[1]
        add('Stage D duty area flush boundary',[-40+(a[0]+b[0])/2,1.028,-29.4+(a[1]+b[1])/2],[.09,.012,math.hypot(dx,dz)],'stageDutyLine',rot=math.atan2(dx,dz))
    # 22-second supplied hall video: black arches, rear-stage columns,
    # cream linked chairs and pale transverse aisle runners.
    colors.update(stageArchBlack='#252d2a',hallRunner='#c1ceca',seat='#c1bcaa',acoustic='#d1d9d5')
    for x in [-49,-31]:
        for dx in [-1.05,1.05]:add('Stage video black arch upright',[x+dx,3.45,-36.7],[.10,2.7,.10],'stageArchBlack')
        for j in range(24):
            a=j*math.pi/24;b=(j+1)*math.pi/24
            p0=[x+1.05*math.cos(a),4.8+1.05*math.sin(a)];p1=[x+1.05*math.cos(b),4.8+1.05*math.sin(b)]
            # Small rounded segments create a continuous black curved arch.
            add('Stage video black arch crown',[(p0[0]+p1[0])/2,(p0[1]+p1[1])/2,-36.7],[.16,.16,.16],'stageArchBlack','sphereSmooth')
    for x in [-47.3,-32.7]:
        for dx in [-.15,0,.15]:add('Stage video tall ceremonial column',[x+dx,3.9,-38.0],[.07,3.1,.07],'stageArchBlack')
        for y in [2.4,5.45]:add('Stage ceremonial column gold cap',[x,y,-38.0],[.65,.12,.4],'stageBell')
    for side in [-1,1]:
        for j in range(19):
            x=-40+side*(13+j*.42);y=6.65-j*.055
            add('Stage video overhead orange bunting',[x,y,-39.0],[.30,.25,.035],'stageMarigold')
    for o in objects:
        if o['name'].startswith('Central aisle'):o['mat']='hallRunner'
    cross=[-12.6,-25.2]
    objects[:]=[o for o in objects if not(o['group']=='seating' and any(abs(o['p'][2]-z)<.73 for z in cross))]
    for z in cross:add('Hall video transverse aisle runner',[-40,1.025,-20-z],[39,.025,1.25],'hallRunner')
    # White door mullions and wall clocks observed between curtain bays.
    for x in [-60.4,-19.6]:
        for z in [-8,-24,-38]:
            add('Hall video white window central mullion',[x,2.7,-20-z],[.10,2.7,.08],'white')
        add('Hall video wall clock',[x,3.9,-11],[.04,.25,.25],'stageBell','sphereSmooth')
    # User correction: straight diagonal corners, matching stair width (4.6 m).
    cut=4.6
    outline=[[-17,-5],[17,-5],[17,.4],[12.4,5],[-12.4,5],[-17,.4]]
    mesh=extruded_polygon([[x/34,z/10] for x,z in outline])
    v=mesh.vertices[:,[0,2,1]].copy();v[:,2]*=-1
    MESHES['stageDiagonalCorners']={'vertices':v.tolist(),'faces':mesh.faces.tolist()}
    for o in objects:
        if o['name'].startswith('Raised stage'):o['shape']='stageDiagonalCorners'
        if o['name'].startswith(('Stage green fascia','Stage front stainless horizontal')):o['s'][0]=24.8
        if o['name'].startswith(('Stage fascia','Stage front stainless railing upright')):
            dx=abs(o['p'][0]+40)
            if dx>12.4:o['p'][2]+=dx-12.4
    for side in [-1,1]:
        a=[-40+side*17,-34.6];b=[-40+side*12.4,-30]
        dx,dz=b[0]-a[0],b[1]-a[1];angle=math.atan2(dx,dz)
        add('Stage diagonal corner structural support',[(a[0]+b[0])/2,1.55,(a[1]+b[1])/2],[.13,.95,math.hypot(dx,dz)],'skirt',rot=angle)
        # Keep the diagonal stair landing completely open; no rail across it.
    for o in objects:
        if o['name'].startswith(('Stage left side green stair','Stage right side green stair')):
            side=-1 if 'left' in o['name'] else 1
            i=round((o['p'][1]-1.05)/.12)
            # Diagonal corner midpoint in the current north/south hall orientation.
            outx,outz=side/math.sqrt(2),-1/math.sqrt(2)
            outer=(4-i)*.6+.60
            distance=(outer-.12)/2
            o['p'][0]=-40+side*14.7+outx*distance
            o['p'][2]=12.3+outz*distance
            o['rot']=math.atan2(-outz,outx)
            o['s'][0]=outer+.12;o['s'][2]=math.hypot(4.6,4.6)
    # Remove the old front-rail uprights from both diagonal stair openings.
    objects[:]=[o for o in objects if not(o['name']=='Stage front stainless railing upright' and abs(o['p'][0]+40)>12.2)]
    # Low hand supports run up both stair edges, never across the landing.
    for side in [-1,1]:
        outx,outz=side/math.sqrt(2),-1/math.sqrt(2)
        tx,tz=1/math.sqrt(2),side/math.sqrt(2)
        for edge in [-1,1]:
            points=[]
            for i in range(1,5):
                distance=(4-i)*.6+.25
                x=-40+side*14.7+outx*distance+edge*tx*3.20
                z=12.3+outz*distance+edge*tz*3.20
                top=1.125+i*.24
                # add() uses the original pre-flip stage coordinate convention.
                add('Stage stair low side support post',[x,top+.30,-20-z],[.04,.60,.04],'stageSilver','cylinder')
                points.append((x,top+.60,z))
            for a,b in zip(points,points[1:]):
                dx,dy,dz=b[0]-a[0],b[1]-a[1],b[2]-a[2]
                add('Stage stair low side support handrail',[(a[0]+b[0])/2,(a[1]+b[1])/2,-20-(a[2]+b[2])/2],[.055,.055,math.sqrt(dx*dx+dy*dy+dz*dz)],'stageSilver',rot=-math.atan2(dx,dz))
                objects[-1]['tilt']=math.atan2(dy,math.hypot(dx,dz))
    # Move the lectern back and toward the stage side, clear of the stair landing.
    for o in objects:
        if o['name'].startswith('Lectern'):o['p'][0]=-55.3;o['p'][2]=14.5
    # Centre each low table directly in front of its corresponding stage sofa.
    objects[:]=[o for o in objects if not(o['name']=='Low stage table' or o['name']=='Table leg')]
    sofas=[o for o in objects if o['name']=='Stage sofa upholstered seat']
    for sofa in sofas:
        x,z=sofa['p'][0],sofa['p'][2]-2.2
        add('Low stage table',[x,2.5,-20-z],[3,.1,1.2],'white')
        for dx in [-1.2,1.2]:add('Table leg',[x+dx,2.25,-20-z],[.06,.5,.7],'metal')
    # User-requested queue belts around the curved edge of the clear D apron.
    colors.update(stageQBelt='#8b2030',stageQSteel='#aeb7ba')
    boundary=[[-40+13*math.cos(a),-29.4+7*math.sin(a)] for a in [i*math.pi/18 for i in range(2,17)]]
    for x,z in boundary:
        add('Stage D perimeter Q-belt weighted base',[x,1.07,z],[.23,.09,.23],'stageQSteel','cylinder')
        add('Stage D perimeter Q-belt upright',[x,1.60,z],[.045,1.04,.045],'stageQSteel','cylinder')
        add('Stage D perimeter Q-belt cassette',[x,2.13,z],[.09,.16,.09],'stageQSteel','cylinder')
    for a,b in zip(boundary,boundary[1:]):
        dx,dz=b[0]-a[0],b[1]-a[1]
        add('Stage D perimeter retractable Q-belt',[(a[0]+b[0])/2,2.11,(a[1]+b[1])/2],[.025,.095,math.hypot(dx,dz)],'stageQBelt',rot=math.atan2(dx,dz))
    return objects,colors,signs

def photo_texture():
    im=Image.open(Path(r'C:\Users\HP\Downloads\IMG20261021165204 - Rajesh Malik.jpg'))
    w,h=im.size
    im.crop((int(w*.371),int(h*.355),int(w*.558),int(h*.425))).save(ROOT/'outputs/sign-textures/sign-stage-photo-banner.png')

