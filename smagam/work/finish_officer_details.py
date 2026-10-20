from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("note:DEPLOYMENT_SEED.note,units:depUnits},null,2)", "note:DEPLOYMENT_SEED.note,units:depUnits,existingOfficerDetails:depBaseDetails},null,2)")
s=s.replace("const units=depValidate(JSON.parse(await f.text()));depUndoPush();", "const imported=JSON.parse(await f.text()),units=depValidate(imported);if(imported.existingOfficerDetails&&typeof imported.existingOfficerDetails==='object'&&!Array.isArray(imported.existingOfficerDetails)){depBaseDetails=Object.fromEntries(Object.entries(imported.existingOfficerDetails).map(([key,v])=>[key,Object.fromEntries(['name','rank','contact','duty','location'].map(f=>[f,String(v?.[f]||'').slice(0,500)]))]));try{localStorage.setItem('samagam-existing-officer-details-v1',JSON.stringify(depBaseDetails))}catch{}}depUndoPush();")
p.write_text(s,encoding='utf-8')
