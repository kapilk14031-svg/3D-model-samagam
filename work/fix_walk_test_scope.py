from pathlib import Path
p=Path('work/test_walk_physics.py');s=p.read_text(encoding='utf-8').replace("b=s.index('function focusFeature(f)',a)","b=s.index('// Editable local duty plan.',a)");p.write_text(s,encoding='utf-8')
