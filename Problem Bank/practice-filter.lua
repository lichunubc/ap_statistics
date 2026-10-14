-- Attach source-referenced practice without duplicating questions in lesson QMDs.
local catalog = nil
local function load_catalog()
  if not catalog then
    local file = assert(io.open(quarto.project.directory .. '/Problem Bank/catalog.json', 'r'))
    catalog = pandoc.json.decode(file:read('*a')); file:close()
  end
  return catalog
end
local function escape(s)
  return tostring(s):gsub('&','&amp;'):gsub('<','&lt;'):gsub('>','&gt;'):gsub('"','&quot;')
end
local function mount(topic)
  local html = {'<div class="homework-bank" data-topic="' .. escape(topic) .. '"><div class="bank-fallback">'}
  table.insert(html, '<p>Selected homework references are listed below. Enable JavaScript and open the class question file to display the questions locally; no question file is uploaded.</p><ul>')
  for _, item in ipairs(load_catalog().items) do
    if topic == 'all' or topic == item.topic then
      table.insert(html, '<li>Week ' .. item.source_week .. ', Question ' .. item.source_question .. ' — Topic ' .. escape(item.topic) .. ': ' .. escape(item.title) .. ' (homework pages ' .. table.concat(item.source_pages, ', ') .. ').</li>')
    end
  end
  table.insert(html, '</ul></div></div>')
  return pandoc.RawBlock('html', table.concat(html, '\n'))
end
function Div(div)
  if quarto.doc.is_format('html:js') and div.classes:includes('homework-bank-host') then
    return mount(div.attributes['data-topic'] or 'all')
  end
end
function Pandoc(doc)
  if not quarto.doc.is_format('html:js') then return doc end
  local number = quarto.doc.input_file:match('topic%-1%-(%d+)%.qmd$')
  if not number then return doc end
  local topic = '1.' .. number
  if not load_catalog().topics[topic] then return doc end
  doc.blocks:insert(pandoc.Header(2, 'Selected homework practice', pandoc.Attr('homework-practice')))
  if topic == '1.1' then
    doc.blocks:insert(pandoc.Para('The supplied Week 2 and Week 3 homework sets do not provide a direct practice selection for this introductory topic. Use the existing original practice above; no homework question has been relabelled as a Topic 1.1 question.'))
  else
    doc.blocks:insert(pandoc.Para('These questions were selected from the assigned homework for their topic fit and complementary skills. Original wording, choices, and diagrams are retained in the locally opened class file. Explanations are independently derived, not an official answer key.'))
    doc.blocks:insert(mount(topic))
  end
  doc.blocks:insert(pandoc.Para({pandoc.Link('Browse the selected homework problem bank', '../../Problem%20Bank/practice.html')}))
  return doc
end
