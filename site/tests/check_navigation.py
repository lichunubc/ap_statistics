"""Run ALL historical course-navigation tests with manifest-derived topic counts.
The original comprehensive test remains byte-identical as check_navigation_legacy.py.
"""
from pathlib import Path
path=Path(__file__).with_name('check_navigation_legacy.py')
source=path.read_text()
replacements=[
 ("units[0]['available_topics'] == [t['id'] for t in topics]","units[0]['available_topics'] == [t['id'] for t in topics if t['id'].startswith('1.')]"),
 ("for u in units[1:]","for u in units[2:]"),
 ("len(home.select('main [data-unit-status=\"under-construction\"]')) == 4","len(home.select('main [data-unit-status=\"under-construction\"]')) == 3"),
 ("assert buttons.count() == 1, 'Only Unit 1 currently has published topics.'","assert buttons.count() == 2, 'Units 1 and 2 both have topic disclosures.'"),
 ("assert buttons.first.get_attribute('aria-expanded') == 'false'","assert all(buttons.nth(i).get_attribute('aria-expanded') == 'false' for i in range(buttons.count()))"),
 ("page.locator('#quarto-sidebar .course-topic-list[hidden]').count() == 1","page.locator('#quarto-sidebar .course-topic-list[hidden]').count() == 2"),
 ("button = page.locator('#quarto-sidebar .course-unit-toggle')","button = page.locator('#quarto-sidebar .course-unit-toggle').first"),
 ("page.locator('#quarto-sidebar .course-unit-toggle').click()","page.locator('#quarto-sidebar .course-unit-toggle').first.click()"),
 ("if i != 1:","if i >= 3:"),
 ("else:\n                    assert page.locator('main .topic-grid .route-card').count() == 6","else:\n                    assert page.locator('main .topic-grid .route-card').count() == len(units[i-1]['available_topics'])"),
 ("if unit['id'] == 1:\n            assert len(soup.select('main .topic-grid .route-card')) == 6\n            assert soup.select_one('main [data-chart=\"commute-dot\"]')\n        else:","if unit['id'] == 1:\n            assert len(soup.select('main .topic-grid .route-card')) == 6\n            assert soup.select_one('main [data-chart=\"commute-dot\"]')\n        elif unit['id'] == 2:\n            assert len(soup.select('main .topic-grid .route-card')) == len(unit['available_topics'])\n            assert soup.select('main .route-card a[href*=\"topic-2-1.html\"]')\n        else:"),

 ("== 6", "== len(units[0]['available_topics'])"),
 ("'topic_cards': 6", "'topic_cards': len(units[0]['available_topics'])")
]
for old,new in replacements:
    assert old in source, 'Unexpected change to navigation checker: '+old
    source=source.replace(old,new)
exec(compile(source,str(path),'exec'),{'__file__':str(path),'__name__':'__main__'})
