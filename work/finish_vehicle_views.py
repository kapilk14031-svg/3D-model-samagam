from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace(".scene.vehicle-follow{height:calc(100svh - 12px)!important;min-height:320px}", ".scene.vehicle-follow{height:calc(100svh - 12px)!important;min-height:320px}.scene.vehicle-follow .notice,.scene.vehicle-follow .hint{display:none}")
pos=s.index('function depVehicleShot(')
s=s[:pos]+"function depSmoothHeading(current,next,dt){if(!Number.isFinite(current))return next;const delta=Math.atan2(Math.sin(next-current),Math.cos(next-current));return current+delta*(1-Math.exp(-9*Math.max(.001,dt)))}\n"+s[pos:]
s=s.replace("const pose=depPose(u),shot=depVehicleShot(pose,u.type,state.mode", "const pose=depPose(u);state.heading=depSmoothHeading(state.heading,pose.angle,dt);const shot=depVehicleShot({...pose,angle:state.heading},u.type,state.mode",1)
p.write_text(s,encoding='utf-8')
# Keep standalone regression fixtures aware of the optional follow camera.
p=Path('work/test-nearby-icons.cjs');s=p.read_text(encoding='utf-8');s='let depFollowState=null;\n'+s;p.write_text(s,encoding='utf-8')
