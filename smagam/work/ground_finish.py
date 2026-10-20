from pathlib import Path
root=Path(__file__).resolve().parent
p=root/'build_pdf_model.py';s=p.read_text(encoding='utf-8').replace("1950,2500,2,'#b8c1a4'","1950,2500,2,'#a2b482'")
s=s.replace("flyover_info={'local_anchor'", "meta['ground_finish']='Illustrative grass, dry turf and exposed soil shading in the interactive viewer; not mapped land-cover evidence. GLB retains a grass-coloured base surface.'\nflyover_info={'local_anchor'")
p.write_text(s,encoding='utf-8')
p=root/'viewer-pdf.html';s=p.read_text(encoding='utf-8')
noise='''
float groundHash(vec2 p){p=fract(p*vec2(123.34,456.21));p+=dot(p,p+45.32);return fract(p.x*p.y);}
float groundNoise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(groundHash(i),groundHash(i+vec2(1.,0.)),f.x),mix(groundHash(i+vec2(0.,1.)),groundHash(i+vec2(1.,1.)),f.x),f.y);}
float groundFbm(vec2 p){return .55*groundNoise(p)+.27*groundNoise(p*2.04+17.)+.12*groundNoise(p*4.17+39.)+.06*groundNoise(p*8.3);}
vec3 groundFinish(vec3 base){
  if(distance(base,vec3(162./255.,180./255.,130./255.))>.012)return base;
  vec2 pos=vWorld.xz;
  float patches=groundFbm(pos*.013+11.);
  float turf=groundFbm(pos*.045);
  float grit=groundNoise(pos*.65);
  vec3 grass=mix(vec3(.40,.50,.29),vec3(.59,.64,.40),turf);
  vec3 dry=mix(vec3(.64,.60,.43),vec3(.69,.63,.46),turf);
  vec3 soil=mix(vec3(.51,.42,.30),vec3(.68,.57,.40),groundFbm(pos*.08+82.));
  vec3 finish=mix(grass,dry,smoothstep(.38,.59,patches)*.68);
  finish=mix(finish,soil,smoothstep(.53,.69,patches));
  finish*=.955+.09*grit;
  // Fine elongated variation gives close-up turf a subtle blade-like grain.
  finish+=vec3(.016,.021,.008)*(groundNoise(pos*vec2(2.6,.42))-.5);
  return finish;
}
'''
s=s.replace('float unpack(vec4 c)',noise+'float unpack(vec4 c)',1)
s=s.replace('vec3 lit=vColor*(.62+', 'vec3 lit=groundFinish(vColor)*(.62+',1)
p.write_text(s,encoding='utf-8')
print('Grass / earth ground finish added')
