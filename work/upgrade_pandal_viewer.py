from pathlib import Path
p=Path(__file__).with_name('viewer-v2.html');s=p.read_text(encoding='utf-8')
s=s.replace("o.kind==='roof'||/roof ridge|eave trim/.test(o.name)","o.part==='roof'||o.kind==='roof'||/roof ridge|eave trim/.test(o.name)")
old="let vv=verts.map(v=>{let x=v[0]*o.s[0],z=v[2]*o.s[2],a=o.rotY||0;return [o.p[0]+x*Math.cos(a)+z*Math.sin(a),o.p[1]+v[1]*o.s[1]-(o.kind==='box'?o.s[1]/2:0),o.p[2]-x*Math.sin(a)+z*Math.cos(a)]});"
new="let vv=verts.map(v=>{let x=v[0]*o.s[0],y=v[1]*o.s[1]-(o.kind==='box'?o.s[1]/2:0),z=v[2]*o.s[2],a=o.rotY||0;if(o.quaternion){let [qx,qy,qz,qw]=o.quaternion,tx=2*(qy*z-qz*y),ty=2*(qz*x-qx*z),tz=2*(qx*y-qy*x);return [o.p[0]+x+qw*tx+qy*tz-qz*ty,o.p[1]+y+qw*ty+qz*tx-qx*tz,o.p[2]+z+qw*tz+qx*ty-qy*tx]}return [o.p[0]+x*Math.cos(a)+z*Math.sin(a),o.p[1]+y,o.p[2]-x*Math.sin(a)+z*Math.cos(a)]});"
assert old in s;s=s.replace(old,new)
s=s.replace('<button data-view="pandal">Main pandal<em>Stage & seating</em></button>', '<button data-view="pandal">Main pandal<em>Fabric canopy & entrance</em></button><button data-view="stage">Stage detail<em>Open roof · interior</em></button>')
s=s.replace('pandal:{target:[325,5,90],yaw:.65,elevation:.62,distance:630}', 'pandal:{target:[325,6,95],yaw:.65,elevation:.62,distance:650},stage:{target:[325,10,-15],yaw:.12,elevation:.36,distance:320}')
s=s.replace("sceneEl.classList.toggle('bridge-detail',bridgeFocus||flyoverFocus)","sceneEl.classList.toggle('bridge-detail',bridgeFocus||flyoverFocus||view==='pandal'||view==='stage')")
s=s.replace("topView=view==='top';anim=", "if(view==='pandal'||view==='stage'){p.distance=Math.max(p.distance,(view==='stage'?240:500)/(sceneEl.clientWidth/sceneEl.clientHeight));cutaway=view==='stage';const roofButton=document.getElementById('cutaway');roofButton.classList.toggle('active',cutaway);roofButton.setAttribute('aria-pressed',String(cutaway));roofButton.textContent=cutaway?'Close roofs':'Open roofs';sceneEl.scrollIntoView({block:'start',behavior:'smooth'})}topView=view==='top';anim=")
s=s.replace('varying float vDepth;void main()', 'varying float vDepth;varying vec3 vWorld;void main()')
s=s.replace('vDepth=gl_Position.w;', 'vDepth=gl_Position.w;vWorld=aPos;')
s=s.replace('varying float vDepth;uniform sampler2D', 'varying float vDepth;varying vec3 vWorld;uniform sampler2D')
s=s.replace('float fog=clamp', 'lit+=vec3(.16,.09,.025)*uEvening*exp(-length(vWorld-vec3(325.,12.,-35.))/90.);float fog=clamp')
s=s.replace("document.querySelector('.location b').textContent=flyoverFocus?", "document.querySelector('.location b').textContent=view==='pandal'?'Main pandal · fabric canopy':view==='stage'?'Main pandal · stage interior':flyoverFocus?")
s=s.replace("document.querySelector('.location').lastChild.textContent=flyoverFocus?", "document.querySelector('.location').lastChild.textContent=(view==='pandal'||view==='stage')?'Illustrative design · unmeasured geometry':flyoverFocus?")
p.write_text(s,encoding='utf-8')
