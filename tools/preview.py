"""Build a portable Pandoc preview; the publishing workflow uses Quarto itself."""
from pathlib import Path
import html, re, shutil, subprocess
ROOT = Path(__file__).resolve().parents[1]
def chapters():
    names=re.findall(r'^\s*-\s*([\w/-]+\.qmd)\s*$',(ROOT/'_quarto.yml').read_text(),re.M)
    result=[]
    for name in names:
        title=re.search(r'^# (.+)$',(ROOT/name).read_text(),re.M).group(1)
        title=re.sub(r'\s*\{[^}]*\}\s*$','',title)
        result.append((str(Path(name).with_suffix('')),title))
    return result
CHAPTERS = chapters()
CSS = '''body{margin:0;font:17px/1.75 system-ui,sans-serif}#sidebar{position:fixed;width:215px;top:0;bottom:0;padding:24px;background:#f2f7f7;overflow:auto;border-right:1px solid #ccdada}#sidebar a{display:block;padding:9px 0;text-decoration:none}#sidebar a[aria-current]{font-weight:750;text-decoration:underline}.book-main{margin-left:265px;max-width:840px;padding:35px 45px 60px}h1{line-height:1.25;font-size:2.3rem}h2{line-height:1.3}.nav-page{display:flex;justify-content:space-between;gap:1rem;margin-top:3rem;border-top:1px solid #ccc;padding-top:1rem}table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border-bottom:1px solid #ccdada;padding:.6rem;text-align:left}pre{background:#f2f6f7;padding:1rem;border-radius:5px;overflow:auto}math[display=block]{margin:1rem 0}.callout-note,.callout-tip{padding:.5rem 1rem;background:#eef6f5;border-left:4px solid #087e83}#mobile-nav{display:none}.preview-note{font-size:.8rem;color:#526571}@media(max-width:950px){#sidebar{display:none}.book-main{margin:0;padding:18px;max-width:100%;box-sizing:border-box}#mobile-nav{display:block;background:#f2f7f7;padding:12px}#mobile-nav a{display:block;padding:5px}.book-main h1{font-size:1.9rem}}@media print{#sidebar,#mobile-nav,.nav-page,.preview-note{display:none}.book-main{margin:0;padding:0;max-width:none}}'''
def main():
    out=ROOT/'docs';out.mkdir(exist_ok=True)
    for name in ['assets','data']: shutil.copytree(ROOT/name,out/name,dirs_exist_ok=True)
    for i,(stem,title) in enumerate(CHAPTERS):
        source=(ROOT/(stem+'.qmd')).read_text()
        source=re.sub(r'(?<=\()([\w-]+)\.qmd',r'\1.html',source)
        body=subprocess.run(['pandoc','-f','markdown+raw_html','-t','html5','--mathml'],input=source,text=True,capture_output=True,check=True).stdout
        nav=''.join(f'<a href="{s}.html"'+(' aria-current="page"' if s==stem else '')+f'>{html.escape(t)}</a>' for s,t in CHAPTERS)
        prev=f'<a href="{CHAPTERS[i-1][0]}.html">← {html.escape(CHAPTERS[i-1][1])}</a>' if i else '<span></span>'
        nxt=f'<a href="{CHAPTERS[i+1][0]}.html">{html.escape(CHAPTERS[i+1][1])} →</a>' if i<len(CHAPTERS)-1 else '<span></span>'
        page=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} · Maple Hill School</title><link rel="stylesheet" href="assets/site.css"><link rel="stylesheet" href="assets/foundations.css"><link rel="stylesheet" href="assets/categorical-tables.css"><style>{CSS}</style></head><body><nav id="sidebar" aria-label="Book chapters"><strong>MAPLE HILL SCHOOL</strong><p>AP Statistics · Learning from Data</p>{nav}</nav><details id="mobile-nav"><summary>Chapters · Maple Hill School</summary>{nav}</details><main class="book-main">{body}<nav class="nav-page" aria-label="Previous and next chapters">{prev}{nxt}</nav><p class="preview-note">Portable Pandoc preview of the Quarto source. The hosted Quarto edition adds full-text search.</p></main><script src="assets/data.js"></script><script src="assets/site.js"></script><script src="assets/foundations.js"></script><script src="assets/categorical-tables.js"></script></body></html>'''
        (out/(stem+'.html')).write_text(page)
    (out/'.nojekyll').touch()
    print(f'Built {len(CHAPTERS)} portable preview pages in docs/.')
if __name__=='__main__': main()
