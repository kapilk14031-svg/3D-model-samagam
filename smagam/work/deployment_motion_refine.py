from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("const DEP_KEY='samagam-duty-deployment-v1';", "const DEP_KEY='samagam-duty-deployment-v1';const depRouteEpoch=new Map();",1)
s=s.replace("target=[...u.position];target[1]+=3;distance=100;", "target=[...(depPose(u)?.p||u.position)];target[1]+=3;distance=70;",1)
s=s.replace("u.route=depClone(depDraftRoute);u.position=[...u.route[0]];", "u.route=depClone(depDraftRoute);u.position=[...u.route[0]];depRouteEpoch.set(u.id,depTime);",1)
s=s.replace("let d=depTime*u.speed,reverse=false;", "let d=Math.max(0,depTime-(depRouteEpoch.get(u.id)||0))*u.speed,reverse=false;",1)
s=s.replace("box(0,10.8,0,5.7,.3,5.7,'#59674d');", "part('roof',0,10.6,0,5.7,1.4,5.7,'#59674d');for(const x of[-2.4,2.4])box(x,8.3,0,.2,.9,5,'#6e7758');",1)
p.write_text(s,encoding='utf-8')
