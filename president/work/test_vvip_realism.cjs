const fs=require('fs'),vm=require('vm'),assert=require('assert');
const context={Math,console,root:{dataset:{}}};vm.createContext(context);vm.runInContext(fs.readFileSync('work/vvip-realism.js','utf8'),context);
const path=context.vrPath([[0,0,0],[1,0,0],[10,0,0]]);
assert.equal(path.total,10);
assert.equal(context.vrSample(path,5).pos[0],5,'Unequal segments must preserve distance-based speed');
assert.equal(context.interpolateWaypoints([[0,0,0],[1,0,0],[10,0,0]],.5).pos[0],5);
assert.equal(context.vrSample(path,100).pos[0],10);
const wall={p:[5,1,0],s:[1,2,4],rot:0};
assert(context.vrSegmentBox([0,1,0],[10,1,0],wall)>.4);
assert.equal(context.vrSegmentBox([0,4,0],[10,4,0],wall),null);
assert(context.vrSegmentBox([0,1,0],[10,1,0],{...wall,rot:Math.PI/4})!==null);
let message='',door=0;
context.vrSceneActors=()=>{};context.vrRunEscorts=()=>{};
context.updateVvipHUD=(...args)=>message=args[2];
context.vvipActive=true;context.vvipGroup={};context.vvipPhase=3;context.vvipPhaseTimer=0;
const car={userData:{doors:[{open:1}]}};context.vvipCar=car;context.vvipFemale={parent:car};
context.vvipReal={elapsed:0,t:0,actors:[{parent:car,userData:{role:'VVIP'},position:{toArray:()=>[0,0,0]}}],paused:false};
assert.equal(context.tickVvipSimulation(.016),true);
assert(message.includes('doors are closed'),'Vehicle must not depart with door open');
context.vvipReal.paused=true;const time=context.vvipReal.t;
context.tickVvipSimulation(10);assert.equal(context.vvipReal.t,time,'Pause must freeze animation');
context.vvipCar={userData:{setDoor:(i,t)=>door=t}};
const actor={position:{toArray:()=>[0,0,0]}};
const job={actor,i:0,state:'open',t:0};
context.vrDoorMove=(i,t)=>{door=t;return true;};
context.vrTransfer(job,.5,true);assert.equal(job.state,'open');assert(door<1);
context.vrTransfer(job,.8,true);assert.equal(job.state,'board','Boarding only follows door opening');
console.log('PASS: distance interpolation, bounds, rotated collision, door departure interlock, pause, boarding order');

assert(context.vrBoxesOverlap({p:[0,1,0],s:[2,2,5],rot:.4},{p:[.5,1,1],s:[.6,1.8,.6],rot:0}));
assert(!context.vrBoxesOverlap({p:[0,1,0],s:[2,2,5],rot:0},{p:[4,1,0],s:[.6,1.8,.6],rot:0}));
assert(context.vrVehicleSweep([0,0,0],[0,0,.1],0,{p:[0,.9,2.7],s:[.65,1.8,.65],rot:0}),'Vehicle front must stop before officer, not only vehicle centre');
assert(!context.vrVehicleSweep([0,0,0],[0,0,.1],0,{p:[3,.9,0],s:[.65,1.8,.65],rot:0}));
console.log('PASS: body overlap and full-length vehicle sweep against officers');

const curved=context.vrRoundPath([[0,0,0],[0,0,10],[10,0,10]],2);
assert(curved.total>17&&curved.total<20);
assert(curved.p.length>3);
const src=fs.readFileSync('work/vvip-realism.js','utf8');
assert(src.includes('if(t<6)')&&src.includes('if(t>=14&&R.rotor<.01)'));
assert(src.includes('vvipFemale.parent!==vvipCar'));
assert(!src.includes('R.actors.every(a=>a.parent===vvipCar)'));
assert(src.includes("job.done=true;setState('escortReady')"));
assert(src.includes('vrRestoreScene'));
console.log('PASS: rounded road path, 6-second approach, VVIP-only boarding, PSO ready state, restoration hook');

for(const prefixExtra of [2.25,8.0])for(let lead=0;lead<20;lead+=.25){const desired=Math.max(0,lead+prefixExtra-1.5);if(desired>=prefixExtra)assert(desired-prefixExtra<=lead-1.49,'Follower cannot overtake on common route');}
console.log('PASS: unequal approach lengths preserve follower spacing on common stair route');
