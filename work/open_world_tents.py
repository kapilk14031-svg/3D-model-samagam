from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8');pos=s.index('for(const o of DATA.objects){if(')
addon='''// Replace solid accommodation blocks with actual walls and open doorways.
const openedAccommodation=[];for(const o of DATA.objects){if(o.layer==='tents'&&o.name.endsWith('entrance flap'))continue;if(o.layer==='tents'&&o.name.endsWith('canvas walls')){const[x,y,z]=o.p,[w,h,d]=o.s,H=3.6,door=2.5;for(const[xx,zz,ww,dd]of[[x-w/2,z,.13,d],[x+w/2,z,.13,d],[x,z-d/2,w,.13],[x-(w+door)/4,z+d/2,(w-door)/2,.13],[x+(w+door)/4,z+d/2,(w-door)/2,.13]])openedAccommodation.push({...o,name:o.name+' / open panel',p:[xx,H/2+.1,zz],s:[ww,H,dd]});openedAccommodation.push({...o,name:o.name+' / doorway lintel',p:[x,3.5,z+d/2],s:[door,.4,.13]});continue}if(o.layer==='tents'&&o.kind==='roof'){o.p[1]=3.7;o.s[1]=2.5}if(o.layer==='tents'&&/fascia|ridge seam/.test(o.name))o.p[1]+=1.3;openedAccommodation.push(o)}DATA.objects=openedAccommodation;
'''
s=s[:pos]+addon+s[pos:]
s=s.replace("box(0,6,-72,66,12,20,'#d4d2bf');", "box(0,.3,-72,66,.6,20,'#b4ac92');for(const x of[-32,32])box(x,6,-72,2,12,20,'#d4d2bf');box(0,6,-81,66,12,2,'#d4d2bf');for(const x of[-19,19])box(x,6,-62,28,12,1,'#d4d2bf');box(0,12,-72,66,.5,20,'#b7b5a5');box(0,2,-76,18,4,3,'#745d42');for(const x of[-20,20])box(x,1,-72,4,2,4,'#3d4f5b');")
s=s.replace("box(0,7,-61.8,9,9,.3,'#253c49');", "")
s=s.replace("walker=[p[0],1.3,p[2]]", "walker=[p[0],.3,p[2]]",1)
s=s.replace("target=[...item.world];p=nearestStreetPoint();angle=0", "target=[...item.world];p=nearestStreetPoint();angle=0;if(['residential','ground'].includes(item.category)){const tent=DATA.objects.find(o=>o.layer==='tents'&&o.kind==='roof'&&(item.category==='ground'?o.referenceSector?.startsWith(item.id.slice(-1)):'RES-'+o.referenceSector===item.id));if(tent)p=[tent.p[0],.3,tent.p[2]+tent.s[2]/2+5]}else if(item.category==='railway')p=[item.world[0]+29,.3,item.world[2]+80];else if(item.category==='parking')p=[item.world[0],.3,item.world[2]];else if(item.category==='gate'){p=[item.world[0]+8,.3,item.world[2]];angle=-Math.PI/2}")
p.write_text(s,encoding='utf-8')
