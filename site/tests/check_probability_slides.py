"""Validate the approved standalone probability slide resource and its privacy boundary."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib
R=Path(__file__).resolve().parents[2]
source=R/'Unit 2/resources/probability-simulation-slides.html'
built=R/'docs/Unit 2/resources/probability-simulation-slides.html'
assert source.is_file(),"Approved slide source absent"
raw=source.read_bytes()
expected='88b6f29181315f014b3a91737783cf404fdb36bd2ff138f4e7b238bf149c5a8a'
assert hashlib.sha256(raw).hexdigest()==expected,"Approved slide source differs from exact instructor-reviewed release"
assert built.is_file(),"Quarto did not copy approved slide resource to output"
assert built.read_bytes()==raw,"Standalone resource byte content changed in Quarto output"
s=raw.decode('utf-8')
d=BeautifulSoup(s,'html.parser')
slides=d.select('.slide')
assert len(slides)==42
assert slides[1].get('id')=='familiar-probabilities'
assert slides[2].get('id')=='sample-space-intro'
assert len(d.select('.deck-nav select'))==1
assert len(d.select('script[src]'))==0
assert len(d.select('img[src^="http"]'))==0
assert "connect-src 'none'" in s and "object-src 'none'" in s
assert '0.7599' in s and '52 cards' in s
assert all(v not in s.lower() for v in ('week 9', 'tested positive given that', 'teacher-only midterm', 'ap classroom'))
print("Approved standalone 42-slide source, exact SHA256, public output, sample-space lessons and rights checks passed.")
