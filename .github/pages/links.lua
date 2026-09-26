-- Pandoc filter used by the Pages build: README links point at .md/.adoc
-- sources (which GitHub renders); on the published site they should open
-- the generated .html sibling when one exists.
local function exists(path)
  local f = io.open(path, "r")
  if f then f:close() return true end
  return false
end

function Link(el)
  local target = el.target
  if target:match("^%a[%w+.-]*:") or target:match("^#") then
    return el -- absolute URL or in-page anchor
  end
  local path, frag = target:match("^([^#]*)(#?.*)$")
  local stem = path:match("^(.*)%.md$") or path:match("^(.*)%.adoc$")
  if stem and exists(stem .. ".html") then
    el.target = stem .. ".html" .. frag
  elseif path:match("README%.md$") then
    el.target = path:gsub("README%.md$", "index.html") .. frag
  end
  return el
end
