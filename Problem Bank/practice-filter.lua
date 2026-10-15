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
  table.insert(html, '<p>Open your class question file to practise the selected homework questions below.</p><ul>')
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
  local sources={}
  for i=#doc.blocks,1,-1 do
    local b=doc.blocks[i]
    if b.t=='Div' and b.classes:includes('lesson-sources') then table.insert(sources,1,table.remove(doc.blocks,i)) end
  end
  doc.blocks:insert(pandoc.Header(2, 'Selected homework practice', pandoc.Attr('homework-practice')))
  if topic == '1.1' then
    doc.blocks:insert(pandoc.Para('Use the Practice section above to review this topic.'))
  else
    doc.blocks:insert(pandoc.Para('Open your class question file to work through the selected homework questions.'))
    doc.blocks:insert(mount(topic))
  end
  doc.blocks:insert(pandoc.Para({pandoc.Link('Browse the selected homework problem bank', '../../Problem%20Bank/practice.html')}))
  for _,b in ipairs(sources) do doc.blocks:insert(b) end
  return doc
end
