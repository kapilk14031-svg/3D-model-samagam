"""Approximate P5 parking area beside the source's opposite-side textual annotation."""
current='P08'
p5_feature=next(f for f in features if f['id']=='P08')
cx,cz=497.5,250.5;angle=.264;ca=math.cos(angle);sa=math.sin(angle)
width,depth=180,320;start=len(objects)
def p5box(part,x,z,w,d,h,color,y=0):box('P5 APPROXIMATE AREA / '+part,x,z,w,d,h,color,y,'parking')
p5box('compacted parking surface',0,0,width,depth,.35,'#969781')
for off in [-width/2,width/2]:p5box('parking kerb',off,0,.6,depth,.32,'#d2c9aa',.35)
for off in [-depth/2,depth/2]:p5box('parking kerb end',0,off,width,.6,.32,'#d2c9aa',.35)
for xx in [-17,36]:p5box('longitudinal drive aisle',xx,0,9,depth,.08,'#495650',.36)
p5box('cross circulation aisle',0,0,width,12,.08,'#495650',.37)
p5box('entry throat',-width/2+6,0,15,14,.09,'#495650',.37)
vehicle_count=0
for x in [-65,-49,0,16]:
    for z in range(-135,145,22):
        if abs(z)<19:continue
        parked_vehicle(p5_feature,x,z,False,False,vehicle_count);vehicle_count+=1
for z in range(-130,140,29):
    if abs(z)<18:continue
    parked_vehicle(p5_feature,65,z,True,False,vehicle_count);vehicle_count+=1
# A local service-lane depiction stays entirely on the opposite side; no at-grade pedestrian crossing is invented.
line('P5 approximate local access lane',[[-100,0,-200],[-100,0,200]],8,.7,'#3d4847','parking')
line('P5 entry connection',[[-100,0,0],[-83,0,0]],10,.7,'#3d4847','parking')
p5box('pedestrian refuge beside parking',-84,30,7,40,.18,'#cebd99',.4)
p5box('bus stop shelter platform',-81,73,11,22,.22,'#b7b7a3',.4)
for z in [65,81]:p5box('bus shelter column',-79,z,.45,.45,4.7,'#b6b9aa',.6)
p5box('illustrative shelter roof',-80,73,12,23,.35,'#ded4b9',5.1)
objects[-1]['part']='roof'
for x in [-80,80]:
    for z in [-145,-70,70,145]:
        p5box('light pole',x,z,.4,.4,9,'#9aa79c',.4)
        p5box('luminaire',x,z,1.5,2,.2,'#ead4a1',9.4)
for o in objects[start:]:
    x,y,z=o['p'];o['p']=[cx+x*ca+z*sa,y,cz-x*sa+z*ca];o['rotY']=o.get('rotY',0)+angle
    if o.get('parkingVehicleOrigin'):
        x,z=o['parkingVehicleOrigin'];o['parkingVehicleOrigin']=[cx+x*ca+z*sa,cz-x*sa+z*ca]
    o['userAdded']=True;o['status']='P5 named in PDF near foot-overbridge/local bus stop. Opposite-side area footprint, bays, vehicles, shelter and local access geometry are approximate user-requested modelling, not surveyed source geometry.'
p5_feature['representation']='3D P5 parking area, approximate boundary inferred around source textual annotation'
p5_feature['model_location_status']='Approximate area; PDF supplies annotation only, not a boundary polygon'
p5_feature['model_parking_polygon']=[[cx+x*ca+z*sa,0,cz-x*sa+z*ca] for x,z in [[-90,-160],[90,-160],[90,160],[-90,160]]]
p5_feature['world']=[cx,8,cz]
for l in labels:
    if l.get('featureId')=='P08':l['text']='P5 / DAILY COMMUTERS / APPROX. AREA';l['p']=[cx,16,cz];l['layer']='parking'
p5_info=dict(centre=[cx,0,cz],approximate=True,vehicles_representative=vehicle_count,source='P5 annotation near foot-overbridge/local bus stop; source has no parking polygon')
print('Opposite-side P5 parking added:',vehicle_count,'representative vehicles; footprint approximate')
