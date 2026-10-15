"""Run every existing course test and Topic 1.7's numerical and browser gates."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
checks=['Unit 1/Shared/tests/check_structure.py',
'Unit 1/Shared/tests/check_site.py',
'Unit 1/Topic 1.1/tests/check_foundations.py',
'Unit 1/Topic 1.2/tests/check_variables.py',
'Unit 1/Topic 1.3/tests/check_categorical.py',
'Unit 1/Topic 1.4/tests/check_charts.py',
'site/tests/check_navigation.py','Problem Bank/tests/check_bank.py',
'Unit 1/Topic 1.7/tests/check_summary17.py',
'Unit 1/Topic 1.7/tests/check_summary17_browser.py',
'Unit 1/Topic 1.8/tests/check_box18.py',
'Unit 1/Topic 1.8/tests/check_box18_browser.py',
'Unit 1/Topic 1.9/tests/check_compare19.py',
'Unit 1/Topic 1.9/tests/check_compare19_browser.py',
'site/tests/check_student_presentation.py']
'Unit 1/Topic 1.10/tests/check_study110.py',
'Unit 1/Topic 1.10/tests/check_study110_browser.py']
failures=[]
for check in checks:
    print('\nCHECK:',check,flush=True)
    result=subprocess.run([sys.executable,str(ROOT/check)],cwd=ROOT)
    if result.returncode:failures.append(check)
if failures:
    print('\nFailed checks:',*failures,sep='\n',file=sys.stderr)
    sys.exit(1)
print('\nAll course and new-topic tests passed.')
