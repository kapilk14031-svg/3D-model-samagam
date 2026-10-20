from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8');pos=s.index('function focusFeature(f)');s=s[:pos]+Path('work/world_facilities.js').read_text(encoding='utf-8')+'\n'+s[pos:];p.write_text(s,encoding='utf-8')
