from pathlib import Path
p=Path(__file__).with_name('viewer-v2.html');s=p.read_text(encoding='utf-8')
s=s.replace('bridgeFocus=false,flyoverFocus=false;', 'bridgeFocus=false,flyoverFocus=false,pandalFocus=false;')
s=s.replace("flyoverFocus=view==='flyover';document", "flyoverFocus=view==='flyover';pandalFocus=view==='pandal'||view==='stage';document")
s=s.replace("if(!show||hidden.has(l.layer))continue;", "if(!show||hidden.has(l.layer))continue;if(pandalFocus&&l.layer!=='pandal')continue;if(l.stageOnly&&!cutaway)continue;")
s=s.replace("el.className='map-label'+(/GROUND", "el.className='map-label'+(l.banner?' banner':'')+(/GROUND")
s=s.replace('</style></head>', '.map-label.banner{background:transparent;border:0;box-shadow:none;color:#f2e1ad;font-size:13px;font-weight:650;letter-spacing:.4px;text-shadow:0 1px 3px #244b50}</style></head>')
p.write_text(s,encoding='utf-8')
