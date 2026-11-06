# Contributing

Thanks for helping. Bug reports, example scenes, skills and tool fixes are all welcome.

## Layout

```
.claude-plugin/marketplace.json        marketplace catalog
plugins/aseprite/
  .claude-plugin/plugin.json           plugin manifest (bump "version" on every release)
  .mcp.json                            starts the server
  commands/                            /pixel-* slash commands (Markdown prompts)
  skills/<name>/SKILL.md               skills, plus optional reference files next to them
  server/aseprite_mcp/                 Python MCP server
    core/live.py                       WebSocket bridge to the running Aseprite
    extension/                         Aseprite extension (Lua), installed by the server
    tools/                             one module per tool group
```

## Try your changes locally

```
/plugin marketplace add ./path/to/your/clone
/plugin install aseprite@openscale
```

Start a new Claude session after each change: a running session keeps its old server. After changing `server/aseprite_mcp/extension/`, restart Aseprite as well, so it loads the new extension.

Check that the manifests are valid:

```bash
claude plugin validate .
```

```bash
claude plugin validate plugins/aseprite
```

Check that the server still loads every tool:

```bash
cd plugins/aseprite/server && uv run python -c "import asyncio; from aseprite_mcp import mcp; import aseprite_mcp.tools; print(len(asyncio.run(mcp.list_tools())))"
```

## Guidelines

- **Live mode first.** Tools must work both in the open window and in batch mode. Don't open, close or create sprites unless that is the tool's purpose. The extension closes any temporary sprites a script creates.
- **Small steps.** One tool call should change one visible thing.
- **Skills stay short and practical.** Put long tables and pattern libraries in a reference file next to `SKILL.md`, and link to it.
- **Changelog.** Add an entry to `CHANGELOG.md` and bump the version in `plugin.json`.
