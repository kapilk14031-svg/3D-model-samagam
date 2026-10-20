from pathlib import Path
p=Path('work/test_deployment_picking.py');s=p.read_text(encoding='utf-8').replace("let eye=[0,8,30]", "let depFollowState=null,depVehicleCamera=null;let eye=[0,8,30]");p.write_text(s,encoding='utf-8')
p=Path('work/test-nearby-icons.cjs');s=p.read_text(encoding='utf-8');new=next(l for l in Path('work/viewer-pdf.html').read_text(encoding='utf-8').splitlines() if l.startswith('function depIconNearby('));s='\n'.join(new if l.startswith('function depIconNearby(') else l for l in s.splitlines());p.write_text(s,encoding='utf-8')
