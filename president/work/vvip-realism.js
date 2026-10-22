// Visual rehearsal engine. No aircraft performance or protective protocol certification.
var vvipReal;
function buildRoutePolice(){return new THREE.Group();} // Use the user's deployed officers, not duplicate scripted guards.
function buildRoadBarricades(){return new THREE.Group();} // Keep the actual editable barricade layer.
function vrClamp(t){return Math.max(0,Math.min(1,t));}
function vrEase(t){t=vrClamp(t);return t*t*(3-2*t);}
function vrMix(a,b,t){return a.map((v,i)=>v+(b[i]-v)*t);}
function vrBox(parent,mat,p,s){const m=new THREE.Mesh(geos.box,mat);m.position.fromArray(p);m.scale.fromArray(s);parent.add(m);return m;}
function vrSphere(parent,mat,p,s){const m=new THREE.Mesh(geos.sphereSmooth,mat);m.position.fromArray(p);m.scale.fromArray(s);parent.add(m);return m;}
function vrLimb(parent,mat,a,b,r){const m=new THREE.Mesh(geos.cylinder,mat);parent.add(m);m.userData.between=(a,b)=>{const v=new THREE.Vector3().subVectors(b,a);m.position.copy(a).add(b).multiplyScalar(.5);m.scale.set(r,v.length(),r);m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),v.normalize());};return m;}
function vrActor(female=false){
 const g=new THREE.Group(),upper=new THREE.Group();g.add(upper);
 const cloth=female?depMaterials.vipSaree:depMaterials.dark,skin=depMaterials.skin;
 vrBox(upper,cloth,[0,.27,0],[female?.34:.43,.49,.23]);
 const head=vrSphere(upper,skin,[0,.68,0],[.115,.145,.112]);
 vrSphere(upper,depMaterials.hair,[0,.73,-.045],[.12,.105,.105]);
 vrSphere(upper,skin,[0,.67,.112],[.025,.03,.035]);
 if(female){
  vrSphere(upper,depMaterials.hair,[0,.66,-.14],[.085,.08,.07]);
  for(const x of [-.12,.12])vrSphere(upper,depMaterials.vipGold,[x,.64,0],[.018,.028,.018]);
  const sash=vrBox(upper,depMaterials.vipPallu,[.02,.28,.13],[.15,.52,.035]);sash.rotation.z=-.48;
 }else{
  vrBox(upper,depMaterials.white,[0,.34,.125],[.15,.32,.02]);
  vrBox(upper,depMaterials.dark,[0,.30,.14],[.045,.27,.02]);
  vrBox(upper,depMaterials.dark,[0,.70,.11],[.215,.04,.025]);
 }
 const pallu=female?vrBox(upper,depMaterials.vipPallu,[.15,.15,-.13],[.14,.68,.035]):null;
 const legs=[],arms=[];
 for(const side of [-1,1]){
  const thigh=vrLimb(g,cloth,null,null,.075),shin=vrLimb(g,cloth,null,null,.065);
  const foot=vrBox(g,female?depMaterials.vipGold:depMaterials.dark,[side*.1,.035,.04],[.12,.065,.23]);
  legs.push({side,thigh,shin,foot});
  const arm=new THREE.Group();arm.position.set(side*(female?.205:.255),.47,0);upper.add(arm);
  vrLimb(arm,cloth,null,null,.045).userData.between(new THREE.Vector3(),new THREE.Vector3(0,-.27,0));
  const fore=vrLimb(arm,skin,null,null,.036);fore.userData.between(new THREE.Vector3(0,-.27,0),new THREE.Vector3(0,-.5,.035));
  vrSphere(arm,skin,[0,-.51,.04],[.04,.055,.035]);arms.push(arm);
 }
 const skirt=female?new THREE.Mesh(new THREE.CylinderGeometry(.19,.285,.85,20,3,true),depMaterials.vipSaree):null;
 if(skirt){g.add(skirt);skirt.position.y=.48;const hem=new THREE.Mesh(new THREE.CylinderGeometry(.279,.287,.045,20,1,true),depMaterials.vipGold);hem.position.y=.075;g.add(hem);g.userData.hem=hem;}
 g.userData.pose=(distance=0,walk=0,seated=0,bend=0)=>{
  seated=vrClamp(seated);const run=g.userData.run||0,stride=.80+.80*run,phase=distance/stride*Math.PI*2;
  const hip=.86-.34*seated-.055*run;upper.position.y=hip;upper.rotation.x=bend*.42+.10*run;
  for(const l of legs){
   const q=(phase+(l.side===1?Math.PI:0))%(Math.PI*2),cycle=q/(Math.PI*2);
   // Planted half-stride, then a lifted recovery. Phase derives from travelled distance.
   const fraction=.60-.15*run,half=stride*fraction/2,stance=cycle<fraction,local=stance?cycle/fraction:(cycle-fraction)/(1-fraction);
   const z=(stance?half-half*2*local:-half+half*2*vrEase(local))*walk;
   const y=stance?0:Math.sin(local*Math.PI)*(.12+.07*run)*walk;
   const ankle=new THREE.Vector3(l.side*.10,.034+y,z+.36*seated);
   if(!seated&&g.parent===vvipGroup&&vvipReal){
    const c=Math.cos(g.rotation.y),s=Math.sin(g.rotation.y),wx=g.position.x+c*ankle.x+s*ankle.z,wz=g.position.z-s*ankle.x+c*ankle.z;
    const ground=vrSurface(wx,wz,g.position.y-.012)-g.position.y;
    ankle.y+=Math.max(-.24,Math.min(.24,ground));
   }
   const h=new THREE.Vector3(l.side*.10,hip,0),delta=ankle.clone().sub(h),len=Math.min(.815,Math.max(.1,delta.length()));
   const mid=h.clone().add(ankle).multiplyScalar(.5),height=Math.sqrt(Math.max(0,.415*.415-len*len/4));
   const normal=new THREE.Vector3(0,-delta.z,delta.y).normalize().multiplyScalar(-height);
   const knee=mid.add(normal);l.thigh.userData.between(h,knee);l.shin.userData.between(knee,ankle);
   l.foot.position.copy(ankle);l.foot.position.z+=.055;
  }
  arms.forEach((a,i)=>{a.rotation.x=(i?1:-1)*Math.sin(phase)*(.18+.22*run)*walk-.65*bend-.45*seated;});
  head.rotation.y=walk?Math.sin(distance*.6)*.025:Math.sin((vvipReal?.elapsed||0)*.7)*.035;
  if(skirt){skirt.position.set(0,.48-.18*seated,.15*seated);skirt.scale.set(1,1-.40*seated,1+.45*seated);skirt.rotation.x=-.30*seated;g.userData.hem.visible=seated<.15;}
  if(pallu)pallu.rotation.x=Math.sin(phase)*.035*walk;
 };
 g.userData.animateWalk=p=>g.userData.pose(p*1.05/(Math.PI*2),1,0,0);
 g.userData.setSeated=b=>g.userData.pose(0,0,b?1:0,0);
 g.userData.arms=arms;g.userData.upper=upper;
 g.userData.pose();return g;
}
function buildFemaleVvip(){return vrActor(true);}
function buildSecurityEscort(){return vrActor(false);}

