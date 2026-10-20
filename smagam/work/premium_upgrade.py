from pathlib import Path
root=Path(__file__).resolve().parent
p=root/'build_pdf_model.py';s=p.read_text()
s=s.replace("objects=[];labels=[];routes=[];extra_shapes={};current=''", "objects=[];labels=[];routes=[];extra_shapes={};current=''\nexec((ROOT/'work/pandal_geometry.py').read_text(encoding='utf-8').split('def pb(')[0])")
s=s.replace("'#a8b38d'","'#b8c1a4'").replace("'#626d68'","'#566362'").replace("'#c6c0a8'","'#d7cfba'")
s=s.replace("xx,16,z,bw,9,d,'#f2e6ca'","xx,20,z,bw,16,d,'#f6edda'")
s=s.replace("16+9*math.sqrt", "20+16*math.sqrt")
s=s.replace("box('Maroon fabric valance',xx,zz,bw,1,2,'#985c60',14,'pandal')", "add('Scalloped wine fabric valance','valance',xx,17,zz,bw,3,1,'#804952','pandal');objects[-1]['part']='roof'")
s=s.replace("'#dac48b',16,'pandal'","'#dac48b',20,'pandal'")
s=s.replace("1,1,16,'#cfbfa2'","1,1,20,'#cfbfa2'")
s=s.replace("box('Pandal carpet',x,z,w*.94,d*.92,.2,'#ba9371',.7,'pandal')", """box('Pandal carpet',x,z,w*.94,d*.92,.2,'#bda17c',.7,'pandal')
        for row in range(4):
            for col in range(9):
                xx=x-w*.27+col*w*.078;zz=z-d*.36+row*d*.235
                box('Illustrative seating carpet panel',xx,zz,w*.065,d*.19,.15,'#a96061',1,'pandal')
        for zz in [z-d*.31,z+d*.31]:
            add('Illustrative stage arch','arch',x-w*.4,5,zz,8,11,d*.18,'#dcc68e','pandal');objects[-1]['rotY']=1.5707963
        for zz in [z-d/2-5,z+d/2+5]:
            for j in range(12):
                xx=x-w/2+12+j*(w-24)/11
                box('Decorative planter',xx,zz,3,3,2,'#9c8d6d',0,'pandal')
                add('Decorative topiary','ellipsoid',xx,2,zz,5,5,5,'#648268','pandal')
                box('Warm architectural light post',xx,zz,.5,.5,9,'#8d9c92',0,'pandal')
                add('Lantern diffuser','ellipsoid',xx,9,zz,1.5,1.4,1.5,'#f0d6a0','pandal')""")
