"""Run every topic regression and the course-navigation gate; collect all failures."""
from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
checks=['Unit 1/Shared/tests/check_structure.py','Unit 1/Shared/tests/check_site.py','Unit 1/Topic 1.1/tests/check_foundations.py','Unit 1/Topic 1.2/tests/check_variables.py','Unit 1/Topic 1.3/tests/check_categorical.py','Unit 1/Topic 1.4/tests/check_charts.py','site/tests/check_navigation.py']
failures=[]
for check in checks:
    print('\nCHECK:',check,flush=True)
    result=subprocess.run([sys.executable,str(ROOT/check)],cwd=ROOT)
    if result.returncode:
        failures.append(check)
if failures:
    print('\nFailed checks:',*failures,sep='\n',file=sys.stderr)
    sys.exit(1)
print('\nAll topic and course-navigation checks passed.')
