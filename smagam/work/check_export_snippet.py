from pathlib import Path
ROOT = Path("79-th-nirankari-sant-samagam-bhodwal/smagam")
src = (ROOT / 'work/build_model.py').read_text(encoding='utf-8')
export = src[src.index('cubeV='):src.index('# A separate, recentered GLB')]
print("Export code snippet length:", len(export))
print("First 300 chars of export code:")
print(export[:300])
