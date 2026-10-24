#!/usr/bin/env python3
"""Generate the README's editable, self-contained editorial plates."""
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
    w, h = (600, 470) if compact else (1100, 355)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
             '<title id="title">Build on what works — UI Spec Studio</title>',
             '<desc id="desc">An editorial diagram of three design decisions: inspect mature sources, choose a fitting foundation, and adapt it into an editable published result.</desc>',
             f'<rect width="{w}" height="{h}" fill="{p["paper"]}"/>']

    def line(x1, y1, x2, y2, color="line", width=1):
        parts.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{p[color]}" stroke-width="{width}" fill="none"/>')

    def path(d, color="accent", width=1.5):
        parts.append(f'<path d="{d}" fill="none" stroke="{p[color]}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')

    def text(x, y, s, size=20, color="ink", weight=400, serif=False, extra=""):
        family="Georgia, 'Times New Roman', serif" if serif else "Arial, Helvetica, sans-serif"
        parts.append(f'<text x="{x}" y="{y}" fill="{p[color]}" font-family="{family}" font-size="{size}" font-weight="{weight}" {extra}>{escape(s)}</text>')

    def rect(x, y, width, height, color="surface", rx=0, stroke=None):
        border=f' stroke="{p[stroke]}" stroke-width="1"' if stroke else ''
        parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{rx}" fill="{p[color]}"{border}/>')

    def circle(x,y,r,color="accent"):
        parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{p[color]}"/>')

    margin=38 if compact else 47
    line(margin, 28, w-margin, 28)
    if compact:
        text(38, 63, 'UI SPEC STUDIO   /   DESIGN ENGINEERING', 14, 'muted', 600)
        text(34, 133, 'Build on', 66, serif=True)
        text(34, 201, 'what works.', 66, serif=True)
        text(38, 235, 'Research. Adapt. Verify.', 19, 'muted')
        top=294; xs=(38,216,394); cw=168; ch=124
    else:
        text(47, 73, 'UI SPEC STUDIO   /   DESIGN ENGINEERING', 14, 'muted', 600)
        text(43, 145, 'Build on', 64, serif=True)
        text(43, 211, 'what works.', 64, serif=True)
        text(48, 263, 'Research. Adapt. Verify.', 20, 'muted')
        top=116; xs=(513,705,897); cw=162; ch=173

    headings=('01  STUDY','02  SELECT','03  REALIZE')
    for i,x in enumerate(xs):
        text(x, top-14, headings[i], 13 if not compact else 14, 'muted', 600)
        rect(x, top, cw, ch, 'surface', 2, 'line')
        if i==0:
            # Published references as editorial pages; a real readable unit.
            rect(x+13, top+15, cw-26, 6, 'ink')
            text(x+13, top+48, 'A better start', 15 if compact else 16, 'ink', 400, True)
            for j,length in enumerate((cw-27,cw-45,cw-37)):
                rect(x+13,top+59+11*j,length,3,'line')
            rect(x+13,top+101 if not compact else top+98,cw-26,3,'accent')
            if not compact:
                text(x+13, top+ch-15,'SOURCE / PATTERN',11,'muted')
        elif i==1:
            # Explicit assessment: shared rhythm, selection and suitability.
            text(x+14,top+48,'Aa',42 if not compact else 36,'ink',400,True)
            line(x+65,top+19,x+65,top+91,'line')
            for j,width in enumerate((cw-91,cw-99,cw-85)):
                rect(x+77,top+22+18*j,width,3,'line')
            circle(x+20,top+ch-31,8,'accent')
            path(f'M{x+16} {top+ch-31}l3 3 5 -6','surface',1.7)
            rect(x+36,top+ch-33,cw-52,4,'soft')
            if not compact:
                text(x+13,top+ch-15,'CHOICE / FIT',11,'muted')
        else:
            # A published document rather than a miniature app UI.
            rect(x+14, top+14, cw-28, ch-30, 'soft', 1)
            text(x+27,top+45,'Field notes',18 if not compact else 16,'ink',400,True)
            rect(x+27,top+57,cw-55,3,'accent')
            for j,length in enumerate((cw-55,cw-71,cw-64)):
                rect(x+27,top+72+10*j,length,2,'line')
            rect(x+27,top+ch-43,cw-55,14,'accent',2)
            if not compact:
                text(x+35,top+ch-31,'OPEN / READ',9,'surface',600)
        if i < 2:
            y=top+(ch*0.53)
            line(x+cw+2,y,xs[i+1]-5,y,'mark',1.6)
            path(f'M{xs[i+1]-11} {y-4}l6 4 -6 4','mark',1.6)
    bottom=h-30
    line(margin,bottom,w-margin,bottom)
    text(margin,h-10,'MATURE SOURCES   /   PROFESSIONAL JUDGMENT   /   EDITABLE RESULTS',11 if compact else 12,'muted')
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
