from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("depChoose.style.cssText='position:absolute;z-index:28;", "depChoose.style.cssText='position:fixed;z-index:42;max-height:calc(100vh - 100px);overflow:auto;")
s=s.replace("depReview.style.bottom='22px';", "depReview.style.cssText='position:fixed;left:16px;bottom:18px;z-index:42;max-width:calc(100vw - 32px)';")
s=s.replace("depRoutebar.append(depListButton);", "depRoutebar.append(depListButton);depRoutebar.style.cssText='position:fixed;left:16px;bottom:18px;z-index:40;max-width:calc(100vw - 32px)';")
s=s.replace("Math.min(W-315,x+12)","Math.min(window.innerWidth-315,x+12)")
s=s.replace("Math.max(120,Math.min(H-300,y-70))", "Math.max(80,Math.min(window.innerHeight-370,y-70))")
# Point-first mode should not inherit a selected object from a previous card.
s=s.replace("function depStartPointMode(){if(depFlow)","function depStartPointMode(){if(typeof depDutyCard!=='undefined')depDutyCard.hidden=true;if(depFlow)")
p.write_text(s,encoding='utf-8')
