"""Native Chromium checks for Topic 2.1: chart, original practice, keyboard, print, no-JS and mobile."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from urllib.parse import quote
from playwright.sync_api import sync_playwright
import json,os,threading
ROOT=Path(__file__).resolve().parents[3]
QA=ROOT/'qa';QA.mkdir(exist_ok=True)
remote=os.environ.get('CAFE21_BASE_URL','').rstrip('/')
server=None
if remote: base=remote+'/'
else:
 class Quiet(SimpleHTTPRequestHandler):
  def log_message(self,*args):pass
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT/'docs')))
 threading.Thread(target=server.serve_forever,daemon=True).start()
 base=f'http://127.0.0.1:{server.server_port}/'
url=base+quote('Unit 2/Topic 2.1/topic-2-1.html',safe='/')
errors=[];bad=[]
try:
 with sync_playwright() as p:
  kw={'executable_path':os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
  browser=p.chromium.launch(headless=True,args=['--no-sandbox'],**kw)
  for width in (1440,768,390):
   context=browser.new_context(viewport={'width':width,'height':900},reduced_motion='reduce')
   page=context.new_page()
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 and r.url.startswith(base) else None)
   resp=page.goto(url,wait_until='networkidle',timeout=60000)
   assert resp and resp.ok
   assert page.locator('h1').inner_text().startswith('Topic 2.1 Tabular')
   chart=page.locator('[data-cafe21]')
   assert chart.get_attribute('data-enhanced')=='true'
   assert chart.locator('.cafe21-row').count()==6
   assert chart.locator('[data-view=counts]').get_attribute('aria-pressed')=='true'
   chart.locator('[data-view=percent]').focus()
   page.keyboard.press('Enter')
   assert chart.locator('[data-view=percent]').get_attribute('aria-pressed')=='true'
   assert 'Counter: Coffee 25%' in chart.locator('[data-cafe21-status]').inner_text()
   assert '25%' in chart.locator('.cafe21-row').nth(1).inner_text()
   chart.locator('[data-view=counts]').click()
   assert chart.locator('[data-view=counts]').get_attribute('aria-pressed')=='true'
   q=page.locator('.original-practice')
   q.locator('.original-question-title').wait_for(timeout=15000)
   assert q.locator('.original-question-title').inner_text()=='Question 1 of 8'
   assert q.locator('input:checked').count()==0
   q.locator('[data-action=check]').click()
   assert 'Choose an answer' in q.locator('.original-feedback').inner_text()
   q.locator('input[value=C]').check()
   q.locator('[data-action=check]').click()
   assert 'Correct' in q.locator('.original-feedback').inner_text()
   page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
   assert q.locator('.original-print-question').count()==8
   page.evaluate('window.dispatchEvent(new Event("afterprint"))')
   assert q.locator('.original-print-question').count()==0
   assert not page.evaluate('document.documentElement.scrollWidth > innerWidth+2'),width
   context.close()
  context=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':900})
  page=context.new_page();page.goto(url,wait_until='domcontentloaded')
  assert page.locator('.original-nojs li').count()==8
  assert page.locator('.cafe21-fallback').count()==1
  assert not page.evaluate('document.documentElement.scrollWidth > innerWidth+2')
  context.close();browser.close()
finally:
 if server:server.shutdown();server.server_close()
assert not errors,errors
assert not bad,bad
(QA/('live-cafe21-browser.json' if remote else 'cafe21-browser.json')).write_text(json.dumps({'viewport_widths':[1440,768,390],'original_questions':8,'nojs':True,'errors':errors,'bad':bad},indent=2)+'\n')
print('Topic 2.1 browser, practice, keyboard, print, no-JavaScript and responsive checks passed.')
