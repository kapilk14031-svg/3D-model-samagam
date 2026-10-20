from pathlib import Path
p=Path(__file__).with_name('viewer-v2.html');s=p.read_text(encoding='utf-8')
s=s.replace("c.scale(d,d);c.fillStyle='#173e34'", "c.scale(d,d);for(const {el} of labelNodes){if(el.style.display==='none')continue;const x=parseFloat(el.style.left),y=parseFloat(el.style.top);if(!Number.isFinite(x)||!Number.isFinite(y))continue;c.font='10px Segoe UI';const w=c.measureText(el.textContent).width+14;c.fillStyle='#f8f7ee';c.fillRect(x-w/2,y-10,w,21);c.fillStyle='#37513f';c.fillText(el.textContent,x-w/2+7,y+4)}c.fillStyle='#173e34'")
p.write_text(s,encoding='utf-8')
