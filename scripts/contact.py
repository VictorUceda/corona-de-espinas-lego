import sys, glob
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS=None
out, fs = sys.argv[1], sys.argv[2:]
W=300; H=220; C=6
R=(len(fs)+C-1)//C
m=Image.new('RGB',(W*C,H*R),'white'); d=ImageDraw.Draw(m)
for k,f in enumerate(fs):
    i=Image.open(f).convert('RGB'); i.thumbnail((W-4,H-18))
    x,y=(k%C)*W,(k//C)*H
    m.paste(i,(x+2,y+16)); d.text((x+2,y+2),f.split('/')[-1][-28:],fill='red')
m.save(out)
