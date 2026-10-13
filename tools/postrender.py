"""Use system fonts; do not distribute external font files in the rendered book."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]/'docs'
root.mkdir(exist_ok=True);(root/'.nojekyll').touch()
for p in root.rglob('*.html'):
    text=p.read_text(encoding='utf-8')
    text=re.sub(r'<link\b[^>]*href=["\'][^"\']*bootstrap-icons[^"\']*["\'][^>]*>','',text)
    p.write_text(text,encoding='utf-8')
for p in root.rglob('*.css'):
    text=p.read_text(encoding='utf-8')
    p.write_text(re.sub(r'@font-face\s*\{[^}]*\}','',text,flags=re.S),encoding='utf-8')
for p in root.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.woff','.woff2','.ttf','.otf','.eot'}: p.unlink()
print('Portable output: system fonts; no bundled font files.')
