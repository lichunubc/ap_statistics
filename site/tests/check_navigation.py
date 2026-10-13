"""Five-unit landing flow and explicit sidebar disclosure, locally and after deploy.

NAVIGATION_BASE_URL enables the same real-browser checks against the public site.
INLINE_BROWSER=1 is only an offline layout/interaction fallback, never live proof.
"""
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import json, os, sys, threading
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from browser_support import load_page
DOCS, QA = ROOT / 'docs', ROOT / 'qa'
QA.mkdir(exist_ok=True)
units = json.loads((ROOT / 'project/unit-status.json').read_text())['units']
topics = json.loads((ROOT / 'project/topic-status.json').read_text())['topics']
expected_titles = [f"Unit {u['id']}: {u['title']}" for u in units]
assert [u['id'] for u in units] == [1, 2, 3, 4, 5]
assert units[0]['available_topics'] == [t['id'] for t in topics]
assert all(u['status'] == 'under_construction' and not u['available_topics'] for u in units[1:])
live_base = os.environ.get('NAVIGATION_BASE_URL', '').rstrip('/')
if live_base:
    assert live_base == 'https://lichunubc.github.io/ap_statistics', live_base
    assert not os.environ.get('INLINE_BROWSER'), 'Live checks cannot use offline inlining.'
else:
    home = BeautifulSoup((DOCS / 'index.html').read_text(), 'html.parser')
    cards = home.select('main .unit-card')
    assert len(cards) == 5
    assert [c.h3.get_text(' ', strip=True) for c in cards] == expected_titles
    assert len(home.select('main [data-unit-status="under-construction"]')) == 4
    assert not home.select('main .topic-grid, main [data-chart]')
    for unit, card in zip(units, cards):
        target = str(Path(unit['landing']).with_suffix('.html'))
        assert unquote(urlsplit(card.select_one('h3 a[href*="unit-"]')['href']).path) == target
        soup = BeautifulSoup((DOCS / target).read_text(), 'html.parser')
        assert soup.h1.get_text(' ', strip=True) == f"Unit {unit['id']}: {unit['title']}"
        if unit['id'] == 1:
            assert len(soup.select('main .topic-grid .route-card')) == 6
            assert soup.select_one('main [data-chart="commute-dot"]')
        else:
            assert 'Under construction' in soup.select_one('main .construction-note').get_text()
            assert not soup.select('main .route-card, main [data-widget]')
        assert (ROOT / Path(unit['landing']).parent / 'README.md').is_file()

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass
server = None
if live_base:
    base = live_base + '/'
else:
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(DOCS)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/'
errors, failures, checks = [], [], []
inline = bool(os.environ.get('INLINE_BROWSER'))

def open_page(page, path):
    url = base + quote(path, safe='/')
    if live_base:
        page.goto(url, wait_until='networkidle')
    else:
        load_page(page, DOCS / path, url)
    page.wait_for_selector('#quarto-sidebar[data-course-navigation-ready="true"]', state='attached')

def closed(page):
    buttons = page.locator('#quarto-sidebar .course-unit-toggle')
    assert buttons.count() == 1, 'Only Unit 1 currently has published topics.'
    assert buttons.first.get_attribute('aria-expanded') == 'false'
    assert page.locator('#quarto-sidebar .course-topic-list[hidden]').count() == 1

def open_mobile_menu(page):
    toggle = page.locator('button[aria-label="Toggle sidebar navigation"]')
    if toggle.is_visible() and not page.locator('#quarto-sidebar').is_visible():
        toggle.click()
        page.wait_for_timeout(400)

def no_overflow(page, label):
    assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 2'), label

