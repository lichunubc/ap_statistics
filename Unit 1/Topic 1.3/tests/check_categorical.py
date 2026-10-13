from urllib.parse import unquote
"""Topic 1.3: arithmetic, browser interaction, accessibility, print and mobile checks."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
import json, os
from playwright.sync_api import sync_playwright

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'_quarto.yml').exists())
import sys
sys.path.insert(0,str(ROOT/'tools'))
from browser_support import load_page
DOCS=ROOT/"docs"
QA=ROOT/"qa"
QA.mkdir(exist_ok=True)
data=json.loads((ROOT/"Unit 1/Shared/data/foundations.json").read_text())
status=json.loads((ROOT/"project/topic-status.json").read_text())
topic=next(t for t in status["topics"] if t["id"]=="1.3")
assert topic["status"]=="implemented" and topic["chapter"]=="Unit 1/Topic 1.3/topic-1-3.qmd"
assert topic["learning_objectives"]==["1.3.A","1.3.B"]
assert data["school_a"]["counts"]==[8,6,18,8]
assert sum(data["school_a"]["counts"])==40
assert [round(x/40*100) for x in data["school_a"]["counts"]]==[20,15,45,20]
assert sum(data["study_locations"]["counts"])==24
assert sum(data["movie_satisfaction"]["counts"])==30
assert 18/(18+6)==.75 and (8+6)/40==.35 and 18/8==2.25
assert "topic-1-3.html" in (DOCS/"index.html").read_text()
assert (DOCS/"topic-1-3.html").exists()

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=ThreadingHTTPServer(("127.0.0.1",0),partial(Quiet,directory=str(DOCS)))
Thread(target=server.serve_forever,daemon=True).start()
errors=[]
with sync_playwright() as p:
    launch={"executable_path":os.environ["CHROMIUM_PATH"]} if os.environ.get("CHROMIUM_PATH") else {}
    browser=p.chromium.launch(headless=True,args=["--no-sandbox"],**launch)
    for width in [1440,768,390]:
        page=browser.new_page(viewport={"width":width,"height":1000})
        page.on("pageerror",lambda e:errors.append(str(e)))
        load_page(page,DOCS/"topic-1-3.html",f"http://127.0.0.1:{server.server_port}/topic-1-3.html")
        page.wait_for_function("window.CAT_TABLE_TEST !== undefined")
        assert page.evaluate("window.CAT_TABLE_TEST.counts.join(',')")=="8,6,18,8"
        assert page.evaluate("window.CAT_TABLE_TEST.sampleOrder.reduce((a,k)=>(a[k]++,a),[0,0,0,0]).join(',')")=="8,6,18,8"
        assert page.locator("math").count()>=3
        assert page.locator(".solution details").count()==7
        assert not page.evaluate("document.documentElement.scrollWidth>innerWidth+2"),width
        tally=page.locator('[data-cat-table="tally"]')
        assert tally.get_attribute("data-processed")=="0"
        tally.locator("[data-add-one]").focus()
        page.keyboard.press("Enter")
        assert tally.get_attribute("data-processed")=="1"
        tally.locator("[data-add-five]").click()
        assert tally.get_attribute("data-processed")=="6"
        tally.locator("[data-finish]").click()
        assert tally.get_attribute("data-counts")=="8,6,18,8"
        assert "45%" in tally.inner_text()
        assert tally.locator("[data-add-one]").is_disabled()
        tally.locator("[data-reset]").click()
        assert tally.get_attribute("data-processed")=="0"
        denom=page.locator('[data-cat-table="denominator"]')
        assert "45%" in denom.inner_text()
        denom.locator("[data-comparison]").select_option("3")
        assert "9:4" in denom.inner_text() and "2.25" in denom.inner_text()
        denom.locator("[data-numerator]").select_option("1")
        denom.locator("[data-comparison]").select_option("2")
        assert "1:3" in denom.inner_text()
        denom.locator("[data-reset]").click()
        assert denom.get_attribute("data-denominator")=="all"
        quiz=page.locator('[data-cat-table="claim"]')
        for answer in [1,0,1,2]:
            assert quiz.locator('[aria-pressed="true"]').count()==0
            quiz.locator(f'[data-option="{(answer+1)%4}"]').click()
            assert "Not quite." in quiz.inner_text()
            quiz.locator("[data-clear]").click()
            quiz.locator(f'[data-option="{answer}"]').focus()
            page.keyboard.press("Enter")
            assert "Correct." in quiz.inner_text()
            quiz.locator("[data-next]").click()
        assert quiz.get_attribute("data-case")=="0"
        previous=tally.locator("tbody").inner_html()
        page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
        assert page.locator(".cat-print").count()==3
        assert page.locator(".solution details[open]").count()==7
        page.evaluate('window.dispatchEvent(new Event("afterprint"))')
        assert page.locator(".cat-print").count()==0
        assert page.locator(".solution details[open]").count()==0
        assert tally.locator("tbody").inner_html()==previous
        assert not page.evaluate("document.documentElement.scrollWidth>innerWidth+2"),width
        if width in [1440,390]:
            page.screenshot(path=str(QA/f"categorical-chapter-{width}.png"),full_page=True)
        page.close()
    browser.close()
server.shutdown()
assert not errors,errors
report={"chapter":"topic-1-3","tested_widths":[1440,768,390],"practice_solutions":7,
        "quiz_cases":4,"respondents":40,"javascript_errors":errors}
(QA/"categorical-validation.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
