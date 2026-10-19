from pathlib import Path
p=Path(__file__).with_name('viewer-v2.html');s=p.read_text(encoding='utf-8')
s=s.replace('yaw:1.05,elevation:.5,distance:820','yaw:1.7,elevation:.38,distance:510')
s=s.replace('p.distance=Math.max(820,650/(sceneEl.clientWidth/sceneEl.clientHeight))','p.distance=Math.max(510,420/(sceneEl.clientWidth/sceneEl.clientHeight))')
s=s.replace("const p={...presets[view]};flyoverFocus=", "const previousFlyover=flyoverFocus;const p={...presets[view]};flyoverFocus=")
s=s.replace("if(flyoverFocus){target=[...p.target];yaw=p.yaw;elevation=p.elevation;distance=p.distance;anim=null}","if(flyoverFocus||previousFlyover){target=[...p.target];yaw=p.yaw;elevation=p.elevation;distance=p.distance;anim=null}")
s=s.replace("document.querySelector('.location b').textContent=", "document.querySelector('.notice span').textContent=flyoverFocus?'Vehicle flyover reconstruction: dimensions, ramp lengths and supporting structures are approximate.':'Actual tent positions, site dimensions and traffic directions are unverified. This is a visual study; routes are proposals.';document.querySelector('.location b').textContent=")
s=s.replace("c.fillText('79th Nirankari Sant Samagam · 3D study',20,32)", "c.fillText(flyoverFocus?'Samalkha · NH-44 vehicle flyover · 3D study':'79th Nirankari Sant Samagam · 3D study',20,32)")
p.write_text(s,encoding='utf-8')
