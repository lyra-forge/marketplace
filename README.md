# Lyra Forge — Claude Code plugins

A marketplace of [Claude Code](https://code.claude.com) plugins. Add it once,
then install anything from it.

```
/plugin marketplace add lyra-forge/marketplace
/plugin install claude-bingo@lyra-forge
```

## Plugins

| Plugin | What it does |
|--------|--------------|
| [claude-bingo](https://github.com/lavallee/claude-bingo) | A bingo board of LLM verbal tics, scored against your own Claude Code transcripts. |

## Adding a plugin to this marketplace

Each entry in [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)
points at a plugin's own repository. To list a new one, add a `plugins[]` entry:

```json
{
  "name": "your-plugin",
  "displayName": "Your Plugin",
  "description": "One line on what it does.",
  "source": { "source": "git", "url": "https://github.com/owner/your-plugin.git" },
  "version": "0.1.0",
  "license": "MIT",
  "category": "fun"
}
```

Use an explicit `https` git URL rather than the `github` shorthand — the
shorthand clones over SSH, which fails for anyone without a GitHub SSH key on
their machine.
