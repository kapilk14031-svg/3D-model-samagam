from pathlib import Path
root=Path(__file__).resolve().parents[1];s=(root/'work/viewer-pdf.html').read_text(encoding='utf-8')
fn=s[s.index('function updateAK('):s.index('const akBuffer=')]
pre="""const assert=require('assert');let streetMode=true,walker=[0,1.3,0],heading=0,desiredHeading=0,pitch=.23,desiredPitch=.23,moveVX=0,moveVZ=0,gaitPhase=0,actorHeading=0,stepImpulse=[0,0],dirty=false;let akBlocked=false;function moveWalker(dx,dz){walker[0]+=dx;walker[2]+=dz}const heldKeys=new Set();const document={getElementById:()=>({textContent:''})};
"""
checks="""
function reset(){walker=[0,1.3,0];heading=desiredHeading=0;moveVX=moveVZ=0;stepImpulse=[0,0];heldKeys.clear()}
function simulate(hz){reset();heldKeys.add('w');for(let i=0;i<hz*2;i++)updateAK(1/hz);return [...walker]}
const a=simulate(30),b=simulate(120);assert(Math.abs(a[2]-b[2])<.15);assert(a[2]<-12&&Math.abs(a[0])<1e-6);
heldKeys.clear();for(let i=0;i<120;i++)updateAK(1/120);assert(Math.hypot(moveVX,moveVZ)<.001);
reset();heldKeys.add('e');for(let i=0;i<120;i++)updateAK(1/60);assert(heading>3&&heading<3.4);assert(Math.hypot(walker[0],walker[2])<1e-6);
reset();heldKeys.add('w');heldKeys.add('d');for(let i=0;i<120;i++)updateAK(1/60);assert(Math.hypot(moveVX,moveVZ)<=7.001);
console.log('AK movement: frame-rate consistency, smooth stopping, independent rotation and diagonal speed passed');
"""
(root/'work/test-ak.cjs').write_text(pre+fn+checks,encoding='utf-8')
