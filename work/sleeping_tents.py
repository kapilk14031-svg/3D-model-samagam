"""User-added sleeping tent proposal in the two requested vacant areas."""
current=''
sleeping_tent_centres=[]
camp_groups=[
    ('U01 SIDE',752,337,838,408),
    ('U01 SIDE EXTENSION',839,337,879,408),
    ('REAR U01 PARCEL',752,433,835,495),
    ('BEHIND NORTHERN LANGAR',912,302,948,410),
    ('BEHIND MIDDLE LANGAR',963,435,1006,542),
]
for title,u0,v0,u1,v1 in camp_groups:
    start=len(sleeping_tent_centres)
    cols=list(range(u0+6,u1-4,8));rows=list(range(v0+6,v1-4,8))
    # A wide longitudinal aisle and a cross aisle keep dense rows legible.
    midu=(u0+u1)/2;midv=(v0+v1)/2
    for row,v in enumerate(rows):
        for col,u in enumerate(cols):
            if ((u1-u0)>=35 and title!='U01 SIDE EXTENSION' and abs(u-midu)<5) or abs(v-midv)<6:continue
            x,_,z=planpoint(u,v);index=len(sleeping_tent_centres)+1
            name=f'USER ADDED / Black sleeping tent {index:03}'
            before=len(objects)
            box(name+' groundsheet',x,z,6.5,8.5,.12,'#666956',.05,'tents')
            box(name+' dark canvas walls',x,z,6,8,2.15,'#262b28',.17,'tents')
            add(name+' black fabric roof','roof',x,2.32,z,6.4,1.7,8.4,'#171c1b','tents');objects[-1]['part']='roof'
            box(name+' doorway',x,z+4.03,1.8,.08,1.9,'#101714',.18,'tents')
            box(name+' rolled entrance flap',x,z+4.13,2,.25,.2,'#555c50',2.05,'tents')
            box(name+' ventilation mesh',x,z-4.03,2.1,.08,.5,'#637268',1.3,'tents')
            for side in [-1,1]:
                box(name+' sleeping mat',x+side*1.45,z,1.45,5.5,.12,'#b2ac91',.23,'tents')
                box(name+' folded blanket',x+side*1.45,z-2,1.4,.8,.25,'#7b8774',.35,'tents')
            for sx in [-1,1]:
                for sz in [-1,1]:
                    beam3(name+' guy rope',[x+sx*2.95,2.2,z+sz*3.8],[x+sx*4.1,.15,z+sz*4.9],.045,'#92917b','tents')
            for o in objects[before:]:
                o['userAdded']=True;o['camp']=title;o['status']='User-requested sleeping tent proposal; not drawn in source PDF; illustrative size and quantity'
            sleeping_tent_centres.append(dict(number=index,camp=title,p=[x,0,z],source_uv=[u,v],footprint=[6.4,8.4]))
    # Permeable earth aisles in the requested camp, with no new traffic claim.
    ux,_,uz=planpoint(midu,(v0+v1)/2)
    box('User-added camp longitudinal earth aisle',ux,uz,(v1-v0)*PLAN_SCALE,4,.06,'#b6a181',.02,'tents')
    box('User-added camp cross aisle',ux,uz,4,(u1-u0)*PLAN_SCALE,.06,'#b6a181',.03,'tents')
    labels.append(dict(text=title+' / BLACK SLEEPING TENTS',p=[ux,15,uz],layer='tents',userAdded=True))
    print(title,':',len(sleeping_tent_centres)-start,'user-added tents')
