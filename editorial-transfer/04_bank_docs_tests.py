from pathlib import Path
import os,json,re,hashlib
R=Path(os.environ['SOURCE_ROOT'])
solutions={
'1.7':{
1:r'The total is 110 minutes and $n=9$. The sample mean is $\bar{x}=\frac{110}{9}\approx12.22$ minutes. It describes the average in this sample.',
2:r'The middle pair is 8 and 11, so the median is $\frac{8+11}{2}=9.5$ points. The median can fall between observed scores.',
3:r'The median is 7 km. The lower half gives $Q_1=5$ km; the upper half gives $Q_3=11$ km. Thus $\mathrm{IQR}=11-5=6$ km.',
4:r'The mean is $4\,{}^\circ\mathrm{C}$ and the squared deviations total $8\,{}^\circ\mathrm{C}^2$. The sample variance is $s^2=\frac{8}{3-1}=4\,{}^\circ\mathrm{C}^2$. The sample standard deviation is $s=\sqrt{4}=2\,{}^\circ\mathrm{C}$.',
6:r'$15\text{ minutes}\times60\frac{\text{seconds}}{\text{minute}}=900\text{ seconds}$. The sample SD, median, range and IQR also multiply by 60; variance multiplies by $60^2=3600$.',
7:r'C. The IQR is 6 and the upper fence is $11+1.5(6)=20$, so 30 is outside. The mean is $\bar{x}=\frac{73}{7}\approx10.43$ and $s\approx8.942$. Thus $\bar{x}+2s\approx28.31$, so 30 also exceeds the two-SD boundary. Both rules identify an observation to investigate.',
8:r'The mean is $\bar{x}=\frac{73}{7}\approx10.42857$; $s^2\approx79.95238$ and $s\approx8.94161$. The upper boundary is $\bar{x}+2s\approx10.42857+2(8.94161)\approx28.31179$, or 28.31. Because $30>28.31$, the value is flagged.'},
'1.8':{
1:r'A. The minimum is 4; $Q_1=\operatorname{median}(4,6,8)=6$; the median is 8; $Q_3=\operatorname{median}(9,12,14)=12$; the maximum is 14. Label the display in points.',
2:r'The lower half has $Q_1=\frac{4+5}{2}=4.5$ km. The upper half has $Q_3=\frac{12+14}{2}=13$ km. Therefore $\mathrm{IQR}=13-4.5=8.5$ km.',
3:r'$\mathrm{IQR}=15.5-9=6.5$ minutes. The upper fence is $U=15.5+1.5(6.5)=25.25$ minutes. The fence is a screening boundary; a whisker ends at an observed non-outlier.',
7:r'Both groups have median 6 minutes. Group A has $\mathrm{IQR}_A=8-4=4$ minutes, whereas Group B has $\mathrm{IQR}_B=9-3=6$ minutes. Group B’s middle half is more variable by 2 minutes. These summaries compare the observed groups; dotplots would provide additional evidence about modes and gaps.',
8:r'The five-number summary is 3, $Q_1=\frac{4+5}{2}=4.5$, 7, $Q_3=\frac{9+10}{2}=9.5$, 30 minutes. Thus $\mathrm{IQR}=9.5-4.5=5$ minutes. The fences are $L=4.5-1.5(5)=-3$ and $U=9.5+1.5(5)=17$ minutes. Draw the box from 4.5 to 9.5 and the median at 7. Extend whiskers to observed values 3 and 10, and mark 30 separately. The boundary 17 is not a whisker endpoint.',
9:r'The total is 285 minutes and $n=9$, so $\bar{x}=\frac{285}{9}\approx31.67$ minutes, below the median of 35. The low observation contributes to the long left tail. The graph, rather than the mean–median ordering alone, establishes the tail pattern.'}}
replacements={'1.7':{'s = 4.2':r'$s=4.2$'},'1.8':{},'1.9':{
'16.5 − 13.5 = 3':r'$16.5-13.5=3$',
'z = (86 − 70)/8 = 2':r'$z=\frac{86-70}{8}=2$',
'z = (73 − 85)/6 = −2':r'$z=\frac{73-85}{6}=-2$',
'z_A = 2 and z_B = 1':r'$z_A=2$ and $z_B=1$',
'z = (x − μ)/σ':r'$z=\frac{x-\mu}{\sigma}$',
'z = −1.5':r'$z=-1.5$', 'z = 1':r'$z=1$',
'x = 60 + (−1.5)(4) = 54':r'$x=60+(-1.5)(4)=54$',
'(54 − 60)/4 = −1.5':r'$\frac{54-60}{4}=-1.5$',
'x = μ + zσ':r'$x=\mu+z\sigma$'}}
for tid,mapping in replacements.items():
 p=R/f'Problem Bank/original/unit-1/topic-{tid.replace(".","-")}.json';bank=json.loads(p.read_text())
 for n,q in enumerate(bank['items'],1):
  for owner,k in [(q,k) for k in ['prompt','hint','solution','rubric'] if isinstance(q.get(k),str)]+[(o,'text') for o in q.get('options',[])]:
   s=owner[k].replace('hypothetical ','').replace('Hypothetical ','')
   for old,new in mapping.items():s=s.replace(old,new)
   owner[k]=s
  if n in solutions.get(tid,{}):q['solution']=solutions[tid][n]
 bank['revision']=int(bank.get('revision',1))+1
 p.write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
