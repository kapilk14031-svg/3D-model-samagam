from pathlib import Path
root=Path(__file__).resolve().parent
p=root/'pdf_plan_data.py';s=p.read_text(encoding='utf-8')
s=s.replace("[659,836,713,887]","[659,836,713,875]").replace("[657,888,713,1028]","[657,876,713,932]")
s=s.replace("detail='Separate marked P2 strip; overlaps route arrows to I-PARKING at its lower end'","detail='P2 strip above the separate I-PARKING pocket; shared arrow approach does not make the polygons overlap'")
s=s.replace("[[485,719],[648,719],[720,719],[839,719]]","[[485,719],[648,719]]")
s=s.replace("[[903,871],[1046,871]]","[[903,871],[973,871]]")
s=s.replace("[[899,872],[902,952]]","[[837,742],[837,866]]")
s+='''
# Second visual audit: repeated labels and previously omitted minor geometry.
feature('R22','ROAD 24 WIDE','internal_road',path=[[973,871],[1046,871]],detail='Second printed ROAD 24 WIDE annotation; source punctuation/units should be reviewed')
feature('R23',"ROAD R-2 90'",'internal_road',path=[[650,719],[839,719]],detail='Second printed R-2 90 width annotation beside exhibition')
feature('P14','PARKING','point',[838,875,848,936],detail='Vertical generic PARKING label beside I-PARKING; retained without assigning a new numbered parking')
feature('W29','PANDAL INTERNAL DIVIDER','wall',path=[[721,910],[830,910]],detail='Internal horizontal line in pandal footprint; drawn as a low divider because actual height/function is unspecified')
for n,bbox in enumerate([[1048,801,1064,811],[1048,817,1064,829],[1048,834,1064,846],[1048,851,1064,862],[1054,882,1064,899]]):
    feature(f'B{24+n:02}','UNLABELLED GATE 3 BLOCK '+str(n+1),'building',bbox,detail='Small outlined cell beside Special Residence / Gate 3. No use or capacity printed; no facility name invented')
feature('W30','PDF PARCEL OUTLINE','wall',path=[[719,573],[719,714],[835,714],[835,573]],detail='Central rectangular parcel boundary above exhibition')
feature('W31','PDF PARCEL OUTLINE','wall',path=[[850,575],[899,575],[899,675],[850,675],[850,575]],detail='Narrow parcel west of the alighting boundary')
for f in features:
    if f['id']=='R17':f['detail']='Printed vertical width annotation beside offices east of pandal; position corrected after second visual audit';f['status']='Width appears 80; small print needs review, dimensions unmeasured'
'''
p.write_text(s,encoding='utf-8')
p=root/'build_pdf_model.py';s=p.read_text(encoding='utf-8')
s=s.replace("else 2.6,'#626d68'", "else 2.6,'#626d68'")
# The source divider is a line with unknown structural meaning, not a full wall.
s=s.replace("1.1 if k!='wall' else 2.6", "1.1 if k!='wall' else .35 if current=='W29' else 2.6")
p.write_text(s,encoding='utf-8')
print('Second source audit corrections applied')
