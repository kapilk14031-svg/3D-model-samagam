function depBuildArmedOfficer(g){
 depBuildOfficer(g,'officer');
 const baton=[];g.traverse(m=>{if(m.isMesh&&m.material===depMaterials.lathi)baton.push(m);});for(const m of baton)m.parent.remove(m);
 const rifle=new THREE.Group();rifle.position.set(.12,1.02,-.28);rifle.rotation.y=Math.PI/2;rifle.rotation.z=-.30;g.add(rifle);
 depBuildRifle(rifle,0,0,false);
}
