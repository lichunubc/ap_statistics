from pathlib import Path
import re,os
R=Path(os.environ['SOURCE_ROOT'])
def edit(path,pairs):
 p=R/path;s=p.read_text()
 for old,new in pairs:
  if old not in s: print('Review replacement not found:',path,repr(old[:80]));continue
  s=s.replace(old,new)
 p.write_text(s)
def sources(path,text):
 p=R/path;p.write_text(p.read_text().rstrip()+'\n\n::: {.lesson-sources}\n<details><summary>Sources</summary>\n\n'+text+'\n\n</details>\n:::\n')
for p in (R/'Unit 1').rglob('*.qmd'):
 s=p.read_text()
 s=re.sub(r'^\*\*Learning (?:targets|goal)[^\n]*\n\n?', '',s,flags=re.M)
 s=re.sub(r'\\\((.+?)\\\)',lambda m:'$'+m[1]+'$',s,flags=re.S)
 s=re.sub(r'\\\[(.+?)\\\]',lambda m:'\n$$\n'+m[1].strip()+'\n$$\n',s,flags=re.S)
 s=re.sub(r'<(?:p|strong)><strong>Optional enrichment[^<]*</strong>\s*','<p>',s)
 s=re.sub(r'<strong>Optional enrichment[^<]*</strong>\s*','',s)
 s=s.replace('## Practice · one question at a time','## Practice')
 s=re.sub(r'<p>(?:<strong>Interactive practice:</strong> )?enable JavaScript[^<]*</p>','',s,flags=re.I)
 s=re.sub(r'::: \{\.chapter-lead\}\s*:::\s*','',s)
 p.write_text(s)
p=R/'Unit 1/Topic 1.1/topic-1-1.qmd';s=p.read_text();s=re.sub(r'::: \{\.callout-note\}\n## Our classroom example\n.*?\n:::\n','',s,flags=re.S);s=re.sub(r'::: \{\.small-note\}\n\*\*Curriculum alignment:.*?\n:::\s*$','',s,flags=re.S);p.write_text(s)
edit('Unit 1/Topic 1.1/topic-1-1.qmd',[('1,000 hypothetical School A students','1,000 School A students'),('Attempt each question before expanding its solution. All questions below are original classroom practice.','Try each question before opening its solution.'),('## Practice: identify, formulate, justify','## Practice {#practice-identify-formulate-justify}')])
p=R/'Unit 1/Topic 1.2/topic-1-2.qmd';s=p.read_text();s=re.sub(r'::: \{\.callout-note\}\n## Data provenance\n.*?\n:::\n','',s,flags=re.S);s=s.split('## Source and reusable materials')[0];p.write_text(s)
edit('Unit 1/Topic 1.2/topic-1-2.qmd',[('Recall the hypothetical school from Topic 1.1.','Recall the School A study from Topic 1.1.'),('The following **four illustrative records** repeat the examples from Topic 1.1. They illustrate table structure; they are **not a raw-data extract of the fixed 40-response sample**.','These four example records show how variables and their values are organized in a table.'),('[Illustrative records and their data dictionary](<data/README.md>) · [CSV](<data/illustrative-records.csv>)',''),('These ten exercises are original classroom practice. Name the unit or group and give a reason, rather than only writing a classification label.','Name the unit or group and explain your classification.'),('## Practice: identify and justify {#practice}','## Practice {#practice}')])
p=R/'Unit 1/Topic 1.3/topic-1-3.qmd';s=p.read_text();s=re.sub(r'::: \{\.small-note\}\n\*\*Curriculum and provenance:.*?\n:::\s*$','',s,flags=re.S);p.write_text(s)
edit('Unit 1/Topic 1.3/topic-1-3.qmd',[('**hypothetical sample of 40 School A students**','**sample of 40 School A students**'),('; it is **not** the separate sample of 24 numerical commute times used in Topic 1.5',''),('our hypothetical data specify','the data specify'),('For teaching purposes, the activity **reproducibly shuffles the hypothetical category totals**; it does not claim to preserve an actual survey response order.','Watch how each response contributes to exactly one category.'),('All questions are independently authored classroom exercises. Try each before opening the detailed solution.','Try each question before opening its solution.'),('A **different hypothetical survey** asks','A study-location survey asks'),('A hypothetical movie-satisfaction survey','A movie-satisfaction survey'),('## Practice: construct, calculate, explain','## Practice {#practice-construct-calculate-explain}')])
p=R/'Unit 1/Topic 1.4/topic-1-4.qmd';p.write_text(p.read_text().split('## Source and data provenance')[0])
edit('Unit 1/Topic 1.4/topic-1-4.qmd',[('**hypothetical School A study**','**School A study**'),(', not the separate 24 numerical commute times in Topic 1.5',''),('**different hypothetical School B sample**','**School B sample**'),('**hypothetical movie-satisfaction survey**','**movie-satisfaction survey**'),('Each multiple-choice question starts with **no answer selected**. Check the explanation, clear a choice, or advance to the next case. Questions are original classroom exercises.','Choose an answer, then check your reasoning.'),('All eight problems and solutions below are **original classroom exercises**. Try each before opening the worked answer.','Try each question before opening its solution.'),('A separate hypothetical sample','A sample'),('## Practice: construct, compare, explain','## Practice {#practice-construct-compare-explain}')])
for n,note in [(1,'School A is a course example.'),(2,'School A and the example records are course datasets.'),(3,'School travel, study locations and movie satisfaction are course examples.'),(4,'The surveys are course examples.')]:
 sources(f'Unit 1/Topic 1.{n}/topic-1-{n}.qmd',f'[College Board course framework](https://apcentral.collegeboard.org/media/pdf/ap-statistics-course-and-exam-description-effective-fall-2026.pdf), Topic 1.{n}. '+note)
