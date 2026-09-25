import pymupdf, sys, os
f=sys.argv[1]; dpi=int(sys.argv[2]); name=os.path.basename(f)[:-4]
d=pymupdf.open(f); os.makedirs(f'pages/{name}',exist_ok=True)
for p in sys.argv[3:]:
    d[int(p)-1].get_pixmap(dpi=dpi).save(f'pages/{name}/p{int(p):03d}.png')
