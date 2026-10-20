from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace('let depFlow=null,depPointActive=false;', 'let depDrawnOfficers=[];\nlet depFlow=null,depPointActive=false;',1)
s=s.replace("function drawDeployment(){if(!depVisible||!depModelsOn)return;const out=[];", "function drawDeployment(){depDrawnOfficers=[];if(!depVisible||!depModelsOn)return;const out=[];",1)
s=s.replace("function officer(x=0,z=0,y=0){box", "let officerIndex=0;function officer(x=0,z=0,y=0){const personIndex=officerIndex++;if(u.type!=='officer'&&!u.isPersonnelMarker)depDrawnOfficers.push({key:'DEP-OFFICER-'+u.id+'-'+personIndex,p:[p[0]+(x*c+z*s)*sc,p[1]+y*sc,p[2]+(-x*s+z*c)*sc],unitId:u.id,personIndex,location:u.title,duty:DEP_TYPES[u.type]});box",1)
s=s.replace('placeDeploymentIcons();placeDutyCard()', 'placeDeploymentIcons();depPlaceExtraOfficerIcons();placeDutyCard()',1)
s=s.replace("paths[type==='qrt'?'patrol':type]||'<circle cx=\"12\" cy=\"12\" r=\"5\"/>'", "paths[type==='qrt'?'patrol':type]||paths.officer",1)
start=s.index('function depSyncSimpleOfficer(){');end=s.index('\nfunction depSimplifyEditor',start)
s=s[:start]+'''function depSyncSimpleOfficer(){const name=depEl('depSimpleName');if(!name)return;const ids=['depSimpleName','depSimpleRank','depSimpleMobile','depSimpleRole'];if(ids.every(id=>depEl(id).value===depEl(id).defaultValue))return;const lines=depEl('depPersonnel').value.split('\\n'),old=(lines[0]||'').split('|').map(v=>v.trim());while(old.length<5)old.push('');old[0]=name.value.trim();old[1]=depEl('depSimpleRank').value.trim();old[2]=depEl('depSimpleRole').value.trim();old[4]=depEl('depSimpleMobile').value.trim();lines[0]=old.join(' | ');depEl('depPersonnel').value=lines.join('\\n')}'''+s[end:]
needle=";const routeExtra=document.createElement('details');"
assert needle in s
s=s.replace(needle,";staff.innerHTML+='<label>Mobile<input id=\"depSimpleMobile\" type=\"tel\" value=\"'+depEsc(person.contact||'')+'\"></label><label>Work / duty<input id=\"depSimpleRole\" value=\"'+depEsc(person.role||'')+'\" placeholder=\"Duty / responsibility\"></label><label style=\"grid-column:1/-1\">Duty location<input id=\"depSimpleLocation\" value=\"'+depEsc(u.location||'')+'\" placeholder=\"'+depEsc(depDutyLocation(u))+'\"></label>';const routeExtra=document.createElement('details');",1)
s=s.replace("copy.ground=depEl('depGround').value;", "copy.ground=depEl('depGround').value;copy.location=depEl('depSimpleLocation')?.value.trim()||'';",1)
# Remove old card functions so the new complete implementations are canonical.
a=s.index('function depShowDutyCard(u)');b=s.index('// Point-first deployment wizard.',a)
s=s[:a]+(Path('work/officer_details.js').read_text(encoding='utf-8'))+'\n'+s[b:]
p.write_text(s,encoding='utf-8')
