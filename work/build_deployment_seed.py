from pathlib import Path
import json
units=[]
def shift(force=None,ic=None,extra=0,female=None,ictext='',note=''):
 return dict(force=force,female=female,incharge=ic,extra=extra,inchargeText=ictext,extraText='',notes=note,start='',end='')
def add(id,title,type,anchor=None,day=None,night=None,combined=None,ground='',notes='',offset=None):
 u=dict(id=id,title=title,type=type,anchorId=anchor,ground=ground,position=None,rotation=0,scale=1,enabled=True,speed=7,route=[],routeMode='pingpong',personnel=[],notes=notes,shifts={})
 if day is not None:u['shifts']['day']=day
 if night is not None:u['shifts']['night']=night
 if combined is not None:u['shifts']['combined']=combined
 if offset:u['offset']=offset
 units.append(u);return u
def both(id,title,type,anchor,force,ic=None,extra=0,female=None,ictext='',night=None,notes='',ground='',offset=None):
 return add(id,title,type,anchor,shift(force,ic,extra,female,ictext),shift(force if night is None else night,ic,extra,female,ictext),ground=ground,notes=notes,offset=offset)
u=both('PP-GT','GT Road traffic · Haldana–Samalkha return','traffic',None,None,3,ictext='1 DSP + 2 Inspector per shift',notes='Separate main strength not stated; off-site corridor not surveyed in this venue model.');u['shifts']['night']['extra']=1;u['shifts']['night']['extraText']='Wireless operator'
for id,title,anchor,force in [('PP-P4','Parking 4','P07',20),('PP-P5','Parking 5','P08',20),('PP-LOCAL','Local parking opposite Gates 2–3','G02',10)]:
 u=both(id,title,'parking',anchor,force,1,2,ictext='1 SI',notes='Crane staff additional: 1 NGO + 1 OR per shift.');[v.update(extraText='Crane: 1 NGO + 1 OR') for v in u['shifts'].values()]
for id,title in [('PCR10','PCR-10 · Haldana to Samalkha'),('PCR3','PCR-3 · Samalkha to Haldana / Samagam')]:both(id,title,'patrol',None,3,1,ictext='NGO incharge separate',notes='Off-site patrol location/route needs placement; no route invented.')
for name,direction in [('PS City','Haldana → Samalkha'),('27','Haldana → Samalkha'),('18','Haldana → Samalkha'),('22','Samalkha → Haldana'),('14','Samalkha → Haldana'),('24','Samalkha → Haldana')]:both('PP-R-'+name.replace(' ','-'),'Rider '+name+' · '+direction,'rider',None,1,1,ictext='Separate rider incharge',notes='Main strength is one driver per shift; walkie-talkie required. Draw the assigned route.')
both('PP-FOB','Foot-overbridge · both sides','gate','S04',14,1,female=6,ictext='1 SI',notes='8 OR + 6 women within main 14. A single both-sides duty entry; do not duplicate strength.')
both('PP-IN-FOB','Inside footbridge / X-Ray','xray','B01',8,1,female=2,ictext='1 SI',night=6,notes='Day: 6 OR + 2 women; night: 4 OR + 2 women.')
both('PP-DFMD','DFMD checking · traffic section','dfmd','G02',8,1,ictext='1 NGO',night=6,notes='Kept as a separate supplied row; may overlap gate checking rows and needs reconciliation before summing.')
add('SP-PATROL','Sonipat patrolling','patrol',None,combined=shift(5,1,female=2,ictext='1 Inspector',note='3 NGO/OR + 2 women; Day/Night entry, separate shifts not provided.'))
add('SP-P1','Parking 1 · Sonipat','parking','P01',combined=shift(10,1,female=5,ictext='1 SI',note='5 NGO/OR + 5 women; Day/Night not split.'))
nakas=[('Gannaur flyover below · Delhi → Panipat',7,2,None),('Gannaur flyover below · Panipat → Delhi',7,2,None),('Garhi Kalan flyover below · Delhi → Panipat',7,2,None),('Garhi Kalan flyover below · Panipat → Delhi',7,2,None),('Panchi Gujran Gurudwara cut',4,1,'V01'),('Main adda Panchi Gujran',4,1,'V01'),('Bhakharpur flyover below · Delhi → Panipat',7,2,None),('Bhakharpur flyover below · Panipat → Delhi',7,2,None),('DICT Chowk',5,1,None)]
for i,(title,force,fem,anchor) in enumerate(nakas,1):add('SP-N'+str(i),'Naka '+str(i)+' · '+title,'naka',anchor,combined=shift(force,1,female=fem,ictext='1 SI',note='Day/Night combined entry; women included in main strength.'),notes='Location approximate if anchored; remote points remain unplaced until positioned.',offset=[(i%2)*10,0,(i%3)*8])
add('SP-G1','Gate 1 · Sonipat duty','gate','G01',combined=shift(4,1,female=1,ictext='1 SI',note='Day/Night not split.'))
add('SP-LAW','Sonipat law and order','officer',None,combined=shift(30,1,female=10,ictext='1 Inspector',note='20 NGO/OR + 10 women; Day/Night not split.'))
for i in range(1,7):both('SP-R'+str(i),'Sonipat Rider '+str(i),'rider',None,1,1,ictext='1 OR incharge',notes='Six riders total: 6 OR incharges + 6 OR drivers = 12 per shift. Route not given.')
for i,gate in [(1,'G01'),(2,'G02'),(3,'G03'),(4,'H05')]:
 u=both('QRT'+str(i),'QRT-'+str(i)+' · '+('Gate '+str(i) if i<4 else 'Gate 5 / railway station'),'qrt',gate,4,1,ictext='NGO incharge',notes='4 commandos as main strength; incharge separate.',offset=[-8,0,-8])
 if i==4:u['shifts']['night']['incharge']=None;u['shifts']['night']['inchargeText']='Incharge-2 printed: confirmation needed';u['notes']+=' Night incharge count unresolved; not forced to one or two.'
