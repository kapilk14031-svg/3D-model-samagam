from pathlib import Path
p=Path(__file__).with_name('viewer-v2.html');s=p.read_text(encoding='utf-8')
s=s.replace('</style></head>', '@media(max-width:760px){.scene.bridge-detail{height:max(420px,calc(100svh - 20px))}}</style></head>')
s=s.replace("bridgeFocus=view==='bridge';if(bridgeFocus)","bridgeFocus=view==='bridge';sceneEl.classList.toggle('bridge-detail',bridgeFocus);if(bridgeFocus)")
s=s.replace("canvas.scrollIntoView({block:'center',behavior:'smooth'})", "sceneEl.scrollIntoView({block:'start',behavior:'smooth'})")
s=s.replace("const w=el.offsetWidth,h=el.offsetHeight,r=[p.x-w/2-5,p.y-h/2-4,w+10,h+8];", "const w=el.offsetWidth,h=el.offsetHeight;p.x=Math.max(w/2+9,Math.min(W-w/2-9,p.x));const r=[p.x-w/2-5,p.y-h/2-4,w+10,h+8];")
p.write_text(s,encoding='utf-8')
