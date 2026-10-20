from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("function depBeginPick(mode){const u=depUnits.find(u=>u.id===depSelected);if(!u)return;depMode=mode;depDraftRoute=mode==='route'?depClone(u.route):[];", "function depBeginPick(mode){const u=depUnits.find(u=>u.id===depSelected);if(!u)return;if(!depFlow)depFlow={before:depClone(depUnits),undoLength:depUndoStack.length,id:u.id};depMode=mode;depDraftRoute=mode==='route'&&u.position?[[...u.position]]:[];")
# Closing the editor of an unsaved draft returns to its Save / Cancel preview.
s=s.replace("depEl('depClose').onclick=()=>depPanel.hidden=true;", "depEl('depClose').onclick=()=>{depPanel.hidden=true;if(depFlow)depReviewDraft()};")
# Undo cannot replace the plan while a wizard transaction is pending.
s=s.replace("depEl('depUndo').onclick=()=>{if(!depUndoStack.length)", "depEl('depUndo').onclick=()=>{if(depFlow){depCancelDraft();return}if(!depUndoStack.length)")
p.write_text(s,encoding='utf-8')
