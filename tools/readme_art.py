#!/usr/bin/env python3
"""Generate the README's editable, self-contained visual compositions."""
from __future__ import annotations
import argparse
from html import escape
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    "light": {"paper": "#f3f1e9", "ink": "#213b36", "muted": "#52675f", "line": "#b8c6bb", "surface": "#fcfbf6", "soft": "#dde7df", "accent": "#22665a", "mark": "#b65b3c"},
    "dark": {"paper": "#142c27", "ink": "#f3f0e5", "muted": "#b7cbc0", "line": "#526f63", "surface": "#203e34", "soft": "#375b4c", "accent": "#b4d9be", "mark": "#eda37b"},
}


def render(theme: str, compact: bool = False) -> str:
    p = PALETTES[theme]
    w, h = (600, 510) if compact else (1100, 380)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
             '<title id="title">From meaning to form</title>',
             '<desc id="desc">UI Spec Studio connects meaning, visual form and working proof. An editorial illustration, not a product screenshot.</desc>',
             f'<rect width="{w}" height="{h}" fill="{p["paper"]}"/>']
    def line(x1,y1,x2,y2,color="line",width=1):
        parts.append(f'<path d="M{x1} {y1}H{x2}" stroke="{p[color]}" stroke-width="{width}"/>' if y1==y2 else f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{p[color]}" stroke-width="{width}"/>')
    def text(x,y,s,size=20,color="ink",weight=400,serif=False):
        family="Georgia, 'Times New Roman', serif" if serif else "Arial, Helvetica, sans-serif"
        parts.append(f'<text x="{x}" y="{y}" fill="{p[color]}" font-family="{family}" font-size="{size}" font-weight="{weight}">{escape(s)}</text>')
    def rect(x,y,width,height,color="surface",rx=0,stroke=None):
        border=f' stroke="{p[stroke]}"' if stroke else ''
        parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{rx}" fill="{p[color]}"{border}/>')
    # The grid marks belong to this authored design plate, not to every consuming UI.
    margin=38 if compact else 48
    line(margin,28,w-margin,28)
    if compact:
        text(38,72,'UI SPEC STUDIO',18,'muted',600)
        text(35,142,'From meaning',58,serif=True)
        text(35,203,'to form.',58,serif=True)
        y=260; xs=[38,220,402];pw=160;ph=160
    else:
        text(48,75,'UI SPEC STUDIO',17,'muted',600)
        text(45,153,'From meaning',60,serif=True)
        text(45,218,'to form.',60,serif=True)
        text(48,274,'Design with intent.',20,'muted')
        text(48,304,'Build with evidence.',20,'muted')
        y=112;xs=[500,698,896];pw=158;ph=176
    for i,(x,label) in enumerate(zip(xs,['Meaning','Form','Proof'])):
        rect(x,y,pw,ph,stroke="line")
        text(x+14,y-16,label,28 if compact else 20,'ink',600)
        if i==0:
            text(x+16,y+39,'Why this?',26 if compact else 22,'ink',400,True)
            rect(x+16,y+57,pw-32,4,'accent')
            rect(x+16,y+76,pw-50,3,'line')
            rect(x+16,y+89,pw-39,3,'line')
            rect(x+16,y+102,pw-64,3,'line')
            text(x+16,y+ph-19,'intent',22 if compact else 16,'muted')
        elif i==1:
            rect(x+13,y+16,pw-26,16,'ink')
            rect(x+13,y+43,48,69 if compact else 85,'soft')
            rect(x+71,y+43,pw-85,5,'accent')
            for k,length in enumerate([pw-85,pw-98,pw-91]):
                rect(x+71,y+58+k*13,length,3,'line')
            rect(x+71,y+103,43,9,'accent')
            text(x+13,y+ph-19,'arrange' if compact else 'relationships',22 if compact else 16,'muted')
        else:
            rect(x+14,y+18,pw-28,ph-65,'soft')
            line(x+30,y+51,x+pw-29,y+51,'line')
            line(x+30,y+66,x+pw-43,y+66,'line')
            rect(x+30,y+84,pw-60,18,'accent',2)
            text(x+14,y+ph-19,'verify' if compact else 'working result',22 if compact else 16,'muted')
        if i<2:
            mid=y+ph/2;line(x+pw+5,mid,xs[i+1]-6,mid,'mark',1.5)
            parts.append(f'<path d="M{xs[i+1]-12} {mid-4}l6 4-6 4" fill="none" stroke="{p["mark"]}" stroke-width="1.5"/>')
    bottom=468 if compact else 343
    line(margin,bottom,w-margin,bottom)
    text(margin,bottom+25,'A connected design practice.' if compact else 'UNDERSTAND  /  COMPOSE  /  BUILD  /  INSPECT',22 if compact else 13,'muted',400)
    parts.append('</svg>')
    return '\n'.join(parts)+'\n'


def outputs(root: Path = ROOT) -> dict[Path,str]:
    return {root/'docs/assets'/f'studio-{"compact-" if compact else ""}{theme}.svg': render(theme,compact)
            for compact in (False,True) for theme in PALETTES}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    bad=[]
    for path,body in outputs().items():
        if args.check:
            if not path.is_file() or path.read_text(encoding='utf-8')!=body: bad.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(body,encoding='utf-8',newline='\n')
    if bad:
        print('Regenerate artwork: '+', '.join(bad),file=sys.stderr);return 1
    print('README artwork: '+('verified' if args.check else 'generated'));return 0

if __name__=='__main__':raise SystemExit(main())
