from pathlib import Path
s=Path('work/viewer-pdf.html').read_text(encoding='utf-8')
shot='\n'.join(next(l for l in s.splitlines() if l.startswith('function '+name+'(')) for name in ['depVehicleShot','depSmoothHeading'])
code="const assert=require('node:assert/strict');\n"+shot+"\n"+'''
for(const type of ['rider','qrt','patrol']){const pose={p:[10,1,20],angle:0},f=depVehicleShot(pose,type,'fpv'),third=depVehicleShot(pose,type,'third');assert(f.eye[2]>20&&f.at[2]>f.eye[2]);assert(third.eye[2]<20&&third.at[2]>20);assert(third.eye[1]>f.eye[1]);const east=depVehicleShot({...pose,angle:Math.PI/2},type,'fpv');assert(east.at[0]>east.eye[0]);assert(Math.abs(east.at[2]-east.eye[2])<1e-7);const turn=depVehicleShot(pose,type,'fpv',Math.PI/2);assert(turn.at[0]>turn.eye[0]);const zoom=depVehicleShot(pose,type,'third',0,0,9);assert(Math.abs(zoom.eye[2]-20)<Math.abs(third.eye[2]-20));const moved=depVehicleShot({p:[30,1,50],angle:0},type,'third');assert.equal(moved.eye[0]-third.eye[0],20);assert.equal(moved.eye[2]-third.eye[2],30)}
assert(Math.abs(depSmoothHeading(179*Math.PI/180,-179*Math.PI/180,.016)-179*Math.PI/180)<.01);
console.log('PASS: rider/QRT/patrol FPV and chase transforms, short-angle heading, look-around, zoom and tracking displacement');
'''
Path('work/test-vehicle-views.cjs').write_text(code,encoding='utf-8')
# Isolate user data; initialize one moving fixture with the production camera controls.
html=Path('outputs/samagam-3d.html').read_text(encoding='utf-8').replace("const DEP_KEY='samagam-duty-deployment-v1'", "const DEP_KEY='samagam-vehicle-view-qa'")
setup="""setTimeout(()=>{const t=new URLSearchParams(location.search).get('vehicle')||'patrol';depUnits=[{id:'QA-VEHICLE',title:t+' · camera check',type:t,position:[340,1.3,195],rotation:0,scale:1,enabled:true,speed:1,route:[[340,1.3,195],[340,1.3,255]],routeMode:'pingpong',ground:'',personnel:[],notes:'Isolated camera verification',shifts:{day:{force:null,incharge:null,extra:0}}}];depDirty=true;depSelected='QA-VEHICLE';depMode=null;depRoutebar.hidden=true;depOpen(depSelected);depEl('depLocate').click()},100);"""
html=html.replace('</script>',setup+'</script>');Path('work/vehicle-view-qa.html').write_text(html,encoding='utf-8')
