from PIL import Image,ImageOps,ImageDraw
from pathlib import Path
D=Path(__file__).parent
for sub,names,out,cols in [('references',[f'{k}-{i}.png' for k in ['center','slide'] for i in range(5)],'reference-sequences.jpg',5),('run2',[f'save-{i:02}.png' for i in range(1,7)],'save-sequence.jpg',3)]:
 imgs=[]
 for n in names:
  p=D/sub/n
  if not p.exists():continue
  im=Image.open(p).convert('RGB');im.thumbnail((480,340));tile=Image.new('RGB',(480,366),'#e6e6e3');tile.paste(im,((480-im.width)//2,24));ImageDraw.Draw(tile).text((10,7),n,fill='black');imgs.append(tile)
 sheet=Image.new('RGB',(480*cols,366*((len(imgs)+cols-1)//cols)),'white')
 for i,im in enumerate(imgs):sheet.paste(im,(i%cols*480,i//cols*366))
 sheet.save(D/out)
