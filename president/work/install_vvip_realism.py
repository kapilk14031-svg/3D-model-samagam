from pathlib import Path
p=Path('work/deployment.js')
s=p.read_text(encoding='utf-8')
if '// BEGIN REALISTIC REHEARSAL ENGINE' in s:
 a=s.index('// BEGIN REALISTIC REHEARSAL ENGINE');b=s.index('// END REALISTIC REHEARSAL ENGINE',a)+len('// END REALISTIC REHEARSAL ENGINE');s=s[:a]+s[b:]
else:
 def remove_function(s,name):
  a=s.index('function '+name+'(');start=s.index('{',a);depth=1;i=start+1
  while depth:
   if s[i]=='{':depth+=1
   elif s[i]=='}':depth-=1
   i+=1
  return s[:a]+s[i:]
 for name in ['buildFemaleVvip','buildSecurityEscort','buildVvipCar','interpolateWaypoints','tickVvipSimulation','advanceVvipPhase']:
  s=remove_function(s,name)
 a=s.index('function buildVvipHelicopter');b=s.index('function buildRouteOfficer',a)
 part=s[a:b];part=part.replace('  return g;','  vrHollowHeli(g,bodyUpper,bodyLower,stripe);\n  return g;',1);s=s[:a]+part+s[b:]
 a=s.index('function startVvipSimulation');b=s.index('function stopVvipSimulation',a)
 part=s[a:b];idx=part.rfind('  draw();');part=part[:idx]+'  vrInit();\n  root.dataset.simulation="active";\n'+part[idx:];s=s[:a]+part+s[b:]
 s=s.replace('  vvipActive = false;','  vvipActive = false;\n  delete root.dataset.simulation;\n  if(vvipReal){for(const {shadow} of vvipReal.contacts){shadow.geometry.dispose();shadow.material.map.dispose();shadow.material.dispose();}vvipReal=null;}',1)
 old="function prepareVvipHall(){if(vvipHallPrepared)return;select.value='hall';applyView();controls.enabled=false;groups.roof.visible=false;vvipHallPrepared=true;}"
 new="function prepareVvipHall(){if(vvipHallPrepared)return;const p=camera.position.clone(),t=controls.target.clone();select.value='hall';applyView();camera.position.copy(p);controls.target.copy(t);controls.enabled=false;groups.roof.visible=false;vvipHallPrepared=true;}"
 assert old in s;s=s.replace(old,new)
code=Path('work/vvip-realism.js').read_text(encoding='utf-8')
where=s.index('// Bind VVIP UI Event Listeners')
s=s[:where]+'// BEGIN REALISTIC REHEARSAL ENGINE\n'+code+'\n// END REALISTIC REHEARSAL ENGINE\n'+s[where:]
p.write_text(s,encoding='utf-8')
