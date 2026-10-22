from pathlib import Path
import zipfile,shutil
root=Path(__file__).resolve().parents[1];out=root/'outputs';work=root/'work';delivery=root.parent/'outputs'
new=['GATE-3-UPDATE.md','gate-3-photo-boundary-aligned.jpg','gate-3-open-boundary-aligned.jpg','gate-3-reference-photo.jpg','source/gate3_photo_geometry.py','source/gate_details.py','source/clear_photo_gate_frontage.py','source/test_gate3_photo.py']
new+=['source/'+n for n in ['viewer-pdf.html','frontage_boundary.py','test_keyboard_controls.py','test-keyboard-controls.cjs','test_object_keyboard.py','test-object-keyboard.cjs','test_photo_gates.py','test_photo_gate_walk.py','test-photo-gate-walk.cjs','test_deployment.py','test_pause_movement.py','test_deployment_picking.py']]
archive=delivery/'samagam-3d-package.zip';temp=work/'updated-gate3-package.zip'
with zipfile.ZipFile(archive) as old,zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
 names=old.namelist()
 for name in dict.fromkeys(names+new):
  candidates=[work/name[7:]] if name.startswith('source/') else [out/name,delivery/name]
  p=next((p for p in candidates if p.is_file()),None)
  if p:z.write(p,name)
  elif name in names:z.writestr(name,old.read(name))
temp.replace(archive);shutil.copyfile(archive,out/'samagam-3d-package.zip')
with zipfile.ZipFile(archive) as z:
 assert z.read('samagam-3d.html')==(out/'samagam-3d.html').read_bytes()
 assert b'depManualJump' in z.read('samagam-3d.html')
print('Updated ZIP verified: current HTML/GLB/data, source, controls guide and previews')
