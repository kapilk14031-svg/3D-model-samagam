from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("let depUnits=[],depSelected", "let depFlow=null,depPointActive=false;\nlet depUnits=[],depSelected",1)
s=s.replace("function depPersist(){try", "function depPersist(){if(depFlow){depDirty=true;dirty=true;depEl('depStatus').textContent='Preview only · click Save changes';return}try",1)
s=s.replace("depSimplifyEditor();depEl('depSave').onclick=depSaveEditor;", "depSimplifyEditor();depEl('depSave').onclick=depSaveButton;",1)
s=s.replace("depEl('depDelete').onclick=()=>{depUndoPush();", "depEl('depDelete').onclick=()=>{if(depFlow&&u.id===depFlow.id){depCancelDraft();return}depUndoPush();",1)
s=s.replace("depEl('depSave').textContent='Save';", "depEl('depSave').textContent='Save changes';",1)
s=s.replace("if(!depVisible||!depModelsOn||depMode||boxMode||placeStreet)", "if(!depVisible||!depModelsOn||(depMode&&depMode!=='addPoint')||boxMode||placeStreet)",1)
s=s.replace("if(location.hash==='#deployment')depOpen()", "if(location.hash==='#deployment')depStartPointMode()")
marker='// Screen-space'
i=s.index(marker)
s=s[:i]+(Path('work/point_first_deployment.js').read_text(encoding='utf-8'))+'\n'+s[i:]
p.write_text(s,encoding='utf-8')
