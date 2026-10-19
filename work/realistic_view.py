from pathlib import Path
root=Path(__file__).resolve().parents[1];p=root/'work/viewer-pdf.html';s=p.read_text(encoding='utf-8')
s=s.replace('attribute vec3 aColor;uniform mat4 uVP;uniform mat4 uLightVP;', 'attribute vec3 aColor;attribute float aMaterial;varying float vMaterial;uniform mat4 uVP;uniform mat4 uLightVP;',1)
s=s.replace('vNormal=aNormal;vColor=aColor;', 'vMaterial=aMaterial;vNormal=aNormal;vColor=aColor;',1)
s=s.replace('const fs=`precision highp float;', 'const fs=`precision highp float;varying float vMaterial;uniform vec3 uEye;',1)
pos=s.index('float unpack(vec4 c)')
s=s[:pos]+'''vec3 surface(vec3 c,vec3 n){
 vec2 uv=abs(n.y)>.65?vWorld.xz:(abs(n.x)>.65?vWorld.zy:vWorld.xy);
 float fade=1.-smoothstep(80.,400.,length(uEye-vWorld));
 float grain=groundNoise(uv*8.)-.5;
 if(vMaterial>.5&&vMaterial<1.5){ // Asphalt aggregate, repaired areas and tyre wear.
  c*=.86+.2*groundNoise(uv*.12);c+=vec3(grain*.08*fade);
 }else if(vMaterial<2.5&&vMaterial>1.5){ // Canvas weave and broad tension folds.
  float folds=sin(uv.x*2.7+sin(uv.y*.2)*.25)*.025;
  float weave=sin(uv.x*90.)*sin(uv.y*110.)*.024*fade;
  c*=.96+folds+weave+grain*.045*fade;
 }else if(vMaterial>2.5&&vMaterial<3.5){
  c*=.94+groundNoise(uv*2.)*.09;c+=vec3(grain*.035*fade);
  float foot=1.-smoothstep(0.,1.1,abs(vWorld.y));c*=1.-foot*.13;
 }else if(vMaterial>5.5){
  c*=.88+.2*groundNoise(uv*vec2(.7,18.));
 }
 return c;
}
''' +s[pos:]
s=s.replace('vec3 lit=groundFinish(vColor)*(.62+diffuse*.43*(1.-occ*.62))*sun;', '''vec3 base=surface(groundFinish(vColor),n);float hemi=.36+.16*(n.y*.5+.5);vec3 lit=base*(hemi+diffuse*.58*(1.-occ*.72))*sun;vec3 viewDir=normalize(uEye-vWorld);if(vMaterial>3.5&&vMaterial<4.5){float fres=pow(1.-abs(dot(n,viewDir)),4.);vec3 reflection=mix(vec3(.19,.34,.38),vec3(.65,.81,.88),fres);lit=mix(lit,reflection,.48);vec3 halfV=normalize(uSun+viewDir);lit+=vec3(.8,.9,1.)*pow(max(dot(n,halfV),0.),80.)*.4;}''')
s=s.replace("float fog=clamp((vDepth-3100.)/6000.,0.,.15);gl_FragColor=vec4(mix(lit,uSky,fog),1.);", "float fog=1.-exp(-max(vDepth-100.,0.)*.00010);lit=lit/(lit+vec3(.32))*1.12;gl_FragColor=vec4(mix(lit,uSky,min(fog,.36)),1.);")
s=s.replace('function pushTri(group,pts,n,color){for(const p of pts)group.push(...p,...n,...color)}', '''function pushTri(group,pts,n,color,material=0){for(const p of pts)group.push(...p,...n,...color,material)}
function materialFor(o){const n=o.name.toLowerCase();if(/glaz|windscreen|window glass|entrance door/.test(n))return 4;if(o.layer==='tents'||/fabric|canvas|pandal curved/.test(n))return 2;if(/rail|sleeper|timber/.test(n))return 6;if(/asphalt|carriageway|road surface|paved|parking.*surface/.test(n))return 1;if(['services','toilets','gates','frontage','context'].includes(o.layer))return 3;return 0}''')
s=s.replace('vv[f[k+1]]],n,color)', 'vv[f[k+1]]],n,color,materialFor(o))')
s=s.replace('count:a.length/9','count:a.length/10').replace('triangles+=a.length/27','triangles+=a.length/30')
s=s.replace("['aColor',3,24]", "['aColor',3,24],['aMaterial',1,36]")
s=s.replace('gl.FLOAT,false,36,offset','gl.FLOAT,false,40,offset')
s=s.replace("'uPandalGlow'])uniforms", "'uPandalGlow','uEye'])uniforms")
s=s.replace('gl.uniformMatrix4fv(uniforms.uVP,false,currentVP);', 'gl.uniform3fv(uniforms.uEye,eye);gl.uniformMatrix4fv(uniforms.uVP,false,currentVP);')
# Render atmospheric sky behind the model, using the same camera basis.
pos=s.index('const groups=new Map();')
s=s[:pos]+'''const skyProgram=program('attribute vec2 p;varying vec2 uv;void main(){uv=p;gl_Position=vec4(p,.9999,1.);}',`precision highp float;varying vec2 uv;uniform vec3 forward;uniform vec3 right;uniform vec3 up;uniform float aspectRatio;uniform float fov;uniform float dusk;
float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hash(i),hash(i+vec2(1.,0.)),f.x),mix(hash(i+vec2(0.,1.)),hash(i+1.),f.x),f.y);}
void main(){vec3 ray=normalize(forward+right*uv.x*aspectRatio*fov+up*uv.y*fov);float h=max(ray.y,0.);vec3 sky=mix(vec3(.83,.86,.82),vec3(.32,.57,.78),pow(h,.45));vec2 q=ray.xz/max(ray.y+.12,.08)*1.7;float cloud=noise(q)+noise(q*2.03)*.5+noise(q*4.1)*.25;float c=smoothstep(.92,1.3,cloud)*smoothstep(0.,.28,ray.y);sky=mix(sky,vec3(.96,.95,.89),c*.65);vec3 sun=normalize(vec3(-.65,1.,.55));float sd=max(dot(ray,sun),0.);sky+=vec3(1.,.78,.45)*pow(sd,220.)*.5;sky=mix(sky,sky*vec3(.77,.64,.66)+vec3(.15,.05,.015),dusk);gl_FragColor=vec4(sky,1.);}`);
const skyBuffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,skyBuffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);
function drawSky(at){const f=norm(vsub(at,eye)),r=norm(cross(f,[0,1,0])),u=cross(r,f);gl.disable(gl.DEPTH_TEST);gl.useProgram(skyProgram);gl.bindBuffer(gl.ARRAY_BUFFER,skyBuffer);const loc=gl.getAttribLocation(skyProgram,'p');gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,2,gl.FLOAT,false,8,0);for(const [n,v] of [['forward',f],['right',r],['up',u]])gl.uniform3fv(gl.getUniformLocation(skyProgram,n),v);gl.uniform1f(gl.getUniformLocation(skyProgram,'aspectRatio'),aspect);gl.uniform1f(gl.getUniformLocation(skyProgram,'fov'),Math.tan((streetMode?1.05:.72)/2));gl.uniform1f(gl.getUniformLocation(skyProgram,'dusk'),evening?1:0);gl.drawArrays(gl.TRIANGLES,0,6);gl.enable(gl.DEPTH_TEST)}
''' +s[pos:]
s=s.replace('const view=lookAt(eye,at);','drawSky(at);const view=lookAt(eye,at);')
p.write_text(s,encoding='utf-8')
print('Procedural material textures, reflective glass, atmospheric sky and lighting added')