edit('Unit 1/Topic 1.5/topic-1-5.qmd',[('This topic keeps the original worked lessons and interactive activities together. Use the section links below to continue directly to a particular lesson.','**Choose a graph that makes the numerical values meaningful.** Build dotplots, stem-and-leaf plots and histograms, then explore how grouping observations changes the display.')])
edit('Unit 1/Topic 1.6/topic-1-6.qmd',[('This topic keeps the original worked lessons and interactive activities together. Use the section links below to continue directly to a particular lesson.','**Describe the whole distribution, not just its average.** Connect shape, center, spread and unusual features to the variable and its context.')])
edit('Unit 1/Topic 1.6/_describing.qmd',[('Hypothetical illustrations:','Compare these shapes:'),('These are teaching illustrations; the next activity uses published observations.',''),('The next hypothetical group','The next group')])
edit('Unit 1/Shared/practice.qmd',[('Try each question before opening its solution. These are classroom exercises, not a graded or secure test. The website does not submit your answers to a teacher.','Try each question before opening its solution.')])
edit('Unit 1/unit-1.qmd',[('compact original practice','practice'),('The School A categorical example describes a **hypothetical sample of 40 students**: Walk 8, Bicycle 6, Bus 18, and Car 8. The quantitative graph lessons use a **separate hypothetical sample of 24 one-way commute times**. Neither dataset is a record of actual Maple Hill School students. Changing the display never changes its observations.','The School A travel-method table has **40 responses**: Walk 8, Bicycle 6, Bus 18 and Car 8. The quantitative graph lessons use **24 one-way commute times**. Changing a display keeps its underlying observations the same.')])
edit('Unit 1/Topic 1.7/topic-1-7.qmd',[('Imagine a hypothetical group of **nine students**','Imagine **nine students**'),('Every statistic must refer to a clearly defined group and variable. The nine times above are **hypothetical teaching data**, not measurements from Maple Hill School. They are also **not** the separate 24-time dataset used in earlier lessons.','Every statistic refers to a clearly defined group and variable: here, the nine students and their travel times in minutes.'),('Dotplot of the hypothetical travel times','Dotplot of the travel times'),('Hypothetical nine-person sample:','Nine travel times:'),('Two screening methods appear in the Fall 2026 CED, and **they may disagree**.','Two useful screening methods **may disagree**.'),('**two independent, hypothetical** groups','**two independent groups**'),('The 50-minute observation is real *within the hypothetical data scenario* and should be investigated, not erased merely to improve the summary.','Investigate the unusually long trip before deciding how to interpret it.'),('## 9 · A real released AP Statistics exam connection {#exam-example}','## 9 · AP exam example {#exam-example}')])
p=R/'Unit 1/Topic 1.7/topic-1-7.qmd';s=p.read_text();s=re.sub(r'\*\*2024 released AP Statistics.*?\n\n(?=The given summaries)','**2024 AP Statistics, Question 6(b): whistle prices.**\n\n{{< include _exam-question.qmd >}}\n\n### Worked solution\n\n',s,flags=re.S);s=s.replace(' Other parts of 2024 Question 6 involve additional topics and are not prerequisites for this lesson. Always check the actual exam\'s instructions and the official rubric when practicing released questions.','');s=re.sub(r'The independent, teacher-authored questions below.*?\n\n(?=::: \{\.original-practice-host)','Try each question before opening its solution.\n\n',s,flags=re.S);p.write_text(s)
sources('Unit 1/Topic 1.7/topic-1-7.qmd','[College Board course framework](https://apcentral.collegeboard.org/media/pdf/ap-statistics-course-and-exam-description-effective-fall-2026.pdf), Topic 1.7. [2024 Question 6 and scoring guidelines](https://apcentral.collegeboard.org/media/pdf/ap24-sg-statistics.pdf). Workshop travel times are a course example.')
edit('Unit 1/Topic 1.8/_fundamentals.qmd',[('Imagine **nine hypothetical workshop students**','Imagine **nine workshop students**'),(' These are *invented teaching observations*, not actual Maple Hill School data and not the separate 24-commute dataset in [Topic 1.5](<../Topic 1.5/topic-1-5.qmd>).',''),('Never report these figures as measurements of the full school population: they describe only the nine hypothetical travel times.','These summaries describe the nine travel times in the sample.')])
edit('Unit 1/Topic 1.8/_skew.qmd',[('For the hypothetical times','For the times'),('**285/9 ≈ 31.67**',r'$285/9\approx31.67$')])
p=R/'Unit 1/Topic 1.8/_skew.qmd';s=p.read_text();replacement=r'''
If one observation increases by $d$, the sum $S$ increases by $d$. Therefore,

$$
\bar{x}_{\mathrm{new}}=\frac{S+d}{n}=\frac{S}{n}+\frac{d}{n}=\bar{x}+\frac{d}{n}.
$$

The times sum to $110$ minutes. Changing $18$ to $50$ increases the sum by $32$, so the mean increases by $32/9\approx3.56$ minutes:

$$
\frac{110+32}{9}=\frac{142}{9}\approx15.78\text{ minutes}.
$$

The middle observation remains $12$, so the median is unchanged.
''';s=re.sub(r'<p>If a single observation.*?</p>',lambda m:replacement,s,flags=re.S);p.write_text(s)
p=R/'Unit 1/Topic 1.8/_exam_practice.qmd';s=p.read_text().replace('## 5 · Released exam connection','## 5 · AP exam example {#released-exam-connection}');start=s.index('The final section');end=s.index('## Common mistakes');s=s[:start]+r'''**2019 AP Statistics, Question 1: university room sizes.**

{{< include _exam-question.qmd >}}

### Worked solution: parts (b) and (c)

The five-number summary, in square feet, is $(134,174,253.5,292,315)$. Calculate the middle-half spread and the two fences:

$$
\begin{aligned}
\mathrm{IQR}&=292-174=118,\\
L&=174-1.5(118)=-3,\\
U&=292+1.5(118)=469.
\end{aligned}
$$

Both extremes lie between the fences, so there are no potential outliers. Draw the box from $174$ to $292$, the median at $253.5$, and whiskers at the observed minimum $134$ and maximum $315$.

The histogram shows two clusters that the boxplot does not reveal. A boxplot summarizes ranks and spread, while a histogram shows where observations are concentrated.

'''+s[end:];s=re.sub(r'The following original exercises.*?\n\n(?=::: \{\.original-practice-host)','Try each question before opening its solution.\n\n',s,flags=re.S);p.write_text(s)
sources('Unit 1/Topic 1.8/_exam_practice.qmd','[College Board course framework](https://apcentral.collegeboard.org/media/pdf/ap-statistics-course-and-exam-description-effective-fall-2026.pdf), Topic 1.8. [2019 scoring guidelines, Question 1](https://apstudents.collegeboard.org/ap/2019-08/ap19-sg-statistics.pdf). Workshop travel times are a course example.')
edit('Unit 1/Topic 1.9/_comparison.qmd',[('two hypothetical bus routes','two bus routes'),('12 invented observations','12 observations'),('These are **original simulated teaching values**, not measurements from actual bus riders or Maple Hill School students. They are unrelated to the separate School A categorical dataset and the earlier 24-commute dataset.\n\n',''),('16.5 + 1.5(5) = **24**','$16.5+1.5(5)=24$')])
edit('Unit 1/Topic 1.9/_laboratory.qmd',[('Changing the scenario **does not** change the definition of the variable, the axes, or any real student record.','Keep the measurement units and axis scale fixed as you compare the scenarios.'),('Static alternative: the original 12 observations for each route and their verified comparison are above; all scenarios use invented teaching data.','The data table above gives the original 12 times for each route and their summaries.')])
p=R/'Unit 1/Topic 1.9/_laboratory.qmd';s=p.read_text();replacement=r'''
Suppose each observation changes from $x_i$ to $y_i=x_i+c$. The new mean is

$$
\bar y=\frac{\sum_{i=1}^{n}(x_i+c)}{n}=\bar x+c.
$$

Each deviation from the new mean is unchanged:

$$
(y_i-\bar y)=(x_i+c)-(\bar x+c)=x_i-\bar x.
$$

The squared deviations, sample variance and standard deviation are therefore unchanged. Both quartiles increase by $c$, leaving the IQR unchanged:

$$
(Q_3+c)-(Q_1+c)=Q_3-Q_1.
$$

A shift changes the center without changing the spread.
''';s=re.sub(r'<p>Suppose every observation changes.*?</p>',lambda m:replacement,s,flags=re.S);p.write_text(s)