function buildVvipCar(){
 const g=new THREE.Group(),m=depMaterials.vipCar,glass=depMaterials.vipGlass.clone();glass.transparent=true;glass.opacity=.32;glass.depthWrite=false;
 vrBox(g,m,[0,.39,0],[2.04,.18,5.1]); // cabin floor, no solid block across the doorway
 vrBox(g,m,[0,.76,1.94],[2.04,.62,1.22]);vrBox(g,m,[0,.72,-2.10],[2.04,.52,.94]);
 vrBox(g,m,[0,1.69,-.12],[1.93,.09,3.04]);
 for(const x of [-.96,.96])for(const z of [-1.62,-.05,1.32])vrBox(g,m,[x,1.19,z],[.07,1.0,.08]);
 for(const z of [-1.66,1.35])vrBox(g,glass,[0,1.30,z],[1.83,.62,.045]);
 const doors=[];
 for(const [side,z] of [[-1,-.80],[1,-.80],[1,.69],[-1,.69]]){
  const pivot=new THREE.Group();pivot.position.set(side*1.025,.48,z+.68);g.add(pivot);
  vrBox(pivot,m,[0,.24,-.68],[.065,.48,1.35]);vrBox(pivot,glass,[0,.83,-.68],[.04,.59,1.30]);
  vrBox(pivot,depMaterials.vipChrome,[side*.045,.45,-1.12],[.06,.06,.24]);
  doors.push({pivot,side,z,open:0});
 }
 const seats=[[-.46,.25,-.8],[.46,.25,-.8],[.46,.25,.69],[-.46,.25,.69]];
 for(const p of seats){vrBox(g,depMaterials.dark,[p[0],.67,p[2]],[.64,.16,.60]);vrBox(g,depMaterials.dark,[p[0],1.03,p[2]-.30],[.63,.65,.13]);}
 const wheels=[];
 for(const x of [-1.03,1.03])for(const z of [-1.65,1.65]){const w=new THREE.Group();w.position.set(x,.38,z);g.add(w);const tire=new THREE.Mesh(geos.cylinder,depMaterials.dark);tire.rotation.z=Math.PI/2;tire.scale.set(.38,.25,.38);w.add(tire);const rim=new THREE.Mesh(geos.cylinder,depMaterials.vipChrome);rim.rotation.z=Math.PI/2;rim.scale.set(.23,.27,.23);w.add(rim);wheels.push(w);}
 for(const x of [-.78,.78]){vrBox(g,depMaterials.white,[x,.78,2.57],[.36,.18,.04]);vrBox(g,depMaterials.red,[x,.72,-2.59],[.36,.17,.04]);}
 vrBox(g,depMaterials.vipChrome,[0,.70,2.57],[1.05,.32,.04]);
 // Neutral vehicle: no unsupported claim to an actual presidential vehicle or livery.
 const driver=vrActor(false);driver.userData.pose(0,0,1,0);driver.position.set(-.46,.25,.69);g.add(driver);
 g.userData.doors=doors;g.userData.seats=seats;g.userData.wheels=wheels;
 g.userData.setDoor=(i,t)=>{doors[i].open=vrClamp(t);doors[i].pivot.rotation.y=-doors[i].side*vrEase(t)*1.15;};
 g.userData.setPassengerDoor=t=>g.userData.setDoor(0,t);
 g.userData.passengerPoint=()=>vrWorld(g,[-1.85,0,-.80]);
 g.userData.rollWheels=d=>wheels.forEach(w=>w.rotation.x+=d/.38);
 return g;
}
function vrWorld(g,p){g.updateMatrixWorld(true);return g.localToWorld(new THREE.Vector3(...p));}
function vrHollowHeli(g,bodyUpper,bodyLower,stripe){
 g.remove(bodyUpper,bodyLower,stripe);
 vrBox(g,depMaterials.heliNavy,[0,1.03,0],[1.82,.12,3.7]);
 vrBox(g,depMaterials.heliWhite,[0,2.43,0],[1.90,.10,3.7]);
 vrBox(g,depMaterials.heliWhite,[0,1.72,-1.95],[1.83,1.45,.12]);
 vrBox(g,depMaterials.heliWhite,[.94,1.72,-.1],[.06,1.40,3.5]);
 for(const z of [-1.6,1.65])vrBox(g,depMaterials.heliWhite,[-.94,1.72,z],[.06,1.40,.60]);
 const door=new THREE.Group();door.position.set(-.98,1.08,1.30);g.add(door);
 vrBox(door,depMaterials.heliWhite,[0,.24,-.9],[.06,.48,1.8]);vrBox(door,depMaterials.vipGlass,[0,.95,-.9],[.045,.72,1.74]);
 vrBox(door,depMaterials.vipChrome,[-.05,.53,-1.5],[.06,.07,.23]);
 vrBox(g,depMaterials.vipChrome,[-1.18,.58,.3],[.43,.08,1.25]);
 g.userData.setDoor=t=>door.rotation.y=vrEase(t)*1.20;
 g.userData.door=door;
 // Correct visual navigation-light convention: port red, starboard green.
 const green=new THREE.MeshBasicMaterial({color:0x32d67b});vrSphere(g,green,[1.10,1.5,.3],[.08,.08,.08]);
 const pilot=vrActor(false);pilot.userData.pose(0,0,1,0);pilot.position.set(.38,1.02,1.5);g.add(pilot);g.userData.pilot=pilot;
}

