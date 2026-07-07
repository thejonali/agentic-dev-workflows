# Installation

Agentic Developer Workflows can be used from a source checkout or from the
versioned archives attached to a GitHub release. Install only the workflows and
agent roles that a target repository needs.

## Release Artifacts

The v0.1.0 release preparation command creates these files under `dist/`:

| Artifact | Contents | Use When |
| --- | --- | --- |
| `agentic-dev-workflows-v0.1.0.zip` | Complete core, providers, examples, MCP server, scripts, tests, and documentation | You need the canonical library, generation tools, or MCP server |
| `agentic-dev-workflows-codex-v0.1.0.zip` | Ready-to-copy `.agents/`, `.codex/`, and optional legacy prompts | Installing Codex project assets |
| `agentic-dev-workflows-claude-v0.1.0.zip` | Ready-to-copy `.claude/` skills, agents, and commands | Installing Claude Code project assets |
| `agentic-dev-workflows-cursor-v0.1.0.zip` | Ready-to-copy `.cursor/` rules and commands | Installing Cursor project assets |
| `SHA256SUMS-v0.1.0.txt` | SHA-256 digests for every ZIP | Verifying downloaded artifacts |

Verify downloads before extracting them:

```sh
shasum -a 256 -c SHA256SUMS-v0.1.0.txt
```

On systems that provide GNU coreutils, use `sha256sum -c` instead.

## Codex

Extract `agentic-dev-workflows-codex-v0.1.0.zip`, then copy the project assets
you need:

```sh
TARGET_REPO=/absolute/path/to/repository
cp -R agentic-dev-workflows-codex-v0.1.0/.agents "$TARGET_REPO/"
cp -R agentic-dev-workflows-codex-v0.1.0/.codex "$TARGET_REPO/"
```

The `legacy-prompts/` directory is optional and user-scoped. Read the packaged
`INSTALL.md` before copying those compatibility commands.

## Claude Code

Extract `agentic-dev-workflows-claude-v0.1.0.zip`, then copy `.claude/` into the
target repository:

```sh
TARGET_REPO=/absolute/path/to/repository
cp -R agentic-dev-workflows-claude-v0.1.0/.claude "$TARGET_REPO/"
```

Do not install both a skill and compatibility command with the same name.

## Cursor

Extract `agentic-dev-workflows-cursor-v0.1.0.zip`, then copy `.cursor/` into the
target repository:

```sh
TARGET_REPO=/absolute/path/to/repository
cp -R agentic-dev-workflows-cursor-v0.1.0/.cursor "$TARGET_REPO/"
```

Cursor rules remain agent-requested rather than always-on. Custom commands are
a provider beta surface and may change upstream.

## MCP Workflow Server

The MCP server is included in the complete library archive and currently is not
published to PyPI. From the extracted complete archive:

```sh
cd agentic-dev-workflows-v0.1.0
python3 -m venv .venv
.venv/bin/python -m pip install -e mcp/workflow-server
.venv/bin/workflow-library-mcp
```

The final command starts a stdio server and waits for an MCP client. See the
[MCP server guide](../mcp/workflow-server/README.md) for client configuration,
tools, and permission boundaries.

## Install from a Source Checkout

Clone the repository when you need to modify canonical workflows, regenerate
provider assets, or run the validation suite:

```sh
git clone https://github.com/thejonali/agentic-dev-workflows.git
cd agentic-dev-workflows
python3 -B scripts/generate_provider_assets.py --check
```

For provider-specific selection and verification, use the [Codex](../providers/codex/install.md),
[Claude Code](../providers/claude/install.md), or
[Cursor](../providers/cursor/install.md) installation guide.

## Safety and Updates

- Review destination files before copying and do not overwrite an existing
  asset without comparing behavior.
- Installing an adapter does not authorize repository writes, publication,
  deployment, secret access, or subagent use.
- Pin automation to a versioned release instead of downloading the default
  branch.
- Read the [changelog](../CHANGELOG.md) and release notes before upgrading.
