from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("depMode='addPoint';depSelected=null;depPanel.hidden=true;", "depMode='addPoint';depSelected=null;depPanel.hidden=false;depRefreshList();depEditor();")
s=s.replace("function depPointOptions(p,x,y){depChoose.replaceChildren();", "function depPointOptions(p,x,y){depPanel.hidden=true;depChoose.replaceChildren();")
s=s.replace("SELECT DUTY · PLACE ON MAP · DRAW PATH", "CLICK MODEL TO ADD · SELECT DUTY TO EDIT")
p.write_text(s,encoding='utf-8')
