-- Progressive enhancement: original practice is one question at a time with JS,
-- but no-JS readers receive all original questions and answers from the SAME JSON.
local function escape(s)
  return tostring(s):gsub('&','&amp;'):gsub('<','&lt;'):gsub('>','&gt;'):gsub('"','&quot;')
end
function Div(div)
  if not div.classes:includes('original-practice-host') then return nil end
  local topic=div.attributes['data-original-practice']
  if not topic or not topic:match('^%d+%.%d+$') then return nil end
  local slug=topic:gsub('%.','-')
  local unit=topic:match('^(%d+)')
  local path=quarto.project.directory..'/Problem Bank/original/unit-'..unit..'/topic-'..slug..'.json'
  local file=io.open(path,'r')
  if not file then return nil end
  local bank=pandoc.json.decode(file:read('*a'));file:close()
  local blocks={'<section class="original-practice" data-original-practice="'..escape(topic)..'" data-bank-url="../../Problem%20Bank/original/unit-'..unit..'/topic-'..slug..'.json">'}
  table.insert(blocks,'<p>Loading the original practice questions. Enable JavaScript for the compact one-question-at-a-time reader.</p>')
  table.insert(blocks,'<noscript><div class="original-nojs"><p>JavaScript is disabled. These are the complete original questions with model solutions; all content comes from the same public JSON bank.</p><ol>')
  for _,q in ipairs(bank.items or {}) do
    table.insert(blocks,'<li><strong>'..escape(q.id)..'</strong><p>'..escape(q.prompt)..'</p>')
    if q.options then for _,o in ipairs(q.options) do
      table.insert(blocks,'<p>'..escape(o.label)..'. '..escape(o.text)..'</p>')
    end end
    table.insert(blocks,'<details><summary>Show solution</summary><p>'..escape(q.solution)..'</p></details></li>')
  end
  table.insert(blocks,'</ol></div></noscript></section>')
  return pandoc.RawBlock('html',table.concat(blocks,'\n'))
end
