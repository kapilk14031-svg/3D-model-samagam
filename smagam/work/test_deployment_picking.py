from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8').replace("depEsc(DEP_TYPES[u.type])}${u.ground?", "depEsc((u.parentId&&depUnits.find(v=>v.id===u.parentId)?.title)||DEP_TYPES[u.type])}${u.ground?",1);p.write_text(s,encoding='utf-8')
# Pure name-card and model-picking checks run without the browser renderer.
lines=s.splitlines();pick=['depScreenRay','depHitDimensions','deploymentModelHit','depDragPlanePoint'];fns='\n'.join(next(l for l in lines if l.startswith('function '+n+'(')) for n in pick)
pre="""const assert=require('assert');const norm=v=>{let l=Math.hypot(...v);return v.map(x=>x/l)},vsub=(a,b)=>a.map((v,i)=>v-b[i]),dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];let depFollowState=null,depVehicleCamera=null;let eye=[0,8,30],target=[0,1.7,0],streetMode=false,topView=false,W=1000,H=800,aspect=1.25,distance=35,walker=[0,0,0],depVisible=true,depModelsOn=true,depMode=null,boxMode=false,placeStreet=false;let depUnits=[{id:'p',type:'officer',position:[0,0,0],rotation:0,scale:1,route:[]}];const depApplicable=()=>true,depPose=u=>({p:u.position,angle:u.rotation});
"""
test="""let h=deploymentModelHit(500,400);assert(h&&h.unit.id==='p');assert(!deploymentModelHit(10,10));for(const type of['machan','morcha','qrt','rider','patrol']){depUnits[0].type=type;assert(deploymentModelHit(500,400),'hit '+type)}depUnits[0].position=[30,0,0];assert(!deploymentModelHit(500,400));console.log('PASS: direct 3D ray picking for officer, Machaan, Morcha, QRT, rider and patrol; miss tests');
"""
Path('work/test-deployment-picking.cjs').write_text(pre+fns+test,encoding='utf-8')
# Retain the final canonical panel source in the editable source package.
a=s.index('// Editable local duty plan.');b=s.index('// Screen-space minimum width',a);addon=s[a:b];start=addon.index('const DEPLOYMENT_SEED=');end=addon.index('\nconst DEP_TYPES',start);addon=addon[:start]+'const DEPLOYMENT_SEED=__DUTY_SEED__;'+addon[end:];Path('work/deployment_panel.js').write_text(addon,encoding='utf-8')
