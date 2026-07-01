---
description: "Correct scoped visual inconsistencies without changing product behavior or introducing an unplanned redesign."
argument-hint: "[TASK_CONTEXT]"
---

# /ui-polish-pass

This is a legacy explicit-invocation Codex prompt adapted from `core/commands/ui-polish-pass.command.md`.
Custom prompts are deprecated; prefer the matching shared skill when one exists.

Treat `$ARGUMENTS` as additional task context. Read applicable repository
instructions, preserve the authorization boundaries in the request, and follow
the canonical command contract below.

## Purpose

Correct scoped visual inconsistencies without changing product behavior or
introducing an unplanned redesign.

## Inputs

- Target screen or component and approved polish scope.
- Existing design tokens, components, and UI brief.
- Representative states, content, viewports, and current screenshots.

## Preconditions

- The UI can be rendered or visual verification is explicitly deferred.
- Product behavior and information architecture remain unchanged.
- UI writes are authorized.

## Procedure

1. Capture the current target at representative narrow and wide viewports.
2. Audit spacing, typography, alignment, hierarchy, controls, overflow, and states.
3. Map each issue to an existing token, component, or established pattern.
4. Prioritize correctness issues before optional polish.
5. Apply small changes without altering interactions or broad layout structure.
6. Render loading, empty, error, success, disabled, focus, and long-content states.
7. Check keyboard access, visible focus, and contrast risks.
8. Compare before and after screenshots and run relevant UI checks.

## Output Format

```text
Scope and viewports:
Issues corrected:
Tokens and components reused:
Files changed:
States reviewed:
Screenshots reviewed:
Accessibility checks:
Remaining visual risks:
```

## Verification

- Review rendered output at all required viewports and states.
- Check clipping, overflow, reflow, content expansion, and touch targets.
- Run configured component, interaction, accessibility, and visual checks.
- Confirm no intended behavior or information hierarchy changed.

## Failure Behavior

- Stop and propose a UI brief if the request requires redesign.
- If the UI cannot be rendered, do not claim visual completion.
- Escalate accessibility conflicts rather than preserving inaccessible styling.
- Avoid adding new arbitrary tokens when design-system ownership is unclear.