# Retain tests of arithmetic/coverage while moving source citations into included image captions.
p=R/'Unit 1/Topic 1.7/tests/check_summary17.py';p.write_text(p.read_text().replace("chapter=(topic/'topic-1-7.qmd').read_text()","chapter=(topic/'topic-1-7.qmd').read_text()+'\\n'+(topic/'_exam-question.qmd').read_text()"))
p=R/'Unit 1/Topic 1.8/tests/check_box18.py';p.write_text(p.read_text().replace("text='\\n'.join((topic/p).read_text() for p in parts)","text='\\n'.join((topic/p).read_text() for p in parts+['_exam-question.qmd'])").replace("assert '2019 AP Statistics FRQ' in text","assert '2019 AP Statistics' in text"))
p=R/'Unit 1/Topic 1.9/tests/check_compare19.py';p.write_text(p.read_text().replace("lessons='\\n'.join((TOP/p).read_text() for p in parts)","lessons='\\n'.join((TOP/p).read_text() for p in parts+['_exam-question.qmd'])").replace("['Optional enrichment','normal'","['Optional','normal'"))
p=R/'Unit 1/Topic 1.9/tests/check_compare19_browser.py';s=p.read_text();s=re.sub(r"^(\s*)assert 'Static alternative' in (\w+)\.locator\('main'\)\.inner_text\(\)",lambda m:m[1]+f"assert {m[2]}.locator('.compare19-table tbody tr').count()==2\n"+m[1]+f"assert '16.50' in {m[2]}.locator('.compare19-table').inner_text()",s,flags=re.M);p.write_text(s)
p=R/'tools/check_all.py';s=p.read_text().replace("'Unit 1/Topic 1.9/tests/check_compare19_browser.py']","'Unit 1/Topic 1.9/tests/check_compare19_browser.py',\n'site/tests/check_student_presentation.py']");p.write_text(s)
for name in ['CONTRIBUTING.md','project/UNIT_1_2_EXPANSION.md']:
 p=R/name;s=p.read_text();i=s.index('\n');link='project/STUDENT_PRESENTATION.md' if name=='CONTRIBUTING.md' else 'STUDENT_PRESENTATION.md'
 p.write_text(s[:i]+f'\n\n**Student presentation:** follow [Chun Li’s current presentation settings]({link}). The October 15 review supersedes earlier instructions about visible curriculum blocks, source disclaimers, question metadata, practice headings and exam-image presentation. Keep complete objective/provenance records in source.\n'+s[i:])
p=R/'README.md';s=p.read_text().replace('Topics 1.1–1.8','Topics 1.1–1.9').replace('with the six official topics as direct children','with the available official topics as direct children');s+='\n## Student presentation\n\nFollow [the presentation guide](project/STUDENT_PRESENTATION.md). Keep mappings and provenance in source; teach through clean introductions, typeset mathematics, on-page exam examples and Practice panels.\n';p.write_text(s)
p=R/'CHANGELOG.md';s=p.read_text().replace('# Changelog','# Changelog\n\n## 2026-10-15 — Student presentation review, Topics 1.1–1.9\n\n- Removed opening curriculum blocks and repeated administrative commentary, retaining source mappings and provenance.\n- Fixed mathematical rendering in lessons, derivations and original-bank practice; preserved numerical answers.\n- Simplified Practice headings and removed visible difficulty, internal IDs and skill labels.\n- Added original released-question images, accessible descriptions and on-page enlargement beside worked examples.\n- Reformatted Topic 1.9’s checklist and recorded future presentation rules.\n- Added rendered-math, image, keyboard, mobile, print and no-JavaScript presentation tests; Actions establishes actual release status.\n',1);p.write_text(s)
(R/'resources.qmd').write_text('''# Sources and study resources

## Course framework

The [College Board AP Statistics course framework](https://apcentral.collegeboard.org/media/pdf/ap-statistics-course-and-exam-description-effective-fall-2026.pdf) lists the course topics. The [released exam archive](https://apcentral.collegeboard.org/courses/ap-statistics/exam/past-exam-questions) provides additional questions and scoring guidelines.

## Datasets

| Dataset | Measurement | Source |
|:--|:--|:--|
| Rivers | Major North American river lengths, in miles | [R datasets: rivers](https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/rivers.html) |
| Old Faithful | Eruption duration, in minutes | [R datasets: faithful](https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/faithful.html) |
| Iris flowers | Sepal length, in centimetres | [R datasets: iris](https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/iris.html) |

[Download the commute-time data](<Unit 1/Shared/data/commute-times.csv>) to build a dotplot, stemplot, or histogram.

## Practice

Use the **Practice** section in each lesson to check your understanding. Try a question before opening its solution, then compare both the result and reasoning. The **Selected Homework** bank uses the class file supplied by your teacher.

## Printing

Use your browser’s Print command for a paper copy of a lesson. Open the explanations you wish to include before printing.
''')
p=R/'.github/workflows/publish.yml';s=p.read_text().replace('      - name: Render the Quarto book','      - name: Install question-image renderer\n        run: python -m pip install PyMuPDF==1.26.7\n      - name: Render the Quarto book');s=s.replace('          git add docs','          git add docs\n          git add -- "Unit 1/Topic 1.6/assets/exam" "Unit 1/Topic 1.7/assets/exam" "Unit 1/Topic 1.8/assets/exam" "Unit 1/Topic 1.9/assets/exam" project/released-exam-figures-provenance.json');s=s.replace('            qa\n          retention-days:', '            qa\n            Unit 1/**/assets/exam/\n            project/released-exam-figures-provenance.json\n          retention-days:');s=s.replace('        run: python "Problem Bank/tests/check_bank.py"','        run: python "Problem Bank/tests/check_bank.py"\n      - name: Verify live student presentation\n        if: steps.deployment.outcome == \'success\'\n        env:\n          PRESENTATION_BASE_URL: ${{ steps.deployment.outputs.page_url }}\n        run: python site/tests/check_student_presentation.py');p.write_text(s)
