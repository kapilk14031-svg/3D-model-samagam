from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8');s=s.replace("if(y>bridge.deck_height-1&&Math.abs(p[0])<bridge.span/2-2&&Math.abs(p[1])>bridge.deck_width/2-AK_RADIUS)return true;", "if(y>bridge.deck_height-1&&Math.abs(p[0])<=bridge.span/2+2.12&&Math.abs(p[1])>bridge.deck_width/2-AK_RADIUS){const stair=([-1,1].some(side=>Math.abs(p[0]-side*bridge.span/2)<2.12&&side*p[1]>=0&&side*p[1]<=(bridge.stair_run||24)));if(!stair)return true;}")
s=s.replace("heading=desiredHeading=side>0?-a:Math.PI-a;", "heading=desiredHeading=side>0?-a:Math.PI-a;actorHeading=heading;")
p.write_text(s,encoding='utf-8')
