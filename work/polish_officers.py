from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("if(feature)return feature.name+(u.ground?' · Ground '+u.ground:'');", "if(feature)return feature.name+(u.ground&&feature.category!=='ground'?' · Ground '+u.ground:'');")
s=s.replace("depDutyCard.style.position='fixed';", "depDutyCard.style.zIndex='45';depDutyCard.style.position='fixed';")
p.write_text(s,encoding='utf-8')
for file in ['test_walk_physics.py','test_full_crossing.py']:
 p=Path('work')/file
 if p.exists():
  s=p.read_text(encoding='utf-8').replace('side*30','side*(b.span/2)').replace('let x=-30','let x=-b.span/2');p.write_text(s,encoding='utf-8')
