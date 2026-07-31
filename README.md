# Lyra Forge — Claude Code plugins

A marketplace of [Claude Code](https://code.claude.com) plugins. Add it once,
then install anything from it.

## Install

```
/plugin marketplace add lyra-forge/marketplace
/plugin install flip@lyra-forge
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

### [flip](https://github.com/lavallee/flip) — 0.16.1

Custody, grading, and corroboration discipline for agent research. You direct
the work in conversation; flip keeps the durable, auditable notebook — sources
captured to local bytes and hashed, sources graded, claims gated by a
corroboration bar, every session logged. Seven skills cover the notebook
lifecycle: create, source capture, session hygiene, claim audit, handoff,
lessons, and kind authoring.

A notebook is a plain directory of markdown pages with YAML frontmatter — an
[Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
bundle at rest, readable with `less`, diffable with `git`, editable as an
Obsidian vault. No services, no proprietary dependencies. A wiki tells an agent
what we know; a notebook can prove where it came from.

The skills drive the `flip` CLI, which installs separately — the PyPI package
is `flip-notebook`:

```bash
uv tool install flip-notebook      # or: pipx install flip-notebook
```

### [claude-bingo](https://github.com/lavallee/claude-bingo) — 0.1.0

```
/plugin install claude-bingo@lyra-forge
```

A bingo board of LLM verbal tics, scored against your own Claude Code
transcripts. A toy — and our canary for marketplace plumbing: if this one
installs clean on a fresh machine, the install path is healthy.

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
