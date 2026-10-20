from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
a=s.index('function depPlaceExtraOfficerIcons(){');b=s.index('\nfunction depShowBaseOfficer',a)
s=s[:a]+'''function depPlaceExtraOfficerIcons(){depExtraOfficers=depCollectExistingOfficers();for(const el of depExtraIconNodes.values())el.remove();depExtraIconNodes.clear()}'''+s[b:]
s=s.replace("paths[type==='qrt'?'patrol':type]||paths.officer", "paths[type==='qrt'?'patrol':type]||'<circle cx=\"12\" cy=\"12\" r=\"5\"/>'")
p.write_text(s,encoding='utf-8')
