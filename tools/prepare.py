"""Generate the browser copy of canonical shared data before every render."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT/'Unit 1/Shared/data/foundations.json').read_text())
for key in ['school_a','school_b_comparison','study_locations','movie_satisfaction']:
    assert sum(data[key]['counts']) == data[key]['sample_size'], key
assert data['school_a']['counts'] == [8,6,18,8]
assert data['school_a']['commute_total_minutes']/40 == 24
output = ROOT/'Unit 1/Shared/assets/foundations-data.js'
output.write_text('// Generated from ../data/foundations.json by tools/prepare.py. Edit the JSON.\nwindow.UNIT1_FOUNDATIONS = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n')
print('Prepared canonical Unit 1 browser data (all totals verified).')
