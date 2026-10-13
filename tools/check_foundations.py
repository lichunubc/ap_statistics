"""Validate foundations components and source assets without changing the site."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import json, os, threading
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
QA = ROOT / 'qa'
QA.mkdir(exist_ok=True)
data = json.loads((ROOT/'data/foundations.json').read_text())
for key in ['school_a', 'school_b_comparison', 'study_locations', 'movie_satisfaction']:
    assert sum(data[key]['counts']) == data[key]['sample_size'], key
assert data['school_a']['commute_total_minutes']/40 == 24
assert data['school_a']['counts'][2]/40 == .45
manifest = json.loads((ROOT/'project/topic-status.json').read_text())
assert len({t['id'] for t in manifest['topics']}) == len(manifest['topics'])
assert (DOCS/'topic-1-1.html').exists()

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass
server = ThreadingHTTPServer(('127.0.0.1',0), partial(QuietHandler,directory=str(DOCS)))
threading.Thread(target=server.serve_forever, daemon=True).start()
errors=[]
with sync_playwright() as p:
    kwargs={'executable_path':os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'],**kwargs)
    for width in [1440,768,390]:
        page=browser.new_page(viewport={'width':width,'height':1000})
        page.on('pageerror',lambda error:errors.append(str(error)))
        if os.environ.get('INLINE_BROWSER'):
            soup=BeautifulSoup((DOCS/'topic-1-1.html').read_text(),'html.parser')
            for tag in soup.select('script[src]'):
                path=DOCS/tag['src'];tag.attrs.pop('src');tag.string=path.read_text()
            for tag in soup.select('link[rel=stylesheet]'):
                path=DOCS/tag['href'];style=soup.new_tag('style');style.string=path.read_text();tag.replace_with(style)
            page.set_content(str(soup),wait_until='load')
        else:
            page.goto(f'http://127.0.0.1:{server.server_port}/topic-1-1.html',wait_until='networkidle')
        page.wait_for_function('window.FOUNDATION_TEST !== undefined')
        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth+2'),width
        population=page.locator('[data-foundation=population]')
        assert population.locator('circle').count()==1000
        initial=population.locator('.foundation-grid').inner_html()
        population.locator('[data-draw]').click()
        assert population.locator('.foundation-grid').inner_html()!=initial
        population.locator('[data-reset]').click()
        assert population.locator('.foundation-grid').inner_html()==initial
        for n in [10,40,100,1000]:
            population.locator('[data-size]').select_option(str(n))
            assert population.locator('circle.selected').count()==n
            assert population.get_attribute('data-total')=='1000'
            assert population.locator('[data-draw]').is_disabled()==(n==1000)
        population.locator('[data-reset]').click()
        quiz=page.locator('[data-foundation=question-check]')
        for answer in [1,2,0]:
            assert quiz.locator('[aria-pressed=true]').count()==0
            wrong=(answer+1)%4
            quiz.locator(f'[data-option="{wrong}"]').click()
            assert 'Not quite.' in quiz.locator('.status').inner_text()
            quiz.locator('[data-clear]').click()
            assert quiz.locator('[aria-pressed=true]').count()==0
            quiz.locator(f'[data-option="{answer}"]').focus()
            page.keyboard.press('Enter')
            assert 'Correct.' in quiz.locator('.status').inner_text()
            assert quiz.locator('[aria-pressed=true]').count()==1
            quiz.locator('[data-next]').click()
        assert quiz.get_attribute('data-case')=='0'
        assert page.locator('.solution details').count()==6
        assert page.locator('math').count()>5
        old_state=population.locator('.foundation-grid').inner_html()
        page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
        assert page.locator('.foundation-print').count()==2
        assert page.locator('.solution details[open]').count()==6
        page.evaluate('window.dispatchEvent(new Event("afterprint"))')
        assert page.locator('.foundation-print').count()==0
        assert page.locator('.solution details[open]').count()==0
        assert population.locator('.foundation-grid').inner_html()==old_state
        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth+2'),width
        if width in [1440,390]:
            population.screenshot(path=str(QA/f'foundation-selection-{width}.png'))
            quiz.screenshot(path=str(QA/f'foundation-questions-{width}.png'))
            page.screenshot(path=str(QA/f'foundation-chapter-{width}.png'),full_page=True)
        page.close()
    browser.close()
server.shutdown()
assert not errors, errors
report={'chapter':'topic-1-1','widths':[1440,768,390],'population':1000,'sizes_tested':[10,40,100,1000],'quiz_cases':3,'practice_solutions':6,'checks':['dataset totals','fixed population','no replacement','repeat/reset','census control','neutral/wrong/correct/next','keyboard selection','mathml','print and restore','no page overflow'],'javascript_errors':errors}
(QA/'foundations-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))

# New categorical-table chapter reuses the existing foundations test gate.
import subprocess,sys
subprocess.run([sys.executable,str(ROOT/'tools/check_categorical.py')],check=True)
