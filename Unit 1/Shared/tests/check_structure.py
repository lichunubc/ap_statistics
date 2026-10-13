"""Official topic titles, source layout, navigation, aliases, links and native search."""
from pathlib import Path
from urllib.parse import unquote,urlsplit,quote
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import hashlib,json,os,threading,sys,yaml
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'_quarto.yml').exists())
sys.path.insert(0,str(ROOT/'tools'))
from browser_support import load_page
DOCS=ROOT/'docs';QA=ROOT/'qa';QA.mkdir(exist_ok=True)
config=yaml.safe_load((ROOT/'_quarto.yml').read_text())
manifest=json.loads((ROOT/'project/topic-status.json').read_text())
titles=['Introducing Statistics: What Can We Learn from Data?','Variables','Tabular Representation and Summary Statistics for One Categorical Variable','Graphical Representations for One Categorical Variable','Graphical Representations for One Quantitative Variable','Descriptions for One Quantitative Variable Distributions']
parts=[p for p in config['book']['chapters'] if isinstance(p,dict)]
assert len(parts)==1 and parts[0]['part']=='Unit 1: Exploring One-Variable Data and Collecting Data'
chapters=[f'Unit 1/Topic 1.{i}/topic-1-{i}.qmd' for i in range(1,7)]
assert parts[0]['chapters'][:6]==chapters
assert not any(isinstance(x,dict) for x in parts[0]['chapters'])
assert not any(p.name.startswith('topic-') for p in ROOT.glob('*.qmd'))
assert not (ROOT/'assets').exists() and not (ROOT/'data').exists()
for i,chapter in enumerate(chapters,1):
    assert (ROOT/chapter).read_text().splitlines()[0]==f'# Topic 1.{i} {titles[i-1]}'
    topic=next(t for t in manifest['topics'] if t['id']==f'1.{i}')
    assert topic['title']==titles[i-1] and topic['chapter']==chapter
    assert topic['status'].startswith('implemented')
    assert (ROOT/Path(chapter).parent/'README.md').is_file()
    objective=json.loads((ROOT/Path(chapter).parent/'objectives.json').read_text())
    assert objective['title']==titles[i-1]
    page=DOCS/Path(chapter).with_suffix('.html');soup=BeautifulSoup(page.read_text(),'html.parser')
    assert soup.h1.get_text(' ',strip=True)==f'Topic 1.{i} {titles[i-1]}'
    nav=soup.select('#quarto-sidebar .sidebar-item-text .chapter-title')
    if nav:assert [n.get_text(' ',strip=True) for n in nav if n.get_text().startswith('Topic ')]==[f'Topic 1.{j} {titles[j-1]}' for j in range(1,7)]
    ids=[n['id'] for n in soup.select('[id]')];assert len(ids)==len(set(ids)),page
# Unmodified original shared datasets and activity engines remain byte-identical.
for item in json.loads((ROOT/'Unit 1/Shared/tests/preserved-assets.json').read_text()):
    assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
legacy=json.loads((ROOT/'Unit 1/legacy-pages.json').read_text())
for name,entry in legacy.items():
    soup=BeautifulSoup((DOCS/name).read_text(),'html.parser');target=BeautifulSoup((DOCS/entry['target']).read_text(),'html.parser')
    assert soup.h1.get_text()==target.h1.get_text()
    assert len(soup.select('[data-widget]'))==len(target.select('[data-widget]'))
    if entry['section']:assert soup.find(id=entry['section']) is not None
# Check all relative links, assets, and same-page fragments, including encoded spaces.
pages=[p for p in DOCS.rglob('*.html') if not ({'assets','site_libs'} & set(p.relative_to(DOCS).parts))]
links=0
for path in pages:
    soup=BeautifulSoup(path.read_text(),'html.parser')
    for tag in soup.select('a[href],script[src],link[href]'):
        u=urlsplit(tag.get('href',tag.get('src','')))
        if u.scheme or u.netloc:continue
        assert not u.path.startswith('/'),(path,u.path)
        target=path.parent/unquote(u.path) if u.path else path
        if target.is_dir():target=target/'index.html'
        assert target.exists(),(path,u.path)
        if u.fragment and target.suffix=='.html':
            assert BeautifulSoup(target.read_text(),'html.parser').find(id=unquote(u.fragment)),(path,u.fragment)
        links+=1
search=json.loads((DOCS/'search.json').read_text()) if (DOCS/'search.json').exists() else []
if search:
    for chapter in chapters:assert any(unquote(r['href']).split('#')[0]==str(Path(chapter).with_suffix('.html')) for r in search),chapter
    for r in search:assert (DOCS/unquote(urlsplit(r['href']).path)).exists(),r['href']
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(DOCS)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/'
errors=[];native=[]
with sync_playwright() as p:
    kwargs={'executable_path':os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'],**kwargs)
    page=browser.new_page(viewport={'width':1440,'height':1000});page.on('pageerror',lambda e:errors.append(str(e)))
    load_page(page,DOCS/'index.html',base+'index.html')
    assert page.locator('.route-card').count()==6
    page.screenshot(path=str(QA/'unit1-home-desktop.png'),full_page=True)
    # Native navigation/search require an HTTP origin. CI always runs these.
    # Offline mode does not claim to test network navigation or search fetches.
    if not os.environ.get('INLINE_BROWSER'):
        page.locator('.route-card a').nth(1).click();page.wait_for_load_state('networkidle')
        assert page.locator('h1').inner_text()=='Topic 1.2 Variables'
        page.locator('nav.page-navigation a[href*="topic-1-3.html"]').click()
        page.wait_for_load_state('networkidle');assert page.locator('h1').inner_text().startswith('Topic 1.3 ')
        native.append('homepage and next-topic links')
        page.goto(base+'topic-1-2.html',wait_until='networkidle')
        field=page.locator('#quarto-search input.aa-Input')
        field.fill('recoding');page.wait_for_selector('.aa-Item a[href*="topic-1-2"]')
        page.locator('.aa-Item a[href*="topic-1-2"]').first.click();page.wait_for_load_state('networkidle')
        assert 'topic-1-2.html' in page.url
        native.append('native full-text search from compatibility page')
        page.set_viewport_size({'width':390,'height':900})
        page.goto(base+quote('Unit 1/Topic 1.2/topic-1-2.html',safe='/'),wait_until='networkidle')
        toggle=page.locator('button[aria-label="Toggle sidebar navigation"]')
        toggle.click();page.wait_for_timeout(400)
        target=page.locator('#quarto-sidebar a[href*="topic-1-4.html"]')
        assert target.is_visible();target.click();page.wait_for_load_state('networkidle')
        assert page.locator('h1').inner_text().startswith('Topic 1.4 ')
        native.append('mobile chapter menu')
    else:
        page.close();page=browser.new_page(viewport={'width':390,'height':900});page.on('pageerror',lambda e:errors.append(str(e)))
        load_page(page,DOCS/'topic-1-2.html',base+'topic-1-2.html')
        page.locator('button[aria-label="Toggle sidebar navigation"]').click();page.wait_for_timeout(400)
        assert page.locator('#quarto-sidebar a[href*="topic-1-4.html"]').is_visible()
    page.screenshot(path=str(QA/'unit1-mobile-navigation.png'))
    browser.close()
server.shutdown();assert not errors,errors
report={'official_topics':6,'unit_parts':1,'compatibility_pages':len(legacy),'local_links_checked':links,'native_HTTP_checks':native,'mode':'offline inlining' if os.environ.get('INLINE_BROWSER') else 'HTTP browser','javascript_errors':errors}
(QA/'structure-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
