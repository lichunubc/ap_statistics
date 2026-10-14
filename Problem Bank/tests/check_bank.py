"""Test the public/local boundary using synthetic, non-homework browser fixtures."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from urllib.parse import quote
import json, os, threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
DOCS, QA = ROOT / 'docs', ROOT / 'qa'
QA.mkdir(exist_ok=True)
catalog = json.loads((ROOT / 'Problem Bank/catalog.json').read_text())
expected = {'1.2': 4, '1.3': 4, '1.4': 4, '1.5': 3, '1.6': 5}
assert len(catalog['items']) == 20
assert {t: sum(i['topic'] == t for i in catalog['items']) for t in expected} == expected
assert len({item['id'] for item in catalog['items']}) == 20
assert not any('answer' in item or 'blocks' in item or 'options' in item for item in catalog['items'])
live = os.environ.get('BANK_BASE_URL', '').rstrip('/')
if not live:
    assert not list(DOCS.rglob('*.practice.json'))
    assert not list(DOCS.rglob('local-content'))
    assert not list(DOCS.rglob('MHS_AP_Statistics_Week_*'))
fixture = {'schema_version': 1, 'bank_id': catalog['bank_id'], 'catalog_revision': catalog['revision'], 'items': []}
for meta in catalog['items']:
    fixture['items'].append({'id': meta['id'], 'blocks': [{'type': 'paragraph', 'text': 'SYNTHETIC TEST FIXTURE — choose option B.'}], 'options': [{'label': label, 'blocks': [{'type': 'paragraph', 'text': 'Synthetic option ' + label}]} for label in 'ABCD'], 'answer': 'B', 'explanation': 'This is an original software test fixture, not a homework question or answer.', 'editorial_notes': []})
fixture_bytes = json.dumps(fixture).encode()
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = None
if live:
    assert live == 'https://lichunubc.github.io/ap_statistics'
    base = live + '/'
else:
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(DOCS)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/'
errors, checks = [], []
def open_page(page, path):
    response = page.goto(base + quote(path, safe='/'), wait_until='networkidle')
    assert response and response.ok, path
    page.wait_for_selector('.homework-bank[data-bank-ready="true"]', state='attached')
def no_overflow(page):
    assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 2')
def upload(page, data, name='synthetic.practice.json'):
    page.locator('.homework-bank input[type=file]').set_input_files({'name': name, 'mimeType': 'application/json', 'buffer': data})
try:
    with sync_playwright() as p:
        kwargs = {'executable_path': os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'], **kwargs)
        for width in [1440, 768, 390]:
            context = browser.new_context(viewport={'width': width, 'height': 1000}, reduced_motion='reduce')
            page = context.new_page()
            page.on('pageerror', lambda error: errors.append(str(error)))
            open_page(page, 'Problem Bank/practice.html')
            assert page.locator('.bank-question').count() == 20
            assert page.locator('.bank-question input[type=radio]').count() == 0
            assert page.locator('#quarto-sidebar a[href*="Problem%20Bank/practice.html"]').count() == 1
            no_overflow(page)
            requests = []
            page.on('request', lambda request: requests.append((request.method, request.url)))
            upload(page, fixture_bytes)
            page.wait_for_selector('.bank-question[data-loaded=true]')
            assert page.locator('.bank-question[data-loaded=true]').count() == 20
            assert not [r for r in requests if r[0] != 'GET'], requests
            assert not page.locator('.bank-question input:checked').count()
            first = page.locator('.bank-question').first
            first.get_by_role('button', name='Check answer', exact=True).click()
            assert 'Choose an answer' in first.locator('.bank-feedback').inner_text()
            first.locator('input[value=A]').check()
            first.get_by_role('button', name='Check answer', exact=True).click()
            assert first.locator('.bank-feedback').get_attribute('data-result') == 'incorrect'
            first.locator('input[value=B]').focus()
            page.keyboard.press('Space')
            first.get_by_role('button', name='Check answer', exact=True).click()
            assert first.locator('.bank-feedback').get_attribute('data-result') == 'correct'
            first.locator('.bank-solution summary').click()
            assert first.locator('.bank-solution').get_attribute('open') is not None
            first.get_by_role('button', name='Reset question', exact=True).click()
            assert first.locator('input:checked').count() == 0
            assert first.locator('.bank-solution').get_attribute('open') is None
            page.get_by_label('Filter selected questions by topic').select_option('1.4')
            assert page.locator('.bank-question').count() == 4
            page.get_by_label('Find a selected question', exact=True).fill('MHS-W02-Q022')
            assert page.locator('.bank-question').count() == 1
            page.get_by_label('Find a selected question', exact=True).fill('')
            no_overflow(page)
            upload(page, b'%PDF-not-a-json-file', 'homework.pdf')
            page.wait_for_function("document.querySelector('.bank-loader .bank-status').textContent.includes('Could not open')")
            assert page.locator('.bank-question[data-loaded=true]').count() == 4
            bad = json.loads(fixture_bytes); bad['items'][0]['blocks'] = [{'type': 'figure', 'alt': 'Unsafe', 'src': 'https://example.invalid/private-content.png'}]
            upload(page, json.dumps(bad).encode())
            page.wait_for_function("document.querySelector('.bank-loader .bank-status').textContent.includes('embedded PNG')")
            assert not any('example.invalid' in url for _, url in requests)
            assert page.locator('.bank-question[data-loaded=true]').count() == 4
            for topic, count in expected.items():
                open_page(page, f'Unit 1/Topic {topic}/topic-{topic.replace(".", "-")}.html')
                assert page.locator('#homework-practice').count() == 1
                assert page.locator('.bank-question[data-loaded=true]').count() == count
                assert page.locator('.bank-question input:checked').count() == 0
                assert page.locator('#quarto-sidebar .course-unit-toggle').get_attribute('aria-expanded') == 'false'
                no_overflow(page)
            page.locator('.bank-loader').scroll_into_view_if_needed()
            page.screenshot(path=str(QA / f'bank-synthetic-{width}.png'))
            page.get_by_role('button', name='Forget class file', exact=True).click()
            assert page.locator('.bank-question[data-loaded=true]').count() == 0
            page.reload(wait_until='networkidle')
            assert page.locator('.bank-question[data-loaded=true]').count() == 0
            assert page.evaluate("sessionStorage.getItem('mhs-ap-statistics-class-file-v1')") is None
            response = page.goto(base + 'Unit%201/Topic%201.1/topic-1-1.html', wait_until='networkidle')
            assert response.ok
            assert page.locator('#homework-practice').count() == 1
            assert page.locator('.homework-bank').count() == 0
            checks.append({'width': width, 'references': 20, 'local_import': True, 'topic_counts': expected, 'keyboard_feedback_reset': True, 'invalid_files_rejected': True, 'forget_and_reload': True, 'no_overflow': True})
            context.close()
        context = browser.new_context(java_script_enabled=False)
        page = context.new_page()
        page.goto(base + 'Problem%20Bank/practice.html', wait_until='networkidle')
        assert page.locator('.bank-fallback li').count() == 20
        context.close(); browser.close()
finally:
    if server: server.shutdown()
assert not errors, errors
report = {'mode': 'live browser' if live else 'local HTTP browser', 'fixtures': 'synthetic only; no College Board text or answers', 'checks': checks, 'javascript_errors': errors, 'no_javascript_references': True}
(QA / ('live-bank-validation.json' if live else 'bank-validation.json')).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
