# Install the Claude Code Adapter

The Claude Code adapter packages canonical workflows as project skills, core
agent roles as custom subagents, and core commands as compatibility slash
commands.

## Requirements

- A current Claude Code installation.
- A target repository where you may add `.claude/` files.
- A checkout of this workflow repository when installing by copy.

## Supported Assets

- `skills/*/SKILL.md`: reusable workflows discovered and invoked as skills.
- `agents/*.md`: custom subagents with explicit `name`, `description`, and
  inherited-model frontmatter.
- `commands/*.md`: explicit-invocation compatibility commands. Claude Code has
  merged custom commands into skills, so prefer skills for new workflows.

Every generated asset names its canonical source under `core/`. Change canonical
behavior in `core/`, then regenerate; direct generated-file edits fail drift
validation.

## Install in a Repository

Copy only the assets the target repository needs:

```sh
TARGET_REPO=/absolute/path/to/repository
mkdir -p "$TARGET_REPO/.claude/skills" "$TARGET_REPO/.claude/agents"
cp -R providers/claude/skills/safe-change "$TARGET_REPO/.claude/skills/"
cp providers/claude/agents/reviewer.md "$TARGET_REPO/.claude/agents/"
```

For a compatibility command:

```sh
mkdir -p "$TARGET_REPO/.claude/commands"
cp providers/claude/commands/review-council.md "$TARGET_REPO/.claude/commands/"
```

Review destination files before copying. Do not overwrite an existing skill,
agent, or command with the same name without comparing behavior.

## Verify

1. Start a fresh Claude Code session in the target repository.
2. Confirm the installed skill appears in `/skills` and can be invoked with
   `/<skill-name>`.
3. Open `/agents` and confirm the installed custom agent is available.
4. If commands were installed, confirm they appear when typing `/`.
5. Use a read-only or dry-run request before authorizing a workflow that writes.

## Limitations

- Skills and compatibility commands can expose overlapping slash-command names;
  do not install both with the same name.
- Generated agents inherit the session model and tool access. Repository and
  user permission settings remain authoritative.
- Installing these assets does not grant permission to write, publish, deploy,
  access secrets, or delegate work beyond the user's request.
