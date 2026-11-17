"""Native browser checks for approved local slide player after Quarto resource copying."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from urllib.parse import quote
from playwright.sync_api import sync_playwright
import os,threading,json
ROOT=Path(__file__).resolve().parents[2];remote=os.environ.get('SLIDES27_BASE_URL','').rstrip('/');server=None
if remote:base=remote+'/'
else:
 class Quiet(SimpleHTTPRequestHandler):
  def log_message(self,*args):pass
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT/'docs')))
 threading.Thread(target=server.serve_forever,daemon=True).start()
 base=f'http://127.0.0.1:{server.server_port}/'
url=base+quote('Unit 2/resources/probability-simulation-slides.html',safe='/')
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
   r=page.goto(url,wait_until='networkidle',timeout=60000)
   assert r and r.ok
   assert page.locator('.slide').count()==42
   assert page.locator('#familiar-probabilities').count()==1
   assert page.locator('#sample-space-intro').count()==1
   nav=page.locator('.deck-nav')
   assert nav.locator('[data-progress]').inner_text().strip()=='1 / 42'
   nav.locator('[data-nav=next]').click()
   assert nav.locator('[data-progress]').inner_text().strip()=='2 / 42'
   assert page.locator('#familiar-probabilities').get_attribute('aria-hidden')=='false'
   page.keyboard.press('ArrowRight')
   assert nav.locator('[data-progress]').inner_text().strip()=='3 / 42'
   assert page.locator('#sample-space-intro').get_attribute('aria-hidden')=='false'
   page.keyboard.press('Home')
   assert nav.locator('[data-progress]').inner_text().strip()=='1 / 42'
   context.close()
  context=br.new_context(java_script_enabled=False,viewport={'width':390,'height':900})
  page=context.new_page();r=page.goto(url,wait_until='domcontentloaded')
  assert r and r.ok
  assert page.locator('.slide').count()==42
  assert page.locator('#sample-space-intro').count()==1
  context.close();br.close()
finally:
 if server:server.shutdown();server.server_close()
assert not errors,errors
assert not bad,bad
qa=ROOT/'qa';qa.mkdir(exist_ok=True)
(qa/('live-probability-slides.json' if remote else 'probability-slides.json')).write_text(json.dumps({'slide_count':42,'viewports':[1440,768,390],'keyboard_navigation':True,'no_js_static':True},indent=2)+'\n')
print('Approved 42-slide resource and keyboard/mobile/no-JS browser checks passed.')
