from pathlib import Path
p=Path(__file__).with_name('viewer-template.html');s=p.read_text(encoding='utf-8')
s=s.replace("for(let fi=0;fi<item.faces.length;fi++){const f=", "for(let fi=0;fi<item.faces.length;fi++){if(item.o.layer==='site'&&fi!==3)continue;const f=")
s=s.replace("const shade=[.82", "let area=0;for(let k=0;k<pts.length;k++){const a=pts[k],b=pts[(k+1)%pts.length];area+=a[0]*b[1]-b[0]*a[1]}if(area>=0)continue;const shade=[.82")
s=s.replace("all.sort((a,b)=>a.depth-b.depth)","all.sort((a,b)=>{const oa=DATA.objects[a.oi],ob=DATA.objects[b.oi];if(oa.layer==='site'&&ob.layer==='site')return oa.p[1]-ob.p[1];if(oa.layer==='site')return -1;if(ob.layer==='site')return 1;return a.depth-b.depth})")
s=s.replace('main{display:grid;grid-template-columns:275px 1fr;min-height:740px}', 'main{display:grid;grid-template-columns:275px 1fr;min-height:740px}section{max-height:940px}')
s=s.replace('3D ground study &nbsp; / &nbsp;', '3D ground study &nbsp; / &nbsp;')
s=s.replace('Exact reconstruction requires', 'A foot overbridge near Haldana in front of the Samagam is confirmed in the Ministry of Road Transport and Highways reply to Lok Sabha Starred Question 11 (20 July 2023), km 66.020; its dimensions here are illustrative. Exact reconstruction requires')
p.write_text(s,encoding='utf-8')
