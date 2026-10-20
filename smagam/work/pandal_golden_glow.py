from pathlib import Path
root=Path(__file__).resolve().parent
p=root/'build_pdf_model.py';s=p.read_text(encoding='utf-8');needle='# User-requested facility identification colours.'
block='''# Golden-brown pandal fabric with warm golden illumination.
gold_bay=0
for o in objects:
    if o['layer']!='pandal':continue
    if o['name']=='Pandal curved fabric roof':
        o['color']='#b78743' if gold_bay%2==0 else '#c69a55';gold_bay+=1
    elif 'fabric valance' in o['name'] or 'wine fabric valance' in o['name']:o['color']='#805230'
    elif 'Curved canopy rib' in o['name'] or 'Golden canopy border' in o['name']:o['color']='#d6b16a'
'''
s=s.replace(needle,block+needle,1)
s=s.replace('exec(export)',"export=export.replace('else [0,0,0]',\"else ([.35,.19,.045] if color in ['#b78743','#c69a55'] else [0,0,0])\")\nexec(export)",1)
p.write_text(s,encoding='utf-8')
p=root/'viewer-pdf.html';s=p.read_text(encoding='utf-8')
s=s.replace('<button id="routeGlow"', '<button id="pandalGlow" class="active" aria-pressed="true">Pandal glow</button><button id="routeGlow"',1)
s=s.replace('uniform float uRouteGlow;', 'uniform float uRouteGlow;uniform float uPandalGlow;',1)
s=s.replace("let directionsGlow=true;", "let directionsGlow=true,pandalGlow=true;")
s=s.replace("'uShadow','uRouteGlow'", "'uShadow','uRouteGlow','uPandalGlow'")
s=s.replace("gl.uniform1f(uniforms.uRouteGlow,directionsGlow?1:0);", "gl.uniform1f(uniforms.uRouteGlow,directionsGlow?1:0);gl.uniform1f(uniforms.uPandalGlow,pandalGlow?1:0);")
gold="if(uPandalGlow>.5&&(distance(vColor,vec3(183./255.,135./255.,67./255.))<.012||distance(vColor,vec3(198./255.,154./255.,85./255.))<.012)){lit=mix(lit,vColor*1.03+vec3(.16,.075,.012),.7);}" 
s=s.replace('lit+=vec3(.16,.09,.025)',gold+'lit+=vec3(.16,.09,.025)',1)
halo='''
for(const [width,alpha] of [[3.8,.035],[2.2,.07],[.8,.16]]){
 let verts=[];const put=p=>verts.push(...p,1.,.59,.16);
 for(const o of DATA.objects.filter(o=>o.name==='Pandal curved fabric roof')){
  for(const side of [-1,1]){
   let pts=[];for(let j=0;j<=32;j++){let q=j/32-.5;pts.push([o.p[0]+q*o.s[0],o.p[1]+Math.sqrt(Math.max(0,1-4*q*q))*o.s[1]+.16,o.p[2]+side*o.s[2]/2])}
   for(let j=1;j<pts.length;j++){
    const a=pts[j-1],b=pts[j],v=[[a[0],a[1],a[2]-width/2],[b[0],b[1],b[2]-width/2],[b[0],b[1],b[2]+width/2],[a[0],a[1],a[2]+width/2]];
    for(const k of [0,1,2,0,2,3])put(v[k]);
   }
  }
 }
 const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(verts),gl.STATIC_DRAW);haloBuffers.push({buffer,count:verts.length/6,alpha,pandal:true});
}
document.getElementById('pandalGlow').onclick=e=>{pandalGlow=!pandalGlow;e.currentTarget.classList.toggle('active',pandalGlow);e.currentTarget.setAttribute('aria-pressed',String(pandalGlow));dirty=true};
'''
s=s.replace('function drawDirectionGlow(){',halo+'\nfunction drawDirectionGlow(){',1)
s=s.replace("if(!directionsGlow||hidden.has('traffic'))return;", "if(!directionsGlow&&!pandalGlow)return;")
s=s.replace('for(const h of haloBuffers){gl.bindBuffer',"for(const h of haloBuffers){if(h.pandal?(!pandalGlow||cutaway||hidden.has('pandal')):(!directionsGlow||hidden.has('traffic')))continue;gl.bindBuffer",1)
p.write_text(s,encoding='utf-8')
print('Golden-brown fabric and warm pandal glow added')
