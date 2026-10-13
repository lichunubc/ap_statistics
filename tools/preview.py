"""Portable Pandoc preview of the same Quarto sources (not a substitute for Quarto QA)."""
from pathlib import Path
from urllib.parse import quote
import html, re, subprocess, posixpath, yaml
ROOT=Path(__file__).resolve().parents[1]
config=yaml.safe_load((ROOT/'_quarto.yml').read_text())
def flatten(items):
    for item in items:
        if isinstance(item,str):yield item
        elif 'chapters' in item:yield from flatten(item['chapters'])
def source(path):
    text=(ROOT/path).read_text()
    return re.sub(r'{{< include ([^>]+?) >}}',lambda m:source(str(Path(path).parent/m[1].strip())),text)
CHAPTERS=[]
for name in flatten(config['book']['chapters']):
    title=re.search(r'^# (.+)$',(ROOT/name).read_text(),re.M)[1]
    title=re.sub(r'\s*\{[^}]*\}\s*$','',title)
    CHAPTERS.append((name,title))
CSS = '''body{margin:0;font:17px/1.75 system-ui,sans-serif}#sidebar{position:fixed;width:215px;top:0;bottom:0;padding:24px;background:#f2f7f7;overflow:auto;border-right:1px solid #ccdada}#sidebar a{display:block;padding:9px 0;text-decoration:none}#sidebar a[aria-current]{font-weight:750;text-decoration:underline}.book-main{margin-left:265px;max-width:840px;padding:35px 45px 60px}h1{line-height:1.25;font-size:2.3rem}h2{line-height:1.3}.nav-page{display:flex;justify-content:space-between;gap:1rem;margin-top:3rem;border-top:1px solid #ccc;padding-top:1rem}table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border-bottom:1px solid #ccdada;padding:.6rem;text-align:left}pre{background:#f2f6f7;padding:1rem;border-radius:5px;overflow:auto}math[display=block]{margin:1rem 0}.callout-note,.callout-tip{padding:.5rem 1rem;background:#eef6f5;border-left:4px solid #087e83}#mobile-nav{display:none}.preview-note{font-size:.8rem;color:#526571}@media(max-width:950px){#sidebar{display:none}.book-main{margin:0;padding:18px;max-width:100%;box-sizing:border-box}#mobile-nav{display:block;background:#f2f7f7;padding:12px}#mobile-nav a{display:block;padding:5px}.book-main h1{font-size:1.9rem}}@media print{#sidebar,#mobile-nav,.nav-page,.preview-note{display:none}.book-main{margin:0;padding:0;max-width:none}}'''
def main():
    subprocess.run(['python','tools/prepare.py'],cwd=ROOT,check=True)
    out=ROOT/'docs';out.mkdir(exist_ok=True)
    for i,(name,title) in enumerate(CHAPTERS):
        parent=str(Path(name).parent)
        def href(target):return quote(posixpath.relpath(target,parent),safe='/')
        text=source(name)
        text=re.sub(r'\.qmd(?=[#>\)"]|$)','.html',text)
        body=subprocess.run(['pandoc','-f','markdown+raw_html','-t','html5','--mathml'],input=text,text=True,capture_output=True,check=True).stdout
        nav=''.join(f'<a href="{href(str(Path(s).with_suffix(".html")))}"'+(' aria-current="page"' if s==name else '')+f'>{html.escape(t)}</a>' for s,t in CHAPTERS)
        nav='<p><strong>Unit 1</strong></p>'+nav
        styles=''.join(f'<link rel="stylesheet" href="{href(p)}">' for p in config['format']['html']['css'])
        footer=(ROOT/config['format']['html']['include-after-body']).read_text()
        footer=re.sub(r'src="/([^"]+)"',lambda m:'src="'+href(m[1])+'"',footer)
        prev=f'<a href="{href(str(Path(CHAPTERS[i-1][0]).with_suffix(".html")))}">← {html.escape(CHAPTERS[i-1][1])}</a>' if i else '<span></span>'
        nxt=f'<a href="{href(str(Path(CHAPTERS[i+1][0]).with_suffix(".html")))}">{html.escape(CHAPTERS[i+1][1])} →</a>' if i<len(CHAPTERS)-1 else '<span></span>'
        page=f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} · Maple Hill School</title>{styles}<style>{CSS}</style></head><body><nav id="sidebar" aria-label="Book chapters"><strong>MAPLE HILL SCHOOL</strong>{nav}</nav><details id="mobile-nav"><summary>Chapters · Maple Hill School</summary>{nav}</details><main class="book-main content">{body}<nav class="nav-page" aria-label="Previous and next chapters">{prev}{nxt}</nav><p class="preview-note">Portable Pandoc preview. The published Quarto book adds full-text search.</p></main>{footer}</body></html>'
        target=out/Path(name).with_suffix('.html');target.parent.mkdir(parents=True,exist_ok=True);target.write_text(page)
    subprocess.run(['python','tools/postrender.py'],cwd=ROOT,check=True)
    print(f'Built {len(CHAPTERS)} portable chapters.')
if __name__=='__main__':main()
