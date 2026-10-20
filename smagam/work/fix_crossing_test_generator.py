from pathlib import Path
p=Path('work/test_full_crossing.py');s=p.read_text(encoding='utf-8').replace("moveWalker(-25*s,-25*c,.016);assert(walker[1]<2,'opposite stair descent failed')", "for(let i=0;i<250;i++)moveWalker(-.1*s,-.1*c,.016);assert(walker[1]<2,'opposite stair descent failed')");p.write_text(s,encoding='utf-8')
