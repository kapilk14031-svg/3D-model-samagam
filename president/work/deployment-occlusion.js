// Visibility against the same opaque venue solids rendered by this viewer.
const depOccluders=[],depOccBox=new THREE.Box3(new THREE.Vector3(-.5,-.5,-.5),new THREE.Vector3(.5,.5,.5));
const depOccTransform=new THREE.Object3D();
for(const o of data.objects){if(o.mat==='glass'||o.mat==='lotusGlass'||!['shell','roof','ceiling','context','campus'].includes(o.group))continue;
 const solidName=/wall|roof|ceiling|slab|column|pier|beam|parapet|spandrel|building|enclosure|boundary|dome|drum/i.test(o.name);
 if(!solidName||!geos[o.shape])continue;
 depOccTransform.position.fromArray(o.p);depOccTransform.scale.fromArray(o.s);depOccTransform.rotation.set(o.tilt||0,o.rot,o.rz||0);depOccTransform.updateMatrix();const matrix=depOccTransform.matrix.clone(),inverse=matrix.clone().invert();
 const bounds=(o.shape==='box'?depOccBox:((geos[o.shape].boundingBox||geos[o.shape].computeBoundingBox()),geos[o.shape].boundingBox)).clone().applyMatrix4(matrix);
 const mesh=o.shape==='box'?null:new THREE.Mesh(geos[o.shape],new THREE.MeshBasicMaterial({side:THREE.DoubleSide}));if(mesh){mesh.matrixAutoUpdate=false;mesh.matrix.copy(matrix);mesh.matrixWorld.copy(matrix);}
 depOccluders.push({group:o.group,matrix,inverse,bounds,mesh});
}
const depOccRay=new THREE.Ray(),depOccLocal=new THREE.Ray(),depOccPoint=new THREE.Vector3(),depOccHit=new THREE.Vector3(),depOccCaster=new THREE.Raycaster();
let depOccStamp=0,depOccCache=new Map(),depOccCamera=new THREE.Matrix4(),depOccSignature='',depOccTimer=null;
function depOccluded(item){const target=new THREE.Vector3(item.x,item.y+(item.kind==='officer'?1.62:item.kind==='dfmd'?1.8:1),item.z),distance=camera.position.distanceTo(target);if(distance<.2)return false;
 depOccRay.set(camera.position,target.clone().sub(camera.position).normalize());depOccCaster.ray.copy(depOccRay);depOccCaster.near=.08;depOccCaster.far=distance-.15;
 for(const o of depOccluders){if(!groups[o.group]?.visible||!depOccRay.intersectBox(o.bounds,depOccHit)||depOccHit.distanceTo(camera.position)>distance-.15)continue;
  if(o.mesh){if(depOccCaster.intersectObject(o.mesh,false).length)return true;continue;}
  depOccLocal.copy(depOccRay).applyMatrix4(o.inverse);const hit=depOccLocal.intersectBox(depOccBox,depOccPoint);if(!hit)continue;const world=hit.clone().applyMatrix4(o.matrix);if(world.distanceTo(camera.position)>.08&&world.distanceTo(camera.position)<distance-.15)return true;
 }return false;
}
function depRefreshOcclusion(){const stamp=performance.now(),signature=current+'|'+depItems.map(o=>[o.id,o.x,o.y,o.z].join(',')).join(';')+'|'+Object.entries(groups).map(([k,g])=>k+g.visible).join(',');
 if(signature===depOccSignature&&camera.matrixWorld.equals(depOccCamera))return;
 if(signature===depOccSignature&&stamp-depOccStamp<100){if(!depOccTimer)depOccTimer=setTimeout(()=>{depOccTimer=null;depOccStamp=0;depUpdate();draw();},105);return;}
 depOccSignature=signature;depOccCamera.copy(camera.matrixWorld);depOccStamp=stamp;depOccCache=new Map(depItems.map(o=>[o.id,depOccluded(o)]));
}
