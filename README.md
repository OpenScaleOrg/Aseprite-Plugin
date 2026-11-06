# OpenScale Claude Code plugins

A [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugins). Add it once, then install plugins from it by name.

```
/plugin marketplace add OpenScaleOrg/Aseprite-Plugin
/plugin install aseprite@openscale
```

## Plugins

| Plugin | What it does |
|---|---|
| [aseprite](plugins/aseprite) | Claude draws and animates pixel art in Aseprite, live in the window you have open. 125 MCP tools, 5 skills, 5 slash commands. |

![A looping farm scene drawn by Claude](plugins/aseprite/examples/farm.gif)

## Layout

```
.claude-plugin/marketplace.json   the catalog: lists every plugin and where it lives
plugins/<name>/                   one folder per plugin, each with .claude-plugin/plugin.json
```

To add a plugin, put it in `plugins/<name>/` and add an entry to `marketplace.json`.
