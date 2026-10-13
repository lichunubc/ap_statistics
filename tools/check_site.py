"""Validate data, local links, and browser interactions. Test rendered docs/ first."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from urllib.parse import urlsplit, unquote
import os, threading, json, re
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs';QA=ROOT/'qa';QA.mkdir(exist_ok=True)
pages=sorted(DOCS.glob('*.html'));assert len(pages)==8, len(pages)
for path in pages:
    soup=BeautifulSoup(path.read_text(),'html.parser')
    for el in soup.select('a[href],script[src],link[href]'):
        href=el.get('href',el.get('src',''));url=urlsplit(href)
        if url.scheme or url.netloc or not url.path or url.path.startswith('/'): continue
        target=path.parent/unquote(url.path)
        assert target.exists(),f'{path.name}: missing {href}'
        if url.fragment and target.suffix=='.html':
            ids=BeautifulSoup(target.read_text(),'html.parser').find(id=unquote(url.fragment))
            assert ids is not None,f'{path.name}: missing anchor {href}'
assert not any(p.suffix in {'.woff','.woff2','.ttf','.otf','.eot'} for p in DOCS.rglob('*'))
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(DOCS)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/'
errors=[];checks=[]
with sync_playwright() as p:
    executable=os.environ.get('CHROMIUM_PATH')
    kwargs={'executable_path':executable} if executable else {}
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'],**kwargs)
    page=browser.new_page(viewport={'width':1440,'height':1000})
    page.on('pageerror',lambda e:errors.append(str(e)))
    current_width=1440
    def goto(name):
        global page
        page.close();page=browser.new_page(viewport={'width':current_width,'height':1000})
        page.on('pageerror',lambda e:errors.append(str(e)))
        if os.environ.get('INLINE_BROWSER'):
            soup=BeautifulSoup((DOCS/(name+'.html')).read_text(),'html.parser')
            for tag in soup.select('script[src]'):
                path=DOCS/tag['src'];tag.attrs.pop('src');tag.string=path.read_text()
            for tag in soup.select('link[rel=stylesheet]'):
                path=DOCS/tag['href'];style=soup.new_tag('style');style.string=path.read_text();tag.replace_with(style)
            page.set_content(str(soup),wait_until='load')
        else:
            page.goto(base+name+'.html',wait_until='networkidle')
        page.wait_for_function('window.STATS_TEST !== undefined')
    for path in pages:
        goto(path.stem)
        assert page.locator('h1').count()>=1
        checks.append(path.stem)
        if path.stem=='index': page.screenshot(path=str(QA/'home-desktop.png'),full_page=True)
        if path.stem=='histograms':
            w=page.locator('[data-widget="hist-build"]')
            assert w.get_attribute('data-step')=='0'
            for i in range(1,7):
                w.locator('[data-action=next]').click()
                assert w.get_attribute('data-step')==str(i)
                assert w.locator('rect[data-bin]').count()==i
            w.locator('[data-action=reset]').click();w.locator('[data-action=play]').click()
            page.wait_for_timeout(1350);assert int(w.get_attribute('data-step'))>=1
            w.locator('[data-action=play]').click();w.locator('[data-action=full]').click()
            w.screenshot(path=str(QA/'histogram-construction.png'))
            scale=page.locator('[data-widget=scale]');scale.locator('select').select_option('percent');assert '33.3%' in scale.inner_text()
        if path.stem=='individual-values':
            w=page.locator('[data-widget=values]');w.locator('[data-action=full]').click();assert w.locator('circle').count()==24
            w.locator('select').select_option('stem');assert '0 2 2 4 5 6 8 8' in w.inner_text()
        if path.stem=='histogram-lab':
            w=page.locator('[data-widget=bin-lab]')
            for width in [3,4,5,6,10,12,15,20,30]:
                w.locator('[data-width]').select_option(str(width));assert int(w.get_attribute('data-bins'))==60//width;assert w.get_attribute('data-total')=='24'
            w.locator('[data-mode]').select_option('count')
            for k in range(2,21):
                w.locator('[data-count]').evaluate('(el,k)=>{el.value=k;el.dispatchEvent(new Event("input",{bubbles:true}));}',k)
                assert w.get_attribute('data-bins')==str(k);assert w.get_attribute('data-total')=='24'
            w.locator('[data-count]').evaluate('(el)=>{el.value=9;el.dispatchEvent(new Event("input",{bubbles:true}));}')
            w.locator('rect[data-bin="2"]').focus();page.keyboard.press('Enter');assert 'Bin 3:' in w.inner_text()
            w.screenshot(path=str(QA/'histogram-lab.png'))
            result=page.evaluate('''() => { const t=window.STATS_TEST,d=window.STATS_DATA;return {counts:t.commuteCounts,real:d.realCases.map(c=>t.sum(t.tally(c.values,c.edges).counts)),oxygen:t.sum(d.oxygen.counts),under30:d.commute.filter(x=>x<30).length};}''')
            assert result=={'counts':[2,8,7,4,2,1],'real':[141,272,50],'oxygen':429,'under30':17},result
        if path.stem=='describing':
            w=page.locator('[data-widget=shape-quiz]')
            for key in ['right','bimodal','symmetric']:
                assert w.locator('[aria-pressed=true]').count()==0
                w.locator(f'[data-choice="{key}"]').click();assert 'Correct.' in w.inner_text();w.locator('[data-action=next]').click()
        if path.stem=='worked-examples':
            w=page.locator('[data-widget=evidence]')
            for key in ['true','false','true','false']:
                assert w.locator('[aria-pressed=true]').count()==0
                w.locator(f'[data-choice="{key}"]').click();assert 'Correct.' in w.inner_text();w.locator('[data-action=next]').click()
            w.locator('[data-action=reveal]').click();assert w.locator('[aria-pressed=true]').count()==0
            page.evaluate('window.dispatchEvent(new Event("beforeprint"))');assert page.locator('.print-activity').count()>0
            page.evaluate('window.dispatchEvent(new Event("afterprint"))');assert page.locator('.print-activity').count()==0
            w.locator('[data-action=clear]').click();assert w.get_attribute('data-selected')==''
        if path.stem=='practice':
            w=page.locator('[data-widget=draw-check]');w.locator('[data-action=check]').click();assert w.get_attribute('data-correct')=='false'
            for i,v in enumerate([3,7,10,6,3,1]):w.locator(f'[data-height="{i}"]').fill(str(v))
            w.locator('[data-action=check]').click();assert w.get_attribute('data-correct')=='true'
    for width in [390,768]:
        current_width=width
        for path in pages:
            goto(path.stem)
            overflow=page.evaluate('document.documentElement.scrollWidth > innerWidth+2')
            assert not overflow,f'Horizontal page overflow: {path.name} at {width}'
            if width==390 and path.stem=='histogram-lab':page.screenshot(path=str(QA/'lab-mobile.png'),full_page=True)
    browser.close()
server.shutdown()
assert not errors,errors
report={'pages':checks,'desktop':1440,'mobile':[390,768],'bin_widths':9,'bin_counts':19,'javascript_errors':errors,'checks':'local links, dataset totals, all bar steps, play/reset, both value plots, scales, bins, quiz choices, print restoration, practice feedback'}
(QA/'validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
