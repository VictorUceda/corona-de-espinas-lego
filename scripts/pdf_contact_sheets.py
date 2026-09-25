import pymupdf, sys, os
from PIL import Image, ImageDraw
f=sys.argv[1]; name=os.path.basename(f)[:-4]; os.makedirs(f'sheets/{name}',exist_ok=True)
d=pymupdf.open(f); cols,rows=5,4; per=cols*rows
for s in range(0,d.page_count,per):
    ims=[]
    for i in range(s,min(s+per,d.page_count)):
        pix=d[i].get_pixmap(dpi=36); im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        ImageDraw.Draw(im).text((3,3),str(i+1),fill=(255,0,0)); ims.append(im)
    w,h=ims[0].size; sh=Image.new('RGB',(w*cols,h*rows),'white')
    for k,im in enumerate(ims): sh.paste(im,((k%cols)*w,(k//cols)*h))
    sh.save(f'sheets/{name}/p{s+1:03d}.jpg',quality=80)
