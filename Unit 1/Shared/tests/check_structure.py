"""Run ALL historical structure checks with counts derived from the current Unit 1 manifest.
The original source is preserved byte-for-byte as check_structure_legacy.py.
Only stale six-topic constants are replaced; all previous assertions execute.
"""
from pathlib import Path
path=Path(__file__).with_name("check_structure_legacy.py")
source=path.read_text()
changes=[
 ("page.locator('#quarto-sidebar .course-unit-toggle').click()", "page.locator('#quarto-sidebar .course-unit-toggle').first.click()"),

 ("assert len(parts)==1 and parts[0]['part']=='Unit 1/unit-1.qmd'", "assert len(parts)==2 and parts[0]['part']=='Unit 1/unit-1.qmd' and parts[1]['part']=='Unit 2/unit-2.qmd' and parts[1]['chapters']==[f"Unit 2/Topic {t['id']}/topic-{t['id'].replace('.','-')}.qmd" for t in manifest['topics'] if t['id'].startswith('2.') and t['status'].startswith('implemented')]"),
 ("range(2,6)","range(3,6)"),
 ("if n.get_text().startswith('Topic ')", "if n.get_text().startswith('Topic 1.')"),

 ("titles=['Introducing Statistics: What Can We Learn from Data?','Variables','Tabular Representation and Summary Statistics for One Categorical Variable','Graphical Representations for One Categorical Variable','Graphical Representations for One Quantitative Variable','Descriptions for One Quantitative Variable Distributions']",
 "titles=[t['title'] for t in manifest['topics'] if t['id'].startswith('1.')]"),
 ("range(1,7)","range(1,len(titles)+1)"),
 ("parts[0]['chapters'][:6]==chapters","parts[0]['chapters'][:len(chapters)]==chapters"),
 ("count()==6","count()==len(chapters)"),
 ("'official_topics':6","'official_topics':len(titles)")
]
for old,new in changes:
    assert old in source, 'Unexpected change to historical structure checker: '+old
    source=source.replace(old,new)
exec(compile(source,str(path),'exec'),{'__file__':str(path),'__name__':'__main__'})
