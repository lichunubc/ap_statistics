"""Run all course checks and save a compact result index plus per-check logs."""
from pathlib import Path
import ast
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CHECKS = [
    'Unit 1/Shared/tests/check_structure.py',
    'Unit 1/Shared/tests/check_site.py',
    'Unit 1/Topic 1.1/tests/check_foundations.py',
    'Unit 1/Topic 1.2/tests/check_variables.py',
    'Unit 1/Topic 1.3/tests/check_categorical.py',
    'Unit 1/Topic 1.4/tests/check_charts.py',
    'site/tests/check_navigation.py',
    'Problem Bank/tests/check_bank.py',
    'Unit 1/Topic 1.7/tests/check_summary17.py',
    'Unit 1/Topic 1.7/tests/check_summary17_browser.py',
    'Unit 1/Topic 1.8/tests/check_box18.py',
    'Unit 1/Topic 1.8/tests/check_box18_browser.py',
    'Unit 1/Topic 1.9/tests/check_compare19.py',
    'Unit 1/Topic 1.9/tests/check_compare19_browser.py',
    'site/tests/check_student_presentation.py',
    'Unit 1/Topic 1.10/tests/check_study110.py',
    'Unit 1/Topic 1.10/tests/check_study110_browser.py',
    'Unit 1/Topic 1.11/tests/check_sampling111.py',
    'Unit 1/Topic 1.11/tests/check_sampling111_browser.py',
]


def main() -> int:
    qa = ROOT / 'qa'
    logs = qa / 'test-logs'
    logs.mkdir(parents=True, exist_ok=True)
    if len(CHECKS) != len(set(CHECKS)):
        print('Duplicate entries in the course test list.', file=sys.stderr)
        return 1
    results = []
    for index, check in enumerate(CHECKS, start=1):
        print(f'\nCHECK {index}/{len(CHECKS)}: {check}', flush=True)
        path = ROOT / check
        try:
            ast.parse(path.read_text(encoding='utf-8'), filename=check)
            result = subprocess.run(
                [sys.executable, str(path)], cwd=ROOT,
                capture_output=True, text=True, encoding='utf-8', errors='replace',
            )
            code = result.returncode
            output = result.stdout + result.stderr
        except (OSError, SyntaxError) as exc:
            code = 1
            output = f'{type(exc).__name__}: {exc}\n'
        log = logs / f'{index:02d}-{path.stem}.log'
        log.write_text(output, encoding='utf-8')
        print(output, end='' if output.endswith('\n') else '\n', flush=True)
        results.append({
            'check': check, 'returncode': code, 'passed': code == 0,
            'log': log.relative_to(ROOT).as_posix(),
        })
        report = {
            'source_revision': os.environ.get('GITHUB_SHA'),
            'expected_checks': len(CHECKS), 'completed_checks': len(results),
            'checks': results,
            'failed': [item['check'] for item in results if not item['passed']],
            'passed': len(results) == len(CHECKS) and all(item['passed'] for item in results),
        }
        (qa / 'test-results.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    failed = [item['check'] for item in results if not item['passed']]
    if failed:
        print('\nFailed checks:', *failed, sep='\n', file=sys.stderr)
        return 1
    print('\nAll course and new-topic tests passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
