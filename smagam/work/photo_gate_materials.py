from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("const n=o.name.toLowerCase();\n if(/foliage", "const n=o.name.toLowerCase();\n if(o.photoGate&&/steel gate leaf|steel panel seam|gate leaf.*frame|lock strap|hinge|drop bolt/.test(n))return 5;\n if(o.photoGate&&/brown lower entrance door/.test(n))return 6;\n if(/foliage",1)
p.write_text(s,encoding='utf-8')
