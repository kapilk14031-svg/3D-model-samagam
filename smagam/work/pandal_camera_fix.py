from pathlib import Path
p=Path(__file__).with_name('viewer-v2.html');s=p.read_text(encoding='utf-8').replace("if(flyoverFocus||previousFlyover){target=", "if(flyoverFocus||previousFlyover||view==='pandal'||view==='stage'){target=")
p.write_text(s,encoding='utf-8')
