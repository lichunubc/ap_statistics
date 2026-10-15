from pathlib import Path
import os,re
R=Path(os.environ['SOURCE_ROOT'])
p=R/'Unit 1/Topic 1.9/_standardization.qmd';tail=p.read_text().split('### Z-score explorer:')[1]
head=r'''## 3 · Relative position: the z-score {#zscore-19}

A score of 86 on one assessment and 90 on another does not say which is stronger **relative to its own distribution**. The reference mean and standard deviation provide the missing context. A **z-score** gives the number of standard deviations an observation lies above or below its reference mean.

For a population with mean $\mu$ and standard deviation $\sigma>0$,

$$
z=\frac{x-\mu}{\sigma}.
$$

Here $x$ is the observed value. Subtracting the mean gives a distance in the original units; dividing by $\sigma$ converts it into standard-deviation units. A z-score is **unit-free**: positive above the mean, negative below it, and zero at the mean.

<details class="math-note">
<summary>Derivation: distance in standard-deviation units (optional)</summary>

If an observation is $z$ standard deviations above the mean, its displacement is $z\sigma$. Thus

$$
x-\mu=z\sigma\quad\Longrightarrow\quad z=\frac{x-\mu}{\sigma}.
$$

The numerator and denominator share the same measurement units, so the units cancel. The condition $\sigma>0$ matters: with no variability, this standardized distance is undefined.

</details>

### Worked example: compare two assessments

On Assessment A, a student scores **86 points**. The population mean is **70 points** and its standard deviation is **8 points**:

$$
z_A=\frac{86-70}{8}=\frac{16}{8}=\boxed{2.00}.
$$

On Assessment B, the student scores **90 points**. The population mean is **80 points** and its standard deviation is **10 points**:

$$
z_B=\frac{90-80}{10}=\frac{10}{10}=\boxed{1.00}.
$$

Assessment A has the stronger relative position: **two standard deviations above its own mean**, compared with one on B, even though its raw score is lower.

### Interpret signs and compare distributions {#interpret-z-19}

A z-score of $-1.5$ means one and a half standard deviations **below** the reference mean; $+2$ means two standard deviations **above** it. Whether a larger value is desirable depends on the variable: a higher assessment score might be desirable, while a longer emergency wait time might not.

A z-score describes **standardized distance**, not a percentile or probability. Equal z-scores in differently shaped distributions can correspond to different percentile ranks. Standardizing preserves shape and ordering; **it does not make a distribution normal**.

### Recover a value from its z-score

Rearrange the standardization formula:

$$
x=\mu+z\sigma.
$$

<details class="math-note">
<summary>Derivation: recover the raw value (optional)</summary>

Multiply both sides of $z=(x-\mu)/\sigma$ by $\sigma$, then add $\mu$:

$$
\begin{aligned}
z\sigma&=x-\mu,\\
x&=\mu+z\sigma.
\end{aligned}
$$

For example, $z=1.5$, $\mu=70$ points and $\sigma=8$ points give $x=70+1.5(8)=82$ points.

</details>

### Describe relative position within a sample

Use the sample's own mean $\bar{x}$ and sample standard deviation $s>0$:

$$
z_{\mathrm{sample}}=\frac{x-\bar{x}}{s}.
$$

<details class="math-note">
<summary>Why use the sample summaries?</summary>

This defines relative position using the sample's own center and spread. Sample summaries estimate population parameters when the sampling context supports that use; they are not automatically equal to them. State which reference group the standardized score describes.

</details>

In Route A's sample, a 21-minute trip has

$$
z_A=\frac{21-16.5}{2.393}\approx1.88.
$$

In Route B's sample, a 19-minute trip has

$$
z_B=\frac{19-15.583}{7.633}\approx0.45.
$$

The Route A trip is farther above **its own route's mean** in standard-deviation units. Percentile comparisons would also require the shapes of the distributions.

### Z-score explorer:''' 
tail=tail.replace('(hypothetical population)','(population)')
tail=re.sub(r'<p class="compare19-access">.*?</p>',lambda m:r'<p class="compare19-access">Assessment A: $x=86$, $\mu=70$, $\sigma=8$ and $z=2$. Assessment B: $x=90$, $\mu=80$, $\sigma=10$ and $z=1$. Reducing a positive SD makes a fixed positive distance correspond to more standard deviations.</p>',tail)
p.write_text(head+tail)
(R/'Unit 1/Topic 1.9/_exam-and-practice.qmd').write_text(r'''## 4 · AP exam example {#released-19}

**2026 AP Statistics, Question 1: comparing goat weights.**

{{< include _exam-question.qmd >}}

### Worked solution: part B

Breed H has median weight **64 pounds**, with $Q_1=56$ and $Q_3=72$, so

$$
\mathrm{IQR}_H=72-56=16\text{ pounds}.
$$

Breed J's boxplot indicates a median near **64 pounds** and quartiles near **56 and 80 pounds**, giving an IQR of approximately **24 pounds**. The observed ranges are **32 pounds** for H and approximately **40 pounds** for J.

**The sampled breeds have similar median weights, but Breed J has greater middle-half and overall variability.** State the groups, variable and units, then support the comparison with numerical evidence.

### Worked solution: part C

The stem-and-leaf plot shows **two concentrations of Breed H weights**. A boxplot records the five-number summary rather than the individual arrangement, so it does not reliably display those two peaks. The stemplot shows detail; the boxplot emphasizes center and spread.

## Common errors and final checklist {#takeaway-19}

- **Compare like with like.** Name both groups, use the same variable and units, and use common scales. For unequal sample sizes, use relative frequencies when comparing proportions.
- **Describe more than the average.** Compare center, spread, shape and unusual features. Name the statistic or graphical feature supporting each claim.
- **Choose a graph for the feature.** Dotplots and histograms reveal gaps and peaks; boxplots summarize quartiles, median and spread. A boxplot alone does not establish normality or the number of modes.
- **Interpret z-scores in their reference groups.** Use a positive standard deviation and explain the sign and magnitude. Standardized distance is not a percentile, and standardization does not create normality.
- **Match conclusions to the evidence.** Descriptive displays show sample patterns; population and causal conclusions depend on study design.

## Practice {#practice-19}

Try each question before opening its solution.

::: {.original-practice-host data-original-practice="1.9"}
:::

::: {.lesson-sources}
<details><summary>Sources</summary>

[College Board course framework](https://apcentral.collegeboard.org/media/pdf/ap-statistics-course-and-exam-description-effective-fall-2026.pdf), Topic 1.9. [2026 scoring guidelines, Question 1](https://apcentral.collegeboard.org/media/pdf/ap26-sg-statistics.pdf). The route and assessment datasets are course examples.

</details>
:::
''')
p=R/'Unit 1/Topic 1.6/_worked-examples.qmd';s=p.read_text();s=re.sub(r'The revised lecture uses .*?College Board graphic\.','**2023 AP Statistics, Question 1(a).**\n\n{{< include _oxygen-question.qmd >}}\n\n### Worked solution',s);s=re.sub(r'The lecture identifies these numerical data.*?past-exam-questions\)\.','**2022 AP Statistics: chocolate study.**\n\n{{< include _chocolate-question.qmd >}}',s);s=s.replace('These classroom follow-ups use our left-inclusive, right-exclusive convention; they are not additional parts of the original exam.','Use left-inclusive, right-exclusive intervals for this calculation.').replace('Each new statement begins with no answer selected.','Explain which part of the graph supports your answer.').replace('Our task here is data recovery, not a causal conclusion about the treatments.','Each dot contributes one observation, including repeated values.');p.write_text(s)
# Simplify private-reader presentation without altering its input validation or storage boundary.
p=R/'Problem Bank/assets/practice.js';s=p.read_text();s=re.sub(r'    const descriptor = .*?\n','',s);s=s.replace('article.append(h, descriptor, source);','article.append(h, source);').replace(' ID: ${meta.id}.','');s=re.sub(r'    for \(const note of item.editorial_notes\).*?\n','',s);s=s.replace(", el('p', 'bank-source', 'Explanation independently derived for this study set; not an official College Board answer key.')",'');s=re.sub(r"const privacy = el\('p', 'bank-privacy', .*?\);", "const privacy = el('p', 'bank-privacy', 'Open mhs-week-2-3.practice.json provided by your teacher. Use Forget class file to clear it from this tab.');",s);p.write_text(s)
p=R/'Problem Bank/practice-filter.lua';s=p.read_text();s=re.sub(r"table.insert\(html, '<p>.*?</p><ul>'\)","table.insert(html, '<p>Open your class question file to practise the selected homework questions below.</p><ul>')",s);s=s.replace("  doc.blocks:insert(pandoc.Header(2,", "  local sources={}\n  for i=#doc.blocks,1,-1 do\n    local b=doc.blocks[i]\n    if b.t=='Div' and b.classes:includes('lesson-sources') then table.insert(sources,1,table.remove(doc.blocks,i)) end\n  end\n  doc.blocks:insert(pandoc.Header(2,",1)
s=re.sub(r"doc.blocks:insert\(pandoc.Para\('These questions.*?'\)\)","doc.blocks:insert(pandoc.Para('Open your class question file to work through the selected homework questions.'))",s)
s=s.replace('  return doc\nend','  for _,b in ipairs(sources) do doc.blocks:insert(b) end\n  return doc\nend');p.write_text(s)
p=R/'index.qmd';s=p.read_text().replace('Topics 1.1–1.6 available','Explore available topics');s=s.split('The activities run in your browser')[0]+'[Sources and study resources](resources.qmd)\n';p.write_text(s)
for p in (R/'Unit 1').rglob('*.qmd'):
 s=p.read_text();s=re.sub(r'::: \{\.chapter-lead\}\s*:::\s*','',s);p.write_text('\n'.join(x.rstrip() for x in s.splitlines())+'\n')
