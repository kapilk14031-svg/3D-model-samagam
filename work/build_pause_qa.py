from pathlib import Path
import json
s=Path('outputs/samagam-3d.html').read_text(encoding='utf-8')
s=s.replace("const DEP_KEY='samagam-duty-deployment-v1'", "const DEP_KEY='samagam-pause-qa-isolated'")
fixture={'id':'QA-MOVING-CAR','title':'Patrol car · interaction check','type':'patrol','position':[340,1.3,195],'rotation':0,'scale':1,'enabled':True,'speed':.2,'route':[[340,1.3,195],[340,1.3,255]],'routeMode':'pingpong','ground':'','notes':'Isolated UI verification','personnel':[],'shifts':{'day':{'force':None,'incharge':None,'extra':0}}}
script="\nsetTimeout(()=>{depUnits=["+json.dumps(fixture)+"];depDirty=true;depSelected='QA-MOVING-CAR';depMode=null;depRoutebar.hidden=true;depOpen(depSelected);depEl('depLocate').click()},100);\n"
s=s.replace('</script>',script+'</script>')
Path('work/pause-qa.html').write_text(s,encoding='utf-8')
