from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
start=s.index('function placeDeploymentIcons(){')
helper="function depIconNearby(p){if(!streetMode&&distance>=1800)return true;const focus=streetMode?walker:target,radius=streetMode?55:Math.max(24,Math.min(240,distance*.65));return Math.hypot(p[0]-focus[0],p[2]-focus[2])<=radius}\n"
s=s[:start]+helper+s[start:]
s=s.replace("const pose=depPose(u);if(!pose)continue;const p=projected([pose.p[0],pose.p[1]+(u.type==='machan'?12:5)*u.scale,pose.p[2]]);", "const pose=depPose(u);if(!pose||!depIconNearby(pose.p))continue;const p=projected([pose.p[0],pose.p[1]+(u.type==='machan'?12:5)*u.scale,pose.p[2]]);")
p.write_text(s,encoding='utf-8')
line=next(l for l in s.splitlines() if l.startswith('function depIconNearby('))
Path('work/test-nearby-icons.cjs').write_text("const assert=require('node:assert/strict');let streetMode=false,distance=3000,target=[0,0,0],walker=[100,0,100];\n"+line+"\nassert(depIconNearby([1500,0,1000]));distance=100;assert(depIconNearby([40,0,0]));assert(!depIconNearby([150,0,0]));distance=700;assert(depIconNearby([200,0,0]));assert(!depIconNearby([300,0,0]));streetMode=true;assert(depIconNearby([120,0,120]));assert(!depIconNearby([200,0,200]));console.log('PASS: overview shows all, zoom and AK show nearby icons only');",encoding='utf-8')
