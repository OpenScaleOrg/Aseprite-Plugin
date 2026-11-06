-- Aseprite MCP Live: connects to the aseprite-mcp server and runs the Lua
-- scripts it sends on the sprites open in this window, so every tool call
-- shows up live.
--
-- Request:  "<id>\n<filename>\n<lua script>"
-- Reply:    "<id>\n<1|0>\n<printed output or error>"
-- Hello:    "hello\n1\n<path of this Aseprite executable>"  (on connect)

local URL = "ws://127.0.0.1:45654"
local ws
local last_restart = 0

local function norm(path)
  return (path:gsub("/", "\\"):lower())
end

local function is_file(path)
  return path ~= "" and app.fs.isFile(path)
end

-- The open tab for `filename`, opening the file if it exists on disk.
-- An empty filename means the active tab.
local function sprite_for(filename)
  if filename == "" then return app.activeSprite end
  for _, spr in ipairs(app.sprites) do
    if norm(spr.filename) == norm(filename) then return spr end
  end
  if is_file(filename) then return app.open(filename) end
  return nil
end

-- Batch scripts make throwaway clones (Sprite(spr)) and never close them,
-- since the process exits. Here they would pile up as tabs: close every
-- sprite the script created unless it is a real new file on disk.
local function close_temporaries(before)
  local names = {}
  for _, s in ipairs(before) do names[norm(s.filename)] = true end
  local created = {}
  for _, s in ipairs(app.sprites) do
    local existed = false
    for _, b in ipairs(before) do if s == b then existed = true break end end
    if not existed then created[#created + 1] = s end
  end
  for _, s in ipairs(created) do
    if names[norm(s.filename)] or not is_file(s.filename) then s:close() end
  end
end

local function run(filename, script)
  local out = {}
  local env = setmetatable({
    print = function(...)
      local parts = {}
      for i = 1, select("#", ...) do parts[#parts + 1] = tostring((select(i, ...))) end
      out[#out + 1] = table.concat(parts, "\t")
    end,
  }, { __index = _G })

  local fn, err = load(script, "=mcp", "t", env)
  if not fn then return false, err end

  local spr = sprite_for(filename)
  if spr then app.activeSprite = spr end
  local before = {}
  for _, s in ipairs(app.sprites) do before[#before + 1] = s end

  local ok
  -- One transaction per tool call: Ctrl+Z undoes one Claude step.
  if app.activeSprite then
    app.transaction(function() ok, err = pcall(fn) end)
  else
    ok, err = pcall(fn)
  end

  pcall(close_temporaries, before)
  if spr then pcall(function() app.activeSprite = spr end) end
  app.refresh()

  if not ok then return false, tostring(err) end
  return true, table.concat(out, "\n")
end

local function handle(data)
  local id, filename, script = data:match("^(.-)\n(.-)\n(.*)$")
  if not id then return end
  local pok, ok, result = pcall(run, filename, script)
  if not pok then ok, result = false, ok end
  -- Fails when the server went away mid-request; it timed out on its side anyway.
  pcall(ws.sendText, ws, id .. "\n" .. (ok and "1" or "0") .. "\n" .. tostring(result or ""))
end

-- The built-in auto-reconnect can stall after the server dies mid-request,
-- so restart the socket ourselves on close/error, at most every 3 seconds.
-- ponytail: older Aseprite builds have no Timer, so recovery rides on the socket's own events.
local function restart()
  if os.clock() - last_restart < 3 then return end
  last_restart = os.clock()
  ws:close()
  ws:connect()
end

function init(plugin)
  ws = WebSocket{
    url = URL,
    deflate = false,
    minreconnectwait = 1,
    maxreconnectwait = 5,
    onreceive = function(kind, data)
      -- An uncaught error here would stop the socket, so keep everything contained.
      if kind == WebSocketMessageType.TEXT then
        pcall(handle, data)
      elseif kind == WebSocketMessageType.OPEN then
        pcall(ws.sendText, ws, "hello\n1\n" .. app.fs.appPath)
      elseif kind == WebSocketMessageType.CLOSE or kind == WebSocketMessageType.ERROR then
        pcall(restart)
      end
    end,
  }
  ws:connect()
end

function exit(plugin)
  if ws then ws:close() end
end
