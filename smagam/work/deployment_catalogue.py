from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace('function depNew(){depUndoPush();','function depNew(type=\'officer\'){if(!DEP_TYPES[type])type=\'officer\';depUndoPush();',1)
s=s.replace("title:'New police duty',type:'officer'", "title:'New '+DEP_TYPES[type],type",1)
pos=s.rindex('depRefreshList();')
s=s[:pos]+'''const depCatalogue=document.createElement('details');const depCatalogueTitle=document.createElement('summary');depCatalogueTitle.textContent='Add 3D object / model catalogue';depCatalogue.append(depCatalogueTitle);const depCatalogueButtons=document.createElement('div');depCatalogueButtons.className='dep-mini-actions';for(const type of ['machan','morcha','barricade','naka','officer','rider','qrt','patrol','ambulance','fire']){const b=document.createElement('button');b.textContent='+ '+DEP_TYPES[type];b.onclick=()=>{depNew(type);depEl('depEditor').scrollIntoView({block:'nearest'})};depCatalogueButtons.append(b)}depCatalogue.append(depCatalogueButtons);depEl('depSummary').after(depCatalogue);
'''+s[pos:]
p.write_text(s,encoding='utf-8')

