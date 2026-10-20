from pathlib import Path
p=Path('work/test-walk-physics.cjs');s=p.read_text(encoding='utf-8');s+='''
{const b=DATA.meta.s04_footbridge,a=b.angle,c=Math.cos(a),s=Math.sin(a);walker=[b.anchor[0]+b.span/2*c+25*s,.3,b.anchor[2]-b.span/2*s+25*c];moveWalker(-25*s,-25*c,.016);assert(walker[1]>24);moveWalker(-b.span*c,b.span*s,.016);assert(walker[1]>24,'crossing deck failed');for(let i=0;i<250;i++)moveWalker(-.1*s,-.1*c,.016);assert(walker[1]<2,'opposite stair descent failed')}
console.log('PASS: full ascent > cross deck > opposite-side descent');
''';p.write_text(s,encoding='utf-8')
