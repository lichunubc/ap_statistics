"""Validate the public catalogue and build metadata-only browser assets."""
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
assert set(catalog) == {'schema_version', 'bank_id', 'revision', 'topics', 'sources', 'items', 'coverage_notes'}
assert catalog['schema_version'] == 1 and catalog['bank_id'] == 'mhs-ap-statistics-homework'
allowed = {'id', 'topic', 'title', 'source_week', 'source_question', 'source_pages', 'skills', 'difficulty', 'delivery', 'secondary_topics'}
ids = set()
source_pages = {s['week']: s['pages'] for s in catalog['sources']}
for item in catalog['items']:
    assert set(item) == allowed, 'Only reference metadata may enter the public catalogue.'
    assert item['id'] not in ids
    ids.add(item['id'])
    assert item['id'] == f"MHS-W{item['source_week']:02}-Q{item['source_question']:03}"
    assert item['topic'] in catalog['topics'] and item['delivery'] == 'local-class-file'
    assert item['source_pages'] and all(1 <= p <= source_pages[item['source_week']] for p in item['source_pages'])
    assert all(t in catalog['topics'] for t in item['secondary_topics'])
if (REPO / '.git').exists():
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=REPO).decode().split('\0')
    forbidden = [p for p in tracked if '/local-content/' in '/' + p or p.endswith('.practice.json') or 'MHS_AP_Statistics_Week_' in p]
    assert not forbidden, f'Private classroom content must not be tracked: {forbidden}'
output = ROOT / 'assets' / 'catalog.js'
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text('/* Generated public metadata only; no source question content. */\nwindow.MHSProblemCatalog = ' + json.dumps(catalog, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
print(f'Prepared {len(ids)} public question references; full questions remain local-only.')
