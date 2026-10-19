from pathlib import Path
p=Path(__file__).with_name('viewer-v2.html');s=p.read_text(encoding='utf-8')
s=s.replace("const fs=`precision highp float;", "const depthTextureExtension=gl.getExtension('WEBGL_depth_texture');\nconst fs=`precision highp float;")
s=s.replace("float dep=unpack(texture2D(uShadow,sc.xy+vec2(float(x),float(y))/2048.));", "float dep=${depthTextureExtension?'texture2D(uShadow,sc.xy+vec2(float(x),float(y))/2048.).r':'unpack(texture2D(uShadow,sc.xy+vec2(float(x),float(y))/2048.))'};")
s=s.replace("sc.z-.0015>dep", "sc.z-.003>dep")
old="const shadowOK=gl.checkFramebufferStatus(gl.FRAMEBUFFER)===gl.FRAMEBUFFER_COMPLETE;"
new="let depthTex=null;if(depthTextureExtension){depthTex=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,depthTex);gl.texImage2D(gl.TEXTURE_2D,0,gl.DEPTH_COMPONENT,2048,2048,0,gl.DEPTH_COMPONENT,gl.UNSIGNED_SHORT,null);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.NEAREST);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.NEAREST);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);gl.framebufferTexture2D(gl.FRAMEBUFFER,gl.DEPTH_ATTACHMENT,gl.TEXTURE_2D,depthTex,0)}const shadowOK=gl.checkFramebufferStatus(gl.FRAMEBUFFER)===gl.FRAMEBUFFER_COMPLETE;"
s=s.replace(old,new).replace("gl.bindTexture(gl.TEXTURE_2D,shadowTex);gl.uniform1i", "gl.bindTexture(gl.TEXTURE_2D,depthTex||shadowTex);gl.uniform1i")
s=s.replace("drawBuffers(shadowProg,true)", "gl.enable(gl.POLYGON_OFFSET_FILL);gl.polygonOffset(2,4);drawBuffers(shadowProg,true);gl.disable(gl.POLYGON_OFFSET_FILL)")
p.write_text(s,encoding='utf-8')
