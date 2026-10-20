from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("if(f.size>2000000)throw Error('File must be smaller than 2 MB.')", "if(f.size>20000000)throw Error('File must be smaller than 20 MB.')",1)
s=s.replace(".dep-icon.selected{", ".dep-icon.shared{border-style:dashed;border-color:#edb65f}.dep-icon.selected{",1)
s=s.replace("el.classList.toggle('selected',u.id===depSelected);el.style.left=p.x+'px'", "el.classList.toggle('selected',u.id===depSelected);el.classList.toggle('shared',!u.shifts[depShift]&&!!u.shifts.combined);el.style.left=p.x+'px'",1)
p.write_text(s,encoding='utf-8')
a=s.index('// Editable local duty plan.');b=s.index('// Screen-space minimum width',a);addon=s[a:b];start=addon.index('const DEPLOYMENT_SEED=');end=addon.index('\nconst DEP_TYPES',start);addon=addon[:start]+'const DEPLOYMENT_SEED=__DUTY_SEED__;'+addon[end:];Path('work/deployment_panel.js').write_text(addon,encoding='utf-8')
