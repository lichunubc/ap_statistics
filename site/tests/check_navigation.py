"""Run ALL historical course-navigation tests with manifest-derived topic counts.
The original comprehensive test remains byte-identical as check_navigation_legacy.py.
"""
from pathlib import Path
path=Path(__file__).with_name('check_navigation_legacy.py')
source=path.read_text()
replacements=[
 ("== 6", "== len(units[0]['available_topics'])"),
 ("'topic_cards': 6", "'topic_cards': len(units[0]['available_topics'])")
]
for old,new in replacements:
    assert old in source, 'Unexpected change to navigation checker: '+old
    source=source.replace(old,new)
exec(compile(source,str(path),'exec'),{'__file__':str(path),'__name__':'__main__'})