p.write_text(s,encoding="utf-8")
p=root/'viewer-pdf.html';s=p.read_text()
css='''
:root{--ink:#153f45;--gold:#bd9a5e;--paper:#f5f3eb}body{background:var(--paper);color:var(--ink)}header{background:#102f36;border-bottom:1px solid #36525a;height:90px;padding:0 30px}.number{color:#dfbd7c;border-color:#536c70;font-size:36px;font-family:Georgia,serif}h1{font-family:Georgia,serif;font-size:24px;font-weight:400;letter-spacing:.4px}.subtitle{font-size:9px;letter-spacing:1.5px;color:#bdcbd0}.stamp{border-radius:4px;border-color:#6d7770;color:#dfbd7c;font-size:9px}main{grid-template-columns:265px 1fr;height:calc(100vh - 90px);min-height:720px}aside{background:#143740;color:#d9e2dd;border:0;padding:24px 18px}.eyebrow{color:#b9a87f;font-size:9px;letter-spacing:2px}.views{gap:8px}.views button{border:1px solid #496169;background:#1c4049;color:#d3deda;border-radius:8px;padding:14px 10px;text-align:left;min-height:56px;transition:background .2s,transform .2s}.views button:hover{background:#30545a;transform:translateY(-1px)}.views button.active{background:#d9bd85;color:#183840;border-color:#d9bd85;font-weight:650;box-shadow:0 5px 16px #071f2533}.divider{background:#49616a;margin:22px 0}.layer{font-size:11px;padding:8px 0;color:#bcccc9}.layer input{accent-color:#ccb17c}.legend,.sidefoot,.range-row,.status{color:#a9bdbb;font-size:10px;line-height:1.9}.legend a,.sidefoot a{color:#e0c48c;text-decoration:none}.scene{background:#e6eadd}.scene-toolbar{top:20px;left:24px;right:24px}.location{padding:10px 14px;background:#f9f8eecc;border:1px solid #fff9;border-radius:9px;backdrop-filter:blur(15px);font-size:10px;color:#648078}.location b{font-size:12px;letter-spacing:.5px;color:#264b4e}.actions{max-width:320px;gap:6px}.actions button{background:#f9f8eee8;border:1px solid #d7ded0;border-radius:7px;color:#365958;font-size:10px;padding:9px 12px;box-shadow:0 3px 12px #35492c08}.actions button.active{background:#204d50}.notice{bottom:17px;left:24px;right:24px;border-radius:9px;background:#f8f8f0e8;backdrop-filter:blur(12px);border-color:#d5ddce;padding:12px 15px;font-size:10px;color:#6b7c71}.notice b{color:#997c44;letter-spacing:1.5px}.hint{bottom:93px;color:#506a63;letter-spacing:1px;font-size:9px}.map-label{background:#faf9f0ee;color:#355952;border:1px solid #d0d9c7;padding:5px 8px;border-radius:5px;font-size:9px;box-shadow:0 3px 10px #23483d10}.map-label.major{background:#204f51;color:#fff0d1;padding:7px 11px;font-size:10px;letter-spacing:1px}.selection{background:#faf9efed;backdrop-filter:blur(16px);border-color:#d3ddcb;border-radius:10px;box-shadow:0 8px 30px #24443a16}footer{padding:30px clamp(16px,4vw,65px);background:#f5f3eb;color:#49635c}footer details{padding:18px 20px;background:#fcfbf5;border:1px solid #dce1d3;border-radius:10px}footer summary{font-size:13px;color:#20474b}footer h2{font-family:Georgia,serif;font-weight:400;font-size:25px}#pdfLegend{display:grid;grid-template-columns:1fr 1fr;gap:5px 24px;font-size:11px}.source-note{background:#e9eddf;border-left:3px solid #b79a60;border-radius:4px;line-height:1.8;font-size:11px}#search{border-radius:8px;background:#fffef8;border-color:#d3dccb}td{font-size:11px}td button{background:#214d50}thead{background:#e5ebdf;position:sticky;top:0}.register-wrap{border:1px solid #d8dfcf;border-radius:8px}
@media(max-width:760px){header{height:auto;min-height:88px;padding:18px}h1{font-size:20px}.number{font-size:30px}.subtitle{font-size:8px;letter-spacing:.8px}main{height:auto;min-height:0}aside{padding:14px 14px 12px}.views{grid-template-columns:repeat(3,1fr);gap:6px}.views button{min-height:40px;padding:10px;font-size:10px}.eyebrow{margin-bottom:9px}.side-layers{grid-template-columns:repeat(3,1fr);margin-top:12px}.layer{font-size:9px;padding:5px 0}.legend{display:none!important}.scene{height:max(650px,calc(100svh - 20px))}.scene-toolbar{top:12px;left:12px;right:12px;gap:6px}.location{padding:7px 9px;max-width:130px!important;font-size:8px}.location b{font-size:10px}.actions{max-width:215px;gap:4px}.actions button{font-size:9px;padding:7px 8px}.notice{left:12px;right:12px;font-size:9px;line-height:1.6}.hint{left:14px;font-size:8px}.selection{top:100px}#pdfLegend{grid-template-columns:1fr}footer{padding:20px 14px}footer details{padding:14px}.map-label{font-size:8px}.map-label.major{font-size:9px}}
'''
s=s.replace('</style>',css+'</style>')
s=s.replace('PDF PLAN RECONSTRUCTION','THE SAMAGAM ATLAS · PDF PLAN EDITION').replace('Explore the source plan','The venue collection')
s=s.replace('PDF · All grounds','79th Samagam · spatial atlas')
s=s.replace("<details open><summary>All 11 source legend entries", "<details><summary>All 11 source legend entries")
s=s.replace("saturation", "saturation")
# Start with a pandal-focused presentation, retaining all-ground presets.
s=s.replace('const initial=presets.overview;', 'const initial=presets.pandal;')
s=s.replace('distance=initial.distance;', 'distance=Math.max(initial.distance,640/(sceneEl.clientWidth/sceneEl.clientHeight));')
s=s.replace("[.895,.92,.865]", "[.905,.93,.89]")
# Save button reveals a durable rendered-image link for browser download tooling.
s=s.replace("a.href=image.toDataURL();a.click()", "a.href=image.toDataURL();a.id='previewExport';a.textContent='Download this rendered view';a.style.cssText='position:absolute;bottom:105px;right:18px;background:#fff9e8;padding:10px;border-radius:6px;z-index:4';document.getElementById('previewExport')?.remove();sceneEl.append(a);a.click()")
p.write_text(s,encoding="utf-8")
print('Premium presentation applied')
