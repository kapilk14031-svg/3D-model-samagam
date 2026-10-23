import sys, json
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

raw = '''
Other	Garound A , स्टोर कैंटीन एवं लंगर	29.185407,77.026083
Other	Garound A, main office 	29.185820,77.025965
Entry/exit gate	Garound A, gate no 3	29.185650,77.027322
Other	Graund A, ATM	29.185698,77.026135
Other	Graund A, मैंन ऑफिस से, पंडाल की तरफ जाने वाला रास्ता	29.184673,77.025929
Canteen	Graund A 	29.183434,77.026021
Langar	Graund A 	29.183435,77.025762
Machan - Watchtower	Graund A, A-13	29.182223,77.026758
Machan - Watchtower	Graund A 	29.182224,77.026008
Other	Graund A, SC parking 	29.182207,77.024781
Machan - Watchtower	C ground C1	29.179668,77.018170
Machan - Watchtower	C ground C2	29.180808,77.018381
Machan - Watchtower	B Block B1	29.180896,77.026905
Machan - Watchtower	C ground C3	29.180944,77.015251
Machan - Watchtower	C ground C4	29.182336,77.014651
Machan - Watchtower	C ground C5	29.182381,77.018259
Machan - Watchtower	Ground B B2	29.176435,77.030246
Machan - Watchtower	C ground C 6	29.184613,77.018476
Machan - Watchtower	C ground C7 गेट NO 10 के पास 	29.186234,77.020999
Machan - Watchtower	C ground C8	29.182334,77.020900
Machan - Watchtower	C ground C 9	29.178123,77.021995
Parking	Gate no 1। Parking no 2	29.076682,77.130634
Machan - Watchtower	Graund A 	29.182288,77.023968
Canteen	Ground B canteen no 4	29.135014,77.065292
Parking	Graund A 	29.182222,77.023162
Machan - Watchtower	Graund A , A-10	29.182329,77.022422
Canteen	Ground B canteen no 5	29.133640,77.062789
Outer cordon	Graund A, pandal back side	29.179504,77.022214
Machan - Watchtower	Grond B machan no 5	29.128256,77.059375
Morcha - Security post	Graund A, pandal back right corner 	29.177949,77.022298
Machan - Watchtower	Graund A, pandal right side	29.177741,77.023650
Machan - Watchtower	Grond B machan no 4	29.166559,77.027469
Entry/exit gate	Graund A, pandal rihgt side	29.178026,77.024734
Machan - Watchtower	Garaund A, watchtower with parking 	29.177655,77.026843
Entry/exit gate	Garaund A, front of pandal right 	29.177869,77.026924
Machan - Watchtower	Garaund A, A6	29.177952,77.029323
Foot-bridge	Garaund A 	29.177984,77.029219
Outer cordon	Garaund A, pandal front side	29.179316,77.028735
Machan - Watchtower	Garaund A, A5	29.180392,77.028536
Machan - Watchtower	Garaund A A4	29.182095,77.028101
Entry/exit gate	Garaund A , gate no 2	29.182409,77.028221
'''

# Transformation matrix M:
M = np.array([
    [ 5.53456049e+04,  6.27126153e+03],
    [ 2.04433779e+03, -6.47985609e+04],
    [-4.32253675e+06,  1.40805118e+06]
])

items = []
for idx, line in enumerate(raw.strip().splitlines()):
    parts = line.split('\t')
    if len(parts) >= 3:
        cat = parts[0].strip()
        name = parts[1].strip()
        c = [float(x.strip()) for x in parts[2].split(',')]
        lat, lon = c[0], c[1]
        model_pos = np.array([lon, lat, 1.0]) @ M
        x, z = model_pos[0], model_pos[1]
        items.append({
            'index': idx + 1,
            'cat': cat,
            'name': name,
            'lat': lat,
            'lon': lon,
            'x': round(float(x), 2),
            'z': round(float(z), 2)
        })

print(f"Total parsed: {len(items)}")
# Check for items
for it in items:
    print(f"{it['index']:2d} | {it['cat'][:15]:15} | {it['x']:7.1f}, {it['z']:7.1f} | {it['name']}")
