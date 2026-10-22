from pathlib import Path
s=Path('work/viewer-pdf.html').read_text(encoding='utf-8').splitlines()
code="const assert=require('node:assert/strict');let depTime=0,depDragPause=null,depFollowState=null,dirty=false;const depPausedRoutes=new Map(),depRouteEpoch=new Map();\n"
for name in ['depPose','depToggleMotion','depMoveUnit']:code+=next(line for line in s if line.startswith('function '+name+'('))+'\n'
code+='''
for(const type of ['rider','qrt','patrol','footpatrol','ambulance','fire']){const u={id:type,type,position:[0,1,0],route:[[0,1,0],[100,1,0]],rotation:0,speed:10,routeMode:'pingpong'};depTime=4;assert.equal(depPose(u).p[0],40);assert.equal(depToggleMotion(u),true);depTime=9;assert.equal(depPose(u).p[0],40);assert.equal(depToggleMotion(u),false);assert.equal(depPose(u).p[0],40);depTime=10;assert.equal(depPose(u).p[0],50);depToggleMotion(u);depMoveUnit(u,[10,1,20]);assert.deepEqual(depPose(u).p,[60,1,20]);depTime=25;assert.deepEqual(depPose(u).p,[60,1,20]);depToggleMotion(u);assert.deepEqual(depPose(u).p,[60,1,20]);depTime=26;assert.equal(depPose(u).p[0],70)}
assert.equal(depToggleMotion({type:'officer',route:[]}),null);console.log('PASS: click pause/resume for six moving types; frozen position, smooth resume, shifted paused route, static model unchanged');
'''
Path('work/test-pause-movement.cjs').write_text(code,encoding='utf-8')
