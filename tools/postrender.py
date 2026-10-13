"""Preserve legacy public URLs and use system fonts, without duplicate QMD sources."""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, quote, unquote
import json, posixpath, re, shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'
OUT.mkdir(exist_ok=True);(OUT/'.nojekyll').touch()
# Explicitly copy teaching assets and provenance. No code/tests are published as pages.
for p in (ROOT/'Unit 1').rglob('*'):
    if p.is_file() and ({'assets','data'} & set(p.relative_to(ROOT/'Unit 1').parts[:-1])):
        dst=OUT/p.relative_to(ROOT);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
attr=re.compile(r'\b(href|src)=("|\')(.*?)(\2)',re.I)
def rebase_html(text,source_dir,dest_dir):
    def replace(m):
        key,mark,value,_=m.groups();u=urlsplit(value)
        if u.scheme or u.netloc or not u.path:return m.group(0)
        path=unquote(u.path)
        if path.startswith('/ap_statistics/'):resolved=path[len('/ap_statistics/'):]
        elif path.startswith('/'):resolved=path.lstrip('/')
        else:resolved=posixpath.normpath(posixpath.join(source_dir,path))
        rel=posixpath.relpath(resolved,dest_dir or '.')
        result=urlunsplit(('', '', quote(rel,safe='/.-_~'),u.query,u.fragment))
        return key+'='+mark+result+mark
    return attr.sub(replace,text)
# Normalize project-root resources and relative URLs before copying any aliases.
for p in OUT.rglob('*.html'):
    text=p.read_text(encoding='utf-8')
    text=re.sub(r'<link\b[^>]*href=["\'][^"\']*bootstrap-icons[^"\']*["\'][^>]*>','',text)
    parent=p.parent.relative_to(OUT).as_posix()
    p.write_text(rebase_html(text,parent,parent),encoding='utf-8')
legacy=json.loads((ROOT/'Unit 1/legacy-pages.json').read_text())
for name,entry in legacy.items():
    source=OUT/entry['target'];assert source.is_file(),source
    text=rebase_html(source.read_text(),source.parent.relative_to(OUT).as_posix(),'.')
    text=re.sub(r'(<meta\s+name="quarto:offset"\s+content=")[^"]*',r'\g<1>./',text)
    text=re.sub(r'<link\s+rel="canonical"[^>]*>','',text)
    canonical='https://lichunubc.github.io/ap_statistics/'+quote(entry['target'],safe='/')
    text=text.replace('</head>',f'<link rel="canonical" href="{canonical}">\n</head>')
    # Old lesson URLs open their own section; explicit old bookmarked fragments win.
    if entry['section']:
        fragment=json.dumps(entry['section'])
        text=text.replace('</body>',f'<script>if(!location.hash){{location.replace(location.href.split("#")[0]+"#"+{fragment});}}</script>\n</body>')
    (OUT/name).write_text(text)
for old,new in json.loads((ROOT/'Unit 1/legacy-assets.json').read_text()).items():
    src=OUT/new;assert src.is_file(),src
    dst=OUT/old;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
for p in OUT.rglob('*.css'):
    text=p.read_text(encoding='utf-8')
    p.write_text(re.sub(r'@font-face\s*\{[^}]*\}','',text,flags=re.S),encoding='utf-8')
for p in OUT.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.woff','.woff2','.ttf','.otf','.eot'}:p.unlink()
print(f'Preserved {len(legacy)} chapter URLs, shared asset URLs and system-font-only output.')
# A build is distinguishable from a previously cached deployment.
import os,subprocess
commit=os.environ.get('GITHUB_SHA')
if not commit:
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
(OUT/'release.json').write_text(json.dumps({'source_commit':commit,'unit1_topics':['1.1','1.2','1.3','1.4','1.5','1.6']},indent=2)+'\n')
