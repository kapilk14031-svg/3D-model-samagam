from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("canvas.addEventListener('wheel',e=>{e.preventDefault();zoomBy(Math.exp(e.deltaY*.001))},{passive:false});",'''// Zoom about the world point under the cursor, keeping it fixed on screen.
function cursorZoom(k,x,y){if(streetMode){zoomBy(k);return}anim=null;orbit=false;const oldDistance=distance,next=Math.max(pandalInterior?12:35,Math.min(5500,oldDistance*k)),ratio=next/oldDistance;
const forward=[-Math.sin(yaw)*Math.cos(elevation),-Math.sin(elevation),-Math.cos(yaw)*Math.cos(elevation)],right=norm(cross(forward,[0,1,0])),up=cross(right,forward),nx=2*x/W-1,ny=1-2*y/H,cam=target.map((v,i)=>v-forward[i]*oldDistance);let anchor;
if(topView){const size=oldDistance*.44;anchor=target.map((v,i)=>v+right[i]*nx*size*aspect+up[i]*ny*size)}else{const q=Math.tan(.72/2),ray=norm(forward.map((v,i)=>v+right[i]*nx*q*aspect+up[i]*ny*q)),groundT=ray[1]<-.0001?-cam[1]/ray[1]:-1;
// Ground-plane anchoring suits the venue map. Near-horizontal interior views
// use the target plane so zooming never jumps to a distant horizon.
const t=!pandalInterior&&groundT>0&&groundT<oldDistance*5?groundT:oldDistance/Math.max(.1,dot(ray,forward));anchor=cam.map((v,i)=>v+ray[i]*t)}
target=target.map((v,i)=>anchor[i]+(v-anchor[i])*ratio);distance=next;range.value=distance;dirty=true}
canvas.addEventListener('wheel',e=>{e.preventDefault();const r=canvas.getBoundingClientRect();cursorZoom(Math.exp(Math.max(-300,Math.min(300,e.deltaY))*.001), (e.clientX-r.left)*W/r.width,(e.clientY-r.top)*H/r.height)},{passive:false});''')
p.write_text(s,encoding='utf-8')
