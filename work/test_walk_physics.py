from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8').replace("side>0?a:Math.PI+a","side>0?-a:Math.PI-a");p.write_text(s,encoding='utf-8');a=s.index('// Capsule movement,');b=s.index('// Editable local duty plan.',a);js=s[a:b]
preamble="""const assert=require('assert'),fs=require('fs');const DATA=JSON.parse(fs.readFileSync('outputs/scene-data.json','utf8'));const SHAPES={};const worldFacilities=new Map();function ensureWorldFacilities(){};function deploymentCollision(){return false};const cworld=p=>[(p[1]-760)*1.4,0,(1000-p[0])*1.4];let walker,dirty;const status={dataset:{}};const document={getElementById:()=>status};
"""
tests="""
ensureWalkPhysics();
// A solid box stops motion even when the requested displacement is large.
insertWalkBox({x:1300,z:1300,w:2,d:12,bottom:0,top:8,angle:0});walker=[1290,.3,1300];moveWalker(30,0,1/60);assert(walker[0]<1298.5,'wall tunnelling');
// A gap between walls remains usable.
insertWalkBox({x:1200,z:1200,w:2,d:8,bottom:0,top:8,angle:0});assert(walkBlockedAt(1200,1200,.3));assert(!walkBlockedAt(1200,1210,.3));assert(!walkBlockedAt(1200,1200,9),'vertical clearance');
// Both stairs can be climbed from ground to deck and descended again.
for(const side of [-1,1]){const b=DATA.meta.s04_footbridge,a=b.angle,c=Math.cos(a),s=Math.sin(a),point=(x,z)=>[b.anchor[0]+x*c+z*s,.3,b.anchor[2]-x*s+z*c];walker=point(side*(b.span/2),side*25);for(let i=0;i<260;i++)moveWalker(-side*.1*s,-side*.1*c,1/60);assert(walker[1]>24,'stairs blocked at '+JSON.stringify(walker));for(let i=0;i<260;i++)moveWalker(side*.1*s,side*.1*c,1/60);assert(walker[1]<2,'stairs descent failed '+walker[1])}
console.log('PASS: swept wall collision, open gap, overhead clearance, both staircase ascent/descent');
"""
Path('work/test-walk-physics.cjs').write_text(preamble+js+tests,encoding='utf-8')
