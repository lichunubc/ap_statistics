-- Compile curated question Markdown once; share rendered math across all views.
local function escape(s)
 return tostring(s):gsub('&','&amp;'):gsub('<','&lt;'):gsub('>','&gt;'):gsub('"','&quot;')
end
local function rich(s)
 local doc=pandoc.read(s or '', 'markdown+tex_math_dollars-raw_html-raw_tex')
 return pandoc.write(doc,'html5',{html_math_method='mathml'})
end
function Div(div)
 if not div.classes:includes('original-practice-host') then return nil end
 local topic=div.attributes['data-original-practice']
 if not topic or not topic:match('^%d+%.%d+$') then return nil end
 local slug=topic:gsub('%.','-');local unit=topic:match('^(%d+)')
 local path=quarto.project.directory..'/Problem Bank/original/unit-'..unit..'/topic-'..slug..'.json'
 local file=assert(io.open(path,'r'),'Missing original practice: '..path)
 local bank=pandoc.json.decode(file:read('*a'));file:close()
 local out={'<section class="original-practice" data-original-practice="'..escape(topic)..'" data-bank-url="../../Problem%20Bank/original/unit-'..unit..'/topic-'..slug..'.json">'}
 table.insert(out,'<p class="original-loading">Loading practice…</p>')
 table.insert(out,'<template data-practice-rich data-bank-revision="'..escape(bank.revision or 1)..'">')
 for _,q in ipairs(bank.items or {}) do
  table.insert(out,'<article data-practice-id="'..escape(q.id)..'">')
  for _,field in ipairs({'prompt','hint','solution','rubric'}) do table.insert(out,'<div data-field="'..field..'">'..rich(q[field])..'</div>') end
  for _,o in ipairs(q.options or {}) do table.insert(out,'<div data-field="option-'..escape(o.label)..'">'..rich(o.text)..'</div>') end
  table.insert(out,'</article>')
 end
 table.insert(out,'</template><noscript><div class="original-nojs"><ol>')
 for i,q in ipairs(bank.items or {}) do
  table.insert(out,'<li><strong>Question '..i..'</strong>'..rich(q.prompt))
  for _,o in ipairs(q.options or {}) do table.insert(out,'<div><strong>'..escape(o.label)..'.</strong> '..rich(o.text)..'</div>') end
  table.insert(out,'<details><summary>Show solution</summary>'..rich(q.solution))
  if q.rubric then table.insert(out,rich(q.rubric)) end
  table.insert(out,'</details></li>')
 end
 table.insert(out,'</ol></div></noscript></section>')
 return pandoc.RawBlock('html',table.concat(out,'\n'))
end
