function depBuildQRT(g){
 if(!depBuildQRT.bodyMat)depBuildQRT.bodyMat=new THREE.MeshStandardMaterial({color:0x10151b,metalness:.65,roughness:.28});
 const body=depBuildQRT.bodyMat;
 const part=(p,s,m=body,shape='box')=>depPart(g,shape,p,s,m);
 part([0,.48,0],[1.85,.24,4.35],'dark');
 part([0,.91,0],[1.93,.64,4.25]);
 part([0,1.29,-1.50],[1.91,.23,1.30]);
 part([0,1.14,1.88],[1.92,.55,.15]);
 for(const x of [-.94,.94]){
  part([x,1.12,.30],[.08,.58,2.9]);
  part([x,1.70,.30],[.045,.76,2.75],'glassTint');
  for(const z of [-1.02,-.10,1.05,1.73])part([x,1.70,z],[.09,.85,.09]);
  part([x,2.10,.30],[.10,.10,2.94]);
  part([x*1.10,.56,.15],[.22,.12,2.78],'chrome');
  for(const z of [-.55,.67]){part([x*1.025,1.19,z],[.045,.06,.23],'chrome');part([x*1.035,.97,z],[.028,.035,1.03],'chrome');}
  part([x*1.14,1.61,-.98],[.21,.19,.29]);
 }
 const windshield=part([0,1.72,-1.04],[1.76,.77,.035],'glassTint');windshield.rotation.x=-.25;
 for(const x of [-.89,.89]){const pillar=part([x,1.72,-1.04],[.085,.85,.07]);pillar.rotation.x=-.25;}
 part([0,1.70,1.80],[1.78,.69,.035],'glassTint');
 part([0,2.12,-.53],[1.94,.12,1.45]);part([0,2.12,1.56],[1.94,.12,.55]);
 for(const x of [-.76,.76])part([x,2.12,.61],[.40,.12,1.6]);
 for(const x of [-.77,.77])part([x,2.25,.32],[.055,.07,2.70],'dark');
 for(const x of [-1.02,1.02])for(const z of [-1.32,1.36]){
  const w=part([x,.48,z],[.46,.25,.46],'tireRubber','cylinder');w.rotation.z=Math.PI/2;
  const rim=part([x*1.13,.48,z],[.30,.04,.30],'chrome','cylinder');rim.rotation.z=Math.PI/2;
  for(let i=0;i<5;i++){const a=i*Math.PI*2/5;part([x*1.16,.48+.18*Math.sin(a),z+.18*Math.cos(a)],[.018,.09,.10],'dark');}
  part([x*.91,.99,z],[.17,.08,.98]);
 }
 part([0,.57,-2.19],[2.02,.28,.19]);part([0,.83,-2.21],[.88,.32,.035],'dark');
 for(let x=-.36;x<.4;x+=.12)part([x,.85,-2.24],[.045,.24,.025],'chrome');
 for(const x of [-.72,.72]){part([x,1.02,-2.17],[.43,.28,.06],'glassTint');for(const dx of [-.10,.10])part([x+dx,1.02,-2.21],[.075,.075,.035],'white','sphereSmooth');part([x,.62,-2.29],[.12,.12,.035],'white','sphereSmooth');part([x,1.20,2.0],[.17,.43,.04],'red');}
 part([0,.63,-2.30],[.48,.12,.025],'white');
 part([0,2.25,-.72],[1.05,.06,.26],'dark');part([-.28,2.32,-.72],[.48,.12,.24],'vipBeaconRed');part([.28,2.32,-.72],[.48,.12,.24],'vipBeaconBlue');
 // Two personnel: driver within the cabin and roof gunner through the hatch.
 for(const [x,y,z,scale] of [[.46,.25,-.40,.78],[0,1.32,.72,.84]]){
  const man=new THREE.Group();depBuildOfficer(man,'officer');
  man.traverse(m=>{if(m.isMesh&&(m.material===depMaterials.khaki||m.material===depMaterials.trousers))m.material=depMaterials.blue;});
  man.scale.setScalar(scale);man.position.set(x,y,z);g.add(man);
 }
 // Roof-mounted LMG and plain protective side shields, following the reference silhouette.
 part([0,2.28,.36],[.055,.38,.055],'chrome','cylinder');
 const mount=new THREE.Group();depBuildRifle(mount,2.58,.20,true);g.add(mount);
 for(const x of [-.48,.48]){part([x,2.63,.72],[.07,.83,.97],'dark');for(const z of [.30,1.11])part([x,2.63,z],[.08,.73,.025],'shutterMetal');}
 part([0,2.21,.72],[1.13,.09,1.15],'dark');
 if(!depBuildQRT.labelMat){const c=document.createElement('canvas');c.width=512;c.height=256;const ctx=c.getContext('2d');ctx.clearRect(0,0,512,256);ctx.fillStyle='#f04444';ctx.textAlign='center';ctx.font='bold 66px Arial';ctx.fillText('GURUGRAM',256,100);ctx.fillText('POLICE',256,182);const tex=new THREE.CanvasTexture(c);tex.encoding=THREE.sRGBEncoding;depBuildQRT.labelMat=new THREE.MeshStandardMaterial({map:tex,transparent:true,side:THREE.DoubleSide,roughness:.7});}
 for(const side of [-1,1]){const label=part([side*.99,1.08,-.53],[.82,.40,1],depBuildQRT.labelMat,'sign');label.rotation.y=side*Math.PI/2;}
}
