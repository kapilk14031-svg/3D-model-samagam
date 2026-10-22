from pathlib import Path
import subprocess,json,math
root=Path(__file__).resolve().parents[1];s=(root/'work/viewer-pdf.html').read_text(encoding='utf-8')
functions='\n'.join(next(l for l in s.splitlines() if l.startswith('function '+name+'(')) for name in ['depPose','depMoveUnit','depVehicleShot'])
manual=s[s.index('function depEnterObjectControl('):s.index("depEl('depViewSave').onclick")]
code=r'''
const assert=require('node:assert/strict');
let depFollowState=null,depVehicleCamera=null,depTime=10,depUnits=[],dirty=false,saved=0,undo=0;
const heldKeys=new Set(),depPausedRoutes=new Map(),depRouteEpoch=new Map(),canvas={dataset:{}};let depDragPause=null;
function depEl(){return {textContent:''}};function depPersist(){saved++};function depUndoPush(){undo++};function depFollowTick(){};
function depEnterVehicleView(id,mode){depFinishManualControl();depFollowState={id,mode}}
function unit(type,route=[]){return {id:type,type,position:[0,1,0],rotation:0,scale:1,speed:2,route,routeMode:'pingpong'}}
function tick(f=0,side=0,turn=0,n=60){for(let i=0;i<n;i++)depManualTick(1/60,{forward:f,side,turn})}
'''+functions+'\n'+manual+r'''
for(const type of ['machan','morcha','barricade','naka','officer','rider','qrt','patrol','ambulance','fire','parking']){
 depFollowState=null;depUnits=[unit(type)];const u=depUnits[0];depEnterObjectControl(u.id);assert.equal(depFollowState.mode,'third');
 tick(1);assert(Math.abs(u.position[2]-(type==='rider'||type==='patrol'||type==='qrt'?10:5))<1e-7);
 const old=[...u.position];tick(0,1);assert(u.position[0]<old[0]&&Math.abs(u.position[2]-old[2])<1e-7,'screen-relative right');
 tick(0,0,1);assert(Math.abs(u.rotation+1.15)<1e-7);const pose=depPose(u);assert.deepEqual(pose.p,u.position);assert.equal(pose.angle,u.rotation);
 const ground=u.position[1];depManualJump();tick(0,0,0,15);assert(depPose(u).p[1]>ground+1);const airborneVelocity=depFollowState.manual.jump.velocity;depManualJump();assert.equal(depFollowState.manual.jump.velocity,airborneVelocity,'no repeated airborne jump');tick(0,0,0,90);assert.equal(depPose(u).p[1],ground);assert.equal(u.position[1],ground,'jump never saves elevated Y');
 tick(1);const before=saved;tick();assert(saved>before,'idle autosave');tick(1);depFinishManualControl();assert.equal(depFollowState.manual,null);assert.deepEqual(depPose(u).p,u.position);
}
// Route must stay paused, move/rotate as a complete plan, then continue at the
// adjusted location without losing its points or jumping when control exits.
depFollowState=null;depUnits=[unit('patrol',[[0,1,0],[0,1,100]])];let u=depUnits[0],pose=depPose(u);assert.equal(pose.p[2],20);
depEnterObjectControl(u.id);assert(depPausedRoutes.has(u.id));tick(1);depTime+=5;assert(Math.abs(depPose(u).p[2]-30)<1e-7);tick(0,0,1);pose=depPose(u);const lengths=Math.hypot(u.route[1][0]-u.route[0][0],u.route[1][2]-u.route[0][2]);assert(Math.abs(lengths-100)<1e-7);depFinishManualControl();const after=depPose(u);assert(Math.hypot(after.p[0]-pose.p[0],after.p[2]-pose.p[2])<1e-7);assert(Math.abs(after.angle-pose.angle)<1e-7);assert.equal(u.route.length,2);
console.log('PASS: 11 deployment types, object-relative keyboard placement, rotation, idle save, manual pose, whole-route translation/rotation, paused route and no exit jump');
'''
p=root/'work/test-object-keyboard.cjs';p.write_text(code,encoding='utf-8');subprocess.run(['C:/Program Files/nodejs/node.exe',str(p)],check=True)
# Native UI fixture has its own local plan key; never changes the user's duty data.
html=(root/'outputs/samagam-3d.html').read_text(encoding='utf-8').replace("const DEP_KEY='samagam-duty-deployment-v1'", "const DEP_KEY='samagam-object-control-qa-v1'")
setup=r'''setTimeout(()=>{if(!localStorage.getItem(DEP_KEY)){depUnits=[{id:'QA-MACHAN',title:'QA Machaan',type:'machan',position:[340,1.3,195],rotation:0,scale:1,enabled:true,speed:2,route:[],routeMode:'pingpong',ground:'',personnel:[],notes:'Isolated UI test',shifts:{day:{force:1,incharge:0,extra:0}}}];}depDirty=true;depSelected='QA-MACHAN';depMode=null;depRoutebar.hidden=true;depOpen(depSelected);depEl('depLocate').click();const o=document.createElement('output');o.id='qaState';o.style.cssText='position:fixed;top:0;left:0;z-index:99;background:white;font-size:9px;max-width:90vw';document.body.append(o);setInterval(()=>{const u=depUnits.find(v=>v.id==='QA-MACHAN');o.textContent=JSON.stringify({position:u.position,rotation:u.rotation,manual:!!depFollowState?.manual,following:!!depFollowState,saved:!!localStorage.getItem(DEP_KEY)})},100)},100);'''
html=html.replace('</script>',setup+'</script>');(root/'work/object-control-qa.html').write_text(html,encoding='utf-8')
# Geometric alignment is exact: local gate span is parallel to the boundary and
# the centre lies on it. Gate openings end where their boundary returns end.
d=json.loads((root/'outputs/scene-data.json').read_text(encoding='utf-8'))
for f in d['features']:
 if f['id'] not in ['G01','G02']:continue
 a=f['gateAlignment'];assert math.dist([f['world'][0],0,f['world'][2]],a['boundaryCentre'])<1e-7
 assert abs(math.cos(a['angle'])*a['tangent'][1]+math.sin(a['angle'])*a['tangent'][0])<1e-7
 assert all(abs(o.get('rotY',0)-a['angle'])<1e-7 for o in d['objects'] if o['featureId']==f['id'])
 print(f['id'],'aligned to boundary, shift',round(math.dist(f['world'],a['sourceWorld']),2),'units')
print('PASS: both gate planes/anchors parallel and centred on the highway boundary')
