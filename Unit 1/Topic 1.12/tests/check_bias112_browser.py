"""Actual HTTP/Chromium checks for Topic 1.12 sampling bias and original practice."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from urllib.parse import quote
from playwright.sync_api import sync_playwright
import json,os,threading

ROOT=Path(__file__).resolve().parents[3]
QA=ROOT/'qa'
QA.mkdir(exist_ok=True)
remote=os.environ.get('BIAS112_BASE_URL','').rstrip('/')
srv=None
if remote:
    base=remote+'/'
else:
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self,*args): pass
    srv=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT/'docs')))
    threading.Thread(target=srv.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{srv.server_port}/'
url=base+quote('Unit 1/Topic 1.12/topic-1-12.html',safe='/')
errors=[]
bad=[]
try:
 with sync_playwright() as p:
  kw={'executable_path':os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
  b=p.chromium.launch(headless=True,args=['--no-sandbox'],**kw)
  for w in (1440,768,390):
   c=b.new_context(viewport={'width':w,'height':900},reduced_motion='reduce')
   page=c.new_page()
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 and r.url.startswith(base) else None)
   res=page.goto(url,wait_until='networkidle',timeout=60000)
   assert res and res.ok
   assert page.locator('h1').inner_text().startswith('Topic 1.12 Potential Problems with Sampling')
   assert page.locator('main math').count()>=2
   lab=page.locator('[data-bias112]')
   assert 'No sample drawn' in lab.locator('[data-b112-status]').inner_text()
   lab.locator('[data-b112-method]').select_option('gate')
   lab.locator('[data-b112-n]').select_option('30')
   lab.locator('[data-b112-draw]').focus()
   page.keyboard.press('Enter')
   assert '30 selected: 30 walkers, 0 bus riders' in lab.locator('[data-b112-detail]').inner_text()
   assert '10.0 minutes' in lab.locator('[data-b112-label]').inner_text()
   lab.locator('[data-b112-method]').select_option('srs')
   lab.locator('[data-b112-n]').select_option('20')
   lab.locator('[data-b112-draw]').click()
   first=lab.locator('[data-b112-detail]').inner_text()
   assert '20 selected' in first
   lab.locator('[data-b112-reset]').click()
   assert 'No sample drawn' in lab.locator('[data-b112-status]').inner_text()
   lab.locator('[data-b112-draw]').click()
   assert first==lab.locator('[data-b112-detail]').inner_text()
   q=page.locator('.original-practice')
   q.locator('.original-question-title').wait_for(timeout=15000)
   assert q.locator('.original-question-title').inner_text()=='Question 1 of 8'
   assert q.locator('input:checked').count()==0
   q.locator('[data-action=check]').click()
   assert 'Choose an answer' in q.locator('.original-feedback').inner_text()
   q.locator('input[value=B]').check()
   q.locator('[data-action=check]').click()
   assert 'Correct' in q.locator('.original-feedback').inner_text()
   for _ in range(4): q.locator('[data-action=next]').click()
   assert q.locator('.original-question-title').inner_text()=='Question 5 of 8'
   q.locator('input[type=number]').fill('22')
   q.locator('[data-action=check]').click()
   assert 'Correct' in q.locator('.original-feedback').inner_text()
   page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
   assert q.locator('.original-print-question').count()==8
   page.evaluate('window.dispatchEvent(new Event("afterprint"))')
   assert q.locator('.original-print-question').count()==0
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),w
   page.screenshot(path=str(QA/f'bias112-{w}.png'),full_page=True)
   c.close()
  nc=b.new_context(java_script_enabled=False,viewport={'width':390,'height':900})
  p0=nc.new_page()
  p0.goto(url,wait_until='domcontentloaded')
  assert p0.locator('.original-nojs li').count()==8
  assert 'Without JavaScript' in p0.locator('main').inner_text()
  assert not p0.evaluate('document.documentElement.scrollWidth>innerWidth+2')
  nc.close()
  b.close()
finally:
 if srv: srv.shutdown();srv.server_close()
assert not errors,errors
assert not bad,bad
(QA/('live-bias112-browser.json' if remote else 'bias112-browser.json')).write_text(json.dumps({'widths':[1440,768,390],'questions':8,'nojs':True,'errors':errors,'bad':bad},indent=2)+'\n')
print('Topic 1.12 native browser, practice, print, no-JS and responsive checks passed.')
