"""Topic 2.7 native Playwright: keyboard, independent/union logic, practice, print, no-JS and mobile."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from urllib.parse import quote
from playwright.sync_api import sync_playwright
import json,os,threading
ROOT=Path(__file__).resolve().parents[3]
remote=os.environ.get('EVENT27_BASE_URL','').rstrip('/')
server=None
if remote: base=remote+'/'
else:
 class Quiet(SimpleHTTPRequestHandler):
  def log_message(self,*args):pass
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT/'docs')))
 threading.Thread(target=server.serve_forever,daemon=True).start()
 base=f'http://127.0.0.1:{server.server_port}/'
url=base+quote('Unit 2/Topic 2.7/topic-2-7.html',safe='/')
errors=[];bad=[]
try:
 with sync_playwright() as pw:
  kw={'executable_path':os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
  br=pw.chromium.launch(headless=True,args=['--no-sandbox'],**kw)
  for width in (1440,768,390):
   context=br.new_context(viewport={'width':width,'height':900},reduced_motion='reduce')
   page=context.new_page()
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 and r.url.startswith(base) else None)
   response=page.goto(url,wait_until='networkidle',timeout=60000)
   assert response and response.ok,url
   assert page.locator('h1').inner_text().startswith('Topic 2.7 Independent')
   assert page.locator('math').count()>=7
   box=page.locator('[data-event27]')
   assert box.get_attribute('data-enhanced')=='true'
   assert box.locator('[data-event27-joint]').inner_text()=='—'
   box.locator('[data-event27-choice="evenmultiple"]').focus()
   page.keyboard.press('Enter')
   assert box.locator('[data-event27-intersection]').inner_text()=='{6}'
   assert box.locator('[data-event27-joint]').inner_text()=='1/6'
   assert box.locator('[data-event27-independent]').inner_text()=='Yes'
   assert box.locator('[data-event27-union]').inner_text()=='4/6'
   box.locator('[data-event27-choice="evenodd"]').click()
   assert box.locator('[data-event27-joint]').inner_text()=='0/6'
   assert box.locator('[data-event27-independent]').inner_text()=='No'
   assert box.locator('[data-event27-union]').inner_text()=='6/6'
   box.locator('[data-event27-choice="evengreater"]').click()
   assert box.locator('[data-event27-intersection]').inner_text()=='{4, 6}'
   assert box.locator('[data-event27-union]').inner_text()=='4/6'
   box.locator('[data-event27-reset]').click()
   assert box.locator('[data-event27-joint]').inner_text()=='—'
   assert box.locator('[aria-pressed="true"]').count()==0
   practice=page.locator('.original-practice')
   practice.locator('.original-question-title').wait_for(timeout=16000)
   assert practice.locator('.original-question-title').inner_text()=='Question 1 of 8'
   assert practice.locator('input:checked').count()==0
   practice.locator('[data-action=check]').click()
   assert 'Choose an answer' in practice.locator('.original-feedback').inner_text()
   practice.locator('input[value=A]').check()
   practice.locator('[data-action=check]').click()
   assert 'Correct' in practice.locator('.original-feedback').inner_text()
   page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
   assert practice.locator('.original-print-question').count()==8
   page.evaluate('window.dispatchEvent(new Event("afterprint"))')
   assert practice.locator('.original-print-question').count()==0
   assert not page.evaluate('document.documentElement.scrollWidth > innerWidth+2'),width
   context.close()
  context=br.new_context(java_script_enabled=False,viewport={'width':390,'height':900})
  page=context.new_page()
  resp=page.goto(url,wait_until='domcontentloaded')
  assert resp and resp.ok
  assert page.locator('.original-nojs li').count()==8
  assert 'No pair selected' in page.locator('[data-event27-status]').inner_text()
  assert 'even and multiple' in page.locator('.event27-static').inner_text()
  assert not page.evaluate('document.documentElement.scrollWidth > innerWidth+2')
  context.close()
  br.close()
finally:
 if server: server.shutdown();server.server_close()
assert not errors,errors
assert not bad,bad
qa=ROOT/'qa';qa.mkdir(exist_ok=True)
(qa/('live-event27-browser.json' if remote else 'event27-browser.json')).write_text(json.dumps({'viewports':[1440,768,390],'practice_count':8,'no_js':True,'keyboard':True,'printing':True},indent=2)+'\n')
print('Topic 2.7 desktop/mobile, keyboard, die explorer, practice, print and no-JS checks passed.')
