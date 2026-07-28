# Lyra Forge — Claude Code plugins

A marketplace of [Claude Code](https://code.claude.com) plugins. Add it once,
then install anything from it.

## Install

```
/plugin marketplace add lyra-forge/marketplace
/plugin install claude-bingo@lyra-forge
```

That's it — no SSH key, no environment variables, no git config. Plugins here
are sourced over plain HTTPS, so `/plugin install` works on any machine with
network access.

> **Why this matters.** Claude Code clones a `github` shorthand plugin source
> (`owner/repo`) over **SSH** by default, which fails with
> `git@github.com: Permission denied (publickey)` for anyone without a GitHub
> SSH key on that machine. Every plugin in this marketplace uses the `url`
> source type with an explicit `https://…` URL instead, which Claude Code
> clones verbatim over HTTPS. Nothing to configure on your end.
>
> (If you install a plugin elsewhere that still uses the `github` shorthand and
> hit that SSH error, the client-side escape hatch is
> `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` in `~/.claude/settings.json`.)

## Plugins

| Plugin | What it does |
|--------|--------------|
| [claude-bingo](https://github.com/lavallee/claude-bingo) | A bingo board of LLM verbal tics, scored against your own Claude Code transcripts. |
| [flip-notebook](https://github.com/lavallee/flip) | Custody, grading, and corroboration discipline for agent research — you direct the work, flip keeps the durable, auditable notebook. |

## Adding a plugin to this marketplace

Each entry in [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)
points at a plugin's own repository. To list a new one, add a `plugins[]` entry:

```json
{
  "name": "your-plugin",
  "displayName": "Your Plugin",
  "description": "One line on what it does.",
  "source": { "source": "url", "url": "https://github.com/owner/your-plugin.git" },
  "version": "0.1.0",
  "license": "MIT",
  "category": "fun"
}
```

Always use the `url` source with a full `https://…git` URL — **not** the
`github`/`owner-repo` shorthand. The shorthand clones over SSH and breaks
installs for anyone without a GitHub SSH key; the `url` source clones the
literal HTTPS URL for everyone. Validate before committing:

```bash
claude plugin validate . --strict
```
