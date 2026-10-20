from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace('function frame(t){let dt=', 'let lastSceneRender=0;\nfunction frame(t){let dt=',1)
s=s.replace('if(dirty)render();requestAnimationFrame(frame)', 'if(dirty&&t-lastSceneRender>=40){render();lastSceneRender=t}requestAnimationFrame(frame)',1)
p.write_text(s,encoding='utf-8')
