from pathlib import Path
p = Path("79-th-nirankari-sant-samagam-bhodwal/smagam/work/viewer-pdf.html.bak")
lines = p.read_text(encoding="utf-8").splitlines()
l624 = lines[623]
print("Line 624 length:", len(l624))
print("Starts with:", l624[:60])
print("Ends with:", l624[-60:])