function vrPath(points){
 const p=points.filter((p,i)=>!i||Math.hypot(...p.map((v,k)=>v-points[i-1][k]))>.001),lengths=[0];
 for(let i=1;i<p.length;i++)lengths.push(lengths.at(-1)+Math.hypot(...p[i].map((v,k)=>v-p[i-1][k])));
 return {p,lengths,total:lengths.at(-1)};
}
function vrRoundPath(points,radius=2){
 const out=[points[0]];
 for(let i=1;i<points.length-1;i++){
  const a=points[i-1],b=points[i],c=points[i+1],la=Math.hypot(...b.map((v,k)=>v-a[k])),lb=Math.hypot(...c.map((v,k)=>v-b[k])),trim=Math.min(radius,la*.25,lb*.25);
  const start=vrMix(b,a,trim/la),end=vrMix(b,c,trim/lb);out.push(start);
  for(let j=1;j<=10;j++){const t=j/10;out.push(start.map((v,k)=>(1-t)*(1-t)*v+2*(1-t)*t*b[k]+t*t*end[k]));}
 }
 out.push(points.at(-1));return vrPath(out);
}
function vrSample(path,d){
 d=Math.max(0,Math.min(path.total,d));let i=1;while(i<path.p.length-1&&path.lengths[i]<d)i++;
 const a=path.p[i-1],b=path.p[i],t=(d-path.lengths[i-1])/Math.max(.0001,path.lengths[i]-path.lengths[i-1]);
 return {pos:vrMix(a,b,t),angle:Math.atan2(b[0]-a[0],b[2]-a[2])};
}
function interpolateWaypoints(points,t){const path=vrPath(points);return vrSample(path,vrClamp(t)*path.total);}
function vrSurface(x,z,fallback=.16){
 let y=fallback;
 for(const o of vvipReal.surfaces){const dx=x-o.p[0],dz=z-o.p[2],r=o.rot||0,c=Math.cos(r),s=Math.sin(r),lx=c*dx-s*dz,lz=s*dx+c*dz;
  if(Math.abs(lx)<=o.s[0]/2+.015&&Math.abs(lz)<=o.s[2]/2+.015)y=Math.max(y,o.p[1]+o.s[1]/2);
 }
 const h=geo.helipadProposal;if(Math.hypot(x-h.centre[0],z-h.centre[1])<15.6)y=Math.max(y,.33);
 return y+.012;
}
function vrAngle(a,b,rate,dt){return a+Math.atan2(Math.sin(b-a),Math.cos(b-a))*(1-Math.exp(-rate*dt));}
function vrSegmentBox(a,b,o,radius=0){
 const bound=(o.s[0]+o.s[2])*.5+radius,vertical=o.s[1]*.5+radius;
 if(Math.max(a[0],b[0])<o.p[0]-bound||Math.min(a[0],b[0])>o.p[0]+bound||Math.max(a[2],b[2])<o.p[2]-bound||Math.min(a[2],b[2])>o.p[2]+bound||Math.max(a[1],b[1])<o.p[1]-vertical||Math.min(a[1],b[1])>o.p[1]+vertical)return null;
 const r=o.rot||0,c=Math.cos(r),s=Math.sin(r),local=p=>{const x=p[0]-o.p[0],z=p[2]-o.p[2];return [c*x-s*z,p[1]-o.p[1],s*x+c*z];};
 const u=local(a),v=local(b);let lo=0,hi=1;
 for(let k=0;k<3;k++){const extent=o.s[k]/2+radius,dir=v[k]-u[k];if(Math.abs(dir)<1e-7){if(Math.abs(u[k])>extent)return null;}else{let t1=(-extent-u[k])/dir,t2=(extent-u[k])/dir;if(t1>t2)[t1,t2]=[t2,t1];lo=Math.max(lo,t1);hi=Math.min(hi,t2);if(lo>hi)return null;}}
 return lo;
}
function vrBoxesOverlap(a,b,gap=0){
 if(Math.abs(a.p[1]-b.p[1])>(a.s[1]+b.s[1])/2+gap)return false;
 const axes=o=>[[Math.cos(o.rot||0),-Math.sin(o.rot||0)],[Math.sin(o.rot||0),Math.cos(o.rot||0)]],aa=axes(a),bb=axes(b),d=[b.p[0]-a.p[0],b.p[2]-a.p[2]];
 for(const axis of [...aa,...bb]){const dot=(u,v)=>u[0]*v[0]+u[1]*v[1],ra=Math.abs(dot(axis,aa[0]))*a.s[0]/2+Math.abs(dot(axis,aa[1]))*a.s[2]/2,rb=Math.abs(dot(axis,bb[0]))*b.s[0]/2+Math.abs(dot(axis,bb[1]))*b.s[2]/2;if(Math.abs(dot(d,axis))>ra+rb+gap)return false;}
 return true;
}
function vrVehicleSweep(a,b,heading,obstacle){
 const angle=heading-(obstacle.rot||0),c=Math.abs(Math.cos(angle)),s=Math.abs(Math.sin(angle));
 const expanded={...obstacle,s:[obstacle.s[0]+2*(c*1.1+s*2.7),obstacle.s[1]+1.65,obstacle.s[2]+2*(s*1.1+c*2.7)]};
 return vrSegmentBox([a[0],a[1]+.85,a[2]],[b[0],b[1]+.85,b[2]],expanded,.12)!==null;
}
function vrDynamicObstacles(ignore){
 const out=[];
 // Read deployment positions; never move or overwrite the user's saved deployment.
 for(const o of depItems){
  const node=depNodes.find(n=>n.item.id===o.id);if(node?.g.userData.vvipHidden)continue;
  const actual=node?.g.position||{x:o.x,y:o.y,z:o.z};
  const kind=o.kind,rot=(o.angle||0)*Math.PI/180;
  if(kind==='dfmd'){
   for(const x of [-.58,.58])out.push({p:[o.x+Math.cos(rot)*x,o.y+1.1,o.z-Math.sin(rot)*x],s:[.16,2.2,.40],rot});
   out.push({p:[o.x,o.y+2.2,o.z],s:[1.30,.18,.40],rot});
  }else{
   const person=['officer','armed_officer','hhmd','binocular','radio'].includes(kind),size=person?[.65,1.8,.65]:kind==='qrt'?[2.3,2.5,4.5]:kind==='xray'?[1.9,2.1,3.5]:kind==='ambulance'?[2.3,2.7,5.8]:kind==='firebrigade'?[2.6,3.6,7.2]:kind==='barricade'?[2.2,1.2,.7]:kind==='cone'?[.5,.8,.5]:[.8,1.3,.8];
   out.push({p:[actual.x,actual.y+size[1]/2,actual.z],s:size,rot,name:o.name,id:o.id});
  }
 }
 for(const actor of vvipReal.actors){if(actor===ignore||actor.parent!==vvipGroup)continue;out.push({p:[actor.position.x,actor.position.y+.85,actor.position.z],s:[.64,1.7,.64],rot:actor.rotation.y,name:actor.userData.role||'escort'});}
 if(vvipReal.host&&ignore!==vvipReal.host){const a=vvipReal.host;out.push({p:[a.position.x,a.position.y+.85,a.position.z],s:[.64,1.7,.64],rot:a.rotation.y});}
 return out;
}
function vrDoorMove(i,t,ignore){
 const door=vvipCar.userData.doors[i],turn=-door.side*vrEase(t)*1.15,point=vrWorld(vvipCar,[door.side*1.025-Math.sin(turn)*.68,1.05,door.z+.68-Math.cos(turn)*.68]);
 const box={p:point.toArray(),s:[.11,1.12,1.35],rot:vvipCar.rotation.y+turn};
 if([...vvipReal.walkObstacles,...vrDynamicObstacles(ignore)].some(o=>vrBoxesOverlap(box,o,.08))){vvipReal.blocked=true;return false;}
 vvipCar.userData.setDoor(i,t);return true;
}
function vrCamera(target,offset,dt){
 const aim=new THREE.Vector3(...target),desired=aim.clone().add(new THREE.Vector3(...offset));let nearest=1;
 for(const o of vvipReal.cameraObstacles){const hit=vrSegmentBox(target,desired.toArray(),o,.18);if(hit!==null&&hit>.025)nearest=Math.min(nearest,hit);}
 if(nearest<1)desired.copy(aim).lerp(desired,Math.max(.12,nearest-.04));
 desired.y=Math.max(desired.y,vrSurface(desired.x,desired.z,.15)+.40);
 // Check the actual interpolated position too, not only the desired shot.
 const candidate=camera.position.clone().lerp(desired,1-Math.exp(-4*dt));let blocked=false;
 for(const o of vvipReal.cameraObstacles)if(vrSegmentBox(target,candidate.toArray(),o,.12)!==null){blocked=true;break;}
 camera.position.copy(blocked?desired:candidate);controls.target.lerp(aim,1-Math.exp(-7*dt));
}
function vrMove(actor,path,d,speed,dt){
 const q=vrSample(path,d),last=actor.position.clone();
 const next=new THREE.Vector3(...q.pos);next.y=vrSurface(next.x,next.z,q.pos[1]-.012);
 // Ground-route collision guard at torso height. Pause instead of walking through a wall.
 const blockers=[...vvipReal.walkObstacles,...vrDynamicObstacles(actor),{p:[vvipCar.position.x,vvipCar.position.y+.85,vvipCar.position.z],s:[2.2,1.7,5.4],rot:vvipCar.rotation.y}];
 const obstruction=last.distanceTo(next)<2?blockers.find(o=>[.25,.70,1.25].some(h=>vrSegmentBox([last.x,last.y+h,last.z],[next.x,next.y+h,next.z],o,.15)!==null)):null;if(obstruction){if(!vvipReal.blocked){vvipReal.blockedName=(actor.userData.role||'person')+' → '+(obstruction.name||'nearby object');}vvipReal.blocked=true;return false;}
 actor.position.copy(next);actor.rotation.y=vrAngle(actor.rotation.y,q.angle,8,dt);
 actor.userData.distance=(actor.userData.distance||0)+last.distanceTo(next);
 actor.userData.run=vrClamp((speed-1.8)/1.3);actor.userData.pose(actor.userData.distance,speed>.02?Math.min(1,speed/.7):0,0,0);return true;
}
function vrAttach(actor,parent,p,seated=1){parent.add(actor);const scale=parent.getWorldScale(new THREE.Vector3());actor.scale.set(1/scale.x,1/scale.y,1/scale.z);actor.position.fromArray(p);actor.rotation.set(0,0,0);actor.userData.pose(0,0,seated,0);}
function vrDetach(actor){const pos=actor.getWorldPosition(new THREE.Vector3()),angle=actor.getWorldQuaternion(new THREE.Quaternion()),scale=actor.getWorldScale(new THREE.Vector3());vvipGroup.add(actor);actor.position.copy(pos);actor.quaternion.copy(angle);actor.scale.copy(scale);}
function vrContact(actor,size){
 const canvas=document.createElement('canvas');canvas.width=canvas.height=64;const cx=canvas.getContext('2d'),grad=cx.createRadialGradient(32,32,0,32,32,32);grad.addColorStop(0,'rgba(0,0,0,.28)');grad.addColorStop(1,'rgba(0,0,0,0)');cx.fillStyle=grad;cx.fillRect(0,0,64,64);
 const shadow=new THREE.Mesh(new THREE.PlaneGeometry(size[0],size[1]),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(canvas),transparent:true,depthWrite:false}));shadow.rotation.x=-Math.PI/2;vvipGroup.add(shadow);vvipReal.contacts.push({actor,shadow});
}
function vrInit(){
 const h=geo.helipadProposal,gate=h.gate,carStart=h.vehicleAccess[0];
 const walls=data.objects.filter(o=>['box','rounded','cylinder'].includes(o.shape)&&/wall|column|pillar|pier|jamb|railing|roof|ceiling|tree trunk|fence|bollard|lamp post|bench/i.test(o.name)&&!(/paint|sign|stripe|coping|texture|shadow/i.test(o.name)));
 const furniture=data.objects.filter(o=>o.group==='interior'&&/sofa|Low stage table|chair.*(seat|back)/i.test(o.name));
 vvipReal={elapsed:0,t:0,contacts:[],blocked:false,actors:[vvipFemale,vvipEscort1,vvipEscort2],walkObstacles:[...walls.filter(o=>!/roof|ceiling/i.test(o.name)),...furniture],cameraObstacles:[...walls,...furniture],surfaces:data.objects.filter(o=>(o.shape==='box'||o.name.startsWith('Raised stage'))&&/Hall floor|Raised stage|External black entry step|Stage right side green stair|Auditorium red-carpet|Proposed red carpet|Core compound|main road.*surface|road asphalt|paved.*road/i.test(o.name)),carDistance:0,speed:0,rotor:35,completed:false};
 vvipCar.position.set(carStart[0],vrSurface(...[carStart[0],carStart[1]],.30),carStart[1]);
 const access=h.vehicleAccessPolyline||h.vehicleAccess;vvipCar.rotation.y=Math.atan2(access[1][0]-carStart[0],access[1][1]-carStart[1]);
 const heliScale=h.helicopterDisplayScale||1.45;vvipHeli.scale.setScalar(heliScale);if(vvipHeli.userData.pilot)vvipHeli.userData.pilot.scale.setScalar(1/heliScale);
 vvipReal.landing=[h.helicopterCentre[0],vrSurface(h.centre[0],h.centre[1],.33)-.06*heliScale,h.helicopterCentre[1]];
 vvipReal.heading=vvipCar.rotation.y;
 vvipHeli.position.set(vvipReal.landing[0]-9,18,vvipReal.landing[2]-50);vvipHeli.rotation.y=vvipReal.heading;
 for(const [i,a] of vvipReal.actors.entries()){a.userData.role=i?'PSO '+i:'VVIP';a.visible=true;vrAttach(a,vvipHeli,[-.30+i*.28,1.09,.1-i*.7],1);vrContact(a,[.75,.7]);}
 vrContact(vvipCar,[3.3,6.1]);vrContact(vvipHeli,[5,10]);
 const outer=data.objects.filter(o=>o.name.startsWith('External black entry step')).sort((a,b)=>a.p[1]-b.p[1]);
 const end=[gate[0],vrSurface(gate[0],outer[0].p[2],.30),outer[0].p[2]];
 // Stop parallel to the auditorium entry road; left passenger door faces the existing steps.
 const accessPoints=access.map(p=>[p[0],.312,p[1]]),join=h.roadConnectionCentre,frontage=h.campusRoadCentre;vvipReal.carPath=vrRoundPath([...accessPoints,...(join?[[join[0],.31,join[1]]]:[]),...(frontage?[[frontage[0],.31,frontage[1]]]:[]),[gate[0],.39,gate[1]+5],end],2);
 vvipReal.stageRoute=vrPath(vvipAuditoriumRoute().path);
 camera.position.set(vvipHeli.position.x-15,vvipHeli.position.y+7,vvipHeli.position.z-22);controls.target.copy(vvipHeli.position);
 root.querySelector('#vvip-skip-btn').textContent='Next chapter';
 const pause=root.querySelector('#vvip-pause-btn');if(pause){pause.textContent='Pause';pause.onclick=()=>{vvipReal.paused=!vvipReal.paused;if(vvipReal.paused)vvipReal.pauseStart=performance.now();else if(vvipReal.pauseStart)vvipReal.flightStart+=performance.now()-vvipReal.pauseStart;pause.textContent=vvipReal.paused?'Resume':'Pause';};}
 vvipReal.facing=[];for(const n of depNodes)if(['officer','armed_officer','hhmd','binocular','radio'].includes(n.item.kind))vvipReal.facing.push({node:n,angle:n.g.rotation.y});
 vvipReal.temporaryHidden=[];if(typeof gateController!=='undefined'){vvipReal.savedGateOpen=gateController.isOpen;gateController.open();}vvipReal.flightStart=performance.now();vrBuildLandingCarpet();vrBuildWelcome();
}
function vrBuildLandingCarpet(){
 const a=vrWorld(vvipHeli,[-2,0,.95]).toArray(),b=vrWorld(vvipCar,[-2.6,0,-1.35]).toArray();
 // Use landed helicopter coordinates, not its in-flight transform.
 const heading=vvipReal.heading,scale=geo.helipadProposal.helicopterDisplayScale||1.45,L=vvipReal.landing;
 a[0]=L[0]+Math.cos(heading)*(-2*scale)+Math.sin(heading)*(.95*scale);a[2]=L[2]-Math.sin(heading)*(-2*scale)+Math.cos(heading)*(.95*scale);
 const c=vrWorld(vvipCar,[-3.2,0,-4]).toArray(),points=[a,c,b];vvipReal.carpet=[];let accumulated=0;
 const material=new THREE.MeshStandardMaterial({color:0xa71c32,roughness:.95});
 for(let i=1;i<points.length;i++){const p=points[i-1],q=points[i],len=Math.hypot(q[0]-p[0],q[2]-p[2]),g=new THREE.Group();g.visible=false;vvipGroup.add(g);const strip=vrBox(g,material,[0,0,0],[1.5,.014,1]);for(const x of [-.73,.73])vrBox(g,depMaterials.vipGold,[x,.009,0],[.025,.005,1]);g.rotation.y=Math.atan2(q[0]-p[0],q[2]-p[2]);vvipReal.carpet.push({g,start:p,end:q,len,accumulated});accumulated+=len;}
 vvipReal.carpetLength=accumulated;
}
function vrRevealCarpet(t){for(const part of vvipReal.carpet){const length=Math.max(0,Math.min(part.len,vrEase(t)*vvipReal.carpetLength-part.accumulated));part.g.visible=length>.001;part.g.scale.z=Math.max(.001,length);const q=vrMix(part.start,part.end,length/part.len/2);part.g.position.set(q[0],vrSurface(q[0],q[2],.33)+.008,q[2]);}}
function vrBuildWelcome(){
 const R=vvipReal,end=vvipAuditoriumRoute().end;R.host=vrActor(false);R.host.position.set(end[0]+3.6,end[1],end[2]+1.3);R.host.rotation.y=-Math.PI/2;R.host.userData.pose();R.host.userData.arms[0].rotation.x=-.95;vvipGroup.add(R.host);vrContact(R.host,[.75,.7]);
 const bouquet=new THREE.Group();vrLimb(bouquet,new THREE.MeshStandardMaterial({color:0x3b7846}),null,null,.035).userData.between(new THREE.Vector3(0,0,0),new THREE.Vector3(0,.35,0));
 const colors=[0xe94973,0xffe3a5,0xc83949];for(let i=0;i<9;i++){const angle=i*Math.PI*2/9,r=i===8?0:.12;vrSphere(bouquet,new THREE.MeshStandardMaterial({color:colors[i%3],roughness:.85}),[Math.cos(angle)*r,.34+(i%2)*.05,Math.sin(angle)*r],[.075,.065,.075]);}
 const wrap=new THREE.Mesh(new THREE.ConeGeometry(.16,.25,12,1,true),depMaterials.vipGold);wrap.rotation.x=Math.PI;wrap.position.y=.18;bouquet.add(wrap);R.host.userData.arms[0].add(bouquet);bouquet.position.set(0,-.51,.04);R.bouquet=bouquet;
}
function vrRunEscorts(dt){
 for(let i=1;i<3;i++){const a=vvipReal.actors[i];if(a.parent!==vvipGroup)vrDetach(a);const target=vrWorld(vvipCar,[i===1?-3.2:3.2,0,-3.6]);target.y=vrSurface(target.x,target.z,.30);const distance=a.position.distanceTo(target);if(distance<.04){a.userData.pose();continue;}const speed=Math.min(3.6,Math.max(1.4,distance*2.0));
  const path=vrRouteAroundPeople(vrPath([a.position.toArray(),target.toArray()]),a);vrMove(a,path,Math.min(path.total,speed*dt),speed,dt);
 }
}
function vrRouteAroundPeople(path,actor){
 const people=[...vrDynamicObstacles(actor).filter(o=>o.id),...vvipReal.walkObstacles.filter(o=>o.s[0]<2&&o.s[2]<2&&o.s[1]>.25)],out=[path.p[0]];
 for(let i=1;i<path.p.length;i++){
  const b=path.p[i],a=out.at(-1),dx=b[0]-a[0],dz=b[2]-a[2],length=Math.hypot(dx,dz);if(length<.1){out.push(b);continue;}
  const forward=[dx/length,dz/length],normal=[-forward[1],forward[0]];
  const blocking=people.filter(o=>vrSegmentBox([a[0],a[1]+.85,a[2]],[b[0],b[1]+.85,b[2]],o,.36)!==null).sort((p,q)=>Math.hypot(p.p[0]-a[0],p.p[2]-a[2])-Math.hypot(q.p[0]-a[0],q.p[2]-a[2]));
  for(const obstacle of blocking){
   const radius=Math.hypot(obstacle.s[0],obstacle.s[2])*.5+.85;
   for(const side of [-1,1]){
    const p=[obstacle.p[0]-forward[0]*radius+normal[0]*side*radius,a[1],obstacle.p[2]-forward[1]*radius+normal[1]*side*radius],q=[obstacle.p[0]+forward[0]*radius+normal[0]*side*radius,a[1],obstacle.p[2]+forward[1]*radius+normal[1]*side*radius],points=[out.at(-1),p,q,b];
    const car={p:[vvipCar.position.x,vvipCar.position.y+.85,vvipCar.position.z],s:[2.2,1.7,5.4],rot:vvipCar.rotation.y};
    const blockers=[...vvipReal.walkObstacles,...people,car];let clear=true;
    for(let k=1;k<points.length&&clear;k++)for(const o of blockers){const hit=vrSegmentBox([points[k-1][0],points[k-1][1]+.85,points[k-1][2]],[points[k][0],points[k][1]+.85,points[k][2]],o,.34);if(hit!==null&&hit>.005){clear=false;break;}}
    if(clear){out.push(p,q);break;}
   }
  }
  out.push(b);
 }
 return vrPath(out);
}
function vrPrepareRoadDuty(){
 const R=vvipReal;if(vvipPhase>2)return;
 for(const {node:n} of R.facing){
  if(n.g.userData.vvipRoadPrepared)continue;
  n.g.userData.vvipRoadPrepared=true;
  let nearest=null,best=Infinity;
  for(let d=0;d<R.carPath.total;d+=.5){const q=vrSample(R.carPath,d),gap=Math.hypot(q.pos[0]-n.g.position.x,q.pos[2]-n.g.position.z);if(Math.abs(n.g.position.y-q.pos[1])<1.3&&gap<best){best=gap;nearest=q;}}
  if(!nearest||best>5.8)continue;
  const normal=[Math.cos(nearest.angle),-Math.sin(nearest.angle)],signed=(n.g.position.x-nearest.pos[0])*normal[0]+(n.g.position.z-nearest.pos[2])*normal[1],preferred=signed<0?-1:1;
  for(const side of [preferred,-preferred])for(const offset of [5.9,6.7,7.5]){
   if(n.g.userData.vvipRoadPositioned)break;
   const target=new THREE.Vector3(nearest.pos[0]+normal[0]*side*offset,n.g.position.y,nearest.pos[2]+normal[1]*side*offset),box={p:[target.x,target.y+.85,target.z],s:[.7,1.7,.7],rot:0};
   const occupied=R.walkObstacles.some(o=>vrSegmentBox(box.p,box.p,o,.42)!==null)||depNodes.some(other=>other!==n&&Math.abs(other.g.position.y-target.y)<1.3&&other.g.position.distanceTo(target)<1.2);
   if(!occupied){n.g.position.copy(target);n.g.userData.vvipYield=target.clone();n.g.userData.vvipRoadPositioned=true;}
  }
 }
}
function vrCruiseTarget(path,distance){
 const now=vrSample(path,distance),ahead=vrSample(path,Math.min(path.total,distance+7));
 const turn=Math.abs(Math.atan2(Math.sin(ahead.angle-now.angle),Math.cos(ahead.angle-now.angle)));
 return Math.min(2.4,turn>.45?1.0:turn>.20?1.6:2.4,Math.sqrt(Math.max(0,1.4*(path.total-distance))));
}
function vrSceneActors(dt){
 const R=vvipReal,vip=vvipFemale.getWorldPosition(new THREE.Vector3());
 if(typeof gateController!=='undefined'&&!gateController.isOpen)gateController.open();
 // Deployment can finish loading or rebuild after playback starts. Always follow live nodes.
 R.facing=depNodes.filter(n=>['officer','armed_officer','hhmd','binocular','radio'].includes(n.item.kind)).map(n=>R.facing.find(old=>old.node.g===n.g)||{node:n,angle:n.g.rotation.y});
 vrPrepareRoadDuty();
 const gate=geo.helipadProposal.gate;
 if(vvipPhase===3&&Math.hypot(vvipCar.position.x-gate[0],vvipCar.position.z-gate[1])<20){for(const n of depNodes)if(n.item.kind==='dfmd'&&Math.hypot(n.item.x-gate[0],n.item.z-gate[1])<22&&!n.g.userData.vvipHidden){n.g.userData.vvipHidden=true;n.g.visible=false;R.temporaryHidden.push(n);}}
 for(const {node:n} of R.facing){if(n.g.position.distanceTo(vip)<25&&(!n.g.userData.vvipYield||n.g.position.distanceTo(n.g.userData.vvipYield)<.05))n.g.rotation.y=vrAngle(n.g.rotation.y,Math.atan2(n.g.position.x-vip.x,n.g.position.z-vip.z),4,dt);}
 if(vvipPhase!==3){if(vvipPhase===4||vvipPhase===5)vrPedestrianYield();vrMoveYielders(dt);return;}
 // Animation-only yielding: keep existing saved duty positions untouched.
 for(const {node:n} of R.facing){
  const pos=n.g.position,car=vvipCar.position;if(pos.distanceTo(car)>16)continue;
  let nearest=null,best=Infinity;for(let d=R.carDistance;d<Math.min(R.carPath.total,R.carDistance+16);d+=.6){const q=vrSample(R.carPath,d),gap=Math.hypot(q.pos[0]-pos.x,q.pos[2]-pos.z);if(gap<best){best=gap;nearest=q;}}
  if(!nearest||best>3.6)continue;
  if(!n.g.userData.vvipYield){
   for(const side of [-1,1]){const target=new THREE.Vector3(nearest.pos[0]+Math.cos(nearest.angle)*side*3.3,pos.y,nearest.pos[2]-Math.sin(nearest.angle)*side*3.3),a=[pos.x,pos.y+.85,pos.z],b=[target.x,target.y+.85,target.z];
    if(!R.walkObstacles.some(o=>vrSegmentBox(a,b,o,.35)!==null)&&!vrDynamicObstacles().filter(o=>o.id!==n.item.id).some(o=>{const hit=vrSegmentBox(a,b,o,.35);return hit!==null&&hit>.02;})){n.g.userData.vvipYield=target;break;}}
  }
 }
 vrMoveYielders(dt);
}
function vrPedestrianYield(){
 const R=vvipReal,paths=vvipPhase===5?[R.stageRoute,...(R.followPaths||[])]:[];
 for(const {node:n} of R.facing){
  if(!R.actors.some(a=>a.parent===vvipGroup&&a.position.distanceTo(n.g.position)<7))continue;
  let closest=null,best=1.0;
  for(const path of paths){if(!path)continue;for(let d=0;d<path.total;d+=.4){const q=vrSample(path,d),gap=Math.hypot(q.pos[0]-n.g.position.x,q.pos[2]-n.g.position.z);if(Math.abs(q.pos[1]-n.g.position.y)<1&&gap<best){best=gap;closest=q;}}}
  if(!closest)continue;
  if(n.g.userData.vvipYield&&n.g.position.distanceTo(n.g.userData.vvipYield)>.08)continue;
  const pos=n.g.position,forward=[Math.sin(closest.angle),Math.cos(closest.angle)],normal=[Math.cos(closest.angle),-Math.sin(closest.angle)];
  for(const side of [-1,1])for(const ahead of [0,1.4,-1.4]){
   if(n.g.userData.vvipYield&&n.g.position.distanceTo(n.g.userData.vvipYield)>.08)break;
   const target=new THREE.Vector3(pos.x+normal[0]*side*1.4+forward[0]*ahead,pos.y,pos.z+normal[1]*side*1.4+forward[1]*ahead),a=[pos.x,pos.y+.85,pos.z],b=[target.x,target.y+.85,target.z];
   const obstacles=[...R.walkObstacles,...vrDynamicObstacles().filter(o=>o.id!==n.item.id)];
   if(!obstacles.some(o=>{const hit=vrSegmentBox(a,b,o,.34);return hit!==null&&hit>.01;})){n.g.userData.vvipYield=target;break;}
  }
 }
}
function vrMoveYielders(dt){
 const R=vvipReal;
 for(const {node:n} of R.facing){const target=n.g.userData.vvipYield;if(!target)continue;const delta=target.clone().sub(n.g.position),length=delta.length();if(length>.02){n.g.rotation.y=vrAngle(n.g.rotation.y,Math.atan2(delta.x,delta.z),5,dt);n.g.position.addScaledVector(delta.normalize(),Math.min(length,1.4*dt));const rig=n.g.userData.rig;if(rig){rig.walkPhase+=dt*7;rig.leftLeg.rotation.x=Math.sin(rig.walkPhase)*.35;rig.rightLeg.rotation.x=-Math.sin(rig.walkPhase)*.35;}}else{const rig=n.g.userData.rig;if(rig){rig.leftLeg.rotation.x=0;rig.rightLeg.rotation.x=0;}}}
}
function vrRestoreScene(){
 if(!vvipReal)return;
 if(typeof gateController!=='undefined'&&vvipReal.savedGateOpen!==undefined){if(vvipReal.savedGateOpen)gateController.open();else gateController.close();}
 for(const {node:n} of vvipReal.facing||[]){n.g.position.set(n.item.x,n.item.y,n.item.z);n.g.rotation.y=-n.item.angle*Math.PI/180;delete n.g.userData.vvipYield;delete n.g.userData.vvipRoadPrepared;delete n.g.userData.vvipRoadPositioned;}
 for(const n of vvipReal.temporaryHidden||[]){delete n.g.userData.vvipHidden;n.g.visible=true;}
}
function vrStagePaths(){
 const R=vvipReal,route=vvipAuditoriumRoute().path,end=vvipAuditoriumRoute().end,common=route[3];
 R.stageRoute=vrRouteAroundPeople(vrPath([vvipFemale.position.toArray(),...route.slice(3)]),vvipFemale);
 const near=p=>Math.hypot(...p.map((v,k)=>v-common[k]))<.05,commonIndex=R.stageRoute.p.findIndex(near),tail=R.stageRoute.p.slice(Math.max(0,commonIndex),-1);
 R.followPaths=R.actors.map((a,i)=>{
  if(!i)return R.stageRoute;
  const way=[];if(i===2){for(const local of [[3.2,0,-4.5],[-3.2,0,-4.5]]){const p=vrWorld(vvipCar,local).toArray();p[1]=vrSurface(p[0],p[2],.30);way.push(p);}}
  const prefix=vrRouteAroundPeople(vrPath([a.position.toArray(),...way,common]),a);
  return vrPath([...prefix.p,...tail.slice(1),...(i===1?[[route.at(-2)[0],end[1],.30],[end[0]-1.1,end[1],.30]]:[]),[end[0]+(i===1?-1.1:1.1),end[1],end[2]-.9]]);
 });
 const prefix=path=>{const i=path.p.findIndex(near);return i<0?0:path.lengths[i];},base=prefix(R.stageRoute);R.followOffsets=R.followPaths.map(path=>prefix(path)-base);R.walkDistance=0;R.followD=[0,0,0];R.speed=0;vrChange(5);
}
function vrWelcome(dt){
 const R=vvipReal,end=vvipAuditoriumRoute().end;
 if(!R.finalPaths){R.finalPaths=R.actors.map((a,i)=>i?vrPath([a.position.toArray(),[a.position.x,end[1],end[2]-1],[end[0]+(i===1?-2.4:2.4),end[1],end[2]-1]]):null);R.finalD=[0,0,0];}
 for(let i=1;i<3;i++){const path=R.finalPaths[i],d=Math.min(path.total,R.finalD[i]+1.4*dt);if(d>R.finalD[i]&&vrMove(R.actors[i],path,d,1.4,dt))R.finalD[i]=d;if(d>=path.total-.01){R.actors[i].userData.pose();R.actors[i].rotation.y=vrAngle(R.actors[i].rotation.y,Math.PI,3,dt);}}
 const ready=[1,2].every(i=>R.finalD[i]>=R.finalPaths[i].total-.01);
 if(ready&&!R.welcomePath){R.welcomePath=vrPath([R.host.position.toArray(),[R.host.position.x,end[1],end[2]],[end[0]+.85,end[1],end[2]]]);R.welcomeD=0;}
 if(R.welcomePath&&R.welcomeD<R.welcomePath.total-.01){const d=Math.min(R.welcomePath.total,R.welcomeD+1.05*dt);if(vrMove(R.host,R.welcomePath,d,1.05,dt))R.welcomeD=d;R.host.userData.arms[0].rotation.x=-.95;}
 if(R.welcomePath&&R.welcomeD>=R.welcomePath.total-.01){
  if(!R.handOver){R.handOver=0;const p=R.bouquet.getWorldPosition(new THREE.Vector3());vvipGroup.add(R.bouquet);R.bouquet.position.copy(p);R.flowerStart=p.clone();}
  R.handOver+=dt;R.host.userData.pose();R.host.rotation.y=vrAngle(R.host.rotation.y,-Math.PI/2,3,dt);R.host.userData.arms[0].rotation.x=-.95*(1-vrEase(R.handOver/2.5));
  vvipFemale.userData.pose();vvipFemale.userData.arms[0].rotation.x=-.95*vrEase(R.handOver/1.2);
  const target=vrWorld(vvipFemale.userData.arms[0],[0,-.51,.04]);if(!R.flowersReceived)R.bouquet.position.copy(R.flowerStart).lerp(target,vrEase(R.handOver/2));
  if(R.handOver>=2&&!R.flowersReceived){const p=R.bouquet.position.clone();vvipFemale.userData.arms[0].add(R.bouquet);R.bouquet.position.copy(vvipFemale.userData.arms[0].worldToLocal(p));R.flowersReceived=true;}
 }
 if(R.flowersReceived){vvipFemale.userData.arms[0].rotation.x=-.95;root.dataset.simulation='complete';}
 vvipFemale.rotation.y=vrAngle(vvipFemale.rotation.y,Math.PI,3,dt);vrCamera([end[0]+.35,end[1]+1,end[2]],[-3,1.5,-8],dt);
 updateVvipHUD(5,'Stage welcome',R.flowersReceived?'Bouquet received · Visual rehearsal complete · Replay / Exit':R.welcomePath?'Welcome on the existing stage — bouquet presentation':'Main stage reached — escorts taking their places');
}
function vrChange(phase){vvipPhase=phase;vvipPhaseTimer=0;vvipReal.t=0;vvipReal.jobs=null;vvipReal.blocked=false;}
function vrBeginTransfers(exitHeli){
 const order=[1,0,2];vvipReal.jobs=vvipReal.actors.map((actor,i)=>({actor,i,state:exitHeli?'heliWait':'open',t:exitHeli?-order.indexOf(i)*3.2:-i*.8,d:0,speed:0,done:false}));
 if(!exitHeli){vvipReal.jobs=vvipReal.jobs.filter(j=>j.i===0);vvipReal.jobs.forEach(j=>{j.outside=vrWorld(vvipCar,[-2.6,0,-1.35]).toArray();j.seat=vvipCar.userData.seats[0];});}
}
function vrTransfer(job,dt,fromHeli){
 const a=job.actor,i=job.i;job.t+=dt;if(job.t<0)return;
 const setState=s=>{job.state=s;job.t=0;};
 if(job.state==='heliWait'){
  if(vvipReal.rotor>.01)return;
  if(!vvipReal.heliDoorOpen||vvipReal.t<vvipReal.heliDoorOpenedAt+[1,0,2].indexOf(i)*4.6)return;
  vrDetach(a);job.start=a.position.toArray();setState('heliExit');
 }else if(job.state==='heliExit'){
  const door=vrWorld(vvipHeli,[-1.35,1.09,.40]).toArray(),step=vrWorld(vvipHeli,[-1.40,.64,.40]).toArray(),ground=vrWorld(vvipHeli,[-2.0,0,.95]).toArray();ground[1]=vrSurface(ground[0],ground[2],.33);
  const t=job.t,p=t<1.5?vrMix(job.start,door,vrEase(t/1.5)):t<2.8?vrMix(door,step,vrEase((t-1.5)/1.3)):vrMix(step,ground,vrEase((t-2.8)/1.7));
  a.position.fromArray(p);a.rotation.y=vrAngle(a.rotation.y,vvipReal.heading-Math.PI/2,6,dt);a.userData.pose(job.t*.45,t>1.5?1:0,1-vrEase(t/1.5),Math.sin(vrClamp(t/4.5)*Math.PI)*.5);
  if(t>=4.5){const side=i===2?1:-1,waiting=i===0?[-2.6,0,-1.35]:[side*(i===1?3.6:3.2),0,-3.6];job.outside=vrWorld(vvipCar,waiting).toArray();job.outside[1]=vrSurface(job.outside[0],job.outside[2],.30);
   const clearance=vrWorld(vvipCar,[side*(i===0?2.6:i===1?4.2:3.2),0,-4.0]).toArray();clearance[1]=vrSurface(clearance[0],clearance[2],.30);job.path=vrPath([ground,clearance,job.outside]);setState('walkCar');}
 }else if(job.state==='walkCar'){
  const remaining=job.path.total-job.d,target=Math.min(i===0?1.40:1.65,Math.sqrt(Math.max(0,2*1.1*remaining)));job.speed=Math.min(target,job.speed+1.1*dt);const next=Math.min(job.path.total,job.d+Math.max(.04,job.speed)*dt);
  if(vrMove(a,job.path,next,job.speed,dt))job.d=next;
  if(job.d>=job.path.total-.005){a.userData.pose(0);if(i>0){job.done=true;setState('escortReady');}else setState('open');}
 }else if(job.state==='open'){
  if(!vrDoorMove(i,vrClamp(job.t/1.2),a)){job.t-=dt;return;}
  if(job.t>=1.2){if(fromHeli){job.start=a.position.toArray();setState('board');}else{vrDetach(a);job.start=a.position.toArray();setState('exit');}}
 }else if(job.state==='board'){
  const seat=vrWorld(vvipCar,vvipCar.userData.seats[i]).toArray(),t=vrEase(job.t/2.8),threshold=vrWorld(vvipCar,[i===0?-1.2:1.2,.12,(i===2?.69:-.8)-.4]).toArray();a.position.fromArray(t<.5?vrMix(job.start,threshold,t*2):vrMix(threshold,seat,(t-.5)*2));a.rotation.y=vrAngle(a.rotation.y,vvipCar.rotation.y,4,dt);a.userData.pose(0,0,t,Math.sin(t*Math.PI)*.9);
  if(job.t>=2.8){vrAttach(a,vvipCar,vvipCar.userData.seats[i],1);setState('close');}
 }else if(job.state==='exit'){
  const t=vrEase(job.t/2.8),threshold=vrWorld(vvipCar,[i===0?-1.2:1.2,.12,(i===2?.69:-.8)-.4]).toArray();a.position.fromArray(t<.5?vrMix(job.start,threshold,t*2):vrMix(threshold,job.outside,(t-.5)*2));a.rotation.y=vrAngle(a.rotation.y,vvipCar.rotation.y,4,dt);a.userData.pose(0,0,1-t,Math.sin(t*Math.PI)*.9);
  if(job.t>=2.8){
   job.start=a.position.toArray();const front=vrWorld(vvipCar,[-3.2,0,-1.35]).toArray();front[1]=vrSurface(front[0],front[2],.30);job.path=vrPath([job.start,front]);job.d=0;job.speed=0;setState('clear');
  }
 }else if(job.state==='clear'){
  job.speed=Math.min(1.4,job.speed+1.0*dt);const next=Math.min(job.path.total,job.d+job.speed*dt);if(vrMove(a,job.path,next,job.speed,dt))job.d=next;
  if(job.d>=job.path.total-.005){a.userData.pose();setState('close');}
 }else if(job.state==='close'){
  if(!vrDoorMove(i,vrClamp(1-job.t/1.2),a)){job.t-=dt;return;}if(job.t>=1.2){job.done=true;setState('done');}
 }
}
function vrFlight(dt){
 const R=vvipReal,t=R.t,L=R.landing;
 // Slow final descent, level touchdown, then explicit visual shutdown before the cabin opens.
 if(t<6){const u=vrEase(t/6),p=vrMix([L[0]-9,18,L[2]-50],L,u);p[1]=L[1]+(18-L[1])*Math.pow(1-u,1.6);vvipHeli.position.fromArray(p);vvipHeli.rotation.x=Math.sin(Math.PI*vrClamp(t/6))*.035;}
 else{vvipHeli.position.fromArray(L);vvipHeli.rotation.x=0;R.rotor=35*(1-vrEase((t-8)/6));}
 const p=vvipHeli.position;vrCamera([p.x,p.y+1.6,p.z],[-13,6,-18],dt);
 updateVvipHUD(1,'Arrival & shutdown',t<6?'Helicopter approach — visual rehearsal':R.rotor>.01?'Landed — cabin closed while rotors stop':'Rotors stopped — cabin exit sequence');
 if(t>=14&&R.rotor<.01)vrChange(2);
}
function tickVvipSimulation(dt){
 if(!vvipActive||!vvipGroup||!vvipReal)return false;
 if(vvipReal.paused)return false;
 const R=vvipReal;if(!R.lastDiagnostic||R.elapsed-R.lastDiagnostic>.3){R.lastDiagnostic=R.elapsed;root.dataset.rehearsalState=JSON.stringify({phase:vvipPhase,walk:R.walkDistance,offset:R.followOffsets,follow:R.followD,actors:R.actors.map(a=>({role:a.userData.role,p:a.position.toArray()})),blocked:R.blockedName,car:vvipCar.position?.toArray?.(),carDistance:R.carDistance,carTotal:R.carPath?.total,speed:R.speed,dfmdCleared:R.temporaryHidden?.length||0});}R.blocked=false;dt=Math.min(.10,Math.max(0,dt));R.elapsed+=dt;R.t+=dt;vvipPhaseTimer=R.t;
 vrSceneActors(dt);
 if(vvipPhase===1){R.t=(performance.now()-R.flightStart)/1000;vrFlight(dt);}
 else if(vvipPhase===2||vvipPhase===4){
  const fromHeli=vvipPhase===2;if(!R.jobs)vrBeginTransfers(fromHeli);
  if(fromHeli){
   vrRevealCarpet(R.t/2);if(!R.heliDoorOpen){vvipHeli.userData.setDoor(vrClamp((R.t-2)/1.4));if(R.t>=3.4){R.heliDoorOpen=true;R.heliDoorOpenedAt=R.t;}}
  }
  for(const job of R.jobs)if(!job.done)vrTransfer(job,dt,fromHeli);
  const a=vvipFemale.getWorldPosition(new THREE.Vector3());vrCamera([a.x,a.y+1.05,a.z],[-5,2.4,-6.5],dt);
  if(fromHeli&&R.jobs.every(j=>!['heliWait','heliExit'].includes(j.state))){if(!R.heliCloseAt)R.heliCloseAt=R.t;vvipHeli.userData.setDoor(1-vrEase((R.t-R.heliCloseAt)/1.4));}
  const state=R.jobs[0].state,caption={heliWait:'Cabin door opening after rotor stop',heliExit:'Step down from cabin',walkCar:'Walk to the vehicle',open:'Vehicle stopped — passenger door opening',board:'Turn, bend and sit in vehicle',exit:'Stand and step out of vehicle',clear:'Walk clear of the door',close:'Door closing after clearance',done:'Waiting for all passengers'}[state];
  updateVvipHUD(vvipPhase,fromHeli?'Disembark & board':'Vehicle exit',R.blocked?'Waiting for clearance: '+R.blockedName:caption);
  if(R.jobs.every(j=>j.done)&&vvipCar.userData.doors.every(d=>d.open<.001)){
   if(fromHeli){R.speed=0;R.carDistance=0;vrChange(3);}else vrStagePaths();
  }
 }else if(vvipPhase===3){
  vrRunEscorts(dt);
  if(vvipFemale.parent!==vvipCar||vvipCar.userData.doors.some(d=>d.open>.001)){updateVvipHUD(3,'Waiting','Vehicle remains stopped until VVIP is seated and doors are closed');return true;}
  const remaining=R.carPath.total-R.carDistance,target=vrCruiseTarget(R.carPath,R.carDistance);R.speed+=Math.max(-.85*dt,Math.min(.65*dt,target-R.speed));const distance=Math.min(R.carPath.total,R.carDistance+Math.max(.015,R.speed)*dt),q=vrSample(R.carPath,distance),last=vvipCar.position.clone();
  const carTarget=[q.pos[0],vrSurface(q.pos[0],q.pos[2],.30),q.pos[2]];
  const blocker=[...R.walkObstacles,...vrDynamicObstacles()].find(o=>vrVehicleSweep(last.toArray(),carTarget,vvipCar.rotation.y,o));if(blocker){R.speed=0;R.blocked=true;updateVvipHUD(3,'Vehicle stopped','Vehicle stopped for clearance: '+(blocker.name||'nearby person or equipment'));return true;}
  vvipCar.position.fromArray(carTarget);vvipCar.rotation.y=vrAngle(vvipCar.rotation.y,q.angle,2.5,dt);vvipCar.userData.rollWheels(last.distanceTo(vvipCar.position));R.carDistance=distance;
  const p=vvipCar.position,ang=vvipCar.rotation.y;vrCamera([p.x,p.y+1,p.z],[-Math.sin(ang)*8-4,3,-Math.cos(ang)*8],dt);updateVvipHUD(3,'Vehicle transfer','Vehicle transfer — gradual acceleration and braking');
  if(distance>=R.carPath.total-.01&&R.speed<.18){R.speed=0;vrChange(4);}
 }else if(vvipPhase===5){
  if(!vvipHallPrepared){prepareVvipHall();groups.roof.visible=false;}
  const remain=R.stageRoute.total-R.walkDistance,target=Math.min(1.4,Math.sqrt(Math.max(0,1.6*remain)));R.speed+=Math.max(-1.0*dt,Math.min(.85*dt,target-R.speed));const d=Math.min(R.stageRoute.total,R.walkDistance+Math.max(.025,R.speed)*dt);
  if(vrMove(vvipFemale,R.stageRoute,d,R.speed,dt))R.walkDistance=d;
  for(let i=1;i<3;i++){if(R.walkDistance<R.stageRoute.total-.01&&R.actors[i].position.distanceTo(i===1?vvipFemale.position:R.actors[1].position)<1.4){R.actors[i].userData.pose();continue;}const path=R.followPaths[i],finished=R.walkDistance>=R.stageRoute.total-.01,desired=finished?path.total:Math.max(0,Math.min(path.total,R.walkDistance+R.followOffsets[i]-i*1.5)),travel=Math.min(desired,R.followD[i]+1.65*dt);if(travel>R.followD[i]&&vrMove(R.actors[i],path,travel,1.65,dt))R.followD[i]=travel;}
  const a=vvipFemale.position;vrCamera([a.x,a.y+1.05,a.z],[-3.5,2,-5.7],dt);updateVvipHUD(5,'Main stage',R.blocked?'Waiting for clearance: '+R.blockedName:'Walking through auditorium entry and side stairs to the existing stage');
  if(R.walkDistance>=R.stageRoute.total-.01){vvipFemale.userData.pose();if([1,2].every(i=>R.followD[i]>=R.followPaths[i].total-.01)){R.actors.forEach(a=>a.userData.pose(0));R.finishStart=R.elapsed;vrChange(6);}}
 }else if(vvipPhase===6){
  root.querySelector('#vvip-skip-btn').textContent='Replay';vrWelcome(dt);
 }
 if(vvipHeli.userData.mainRotor){vvipHeli.userData.mainRotor.rotation.y+=R.rotor*dt;vvipHeli.userData.tailRotor.rotation.x+=R.rotor*1.5*dt;vvipHeli.userData.rotorDisc.visible=R.rotor>15;}
 for(const {actor,shadow} of R.contacts){const p=actor.getWorldPosition(new THREE.Vector3());shadow.position.set(p.x,vrSurface(p.x,p.z,.15)+.006,p.z);shadow.visible=actor.parent===vvipGroup&&p.y-shadow.position.y<3;}
 // Pause/resume does not advance wall-clock animation time.
 return true;
}
function advanceVvipPhase(){
 // User-requested chapter skipping is an explicit edit, not hidden teleportation during playback.
 if(!vvipReal)return;
 if(vvipPhase===1){vvipHeli.position.fromArray(vvipReal.landing);vvipReal.rotor=0;vrChange(2);}
 else if(vvipPhase===2){vrAttach(vvipFemale,vvipCar,vvipCar.userData.seats[0],1);for(let i=1;i<3;i++){const actor=vvipReal.actors[i];vrDetach(actor);actor.position.copy(vrWorld(vvipCar,[i===1?-3.2:3.2,0,-3.6]));actor.userData.pose();}vvipCar.userData.setDoor(0,0);vvipHeli.userData.setDoor(0);vrRevealCarpet(1);vrChange(3);}
 else if(vvipPhase===3){const p=vrSample(vvipReal.carPath,vvipReal.carPath.total);vvipCar.position.fromArray(p.pos);vvipCar.rotation.y=p.angle;for(let i=1;i<3;i++){const actor=vvipReal.actors[i];actor.position.copy(vrWorld(vvipCar,[i===1?-3.2:3.2,0,-3.6]));actor.userData.pose();}vvipReal.speed=0;vrChange(4);}
 else if(vvipPhase===4){if(vvipFemale.parent!==vvipGroup)vrDetach(vvipFemale);vvipFemale.position.copy(vrWorld(vvipCar,[-3.2,0,-1.35]));vvipFemale.position.y=vrSurface(vvipFemale.position.x,vvipFemale.position.z,.30);vvipFemale.userData.pose();vvipCar.userData.setDoor(0,0);vrStagePaths();}
 else if(vvipPhase===5){placeVvipOnActualStage();vrChange(6);}
 else{stopVvipSimulation();startVvipSimulation();}
}