for gate,anchor,xray in [(1,'G01',True),(2,'G02',False),(3,'G03',True)]:
 if xray:both('G'+str(gate)+'-XRAY','Gate '+str(gate)+' · X-Ray','xray',anchor,8,1,female=2,ictext='1 SI',night=6,offset=[7,0,5])
 both('G'+str(gate)+'-DFMD','Gate '+str(gate)+' · DFMD','dfmd',anchor,8,1,female=2,ictext='1 NGO',night=6,offset=[-7,0,6])
 both('G'+str(gate)+'-SI','Gate '+str(gate)+' · gate-level SI','officer',anchor,0,1,ictext='1 SI separate from QRT/checking incharges',offset=[0,0,10])
both('OUT-G10','Gate 10','gate',None,8,1,female=2,ictext='1 SI',night=6,notes='Gate 10 has no confirmed footprint in the supplied venue model; place manually.')
both('OUT-G5','Gate 5 · Bhodwal Majri railway station','gate','H05',22,1,female=7,ictext='1 SI',notes='Gate 5 mapped approximately to station area; no surveyed entrance footprint.',offset=[20,0,0])
u=both('OUT-P3','Parking 3 · near railway station','parking','P06',30,1,2,ictext='1 SI',night=20,notes='Crane: 1 NGO + 1 OR additional per shift.');[v.update(extraText='Crane: 1 NGO + 1 OR') for v in u['shifts'].values()]
both('OUT-PCR','Outer ring PCR patrol','patrol','G01',3,1,ictext='NGO incharge',offset=[0,0,-20])
for gate,anchor in [(1,'G01'),(2,'G02'),(3,'G03'),(4,'G04'),(10,None),(12,None),(15,None)]:both('OUT-M'+str(gate),'Outer Machaan · Gate '+str(gate),'machan',anchor,1,0,ictext='1 OR on machaan; no separate incharge stated',notes='7 outer machaans total, 7 OR per shift. Unmapped gates require placement.',offset=[-12,0,12])
for letter,mc,morcha in [('A',15,12),('B',10,5),('C',9,4),('D',10,7)]:
 anchor='GROUND-'+letter
 both(letter+'-FOOT','Ground '+letter+' · foot patrol','footpatrol',anchor,12,1,female=4,ictext='1 Inspector',ground=letter,notes='8 OR + 4 women; main 12 per shift.')
 both(letter+'-CANTEEN','Ground '+letter+' · canteen','canteen',anchor,14,1,female=4,ictext='1 SI',night=10,ground=letter,offset=[12,0,10],notes='Day 10 OR + 4 women; night 6 OR + 4 women.')
 both(letter+'-LANGAR','Ground '+letter+' · langar','langar',anchor,14,1,ictext='1 SI',night=10,ground=letter,offset=[-12,0,10],notes='The supplied common duties sum to main 40 day / 32 night per ground; incharges separate.')
 for j in range(1,mc+1):
  no=14 if letter=='A' and j==15 else j
  u=both(letter+'-M-'+str(j),'Machaan '+letter+'-'+str(no)+(' · duplicate chart row' if letter=='A' and j==15 else ''),'machan',None if letter=='A' and j==15 else anchor,1,0,ground=letter,notes='1 OR per shift.'+(' A-14 appears twice: 15 rows, unique number unresolved; duplicate remains unplaced.' if letter=='A' and j==15 else ' Approximate point distributed around the model ground.'))
  u['distribution']={'index':j-1,'count':mc,'kind':'perimeter'}
 for j in range(1,morcha+1):
  u=both(letter+'-MO-'+str(j),'Morcha '+letter+'-'+str(j),'morcha',anchor,4,1,ictext='1 NGO',ground=letter,notes='4 OR include the armed OR. 4 main + 1 NGO incharge = 5; do not add armed OR again.');u['distribution']={'index':j-1,'count':morcha,'kind':'perimeter-inner'}
