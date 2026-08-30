# Lyra Forge — agent plugins

A marketplace for [Claude Code](https://code.claude.com) and Codex. Add it once,
then install a compatible plugin from inside your harness or its CLI.

## Install in Claude Code

```
/plugin marketplace add lyra-forge/marketplace
/plugin install spindle@lyra-forge
/plugin install flip@lyra-forge
/plugin install vizier@lyra-forge
/plugin install ergo@lyra-forge
/plugin install claude-bingo@lyra-forge
/plugin install yoinker@lyra-forge
```

Install only the plugins you want, then start a new session. Bundled skills use
`/plugin:skill` names: for example, `/spindle:spindle`,
`/flip:notebook-create`, `/vizier:chart-design`, `/ergo:ergo`, and
`/claude-bingo:bingo`. Yoinker is `/yoinker:yoinker`. Once Spindle sets up its
project-local operator, a subsequent session can use the shorter `/spindle`.

## Install in Codex

```bash
codex plugin marketplace add lyra-forge/marketplace
codex plugin add spindle@lyra-forge
codex plugin add flip@lyra-forge
codex plugin add vizier@lyra-forge
codex plugin add ergo@lyra-forge
codex plugin add claude-bingo@lyra-forge
codex plugin add yoinker@lyra-forge
```

Install only the plugins you want, then start a new Codex session. Bundled
skills use `$plugin:skill` names: for example, `$spindle:spindle`,
`$flip:notebook-create`, `$vizier:chart-design`, `$ergo:ergo`, and
`$claude-bingo:bingo`. Yoinker is `$yoinker:yoinker`. Once Spindle sets up its
project-local operator, a subsequent session can use the shorter `$spindle`.

## Update an installed plugin

Refresh the marketplace, update or reinstall the selected plugin, and start a
new session so the harness loads the new components:

```text
# Claude Code
/plugin marketplace update lyra-forge
/plugin update vizier@lyra-forge

# Codex
codex plugin marketplace upgrade lyra-forge
codex plugin add vizier@lyra-forge
```

Codex currently uses `plugin add` for both initial installation and reinstall;
it has no separate `plugin update` command.

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

### [spindle](https://github.com/lavallee/spindle)

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

### [flip](https://github.com/lavallee/flip)

```text
# Claude Code
/plugin install flip@lyra-forge

# Codex
codex plugin add flip@lyra-forge
```

Custody, grading, and corroboration discipline for agent research. You direct
the work in conversation; flip keeps the durable, auditable notebook — sources
captured to local bytes and hashed, sources graded, claims gated by a
corroboration bar, every session logged. Seven skills cover the notebook
lifecycle: create, source capture, session hygiene, claim audit, handoff,
lessons, and kind authoring.

Both harnesses install the same seven skills. Claude Code also runs Flip's
custody hook around web fetches; Codex's hosted web tools do not expose those
tool-hook events, so the skills carry the capture-before-cite discipline there.

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

### [vizier](https://github.com/lavallee/vizier)

```text
# Claude Code
/plugin install vizier@lyra-forge

# Codex
codex plugin add vizier@lyra-forge
```

Chart judgment for agents. Most bad charts are a defensible-looking answer to
a question nobody asked — decided before the first line of plotting code runs.
vizier moves that decision onto a documented library: two skills that pick the
chart form from the reader's question, run the honesty checks a graphics desk
would apply (fair comparison, denominator, counter-reading), and critique a
finished chart against 43 documented forms and a corpus of critical writing.

The plugin bundles vizier's MCP server, so the same answers are available as
tools. It runs the `vizier` CLI, which installs separately — the PyPI package
is `datavizier`:

```bash
uv tool install datavizier      # or: pip install datavizier
```

The core needs no keys and no network: form recommendation, the journalism
checks, the pattern library, structural analysis of a rendered chart, and
colorblind-safe palettes all work offline. Corpus-backed LLM critique is an
opt-in extra. If `uvx` is on PATH, the MCP server runs without the separate
install; `vizier doctor` reports what's live.

### [ergo](https://github.com/lavallee/ergo)

```text
# Claude Code
/plugin install ergo@lyra-forge

# Codex
codex plugin add ergo@lyra-forge
```

Dataset pitfalls, written down. Every dataset has quirks, mislabelings and
decisions that will bite you, and publishers usually document them — somewhere
the download never points to. ergo teaches your agent to go looking before it
touches the data, to record what it learns as a checkable page, and to offer
the public-safe part back so the next person does not pay for the same lesson.

One skill covers two roles. It works with data pages — reading known issues
before writing a loader, honouring the ones that constrain what may honestly be
said, and registering new ones at discovery — and recovers a page from code
that already parses the data, starting with tests, fixtures, and NEWS files
before reaching for the parser.

A data page is one markdown file per dataset carrying TOML blocks: a manifest,
a registry of issues each scoped to the years and columns it touches, the
practices that say what may be computed, and the publisher's own words quoted
with a date. Plain files, no services.

The skills drive the `ergo` validator, which is a single dependency-free file
you copy into your repository rather than install:

```bash
curl -sSLo tools/ergo.py https://raw.githubusercontent.com/lavallee/ergo/main/tools/ergo.py
```

[The background](https://lavallee.github.io/ergo/review/) — what the benchmark
record shows about models doing data work, and why this is worth writing down.

### [claude-bingo](https://github.com/lavallee/claude-bingo)

```text
# Claude Code
/plugin install claude-bingo@lyra-forge

# Codex
codex plugin add claude-bingo@lyra-forge
```

A bingo board of LLM verbal tics, scored against your own Claude Code
transcripts. A toy — and our canary for marketplace plumbing: if this one
installs clean on a fresh machine in either harness, the install path is
healthy. From Codex it still reads the local Claude Code transcript history.

### [yoinker](https://github.com/lavallee/yoinker)

```text
# Claude Code
/plugin install yoinker@lyra-forge

# Codex
codex plugin add yoinker@lyra-forge
```

Understand how it works. Yoink what transfers. Give your agent a repository,
paper, product, technique, or open question. Yoinker follows discovery links
to original artifacts, separates observation from claims and inference, checks
the mechanism against the situation you actually have, and returns a decision
per mechanism: borrow, try, track, or reject.

One skill, no service, no package dependency, and no automatic implementation.
A recommendation remains evidence-linked advice rather than permission to
install, merge, publish, or change production.

## Adding a plugin to this marketplace

Each entry in [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)
points at a Claude Code plugin repository. Codex-compatible entries also need an
entry in [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json).
The two catalogs expose the same plugin set. Do not list a plugin in both
unless the source repository ships and tests both manifests.

The source repository owns the plugin. Before adding it here, it must contain:

- `.claude-plugin/plugin.json` for Claude Code;
- `.codex-plugin/plugin.json` for Codex;
- the shared `skills/` tree and any declared `.mcp.json`, hooks, scripts, or
  assets;
- tests that keep both manifest versions aligned and exercise any bundled
  launcher or MCP server.

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

To list the same plugin in Codex, add the corresponding entry to
`.agents/plugins/marketplace.json` using the same remote source and selector:

```json
{
  "name": "your-plugin",
  "source": {
    "source": "url",
    "url": "https://github.com/owner/your-plugin.git"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Productivity"
}
```

Keep the Claude and Codex manifest versions equal. Omit a duplicate marketplace
version — numbers in three places drift, and the source manifest is what an
install actually resolves. Pin released remote sources with a full `sha` when
an install should resolve to the exact bytes that were validated.

Pinning is per plugin, not a house rule. Unless a documented compatibility
reason requires otherwise, pin both catalogs to the same commit or leave both
tracking upstream. A pin must point at a commit containing the manifest for the
harness that will install it; a release cut before `.codex-plugin/plugin.json`
existed is not a Codex release.

During a first Codex migration, the local Codex entry may temporarily remain
unpinned because no published commit contains its manifest yet. Do not publish
that intermediate catalog. Publish the source repository, then align both
catalog selectors to the intended dual-harness release before publishing this
repository.

Always use the `url` source with a full `https://…git` URL — **not** the
`github`/`owner-repo` shorthand. The shorthand clones over SSH in Claude Code
and breaks installs for anyone without a GitHub SSH key; the `url` source
clones the literal HTTPS URL for everyone.

Publish the source repository before the marketplace commit. A local manifest
passing validation is not enough: the remote branch or pinned commit must
already contain every file the catalog declares. Then validate the catalogs:

```bash
claude plugin validate . --strict
python3 -m unittest discover tests
```

For Codex, test a temporary copy of the marketplace with a unique top-level
`name`: add it with `codex plugin marketplace add <temporary-root>`, confirm the
entry with `codex plugin list`, install it with
`codex plugin add <plugin>@<temporary-name>`, and start a new session. Remove
the temporary install and marketplace afterward.

A Codex entry must include installation and authentication policy plus a
category. If the plugin bundles an MCP server, declare the root `.mcp.json`
through `mcpServers`; if it uses `hooks/hooks.json`, test the hook separately
because Codex and Claude Code do not expose identical tool events. Report
catalog discovery, installation, component activation, and a live model session
as separate checks rather than treating one as proof of all four.
