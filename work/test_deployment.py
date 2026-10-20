from pathlib import Path
import json
s=Path('work/viewer-pdf.html').read_text(encoding='utf-8');lines=s.splitlines();names=['depValidate','depTotals','depPose','depMoveUnit'];fns='\n'.join(next(l for l in lines if l.startswith('function '+n+'(')) for n in names)
types=next(l for l in lines if l.startswith('const DEP_TYPES='));shifts=next(l for l in lines if l.startswith('const DEP_SHIFT='))
pre="const assert=require('assert'),fs=require('fs');const seed=JSON.parse(fs.readFileSync('work/deployment-seed.json','utf8'));const depClone=o=>JSON.parse(JSON.stringify(o));let depTime=0,depDragPause=null;const depRouteEpoch=new Map(),depPausedRoutes=new Map();\n"+types+'\n'+shifts+'\n'
test=r'''
const units=depValidate(seed);assert.equal(units.length,162);const find=id=>units.find(u=>u.id===id);
assert.equal(find('PP-GT').shifts.day.force,null);assert.equal(find('PP-GT').shifts.night.extra,1);
assert.equal(find('SP-P1').shifts.day,undefined);assert.equal(find('SP-P1').shifts.combined.force,10);
assert.equal(find('QRT4').shifts.night.incharge,null);assert(find('A-M-15').notes.includes('twice'));
for(const [g,n,total] of [['A',12,60],['B',5,25],['C',4,20],['D',7,35]]){const rows=units.filter(u=>u.id.startsWith(g+'-MO-'));assert.equal(rows.length,n);const t=depTotals(rows,'day');assert.equal(t.force+t.incharge,total)}
for(const g of ['A','B','C','D']){const rows=['FOOT','CANTEEN','LANGAR'].map(k=>find(g+'-'+k));assert.equal(depTotals(rows,'day').force,40);assert.equal(depTotals(rows,'night').force,32)}
assert.equal(depTotals(units.filter(u=>u.id.startsWith('SP-R')),'day').force+depTotals(units.filter(u=>u.id.startsWith('SP-R')),'day').incharge,12);
assert.throws(()=>depValidate({units:[{...find('PP-P4'),shifts:{day:{force:2,female:3}}}]}));
const rider={...depClone(find('PP-R-27')),position:[0,1,0],route:[[0,1,0],[100,1,0]],speed:10,routeMode:'pingpong'};depTime=5;assert.equal(depPose(rider).p[0],50);depTime=15;assert.equal(depPose(rider).p[0],50);depMoveUnit(rider,[10,1,20]);assert.deepEqual(rider.route[0],[10,1,20]);assert.deepEqual(rider.route[1],[110,1,20]);const before=depTotals([rider],'day');assert.equal(before.force,1);assert.equal(before.incharge,1);
const parent=find('PP-P4');const child={...depClone(parent),id:'child',isPersonnelMarker:true};assert.deepEqual(depTotals([parent,child],'day'),depTotals([parent],'day'));depRouteEpoch.set(rider.id,10);depTime=10;assert.equal(depPose(rider).p[0],10);
console.log('PASS: 162 records; shift/count uncertainty; women subset validation; all ground/Morcha subtotals; rider totals; route animation/return and relocation');
'''
Path('work/test-deployment.cjs').write_text(pre+fns+test,encoding='utf-8')
