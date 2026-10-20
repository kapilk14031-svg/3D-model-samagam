from pathlib import Path
root=Path(__file__).resolve().parent
p=root/'viewer-pdf.html';s=p.read_text(encoding='utf-8')
s=s.replace('<button id="light">Evening light</button>','<button id="light">Evening light</button><button id="routeGlow" class="active" aria-pressed="true">Route glow</button>')
s=s.replace('uniform float uShadowOn;','uniform float uShadowOn;uniform float uRouteGlow;',1)
colors=['8c285c','963564','175b88','1f628a','912f4d','176644','135b3d']
conditions=['distance(vColor,vec3('+','.join(str(int(c[i:i+2],16)/255) for i in [0,2,4])+'))<.012' for c in colors]
emission="if(uRouteGlow>.5&&("+'||'.join(conditions)+")){lit=vColor*1.65+vec3(.06,.06,.04);}" 
s=s.replace('lit+=vec3(.16,.09,.025)',emission+'lit+=vec3(.16,.09,.025)',1)
s=s.replace("'uShadowOn','uShadow'","'uShadowOn','uShadow','uRouteGlow'")
s=s.replace("gl.uniform1f(uniforms.uEvening,evening?1:0);","gl.uniform1f(uniforms.uEvening,evening?1:0);gl.uniform1f(uniforms.uRouteGlow,directionsGlow?1:0);")
halo='''
let directionsGlow=true;
const glowProgram=program('attribute vec3 aPos;attribute vec3 aColor;uniform mat4 uVP;varying vec3 vGlowColor;void main(){gl_Position=uVP*vec4(aPos,1.);vGlowColor=aColor;}', 'precision mediump float;varying vec3 vGlowColor;uniform float uAlpha;void main(){gl_FragColor=vec4(vGlowColor,uAlpha);}');
const glowVP=gl.getUniformLocation(glowProgram,'uVP'),glowAlpha=gl.getUniformLocation(glowProgram,'uAlpha'),haloBuffers=[];
for(const [width,alpha] of [[16,.032],[10,.055],[6,.095],[3.2,.15]]){
 let verts=[];
 for(const route of DATA.routes){
  const col=route.name==='L10'||route.name==='L11'?[.16,.95,.57]:['L05','L06','L08'].includes(route.name)?[.12,.62,1.]:[1.,.22,.55];
  const put=p=>verts.push(...p,...col);
  for(let j=1;j<route.points.length;j++){
   const a=route.points[j-1],b=route.points[j],dx=b[0]-a[0],dz=b[2]-a[2],length=Math.hypot(dx,dz);if(length<.01)continue;
   const nx=-dz/length*width/2,nz=dx/length*width/2,y=4.12;
   const v=[[a[0]+nx,y,a[2]+nz],[b[0]+nx,y,b[2]+nz],[b[0]-nx,y,b[2]-nz],[a[0]-nx,y,a[2]-nz]];
   for(const k of [0,1,2,0,2,3])put(v[k]);
  }
 }
 const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(verts),gl.STATIC_DRAW);haloBuffers.push({buffer,count:verts.length/6,alpha});
}
function drawDirectionGlow(){
 if(!directionsGlow||hidden.has('traffic'))return;
 gl.useProgram(glowProgram);gl.uniformMatrix4fv(glowVP,false,currentVP);gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE);gl.depthMask(false);
 for(const h of haloBuffers){gl.bindBuffer(gl.ARRAY_BUFFER,h.buffer);for(const [name,off] of [['aPos',0],['aColor',12]]){let loc=gl.getAttribLocation(glowProgram,name);gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,3,gl.FLOAT,false,24,off)}gl.uniform1f(glowAlpha,h.alpha*(evening?1.25:1));gl.drawArrays(gl.TRIANGLES,0,h.count)}
 gl.depthMask(true);gl.disable(gl.BLEND);
}
document.getElementById('routeGlow').onclick=e=>{directionsGlow=!directionsGlow;e.currentTarget.classList.toggle('active',directionsGlow);e.currentTarget.setAttribute('aria-pressed',String(directionsGlow));dirty=true};
'''
s=s.replace('const shadowTex=gl.createTexture();',halo+'\nconst shadowTex=gl.createTexture();',1)
s=s.replace('drawBuffers(prog,false);placeLabels();','drawBuffers(prog,false);drawDirectionGlow();placeLabels();',1)
p.write_text(s,encoding='utf-8')
print('Direction glow and toggle added')
