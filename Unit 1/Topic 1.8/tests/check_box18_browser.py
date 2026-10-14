"""Live HTTP browser gate for boxplot construction, accessibility and original practice."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from urllib.parse import quote
from playwright.sync_api import sync_playwright
import os,threading,math,json
ROOT=Path(__file__).resolve().parents[3];DOCS=ROOT/'docs'
QA=ROOT/'qa';QA.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(DOCS)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base='http://127.0.0.1:'+str(server.server_port)+'/'
errors=[]
try:
  with sync_playwright() as p:
    kw={'executable_path':os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'],**kw)
    for width in [1440,768,390]:
      context=browser.new_context(viewport={'width':width,'height':950})
      page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
      page.goto(base+quote('Unit 1/Topic 1.8/topic-1-8.html',safe='/'),wait_until='networkidle')
      assert 'Topic 1.8 Graphical Representations of Summary Statistics' in page.locator('h1').inner_text()
      box=page.locator('[data-box18]')
      assert box.locator('svg circle').count()==9
      assert float(box.get_attribute('data-median'))==12
      assert float(box.get_attribute('data-q1'))==9
      assert float(box.get_attribute('data-q3'))==15.5
      assert math.isclose(float(box.get_attribute('data-mean')),110/9,abs_tol=.005)
      box.locator('[data-box18-action=next]').click()
      assert box.get_attribute('data-step')=='1'
      for i in range(3):box.locator('[data-box18-action=next]').click()
      assert box.get_attribute('data-step')=='4'
      box.locator('[data-box18-scenario]').select_option('extreme')
      assert box.get_attribute('data-step')=='0'
      assert box.get_attribute('data-whisker-right')=='16'
      assert box.get_attribute('data-flagged')=='1'
      for i in range(4):box.locator('[data-box18-action=next]').click()
      assert box.locator('svg circle[r="6"]').count()==1
      box.locator('[data-box18-style]').select_option('unmodified')
      assert box.get_attribute('data-whisker-right')=='50'
      box.locator('[data-box18-scenario]').select_option('left')
      assert box.get_attribute('data-median')=='35'
      assert math.isclose(float(box.get_attribute('data-mean')),285/9,abs_tol=.005)
      box.locator('[data-box18-values]').fill('10,,20')
      box.locator('[data-box18-action=apply]').click()
      assert 'Invalid entry' in box.locator('[data-box18-step]').inner_text()
      box.locator('[data-box18-action=reset]').click()
      assert float(box.get_attribute('data-median'))==12
      notes=page.locator('main details.math-note')
      assert notes.count()>=4
      assert notes.first.get_attribute('open') is None
      notes.first.locator('summary').focus();page.keyboard.press('Enter')
      assert notes.first.get_attribute('open') is not None
      mathml=page.locator('main math')
      assert mathml.count()>=4,'Expected rendered MathML in the lesson'
      host=page.locator('.original-practice')
      host.locator('.original-question-title').wait_for()
      assert host.locator('.original-question-title').inner_text()=='Question 1 of 9'
      assert host.locator('input[type=radio]:checked').count()==0
      host.locator('[data-action=check]').click()
      assert 'Choose an answer' in host.locator('.original-feedback').inner_text()
      host.locator('input[type=radio][value=A]').check()
      host.locator('[data-action=check]').click()
      assert 'Correct' in host.locator('.original-feedback').inner_text()
      host.locator('[data-action=solution]').click()
      assert host.locator('.original-solution').is_visible()
      host.locator('[data-action=next]').click()
      assert host.locator('.original-question-title').inner_text()=='Question 2 of 9'
      assert host.locator('.original-solution').is_hidden()
      host.locator('[data-action=previous]').click()
      assert host.locator('input[type=radio]:checked').count()==0
      page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
      assert host.locator('.original-print-question').count()==9
      page.evaluate('window.dispatchEvent(new Event("afterprint"))')
      assert host.locator('.original-print-question').count()==0
      assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
      if width==390:page.screenshot(path=str(QA/'topic-1-8-mobile.png'),full_page=True)
      context.close()
    nojs=browser.new_context(java_script_enabled=False)
    page=nojs.new_page()
    page.goto(base+quote('Unit 1/Topic 1.8/topic-1-8.html',safe='/'))
    assert page.locator('.original-nojs li').count()==9
    nojs.close();browser.close()
finally:server.shutdown()
assert not errors,errors
(QA/'topic-1-8-browser.json').write_text(json.dumps({'widths':[1440,768,390],'practice':9,'no_js':True,'errors':errors},indent=2))
print('Topic 1.8 boxplot, practice, math, keyboard, print, responsive and no-JS gate passed.')
