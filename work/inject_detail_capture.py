from pathlib import Path
p=Path('outputs/samagam-3d.html');s=p.read_text(encoding='utf-8');s=s.replace("a.id='previewExport'","image.toBlob(blob=>fetch('http://127.0.0.1:8766/'+featureDetailCategory,{method:'POST',headers:{'Content-Type':'image/png'},body:blob}));a.id='previewExport'");p.write_text(s,encoding='utf-8')
