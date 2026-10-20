from pathlib import Path
root=Path(__file__).resolve().parents[1];p=root/'work/viewer-pdf.html';s=p.read_text(encoding='utf-8')
assert 'function enterFeatureDetail' not in s
s=s.replace("if(item.category==='pandal'){enterPandalInterior();return}pandalInterior=false;setConcept(false);", "if(item.category==='pandal'){enterPandalInterior();return}enterFeatureDetail(item);return;pandalInterior=false;setConcept(false);",1)
s=s.replace('function drawPandalInterior(){buildPandalInterior();', "function drawPandalInterior(){if(featureDetailCategory!=='pandal'){drawFeatureDetail();return}buildPandalInterior();",1)
s=s.replace('function enterPandalInterior(){setConcept(false);', "function enterPandalInterior(){featureDetailCategory='pandal';setConcept(false);",1)
addon=(root/'work/feature_scenes.js').read_text(encoding='utf-8');s=s.replace('const initial=presets.pandal;',addon+'\nconst initial=presets.pandal;',1)
p.write_text(s,encoding='utf-8');print('All six main concept features now open their own detailed 3D scene')
