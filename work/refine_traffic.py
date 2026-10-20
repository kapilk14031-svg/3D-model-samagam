from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("if(item.category==='traffic'){for(const x", "if(item.category==='traffic'){if(item.source?.kind==='underpass'){box(0,18,-64,95,2,24,'#7a7c71');for(const x of[-21,21])box(x,8.5,-64,4,17,18,'#96998c');for(const z of[-75,-53])box(0,20,z,95,2,.5,'#c2b597')}for(const x")
p.write_text(s,encoding='utf-8')