try:
    with sync_playwright() as p:
        kwargs = {'executable_path': os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'], **kwargs)
        for width in [1440, 768, 390]:
            context = browser.new_context(viewport={'width': width, 'height': 1000}, reduced_motion='reduce')
            page = context.new_page()
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('response', lambda response: failures.append(response.url) if response.status >= 400 and response.url.startswith(base) else None)
            open_page(page, 'index.html')
            assert page.locator('main .unit-card').count() == 5
            closed(page)
            no_overflow(page, f'Home at {width}')
            page.screenshot(path=str(QA / f'course-home-{width}.png'), full_page=True)
            for i, unit in enumerate(units, 1):
                if not inline:
                    open_page(page, 'index.html')
                    card = page.locator(f'main .unit-card[data-unit="{i}"]')
                    if i == 1:
                        card.locator('h3 a[href*="unit-"]').focus()
                        page.keyboard.press('Enter')
                    else:
                        # Check the entire box is clickable, not just the title text.
                        card.click(position={'x': 12, 'y': 12})
                    page.wait_for_url(f'**/unit-{i}.html', wait_until='networkidle')
                else:
                    open_page(page, str(Path(unit['landing']).with_suffix('.html')))
                assert page.locator('h1').inner_text() == expected_titles[i - 1]
                closed(page)
                no_overflow(page, f'Unit {i} at {width}')
                if i != 1:
                    assert 'Under construction' in page.locator('main .construction-note').inner_text()
                    assert page.locator('main .route-card').count() == 0
                else:
                    assert page.locator('main .topic-grid .route-card').count() == 6
                    page.screenshot(path=str(QA / f'unit1-topics-{width}.png'), full_page=True)
            open_page(page, 'Unit 1/unit-1.html')
            open_mobile_menu(page)
            button = page.locator('#quarto-sidebar .course-unit-toggle')
            first = page.locator('#quarto-sidebar a[href*="topic-1-1.html"]')
            bounds = button.bounding_box()
            assert bounds and bounds['x'] >= 0 and bounds['x'] + bounds['width'] <= width + 1, ('Unit toggle outside viewport', bounds)
            button.focus()
            page.keyboard.press('Enter')
            assert button.get_attribute('aria-expanded') == 'true' and first.is_visible()
            assert button.get_attribute('aria-label') == 'Hide topics for Unit 1'
            page.keyboard.press('Space')
            assert button.get_attribute('aria-expanded') == 'false' and not first.is_visible()
            button.click()
            assert first.is_visible()
            page.screenshot(path=str(QA / f'course-sidebar-expanded-{width}.png'))
            if not inline:
                page.locator('#quarto-sidebar a[href*="topic-1-2.html"]').click()
                page.wait_for_load_state('networkidle')
                assert page.locator('h1').inner_text() == 'Topic 1.2 Variables'
                closed(page)
                open_mobile_menu(page)
                page.locator('#quarto-sidebar .course-unit-toggle').click()
                assert page.locator('#quarto-sidebar a[href*="topic-1-6.html"]').is_visible()
                page.reload(wait_until='networkidle')
                closed(page)
                # Sidebar unit title opens the landing page; it is not a dead toggle.
                open_mobile_menu(page)
                page.locator('#quarto-sidebar a[href*="unit-1.html"]').click()
                page.wait_for_load_state('networkidle')
                assert page.locator('h1').inner_text() == expected_titles[0]
                page.locator('main .topic-grid .route-card a').nth(5).click()
                page.wait_for_load_state('networkidle')
                assert page.locator('h1').inner_text().startswith('Topic 1.6 ')
                closed(page)
            checks.append({'width': width, 'unit_cards': 5, 'unit_pages': 5, 'topic_cards': 6, 'keyboard_and_mouse_disclosure': True, 'collapsed_on_lesson_and_reload': not inline})
            context.close()
        if not inline:
            context = browser.new_context(java_script_enabled=False, viewport={'width': 1440, 'height': 1000})
            page = context.new_page()
            page.goto(base, wait_until='networkidle')
            page.locator('main .unit-card[data-unit="1"] h3 a[href*="unit-"]').click()
            page.wait_for_load_state('networkidle')
            assert page.locator('main .topic-grid .route-card').count() == 6
            page.locator('main .topic-grid .route-card a').nth(1).click()
            page.wait_for_load_state('networkidle')
            assert page.locator('h1').inner_text() == 'Topic 1.2 Variables'
            assert page.locator('main details').count() >= 10
            context.close()
        browser.close()
finally:
    if server:
        server.shutdown()
assert not errors, errors
assert not failures, failures
report = {'mode': 'live browser' if live_base else 'offline inlining' if inline else 'local HTTP browser', 'base': base, 'checks': checks, 'no_javascript_navigation': not inline, 'javascript_errors': errors, 'failed_local_requests': failures}
(QA / ('live-navigation-validation.json' if live_base else 'navigation-validation.json')).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
