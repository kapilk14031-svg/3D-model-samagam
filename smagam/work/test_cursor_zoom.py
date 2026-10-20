from pathlib import Path
s=Path('work/viewer-pdf.html').read_text(encoding='utf-8');fn=s[s.index('function cursorZoom('):s.index("canvas.addEventListener('wheel'",s.index('function cursorZoom('))]
pre="""const assert=require('assert');const norm=v=>{const l=Math.hypot(...v);return v.map(x=>x/l)},cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0);let streetMode=false,pandalInterior=false,topView=false,target,yaw,elevation,distance,W=1200,H=800,aspect=1.5,range={},dirty,anim,orbit;function zoomBy(){};
"""
test="""
for(const top of [false,true])for(const interior of [false,true])for(const el of [.03,.6,1.56])for(const xy of [[220,550],[950,220],[600,400]]){topView=top;pandalInterior=interior;target=[50,4,-20];yaw=.65;elevation=el;distance=500;const original=[...target];cursorZoom(.8,...xy);const after=[...target];cursorZoom(1.25,...xy);assert(Math.hypot(...target.map((v,i)=>v-original[i]))<1e-8,'cursor anchor drift');assert(Math.abs(distance-500)<1e-8);if(xy[0]!==600)assert(Math.hypot(...after.map((v,i)=>v-original[i]))>1,'off-centre zoom must translate target')};console.log('48 cursor zoom round-trip/anchor checks passed');
"""
Path('work/test-cursor-zoom.cjs').write_text(pre+fn+test,encoding='utf-8')
