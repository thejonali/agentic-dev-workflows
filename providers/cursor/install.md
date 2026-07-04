# Install the Cursor Adapter

The Cursor adapter packages canonical workflows as scoped project rules and core
commands as reusable custom commands.

## Requirements

- A current Cursor installation.
- A target repository where you may add `.cursor/` files.
- A checkout of this workflow repository when installing by copy.

## Supported Assets

- `rules/*.mdc`: agent-requested project rules with descriptions,
  `alwaysApply: false`, and no file globs.
- `commands/*.md`: reusable slash commands. Cursor currently documents custom
  commands as a beta feature whose syntax may change.

The adapter deliberately has no large always-on rule. Workflows remain scoped
and load only when Cursor selects a matching description or the user references
the rule. Cursor's adapter contract does not package the canonical agent-role
documents as separate subagents.

Every generated asset names its canonical source under `core/`. Change canonical
behavior in `core/`, then regenerate; direct generated-file edits fail drift
validation.

## Install in a Repository

Copy only the rules and commands the target repository needs:

```sh
TARGET_REPO=/absolute/path/to/repository
mkdir -p "$TARGET_REPO/.cursor/rules" "$TARGET_REPO/.cursor/commands"
cp providers/cursor/rules/safe-change.mdc "$TARGET_REPO/.cursor/rules/"
cp providers/cursor/commands/review-council.md "$TARGET_REPO/.cursor/commands/"
```

Review destination files before copying. Do not overwrite an existing rule or
command with the same name without comparing behavior.

## Verify

1. Open the target repository in Cursor.
2. Open Cursor Settings, then Rules, and confirm the copied rule is listed as an
   agent-requested rule.
3. Reference the rule by name in a read-only request and inspect its behavior.
4. Type `/` in chat and confirm the installed command appears.
5. Use a read-only or dry-run request before authorizing a workflow that writes.

## Limitations

- Cursor custom commands are beta and may change.
- Rules are repository-scoped; copying them does not create global user rules.
- Installing these assets does not grant permission to write, publish, deploy,
  access secrets, or perform work beyond the user's request.
