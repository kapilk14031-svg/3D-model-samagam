"""User-added VIP gate at the invited-guest parking approach, not a source PDF gate."""
current=''
vip_x,vip_z=183.4,134.4
# Clear a small opening from representative parked cars, without altering the parking polygon.
objects[:]=[o for o in objects if not(o.get('featureId')=='P10' and o.get('parkingVehicleOrigin') and abs(o['parkingVehicleOrigin'][0]-vip_x)<17 and abs(o['parkingVehicleOrigin'][1]-vip_z)<24)]
before=len(objects)
def vb(part,xx,zz,w,d,h,color,y=0):box('VIP ACCESS GATE / PROPOSED / '+part,xx,zz,w,d,h,color,y,'gates')
for side in [-1,1]:
    xx=vip_x+side*7.4
    vb('base',xx,vip_z,3,3,.8,'#8f3a16')
    vb('orange pillar',xx,vip_z,2,2.5,9.5,'#b94d18',.8)
    vb('gold capital',xx,vip_z,3.1,3,.55,'#dc7b24',10.25)
    add('VIP ACCESS GATE / PROPOSED / warm lantern','ellipsoid',xx,10.8,vip_z,1.8,2,1.8,'#f0a044','gates')
add('VIP ACCESS GATE / PROPOSED / ceremonial arch','arch',vip_x,4.7,vip_z,15.5,10,1.5,'#b94d18','gates')
vb('VIP name board frame',vip_x,vip_z,12,1,2.7,'#dc7b24',15.2)
vb('VIP green name board',vip_x,vip_z+.6,11.4,.15,2.1,'#195846',15.5)
for o in objects[before:]:
    o['userAdded']=True;o['status']='User-proposed VIP access gate beside I-PARKING near Gate 2. PDF labels VIP/Invited Guest parking and green route, but does not name a VIP gate.'
labels.append(dict(text='VIP ACCESS / PROPOSED',p=[vip_x,20,vip_z],layer='gates',userAdded=True))
