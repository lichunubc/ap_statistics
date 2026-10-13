"""Topic 1.4: numeric correctness, interactive graphs, keyboard, print, mobile regression."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
import json
import os
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/"docs"
QA=ROOT/"qa"
QA.mkdir(exist_ok=True)
data=json.loads((ROOT/"data/foundations.json").read_text())
status=json.loads((ROOT/"project/topic-status.json").read_text())
topic=next(t for t in status["topics"] if t["id"]=="1.4")
assert topic["status"]=="implemented" and topic["chapter"]=="topic-1-4.qmd",topic
assert topic["learning_objectives"]==["1.4.A","1.4.B","1.4.C"]
a=data["school_a"];b=data["school_b_comparison"]
assert a["counts"]==[8,6,18,8] and a["sample_size"]==40
assert b["counts"]==[9,6,18,27] and b["sample_size"]==60
assert sum(a["counts"])==a["sample_size"]
assert sum(b["counts"])==b["sample_size"]
assert [round(v/40*360) for v in a["counts"]]==[72,54,162,72]
assert [round(v/60*360) for v in b["counts"]]==[54,36,108,162]
assert sum([round(v/40*360) for v in a["counts"]])==360
assert sum([round(v/60*360) for v in b["counts"]])==360
assert sum(data["study_locations"]["counts"])==24
assert sum(data["movie_satisfaction"]["counts"])==30
assert 18/40==.45 and 18/60==.3 and 27/60==.45
assert "topic-1-4.html" in (DOCS/"index.html").read_text()
assert (DOCS/"topic-1-4.html").exists()

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
        page.goto(f"http://127.0.0.1:{server.server_port}/topic-1-4.html",wait_until="networkidle")
        page.wait_for_function("window.CAT_CHART_TEST !== undefined")
        meta=page.evaluate("window.CAT_CHART_TEST")
        assert meta["A"]==a["counts"] and meta["B"]==b["counts"],meta
        assert meta["anglesA"]==[72,54,162,72] and meta["anglesB"]==[54,36,108,162]
        assert page.locator(".solution details").count()==8
        assert page.locator("math").count()>=1
        assert not page.evaluate("document.documentElement.scrollWidth>innerWidth+2"),width
        builder=page.locator('[data-cat-chart="builder"]')
        assert builder.get_attribute("data-step")=="0"
        assert builder.get_attribute("data-group")=="A"
        assert builder.get_attribute("data-total")=="40"
        assert builder.locator("rect.cat-chart-bar").count()==0
        builder.locator("[data-next]").focus()
        page.keyboard.press("Enter")
        assert builder.get_attribute("data-step")=="1"
        assert builder.locator("rect.cat-chart-bar").count()==1
        builder.locator("[data-full]").click()
        assert builder.locator("rect.cat-chart-bar").count()==4
        builder.locator("[data-type]").select_option("percent")
        assert builder.get_attribute("data-step")=="0"
        builder.locator("[data-full]").click()
        assert builder.get_attribute("data-mode")=="percent"
        assert "45%" in builder.locator("[data-plot]").inner_text()
        builder.locator("[data-type]").select_option("pie")
        builder.locator("[data-full]").click()
        assert builder.locator("path.cat-pie-sector").count()==4
        assert "162°" in builder.inner_text()
        builder.locator("[data-source]").select_option("B")
        assert builder.get_attribute("data-total")=="60"
        assert builder.get_attribute("data-step")=="0"
        builder.locator("[data-full]").click()
        assert builder.locator("path.cat-pie-sector").count()==4
        builder.locator("[data-reset]").click()
        assert builder.get_attribute("data-step")=="0"
        assert builder.locator("path.cat-pie-sector").count()==0
        compare=page.locator('[data-cat-chart="compare"]')
        assert compare.get_attribute("data-selected")==""
        assert compare.locator(".cat-compare-bar").count()==8
        compare.locator("[data-scale]").select_option("count")
        assert compare.get_attribute("data-mode")=="count"
        assert compare.locator(".cat-compare-bar").count()==8
        compare.locator('[data-category-choice="2"]').focus()
        page.keyboard.press("Enter")
        assert compare.get_attribute("data-selected")=="2"
        assert "18 of 40" in compare.locator(".status").inner_text()
        assert "18 of 60" in compare.locator(".status").inner_text()
        assert "15 percentage points" in compare.locator(".status").inner_text()
        compare.locator("[data-scale]").select_option("percent")
        assert compare.get_attribute("data-mode")=="percent"
        quiz=page.locator('[data-cat-chart="audit"]')
        for correct in [1,2,0,1,2]:
            assert quiz.locator('[aria-pressed="true"]').count()==0
            assert quiz.get_attribute("data-selected")==""
            wrong=(correct+1)%3
            quiz.locator(f'[data-option="{wrong}"]').click()
            assert "Not quite." in quiz.locator(".status").inner_text()
            quiz.locator("[data-clear]").click()
            assert quiz.locator('[aria-pressed="true"]').count()==0
            quiz.locator(f'[data-option="{correct}"]').focus()
            page.keyboard.press("Enter")
            assert "Correct." in quiz.locator(".status").inner_text()
            quiz.locator("[data-next]").click()
        assert quiz.get_attribute("data-case")=="0"
        page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
        assert page.locator(".cat-chart-print").count()==3
        assert page.locator(".cat-chart-print .cat-viz").count()==3
        page.evaluate('window.dispatchEvent(new Event("afterprint"))')
        assert page.locator(".cat-chart-print").count()==0
        assert not page.evaluate("document.documentElement.scrollWidth>innerWidth+2"),width
        if width in [1440,390]:
            page.screenshot(path=str(QA/f"categorical-graphs-{width}.png"),full_page=True)
        page.close()
    browser.close()
server.shutdown()
assert not errors,errors
report={"chapter":"topic-1-4","tested_widths":[1440,768,390],
        "bar_chart_modes":2,"pie_chart":True,"groups":["A","B"],
        "audit_cases":5,"practice_solutions":8,"javascript_errors":errors}
(QA/"categorical-charts-validation.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
