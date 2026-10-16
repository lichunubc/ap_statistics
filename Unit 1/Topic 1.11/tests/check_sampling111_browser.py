"""Native HTTP and live-site regression for Topic 1.11, never an inlined preview."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from urllib.parse import quote
from playwright.sync_api import sync_playwright, expect
import threading
import os
import json

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / 'docs'
QA = ROOT / 'qa'
QA.mkdir(exist_ok=True)

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

srv = None
remote = os.environ.get('SAMPLING111_BASE_URL')
if remote:
    base = remote.rstrip('/') + '/'
else:
    srv = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(DOCS)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{srv.server_port}/'
url = base + quote('Unit 1/Topic 1.11/topic-1-11.html', safe='/')
errors, bad = [], []
try:
    with sync_playwright() as p:
        kw = {'executable_path': os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'], **kw)
        for width in [1440, 768, 390]:
            ctx = browser.new_context(viewport={'width': width, 'height': 900}, reduced_motion='reduce')
            page = ctx.new_page()
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('response', lambda r: bad.append((r.status, r.url)) if r.status >= 400 and r.url.startswith(base) else None)
            response = page.goto(url, wait_until='domcontentloaded', timeout=45000)
            assert response and response.ok
            assert page.locator('h1').inner_text().startswith('Topic 1.11 Random Sampling')
            assert page.locator('main math').count() >= 30, 'Mathematics must be rendered by Quarto'
            assert page.locator('main .callout').count() >= 4, 'Derivation panels missing'
            source = page.locator('.sampling111-source img')
            assert source.count() == 2
            for i in range(source.count()):
                source.nth(i).scroll_into_view_if_needed()
                source.nth(i).evaluate('i=>i.decode()')
                assert source.nth(i).evaluate('i=>i.naturalWidth>500')
            anchor = page.locator('.sampling111-source a.exam-enlarge').first
            anchor.focus()
            page.keyboard.press('Enter')
            expect(page.locator('.exam-zoom')).to_be_visible()
            page.keyboard.press('Escape')
            expect(page.locator('.exam-zoom')).to_be_hidden()
            assert anchor.evaluate('(a)=>a===document.activeElement')
            grid = page.locator('[data-sampling111]')
            grid.locator('.sampling111-unit').first.wait_for(timeout=15000)
            assert grid.locator('.sampling111-unit').count() == 36
            assert page.locator('main').get_by_text('unbiased in this example', exact=False).count() >= 1
            assert 'All 36 students' in grid.locator('[data-s111-summary]').inner_text()
            grid.locator('[data-s111-method]').select_option('stratified')
            grid.locator('[data-s111-all]').click()
            text = grid.locator('[data-s111-summary]').inner_text()
            assert '6 distinct students' in text and 'A: 2, B: 2, C: 2' in text, text
            grid.locator('[data-s111-method]').select_option('cluster')
            grid.locator('[data-s111-all]').click()
            assert '6 distinct students' in grid.locator('[data-s111-summary]').inner_text()
            grid.locator('[data-s111-method]').select_option('systematic')
            grid.locator('[data-s111-all]').click()
            line = grid.locator('[data-s111-summary]').inner_text()
            assert any(v in line for v in ['A: 6', 'B: 6', 'C: 6']), line
            grid.locator('[data-s111-method]').select_option('replacement')
            grid.locator('[data-s111-seed]').fill('1')
            grid.locator('[data-s111-all]').click()
            assert '5 distinct students' in grid.locator('[data-s111-summary]').inner_text()
            duplicated = grid.locator('.sampling111-unit[data-id="14"]')
            assert duplicated.locator('.sampling111-multiplicity').inner_text() == '×2 draws'
            assert 'selected 2 time(s)' in duplicated.get_attribute('aria-label')
            grid.locator('[data-s111-seed]').fill('1000000')
            assert 'Choose an integer seed' in grid.locator('[data-s111-status]').inner_text()
            assert 'All 36 students' in grid.locator('[data-s111-summary]').inner_text()
            assert grid.locator('.sampling111-unit[data-picked="true"]').count() == 0
            assert grid.locator('[data-s111-step]').is_disabled()
            assert grid.locator('[data-s111-all]').is_disabled()
            grid.locator('[data-s111-seed]').fill('1')
            assert grid.locator('[data-s111-step]').is_enabled()
            assert grid.locator('[data-s111-all]').is_enabled()
            grid.locator('[data-s111-reset]').click()
            assert grid.locator('[data-s111-method]').input_value() == 'srs'
            grid.locator('[data-s111-step]').focus()
            page.keyboard.press('Enter')
            assert 'Showing 1 of 6' in grid.locator('[data-s111-status]').inner_text()
            assert 'Mean of selections revealed so far:' in grid.locator('[data-s111-summary]').inner_text()
            grid.locator('[data-s111-all]').click()
            assert '6 distinct students' in grid.locator('[data-s111-summary]').inner_text()
            assert 'Sample mean:' in grid.locator('[data-s111-summary]').inner_text()
            host = page.locator('.original-practice')
            host.locator('.original-question-title').wait_for(timeout=15000)
            assert host.locator('.original-question-title').inner_text() == 'Question 1 of 10'
            assert host.locator('input:checked').count() == 0
            host.locator('[data-action=check]').click()
            assert 'Choose an answer' in host.locator('.original-feedback').inner_text()
            host.locator('input[value=B]').check()
            host.locator('[data-action=check]').click()
            assert 'Correct' in host.locator('.original-feedback').inner_text()
            host.locator('[data-action=next]').click()
            assert host.locator('.original-question-title').inner_text() == 'Question 2 of 10'
            assert host.locator('input:checked').count() == 0
            host.locator('[data-action=previous]').click()
            assert host.locator('.original-question-title').inner_text() == 'Question 1 of 10'
            host.locator('[data-action=hint]').click()
            assert host.locator('.original-hint').is_visible()
            host.locator('[data-action=solution]').click()
            assert host.locator('.original-solution').is_visible()
            host.locator('[data-action=reset]').click()
            assert host.locator('input:checked').count() == 0
            for _ in range(4):
                host.locator('[data-action=next]').click()
            assert host.locator('.original-question-title').inner_text() == 'Question 5 of 10'
            assert host.locator('.original-prompt math').count() >= 1
            host.locator('input[type=number]').fill('6')
            host.locator('[data-action=check]').click()
            assert 'Correct' in host.locator('.original-feedback').inner_text()
            host.locator('[data-action=solution]').click()
            assert host.locator('.original-solution math').count() >= 1
            assert 'MHS-U1-' not in host.inner_text()
            page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
            assert host.locator('.original-print-question').count() == 10
            page.evaluate('window.dispatchEvent(new Event("afterprint"))')
            assert host.locator('.original-print-question').count() == 0
            assert host.locator('.original-question-title').inner_text() == 'Question 5 of 10'
            assert host.locator('input[type=number]').input_value() == '6'
            assert host.locator('.original-solution').is_visible()
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'), f'overflow {width}'
            page.screenshot(path=str(QA / f'topic-1-11-{width}.png'), full_page=True)
            grid.screenshot(path=str(QA / f'topic-1-11-lab-{width}.png'))
            ctx.close()
        nojs = browser.new_context(java_script_enabled=False, viewport={'width':390,'height':900})
        pg = nojs.new_page()
        pg.goto(url, wait_until='domcontentloaded')
        assert pg.locator('.original-nojs li').count() == 10
        assert 'Static example to check by hand' in pg.locator('main').inner_text()
        assert not pg.evaluate('document.documentElement.scrollWidth>innerWidth+2')
        nojs.close()
        browser.close()
finally:
    if srv:
        srv.shutdown()
        srv.server_close()
assert not errors, errors
assert not bad, bad
(QA / 'topic-1-11-browser.json').write_text(json.dumps({
    'base_url':base,'mode':'live' if remote else 'local-http',
    'tested_widths':[1440,768,390],'mathml':True,'questions':10,'no_js':True,
    'print_state_restoration':True,'errors':errors,'bad_local_requests':bad
}, indent=2))
print('Topic 1.11 native browser, MathML, practice, accessibility, images and responsive checks passed.')
