from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("for(const o of DATA.objects){const [verts,faces]", "for(const o of DATA.objects){if(['B01','B09','B10','B12','B17'].includes(o.featureId))continue;const [verts,faces]",1)
s=s.replace("interiorCount=out.length/10;", "interiorCount=out.length/10;interiorWorldVertices=new Float32Array(out);",1)
s=s.replace("let pandalInterior=false,interiorBuffer=null", "let interiorWorldVertices=null;let pandalInterior=false,interiorBuffer=null",1)
s=s.replace("interiorScreens.push({buffer,texture})", "interiorScreens.push({buffer,texture,vertices:new Float32Array(verts)})",1)
s=s.replace("boards.push({buffer,texture:tex})", "boards.push({buffer,texture:tex,vertices:new Float32Array(vv)})",1)
s=s.replace("const scene={buffer,count:out.length/10,boards,camera};", "const scene={buffer,count:out.length/10,boards,camera,vertices:new Float32Array(out)};",1)
s=s.replace("function drawFeatureDetail(){const scene=activeFeatureScene;", "function drawFeatureDetail(override){const scene=override||activeFeatureScene;",1)
s=s.replace("else{drawBuffers(prog,false);if(streetMode)drawAK();", "else{drawBuffers(prog,false);drawWorldFacilities();gl.useProgram(prog);gl.uniformMatrix4fv(uniforms.uVP,false,currentVP);if(streetMode)drawAK();",1)
a=s.index('function openConcept3D(item)');b=s.index('\n',a)
s=s[:a]+"function openConcept3D(item){enterWorldFeature(item,false)}"+s[b:]
a=s.index('function enterPandalInterior()');b=s.index('\n',a)
s=s[:a]+"function enterPandalInterior(){enterWorldFeature(conceptItems.find(i=>i.id==='B01'),false,true)}"+s[b:]
s=s.replace("const item=conceptSelected;openConcept3D(item);pandalInterior=false;anim=null;target=[...item.world];enterStreet(nearestStreetPoint())", "enterWorldFeature(conceptSelected,true)")
# Disable obsolete main-world fixed low divider through pandal now that it is walkable.
s=s.replace("if(['B01','B09','B10','B12','B17'].includes(o.featureId))", "if(['B01','B09','B10','B12','B17','W29'].includes(o.featureId))",1)
p.write_text(s,encoding='utf-8')
