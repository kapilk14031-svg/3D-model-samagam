from pathlib import Path
s=Path('work/viewer-pdf.html').read_text(encoding='utf-8');a=s.index('// Capsule movement,');b=s.index('// Editable local duty plan.',a);physics=s[a:b]
helper=next(l for l in s.splitlines() if l.startswith('function photoGateOpened('))
pre="""const assert=require('node:assert/strict'),fs=require('node:fs');const DATA=JSON.parse(fs.readFileSync('outputs/scene-data.json','utf8')),SHAPES={};const worldFacilities=new Map();function ensureWorldFacilities(){}function deploymentCollision(){return false}const cworld=p=>[(p[1]-760)*1.4,0,(1000-p[0])*1.4];let walker,dirty,photoGateOpen=false;const document={getElementById:()=>({dataset:{}})};
"""
test="""for(const open of [false,true]){photoGateOpen=open;walkPhysicsReady=false;walkGrid.clear();walkFloors.clear();ensureWalkPhysics();for(const id of ['G01','G02','G03']){const f=DATA.features.find(v=>v.id===id);for(const side of [-1,1]){const a=f.gateAlignment?.angle??-Math.PI/2,x=f.world[0]+Math.cos(a)*side*15,z=f.world[2]-Math.sin(a)*side*15,y=walkSurfaceAt(x,z,.3);walker=[x,y,z];assert.equal(walkBlockedAt(x,z,y),!open,id+' portal '+side+' open='+open)}}}console.log('PASS: AK collisions follow gate open/closed state at all six vehicle portals');"""
Path('work/test-photo-gate-walk.cjs').write_text(pre+helper+'\n'+physics+'\n'+test,encoding='utf-8')
