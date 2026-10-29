from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import json

OUT=Path(__file__).resolve().parent
d=json.loads((OUT/'observations.json').read_text())
def sheet(files,out,cols=3,width=470,crop=None):
    items=[]
    for f,label in files:
        p=OUT/f
        if not p.exists():continue
        im=Image.open(p).convert('RGB')
        if crop:im=im.crop(crop)
        h=round(im.height*width/im.width)
        im=im.resize((width,h))
        frame=Image.new('RGB',(width,h+30),'#e8e8e8');frame.paste(im,(0,30));ImageDraw.Draw(frame).text((8,8),label,fill='black');items.append(frame)
    if not items:return
    cw=width;ch=max(x.height for x in items);rows=(len(items)+cols-1)//cols
    dest=Image.new('RGB',(cols*cw,rows*ch),'#cccccc')
    for i,im in enumerate(items):dest.paste(im,((i%cols)*cw,(i//cols)*ch))
    dest.save(OUT/out)

for n in range(1,4):
    run=f'variant-{n:02d}-desktop'
    s=next((r for r in d['runs'] if r['name']==run),None)
    if s:
        crop=(500,180,1340,810) if n==1 else (560,180,1330,820)
        sheet([(x['image'],f"{n:02d} {x['label']} actual={x.get('actual_elapsed_ms','?')}ms") for x in s['states'] if x['label'].startswith(('04-save-','06-reverse-'))],f'variant-{n:02d}-motion-sheet.jpg',cols=4,width=350,crop=crop)
    for mode in ('mobile','reduced'):
        run=f'variant-{n:02d}-{mode}'
        s=next((r for r in d['runs'] if r['name']==run),None)
        if s:sheet([(x['image'],f'{n:02d} {mode} {x["label"]}') for x in s['states'] if x['label'] in ['00-empty','01-long-editor-top','03-save-1800ms','04-long-saved-bottom','05-reverse-0850ms','06-collection-top','07-collection-third','08-return-third-orientation','09-dark-chinese-editor','10-dark-saved']],f'variant-{n:02d}-{mode}-sheet.jpg',cols=5,width=300)

for label in ('00-empty','01-long-editor','03-dark-chinese-editor','09-three-card-collection','10-save-failure','12-retry-success'):
    sheet([(f'variant-{n:02d}-desktop/{label}.png',f'Variant {n:02d} {label}') for n in range(1,4)],f'comparison-{label}.jpg',cols=3,width=480)
sheet([(f'variant-{n:02d}-{stage}/{label}.png',f'Variant {n:02d} {stage}') for n in range(1,4) for stage,label in [('initial','01-initial-saved'),('desktop','04-save-1900ms')]],'initial-final-saved.jpg',cols=2,width=720)

if (OUT/'followup-observations.json').exists():
    follow=json.loads((OUT/'followup-observations.json').read_text())
    for n in range(1,4):
        r=next((r for r in follow['runs'] if r['name']==f'variant-{n:02d}-followup'),None)
        if r:
            sheet([(x['image'],f"{n:02d} {x['label']} actual={x.get('actual_elapsed_ms','?')}ms") for x in r['states'] if x['label'].startswith(('03-open','04-return','05-rapid'))],f'variant-{n:02d}-route-sheet.jpg',cols=5,width=390)
    for width in (390,1440):
        sheet([(f'variant-{n:02d}-reduced-repro-{width}/{label}.png',f'{n:02d} reduced {width} {label}') for n in range(1,4) for label in ['01-editor-stable','03-saved-stable','05-collection-return']],f'reduced-repro-{width}.jpg',cols=3,width=390 if width==390 else 480)
