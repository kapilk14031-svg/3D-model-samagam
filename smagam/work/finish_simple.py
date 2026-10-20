from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("if(!name)return;const u=depUnits", "if(!name)return;const rank=depEl('depSimpleRank');if(name.value===name.defaultValue&&rank.value===rank.defaultValue)return;const u=depUnits")
p.write_text(s,encoding='utf-8')
