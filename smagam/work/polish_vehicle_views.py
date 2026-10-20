from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("if(depFollowState){depFollowState.mode=mode;", "if(depFollowState){depFollowState.id=u.id;depFollowState.mode=mode;",1)
s=s.replace("streetMode||depFollowState?.mode==='fpv'?.12:4", "(streetMode||depFollowState)?.12:4",1)
start=s.index('function depScreenRay(');end=s.index('\nfunction ',start+5);line=s[start:end]
line=line.replace("Math.tan((streetMode?1.05:.72)/2)","Math.tan((depFollowState?(depFollowState.mode==='fpv'?depFollowState.fov:.85):streetMode?1.05:.72)/2)")
s=s[:start]+line+s[end:]
p.write_text(s,encoding='utf-8')
