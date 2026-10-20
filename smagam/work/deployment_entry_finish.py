from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8').replace("function depOpen(id){if(id)","function depOpen(id){if(conceptMode)go('top');if(id)",1)
s=s.replace("if(!u||depDraftRoute.length<2){", "if(!u||depDraftRoute.length<2||!depDraftRoute.some((p,i)=>i&&Math.hypot(p[0]-depDraftRoute[i-1][0],p[2]-depDraftRoute[i-1][2])>1)){",1)
pos=s.index('function focusFeature(f)');s=s[:pos]+"window.addEventListener('hashchange',()=>{if(location.hash==='#deployment')depOpen()});if(location.hash==='#deployment')depOpen();\n"+s[pos:];p.write_text(s,encoding='utf-8')
p=Path('work/test_deployment.py');s=p.read_text(encoding='utf-8').replace('let depTime=0;', 'let depTime=0;const depRouteEpoch=new Map();');p.write_text(s,encoding='utf-8')
