from pathlib import Path
import math,wave,array,random
root=Path(__file__).resolve().parents[1];rate=22050;duration=60;out=array.array('h');rng=random.Random(79)
chords=[[130.8128,164.8138,195.9977],[110,130.8128,164.8138],[87.307,110,130.8128],[97.9989,123.4708,146.8324]]
noise=0.
for i in range(rate*duration):
    t=i/rate;bar=int(t/7.5)%4;local=t%7.5;notes=chords[bar]
    envelope=min(1,t/3,(duration-t)/4);pad=0.
    for j,f in enumerate(notes):pad+=(math.sin(2*math.pi*f*t)+.22*math.sin(2*math.pi*f*2*t))*.012*(.8+.2*math.sin(t*.27+j))
    beat=int(t/.75);age=t-beat*.75;note=notes[beat%3]*2;bell=(math.sin(2*math.pi*note*age)+.22*math.sin(2*math.pi*note*2*age))*math.exp(-age*4.8)*min(1,age/.02)*.026
    noise=.985*noise+.015*(rng.random()*2-1);sample=(pad+bell+noise*.008)*max(0,envelope)
    out.append(int(max(-1,min(1,sample))*32767))
with wave.open(str(root/'work/ambient-score.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(out.tobytes())
print('Original ambient score generated: 60 seconds')
