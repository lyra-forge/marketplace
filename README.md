# Lyra Forge — agent plugins

A marketplace for [Claude Code](https://code.claude.com) and Codex. Add it once,
then install a compatible plugin from inside your harness or its CLI.

## Install in Claude Code

```
/plugin marketplace add lyra-forge/marketplace
/plugin install spindle@lyra-forge
```

Start a new session, then invoke the installed plugin as
`/spindle:spindle`. Once it sets up the project-local operator, a subsequent
session can use the shorter `/spindle`.

## Install in Codex

```bash
codex plugin marketplace add lyra-forge/marketplace
codex plugin add spindle@lyra-forge
```

Start a new Codex session, then invoke the installed plugin as
`$spindle:spindle`. Once it sets up the project-local operator, a subsequent
session can use the shorter `$spindle`.

The model is the same in both harnesses: add a catalog, install an entry, and
start a fresh session. The protocols are not identical. Claude Code reads
`.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`; Codex reads
`.agents/plugins/marketplace.json` and `.codex-plugin/plugin.json`. Their install,
update, namespacing, and policy surfaces should be documented and tested
independently.

No SSH key, environment variables, or git config are required. Plugins here
are sourced over plain HTTPS, so `/plugin install` works on any machine with
network access; the Codex catalog uses the same HTTPS source convention.

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

### [spindle](https://github.com/lavallee/spindle) — 0.2.0

```text
# Claude Code
/plugin install spindle@lyra-forge

# Codex
codex plugin add spindle@lyra-forge
```

An evidence-bearing lifecycle and control plane for agent skills. Inspect and
try exact bytes before adoption, borrow them temporarily, verify effective
harness state at startup, realize minimal instructions per agent, and keep the
receipts needed to update, distill, roll back, or retire safely.

The plugin contains a small operator plus a deterministic launcher for the exact
pinned Spindle source. It requires Python 3.11 or newer, but no separate Python
package installation.

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
points at a Claude Code plugin repository. Codex-compatible entries also need an
entry in [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json).
The two catalogs may expose different subsets; do not claim cross-harness support
unless the source repository ships and tests both manifests.

To list a Claude Code plugin, add a `plugins[]` entry:

```json
{
  "name": "your-plugin",
  "displayName": "Your Plugin",
  "description": "One line on what it does.",
  "source": { "source": "url", "url": "https://github.com/owner/your-plugin.git" },
  "license": "MIT",
  "category": "fun"
}
```

If the plugin manifest owns an explicit version, omit the duplicate marketplace
version. Pin released remote sources with a full `sha` so an install resolves to
the bytes that were validated.

Always use the `url` source with a full `https://…git` URL — **not** the
`github`/`owner-repo` shorthand. The shorthand clones over SSH and breaks
installs for anyone without a GitHub SSH key; the `url` source clones the
literal HTTPS URL for everyone. Validate before committing:

```bash
claude plugin validate . --strict
```

For Codex, add the marketplace locally, confirm the plugin is available, install
it, and test it in a new session. A Codex entry must include installation and
authentication policy plus a category; the plugin itself must contain
`.codex-plugin/plugin.json`.
