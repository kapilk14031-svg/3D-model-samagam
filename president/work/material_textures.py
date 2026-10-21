from PIL import Image,ImageDraw
import numpy as np

def create(out):
    folder=out/'material-textures';folder.mkdir(exist_ok=True);rng=np.random.default_rng(42)
    n=512;yy,xx=np.mgrid[:n,:n];noise=rng.normal(0,2.1,(n,n))
    grain=3*np.sin(xx*.12+np.sin(yy*.1))+noise
    wood=np.stack([183+grain,143+grain*.8,103+grain*.6],axis=-1)
    wood[yy%64<2]-=26
    for row in range(8):
        for col in range(4):
            x=(col*128+(row%2)*48)%512;wood[row*64:(row+1)*64,max(0,x-1):x+1]-=22
    im=Image.fromarray(np.uint8(np.clip(wood,0,255)));im.save(folder/'wood-floor.png')
    weave=np.where(xx%4==0,-5,0)+np.where(yy%4==0,4,0)+noise*.35
    for name,base in [('seat-fabric',[202,196,177]),('acoustic-fabric',[215,215,204])]:
        im=Image.fromarray(np.uint8(np.clip(np.array(base)[None,None,:]+weave[:,:,None],0,255)));im.save(folder/f'{name}.png')
    return {'wood':Image.open(folder/'wood-floor.png'),'seat':Image.open(folder/'seat-fabric.png'),'acoustic':Image.open(folder/'acoustic-fabric.png')}
