"""Student presentation regression gate; local HTTP or live production."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from urllib.parse import quote
import os,json,threading,re,hashlib
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];DOCS=ROOT/'docs';QA=ROOT/'qa';QA.mkdir(exist_ok=True)
manifest=json.loads((ROOT/'project/topic-status.json').read_text())
topics=[t for t in manifest['topics'] if t['id'] in {f'1.{i}' for i in range(1,10)}]
assert len(topics)==9
spec=json.loads((ROOT/'project/released-exam-figures.json').read_text())
live=os.environ.get('PRESENTATION_BASE_URL','').rstrip('/');server=None
if live:
 assert live=='https://lichunubc.github.io/ap_statistics';base=live+'/'
else:
 class Quiet(SimpleHTTPRequestHandler):
  def log_message(self,*args):pass
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(DOCS)))
 threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
 provenance=json.loads((ROOT/'project/released-exam-figures-provenance.json').read_text())
 for item in spec['items']:
  path=ROOT/item['output'];record=provenance['items'][item['id']]
  assert path.is_file() and path.stat().st_size>1000
  assert hashlib.sha256(path.read_bytes()).hexdigest()==record['image_sha256']
  assert (DOCS/item['output']).is_file()
 assert not list(DOCS.rglob('ap*-frq-*.pdf'))
errors=[];bad_requests=[];results=[]
try:
 with sync_playwright() as p:
  kw={'executable_path':os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
  browser=p.chromium.launch(headless=True,args=['--no-sandbox'],**kw)
  for width in [1440,768,390]:
   context=browser.new_context(viewport={'width':width,'height':1000},reduced_motion='reduce')
   page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('response',lambda r:bad_requests.append(r.url) if r.status>=400 and r.url.startswith(base) else None)
   for t in topics:
    path=str(Path(t['chapter']).with_suffix('.html'))
    response=page.goto(base+quote(path,safe='/'),wait_until='networkidle');assert response and response.ok,path
    main=page.locator('main');body=main.inner_text()
    assert 'Learning targets' not in body and 'Learning goal' not in body,path
    assert 'Practice · one question' not in body and 'Practice: one question' not in body,path
    assert not re.search(r'MHS-U\d+-T\d+-\d+',body),path
    assert not re.search(r'\b(?:Foundation|Developing|Challenge)\s*·',body),path
    raw=page.evaluate("""() => {let m=document.querySelector('main').cloneNode(true);m.querySelectorAll('math,code,pre,template').forEach(x=>x.remove());return m.textContent;}""")
    assert not re.search(r'\\\(|\\\)|\\boxed|\\frac',raw),path
    assert not any(x in body for x in ['original simulated teaching values','not an official College Board graphic','independently written for instruction','precedes the 2027 exam-format changes','not measurements from actual']),path
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),(path,width)
    images=main.locator('.exam-source img')
    for n in range(images.count()):
     image=images.nth(n);image.scroll_into_view_if_needed();image.evaluate('(i)=>i.decode()')
     assert image.evaluate('(i)=>i.complete&&i.naturalWidth>500&&i.naturalHeight>100')
    if t['id']=='1.9':
     tex=main.locator('math annotation').all_text_contents()
     assert any('z_A' in x and r'\boxed{2.00}' in x for x in tex),tex
     assert any('z_B' in x and r'\boxed{1.00}' in x for x in tex),tex
     assert any(r'\bar' in x and 'x_i' in x for x in tex),tex
     assert page.locator('section#takeaway-19 > ul > li').count()>=5
     anchor=page.locator('.exam-enlarge').first
     anchor.focus();page.keyboard.press('Enter');assert page.locator('.exam-zoom').is_visible()
     page.keyboard.press('Escape');assert page.locator('.exam-zoom').is_hidden()
     assert anchor.evaluate('(a)=>a===document.activeElement')
     host=page.locator('.original-practice');host.locator('.original-question-title').wait_for()
     assert host.locator('.original-meta,.original-privacy').count()==0
     assert host.locator('input:checked').count()==0
     for i in range(4):host.locator('[data-action=next]').click()
     assert host.locator('.original-question-title').inner_text()=='Question 5 of 10'
     host.locator('[data-action=solution]').click()
     assert host.locator('.original-solution math').count()>=1
     assert host.locator('[data-action=solution]').get_attribute('aria-expanded')=='true'
     host.locator('[data-action=next]').scroll_into_view_if_needed();before=page.evaluate('scrollY')
     host.locator('[data-action=next]').click();after=page.evaluate('scrollY')
     assert abs(after-before)<3,('Practice jumped',width,before,after)
     assert host.locator('.original-solution').is_hidden()
     assert host.locator('[data-action=solution]').get_attribute('aria-expanded')=='false'
     page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
     assert host.locator('.original-print-question').count()==10
     assert host.locator('.original-print-set math').count()>=5
     assert 'MHS-U1-' not in host.locator('.original-print-set').text_content()
     page.emulate_media(media='print');assert host.locator('.original-print-set').is_visible()
     page.emulate_media(media='screen');page.evaluate('window.dispatchEvent(new Event("afterprint"))')
     assert host.locator('.original-print-set').count()==0
     page.screenshot(path=str(QA/f'editorial-topic-1-9-{width}.png'),full_page=True)
    sources=main.locator('.lesson-sources')
    if sources.count():
     assert sources.last.evaluate('(s)=>Array.from(document.querySelectorAll("main .original-practice,main .homework-bank")).every(p=>Boolean(p.compareDocumentPosition(s)&Node.DOCUMENT_POSITION_FOLLOWING))'),path
   results.append({'width':width,'chapters':len(topics),'images':len(spec['items'])});context.close()
  nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':950});page=nojs.new_page()
  for tid,count in [('1.7',10),('1.8',9),('1.9',10)]:
   page.goto(base+quote(f'Unit 1/Topic {tid}/topic-{tid.replace(".","-")}.html',safe='/'),wait_until='networkidle')
   host=page.locator('.original-nojs');assert host.locator('li').count()==count
   assert host.locator('math').count()>=5
   assert 'MHS-U1-' not in host.inner_text()
   assert page.locator('.exam-description').count()==2
   page.locator('.exam-description summary').first.click()
   assert page.locator('.exam-description').first.get_attribute('open') is not None
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
  nojs.close();browser.close()
finally:
 if server:server.shutdown()
assert not errors,errors
assert not bad_requests,bad_requests
report={'mode':'production' if live else 'local HTTP','reviewed_topics':[t['id'] for t in topics],'checks':results,'mathml_in_practice_and_print':True,'source_images':len(spec['items']),'javascript_errors':errors,'failed_local_requests':bad_requests}
(QA/('live-student-presentation.json' if live else 'student-presentation.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
