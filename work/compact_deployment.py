from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("if(!u){ed.hidden=true;depEl('depList')", "if(!u){depPanel.classList.remove('editing');ed.hidden=true;depEl('depList')")
s=s.replace("ed.append(heading,name,typeRow);", "ed.append(heading);depPanel.classList.add('editing');const back=document.createElement('button');back.textContent='← All duties';back.onclick=()=>{depSelected=null;depRefreshList();depEditor()};ed.prepend(back);")
s=s.replace("ed.prepend(hint);", "advanced.append(hint);")
s=s.replace("ed.append(staff);const routeExtra", "const routeExtra")
s=s.replace("ed.append(route,actions,advanced);", "if(['rider','patrol','qrt','footpatrol','ambulance','fire'].includes(u.type))ed.append(route);else advanced.append(route);ed.append(staff,actions,advanced);depPanel.querySelector('.dep-scroll').scrollTop=0;")
s=s.replace(".dep-panel{width:340px}.dep-head", ".dep-panel{width:340px}.dep-panel.editing .dep-scroll > :not(#depEditor){display:none}.dep-panel.editing #depEditor{display:block}.dep-head")
s=s.replace("depEl('depSearch').after(depQuick);depCatalogue.hidden", "const addPicker=document.createElement('details');addPicker.innerHTML='<summary>Choose object to add</summary>';addPicker.append(depQuick);depEl('depSearch').after(addPicker);depEl('depNew').onclick=()=>{depSelected=null;depEditor();addPicker.open=!addPicker.open;addPicker.scrollIntoView({block:'nearest'})};depCatalogue.hidden")
# Newly created record collapses picker after selection.
s=s.replace("b.onclick=()=>{depNew(type);depEl('depEditor').scrollIntoView({block:'nearest'})};depQuick", "b.onclick=()=>{depNew(type);addPicker.open=false};depQuick")
p.write_text(s,encoding='utf-8')
