// New deployable visual equipment; shared editor and backend lifecycle.
function depBuildRifle(g,y=1.06,z=-.30,lmg=false){
 depPart(g,'box',[.05,y,z],[.12,.13,.40],'dark');
 depPart(g,'box',[.05,y,z+.30],[.10,.12,.26],'dark');
 const barrel=depPart(g,'cylinder',[.05,y,z-.43],[.026,lmg?.65:.48,.026],'dark');barrel.rotation.x=Math.PI/2;
 depPart(g,'box',[.05,y-.16,z-.03],[.07,.24,.12],'dark');
 depPart(g,'box',[.05,y+.09,z-.08],[.04,.05,.12],'dark');
 if(lmg){depPart(g,'box',[.20,y-.12,z],[.24,.20,.25],'dark');for(const x of [-.14,.24]){const leg=depPart(g,'box',[x,y-.18,z-.57],[.025,.35,.025],'chrome');leg.rotation.z=x<0?-.4:.4;}}
}
function depBuildArmedOfficer(g){depBuildOfficer(g,'officer');depBuildRifle(g);}
function depBuildQRT(g){
 depPart(g,'box',[0,.50,0],[1.85,.22,3.95],'dark');
 depPart(g,'box',[0,.91,-1.35],[1.8,.54,1.25],'whiteBody');
 depPart(g,'box',[0,.89,1.02],[1.82,.44,1.62],'blue');
 for(const x of [-.88,.88])depPart(g,'box',[x,1.16,.12],[.10,.42,2.18],'whiteBody');
 depPart(g,'box',[0,.87,1.93],[1.8,.46,.10],'whiteBody');
 for(const x of [-1,1])for(const z of [-1.25,1.28]){const w=depPart(g,'cylinder',[x,.43,z],[.40,.22,.40],'tireRubber');w.rotation.z=Math.PI/2;const rim=depPart(g,'cylinder',[x*1.12,.43,z],[.21,.04,.21],'chrome');rim.rotation.z=Math.PI/2;}
 for(const x of [-.83,.83]){depPart(g,'box',[x,1.67,-.62],[.06,.85,.06],'dark');depPart(g,'box',[x,1.78,.95],[.06,1.1,.06],'dark');}
 depPart(g,'box',[0,2.32,.95],[1.72,.07,.07],'dark');
 depPart(g,'box',[0,2.12,-.62],[1.72,.07,.07],'dark');
 depPart(g,'box',[0,1.73,-.65],[1.58,.64,.035],'glassTint');
 for(const x of [-.55,.55]){depPart(g,'box',[x,.85,-.10],[.59,.18,.55],'dark');depPart(g,'box',[x,1.1,.15],[.59,.55,.12],'dark');depPart(g,'box',[x,.98,-1.99],[.30,.24,.05],'white');}
 depPart(g,'box',[0,.55,-2.05],[1.98,.14,.18],'dark');
 depPart(g,'box',[0,.94,-2.0],[.66,.24,.04],'dark');
 for(let x=-.28;x<.30;x+=.09)depPart(g,'box',[x,.94,-2.03],[.025,.20,.025],'chrome');
 for(const x of [-.48,.48]){
  const man=new THREE.Group();depBuildOfficer(man,'officer');
  man.traverse(m=>{if(m.isMesh&&(m.material===depMaterials.khaki||m.material===depMaterials.trousers))m.material=depMaterials.blue;});
  depBuildRifle(man,1.06,-.30,false);man.scale.setScalar(.82);man.position.set(x,.65,.72);g.add(man);
 }
 depPart(g,'cylinder',[0,1.43,.06],[.045,.65,.045],'chrome');
 const mount=new THREE.Group();mount.position.set(0,0,.06);depBuildRifle(mount,1.84,-.50,true);g.add(mount);
}
function depBuildXray(g){
 // Open inspection tunnel with opaque side walls and roof.
 depPart(g,'box',[0,.88,0],[1.14,.18,3.2],'chrome');
 depPart(g,'box',[0,.99,0],[.91,.05,3.35],'dark');
 for(const x of [-.58,.58])depPart(g,'box',[x,1.45,0],[.20,1.02,1.35],'blue');
 depPart(g,'box',[0,1.98,0],[1.36,.18,1.35],'blue');
 for(const x of [-.43,.43])for(const z of [-1.25,1.25])depPart(g,'box',[x,.43,z],[.09,.86,.09],'chrome');
 for(const z of [-.71,.71])for(let x=-.40;x<.45;x+=.10)depPart(g,'box',[x,1.49,z],[.085,.80,.025],'dark');
 for(let z=-1.5;z<1.55;z+=.15)depPart(g,'box',[0,1.025,z],[.88,.018,.018],'shutterMetal');
 depPart(g,'box',[.91,1.0,.20],[.48,.10,.65],'chrome');
 depPart(g,'box',[.91,1.36,.35],[.48,.35,.06],'dark');
 depPart(g,'box',[.91,1.36,.313],[.40,.27,.012],'blue');
 depPart(g,'box',[.91,1.08,-.03],[.39,.025,.18],'dark');
 depPart(g,'box',[0,1.20,-1.14],[.46,.30,.48],'crateWood');
 depPart(g,'box',[0,1.38,-1.14],[.18,.06,.05],'dark');
 for(const z of [-.75,.75])depPart(g,'box',[.60,1.84,z],[.08,.08,.06],'hhmdLedGreen');
}
