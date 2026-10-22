else if(mode === 'radio'){
    rightArm.rotation.set(1.88,0,-.16);baseRightArmRotX=1.88;
    const radioHand=new THREE.Group();radioHand.position.set(-.075,-.44,-.18);radioHand.quaternion.copy(rightArm.quaternion).invert();rightArm.add(radioHand);
    const device=new THREE.Group();device.position.set(-.025,.01,-.075);radioHand.add(device);
    depPart(device,'rounded',[0,.055,0],[.10,.19,.060],'hhmdGrip');
    const ant=depPart(device,'cylinder',[-.029,.30,0],[.007,.30,.007],'dark');ant.rotation.z=-.04;
    for(const x of [.005,.030])depPart(device,'cylinder',[x,.163,0],[.010,.028,.010],'dark');
    for(let y=.065;y<=.13;y+=.012)depPart(device,'box',[0,y,-.032],[.073,.004,.004],'hhmdSpeaker');
    depPart(device,'box',[0,.035,-.033],[.055,.028,.004],'glassTint');
    for(const x of [-.02,0,.02])for(const y of [-.012,.006])depPart(device,'box',[x,y,-.033],[.010,.008,.004],'hhmdSpeaker');
    depPart(device,'box',[-.052,.07,0],[.008,.04,.028],'hhmdSpeaker');
    depPart(device,'sphereSmooth',[.03,.14,-.034],[.004,.004,.003],'hhmdLedGreen');
    depPart(radioHand,'rounded',[.040,-.005,-.045],[.025,.070,.035],'skin');
    depPart(radioHand,'rounded',[-.062,-.015,-.040],[.020,.045,.026],'skin');
  }
