from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8').replace("if(location.hash==='#deployment')depOpen();", "setTimeout(()=>{if(location.hash==='#deployment')depOpen()},0);",1)
s=s.replace("if(e.target instanceof HTMLInputElement)return;", "if(e.target instanceof HTMLInputElement||e.target instanceof HTMLTextAreaElement||e.target instanceof HTMLSelectElement||e.target.isContentEditable)return;",1)
s=s.replace("<button id=\"depCardEdit\" style=", "<p style=\"font-size:10px;max-height:65px;overflow:auto\">${depEsc(u.notes||'')}</p><button id=\"depCardEdit\" style=",1)
p.write_text(s,encoding='utf-8')
p=Path('work/test_deployment.py');s=p.read_text(encoding='utf-8').replace('let depTime=0;const depRouteEpoch', 'let depTime=0,depDragPause=null;const depRouteEpoch');p.write_text(s,encoding='utf-8')
