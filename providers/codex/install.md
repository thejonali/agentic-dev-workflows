# Install the Codex Adapter

The Codex adapter packages the canonical `core/` contracts as project skills,
project-scoped custom agents, and optional legacy custom prompts.

## Requirements

- A current Codex CLI, IDE extension, or Codex app installation.
- A target repository where you may add `.agents/` and `.codex/` files.
- A checkout of this workflow repository when installing by copy.

## Supported Assets

- `skills/*/SKILL.md`: the supported shared workflow interface.
- `agents/*.toml`: optional custom agents for explicitly requested subagent work.
- `commands/*.md`: deprecated custom-prompt compatibility assets.

Every generated asset names its canonical source under `core/`. Changes to
canonical behavior must be applied to `core/` first and rendered with
`scripts/generate_provider_assets.py`; direct edits will fail the drift check.

## Install Skills in a Repository

From this repository root, copy the desired skill directories into the target
repository:

```sh
TARGET_REPO=/absolute/path/to/repository
mkdir -p "$TARGET_REPO/.agents/skills"
cp -R providers/codex/skills/safe-change "$TARGET_REPO/.agents/skills/"
```

The result should be:

```text
<target-repository>/
  .agents/
    skills/
      safe-change/
        SKILL.md
```

Codex discovers repository skills from `.agents/skills/` between the current
working directory and repository root. Install only the workflows the target
repository needs to keep skill selection focused.

## Install Custom Agents in a Repository

Copy only the agents the target repository needs:

```sh
TARGET_REPO=/absolute/path/to/repository
mkdir -p "$TARGET_REPO/.codex/agents"
cp providers/codex/agents/reviewer.toml "$TARGET_REPO/.codex/agents/"
```

The destination is:

```text
<target-repository>/.codex/agents/
```

The TOML `name` field identifies the agent. Codex only spawns subagents when
the user explicitly requests subagents or parallel agent work. Agent files
inherit the parent session's model, tools, sandbox, and other settings because
these adapters intentionally avoid stale provider defaults.

## Install Legacy Commands for One User

Codex custom prompts are deprecated and are loaded from the user's Codex home,
not from a repository. If compatibility is required, copy individual Markdown
files after confirming the destination name is unused:

```sh
CODEX_HOME=${CODEX_HOME:-"$HOME/.codex"}
mkdir -p "$CODEX_HOME/prompts"
cp providers/codex/commands/release-check.md "$CODEX_HOME/prompts/"
```

The destination is:

```text
~/.codex/prompts/
```

After restarting Codex, invoke a copied prompt as
`/prompts:<command-name>`. Prefer invoking a skill with
`$<skill-name>` for reusable shared workflows.

Review destination files before copying. Do not overwrite an existing skill,
agent, or prompt with the same name without comparing its behavior.

## Verify

1. Start Codex in the target repository.
2. Confirm installed skills appear in the skill selector.
3. If agents were installed, explicitly ask Codex to delegate a narrow task to
   one named custom agent and inspect its returned scope.
4. If legacy prompts were installed, restart Codex and confirm the
   `/prompts:` entry appears.
5. Verify a dry-run or read-only invocation before using a workflow that writes.

## Limitations

- Generation also targets Claude Code and Cursor; this guide covers only Codex
  packaging and installation.
- Skill selection descriptions remain provider metadata in
  `providers/codex/generator.json` and must be added for each new workflow.
- Codex custom prompts are deprecated and user-local, so `commands/` is a
  compatibility surface rather than the primary shared interface.
- Custom-agent authoring may evolve; these files use the currently documented
  standalone TOML fields only.
- Installing these assets does not grant permission to write, publish, deploy,
  access secrets, or spawn subagents.
