from pathlib import Path
root=Path(__file__).resolve().parents[1];p=root/'work/viewer-pdf.html';s=p.read_text(encoding='utf-8')
a=s.index('vec3 groundFinish(');b=s.index('vec3 surface(',a)
s=s[:a]+'''vec3 groundFinish(vec3 base){
 bool terrain=distance(base,pow(vec3(155./255.,128./255.,92./255.),vec3(2.2)))<.02;
 bool plot=distance(base,pow(vec3(155./255.,158./255.,123./255.),vec3(2.2)))<.02;
 if(!terrain&&!plot)return base;
 vec2 p=vWorld.xz;
 // Domain-warped soil strata: irregular edges rather than round noise blobs.
 vec2 warp=vec2(groundFbm(p*.021+13.),groundFbm(p*.023-29.))*23.;
 float broad=groundFbm((p+warp)*.014);
 float medium=groundFbm((p+warp)*.070+31.);
 float dry=groundFbm(p*.19+7.);
 float closeFade=1.-smoothstep(45.,260.,length(uEye-vWorld));
 vec3 loam=mix(vec3(.155,.094,.044),vec3(.285,.195,.105),smoothstep(.22,.73,medium));
 vec3 dust=mix(vec3(.31,.235,.145),vec3(.37,.285,.18),dry);
 vec3 earth=mix(loam,dust,smoothstep(.47,.68,broad)*.72);
 float grassMask=(1.-smoothstep(.30,.43,broad))*smoothstep(.29,.60,medium);
 vec3 grass=mix(vec3(.10,.125,.045),vec3(.175,.19,.078),dry);
 vec3 col=mix(earth,grass,grassMask*.78);
 float straw=smoothstep(.64,.79,groundFbm(p*.12+61.))*.22;
 col=mix(col,vec3(.265,.235,.13),straw);
 // Distant grit is filtered out; close views retain small mineral grains.
 float grit=groundNoise(p*6.1)-.5;
 col*=1.+grit*.20*closeFade;
 vec2 cell=floor(p*2.3);vec2 f=fract(p*2.3);
 vec2 centre=vec2(groundHash(cell+3.),groundHash(cell+79.))*.6+.2;
 float pebble=(1.-smoothstep(.045,.095,length((f-centre)*vec2(1.,1.5))))*step(.87,groundHash(cell+117.))*closeFade;
 col=mix(col,vec3(.28,.25,.19),pebble*.55);
 return col;
}
''' + s[b:]
s=s.replace('float bumpFade=1.-smoothstep(40.,380.,length(uEye-vWorld));','float bumpFade=1.-smoothstep(55.,420.,length(uEye-vWorld));')
s=s.replace('pow(max(dot(n,halfV),0.),16.)*.045','pow(max(dot(n,halfV),0.),16.)*.015')
s=s.replace("*.12;\n  lit+=(vec3(.85,1.,.72)","*.035;\n  lit+=(vec3(.85,1.,.72)")
p.write_text(s,encoding='utf-8')
# Reuse existing geometric data; this change only affects the interactive material.
import json
out=root/'outputs';old=(out/'samagam-3d.html').read_text(encoding='utf-8')
shapes=old.split(',SHAPES=',1)[1].split(';\nconst canvas',1)[0]
s=s.replace('__SCENE__',json.dumps(json.loads((out/'scene-data.json').read_text(encoding='utf-8')),separators=(',',':'))).replace('__SHAPES__',shapes)
(out/'samagam-3d.html').write_text(s,encoding='utf-8')
(root/'work/viewer-check.js').write_text(s.split('<script>',1)[1].split('</script>',1)[0],encoding='utf-8')
print('Natural layered earth material installed')
