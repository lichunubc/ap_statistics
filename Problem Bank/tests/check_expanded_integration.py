"""Check the Quarto routes, standalone assets, and rendered map interactions."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
import base64
import hashlib
import json
import os
import subprocess
import sys
import threading

from bs4 import BeautifulSoup


REPO = Path(__file__).resolve().parents[2]
BANK = REPO / 'Problem Bank'
DOCS = REPO / 'docs'
PAGE = 'Problem Bank/practice.html'
ASSETS = ('expanded-bank.html', 'dependency-map.html')


def document(path):
    return BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')


def link_paths(soup):
    return {unquote(urlsplit(link['href']).path) for link in soup.select('a[href]')}


def check_artifacts():
    for page in ('index.html', 'resources.html'):
        assert PAGE in link_paths(document(DOCS / page)), page
    links = link_paths(document(DOCS / PAGE))
    for name in ASSETS:
        path = BANK / 'assets' / name
        assert f'assets/{name}' in links
        assert (DOCS / 'Problem Bank/assets' / name).read_bytes() == path.read_bytes(), name
        soup = document(path)
        csp = soup.select_one('meta[http-equiv="Content-Security-Policy"]')['content']
        assert "default-src 'none'" in csp and "connect-src 'none'" in csp
        assert not soup.select('script[src], iframe, link[rel="stylesheet"]')
        for script in soup.find_all('script'):
            if script.get('type') != 'application/json':
                digest = hashlib.sha256(script.string.encode()).digest()
                assert "'sha256-" + base64.b64encode(digest).decode() + "'" in csp
        assert '../practice.html' in link_paths(soup), name

    atlas = document(BANK / 'assets/dependency-map.html')
    graph = json.loads(atlas.select_one('#graph-data').string)
    assert len(graph['nodes']) == 272
    assert sum(e['kind'] == 'prerequisite' for e in graph['edges']) == 482
    parents = {e['from_id'] for e in graph['edges'] if e['kind'] == 'prerequisite'
               and e['to_id'] == 'joint-probability'}
    assert {'two-way-tables', 'probability-from-counts', 'ap-probability-model-meaning'} <= parents, parents
    subprocess.run(['node', str(BANK / 'tests/check_expanded_bank.mjs')], check=True, cwd=REPO)
    print('Quarto entry links, intact standalone assets, script hashes and joint-probability routes passed.')


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def check_browser():
    from playwright.sync_api import sync_playwright

    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(DOCS)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    errors = []
    fixture = {
        'schema_version': '1.2.0',
        'metadata': {},
        'taxonomy': {
            'units': [],
            'knowledge_components': [{'id': 'joint-probability', 'label': 'Joint probability'}],
        },
        'sources': [],
        'questions': [{
            'id': 'synthetic-local-example',
            'title': 'Synthetic local example',
            'Type': 'MCQ',
            'knowledge_component_ids': ['joint-probability'],
            'question_text': 'Software test fixture with two choices.',
            'choices': [{'label': 'A', 'text': 'First'}, {'label': 'B', 'text': 'Second'}],
            'correct_choice': 'B',
        }],
    }
    try:
        with sync_playwright() as playwright:
            kwargs = {'executable_path': os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
            browser = playwright.chromium.launch(**kwargs)
            for width in (1440, 390):
                context = browser.new_context(viewport={'width': width, 'height': 900})
                page = context.new_page()
                page.on('pageerror', lambda error: errors.append(str(error)))
                page.goto(f'{base}/Problem%20Bank/practice.html')
                page.get_by_role('link', name='Open the expanded bank reader').click()
                page.wait_for_url('**/assets/expanded-bank.html')
                requests = []
                page.on('request', lambda request: requests.append(request.url))
                page.locator('#bank-file').set_input_files({
                    'name': 'synthetic.json',
                    'mimeType': 'application/json',
                    'buffer': json.dumps(fixture).encode(),
                })
                page.get_by_role('button', name='Synthetic local example').click()
                page.get_by_role('radio', name='B. Second').check()
                page.get_by_role('button', name='Check answer', exact=True).click()
                assert page.get_by_text('Correct.', exact=True).is_visible()
                assert not requests, requests
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 2')
                page.go_back()
                page.get_by_role('link', name='Explore the skill dependency map').click()
                page.wait_for_url('**/assets/dependency-map.html')
                page.get_by_role('button', name='Explore skills', exact=True).click()
                page.locator('#skill-search').fill('joint probability')
                result = page.locator('#skill-list [data-node="joint-probability"]')
                result.focus()
                page.keyboard.press('Enter')
                assert 'joint-probability' in page.locator('#node-heading').inner_text()
                page.locator('#trace-view').click()
                found = page.evaluate('window.APStatsMap.getVisibleGraph().nodeIds')
                assert {'joint-probability', 'two-way-tables', 'probability-from-counts', 'ap-probability-model-meaning'} <= set(found)
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 2')
                page.get_by_role('link', name='Find practice for this skill').click()
                page.wait_for_url('**/assets/expanded-bank.html?skill=joint-probability')
                page.locator('#bank-file').set_input_files({
                    'name': 'synthetic.json',
                    'mimeType': 'application/json',
                    'buffer': json.dumps(fixture).encode(),
                })
                page.wait_for_function("document.querySelector('#skill').value === 'joint-probability'")
                page.get_by_role('link', name='Return to the Problem Bank').click()
                page.wait_for_url('**/Problem%20Bank/practice.html')
                context.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    assert not errors, errors
    print('Desktop and mobile course navigation, local reader entry and keyboard map trace passed.')


if __name__ == '__main__':
    check_artifacts()
    if '--static-only' not in sys.argv:
        check_browser()