both('QRT5','QRT-5 · inside Samagam','qrt','B01',4,1,ictext='1 NGO',notes='4 commandos + 1 NGO = 5 per shift.',offset=[-20,0,50])
add('PANDAL-F1','Pandal · force group 1','officer','B01',combined=shift(100,None,female=50,ictext='Incharge separate; count not provided',note='Civil dress: 30 + 40 women; uniform: 20 + 10 women. Shift division not stated.'),offset=[10,0,-20])
add('PANDAL-F2','Pandal · force group 2','officer','B01',combined=shift(30,None,female=10,ictext='Incharge separate; count not provided',note='Civil: 10 + 5 women; uniform: 10 + 5 women. Relationship to group 1 unresolved; do not assume additive deployment.'),offset=[10,0,20])
both('RECEPTION','Reception','reception','B01',6,1,female=2,ictext='1 NGO',notes='4 OR + 2 women + 1 NGO = 7 per shift.',offset=[100,0,-30])
u=add('CONTROL','Control room · CCTV','control','B17',offset=[0,0,-30]);u['shifts']={k:shift(4,1,ictext='1 NGO',note='4 OR + 1 NGO = 5; CCTV branch staff separate, number unspecified.') for k in ['morning','evening','night']}
both('VVIP-P','VVIP car parking','parking','P09',10,1,ictext='1 NGO',notes='Armed employee included in main 10; total 11.',offset=[0,0,10])
u=both('IMPORTANT-P2','Parking 2 · important duties','parking','P03',20,1,2,ictext='1 NGO',notes='20 main + 2 crane + 1 NGO = 23 per shift.');[v.update(extraText='Crane staff 2') for v in u['shifts'].values()]
add('PP-LAW','Panipat law and order','officer',None,combined=shift(90,3,female=30,ictext='1 DSP + 2 Inspectors',note='60 NGO/OR + 30 women; shift not specified.'))
add('RESERVE','Reserve force · Haldana chowki','reserve',None,combined=shift(None,None,ictext='',note='1 company including women; numerical strength not provided.'))
u=add('PROTOCOL','Protocol','officer',None,combined=shift(None,None,note='ASI Rakesh Kumar, T/HC Lelu and supporting staff; total unspecified.'));u['personnel']=[dict(name='Rakesh Kumar',rank='ASI',role='staff',shift='combined',contact=''),dict(name='Lelu',rank='T/HC',role='staff',shift='combined',contact='')]
add('LIAISON','Liaison','officer',None,combined=shift(2,None,female=1,note='1 P/SI + 1 female P/SI; protocol staff also referenced, not added again.'))
for type,title in [('ambulance','Ambulance'),('fire','Fire brigade')]:
 for g in ['A','B','C','D','Pandal']:
  u=add(type+'-'+g,title+' · '+('Ground '+g if g!='Pandal' else g),type,'B01' if g=='Pandal' else 'GROUND-'+g,combined=shift(None,None,note='One vehicle allocation; personnel strength not specified.'),ground=g if len(g)==1 else '',offset=[15,0,20]);u['vehicleCount']=1
seed={'version':1,'title':'Approximate duty deployment · supplied chart','note':'Incharge is separate from main force unless explicitly included. Women are subsets of main force. Unknown shifts/counts remain unknown. Positions are conceptual.','units':units}
Path('work/deployment-seed.json').write_text(json.dumps(seed,ensure_ascii=False,indent=2),encoding='utf-8');print(len(units),'editable duty records')
