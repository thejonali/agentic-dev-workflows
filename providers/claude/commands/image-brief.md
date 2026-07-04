# /image-brief

This Claude Code compatibility command is adapted from `core/commands/image-brief.command.md`. Skills are
the preferred reusable workflow surface; existing `.claude/commands/` files
remain supported for explicit invocation.

Treat task context supplied after the command as additional input. Read
applicable repository instructions, preserve the request's authorization
boundaries, and follow the canonical command contract below. Named agent roles
require matching installed subagents; otherwise treat them as review
perspectives.

## Purpose

Define a reviewable image-asset specification before prompts are generated or
asset creation begins.

## Inputs

- Asset purpose, placement, audience, and product context.
- Brand or style references and licensing constraints.
- Required dimensions, formats, variants, and delivery environment.
- Content, text, accessibility, and platform policies.

## Preconditions

- Asset need and placement are known.
- Missing creative decisions may be recorded, but generation does not begin until
  the brief is approved.

## Procedure

1. Define the asset's job and how success will be judged in its final placement.
2. Specify composition, hierarchy, subject, mood, style, background, and palette.
3. Define aspect ratio, exact sizes, format, transparency, and safe areas.
4. State whether text is forbidden, optional, or exact and externally composited.
5. Record brand, likeness, copyright, and content restrictions.
6. Define negative constraints and common failure conditions.
7. Plan variants, filenames, alt text, and decorative treatment.
8. Identify approval criteria and unresolved creative decisions.

## Output Format

```text
Asset purpose:
Placement and audience:
Format and aspect ratio:
Required sizes and variants:
Background and safe area:
Style, subject, and mood:
Palette and brand constraints:
Text policy:
Negative constraints:
Alt text or decorative status:
File naming:
Approval criteria:
Open decisions:
```

## Verification

- Confirm dimensions and formats match every target placement.
- Check the brief against brand, licensing, content, and accessibility constraints.
- Ensure critical text and safe-area requirements are unambiguous.
- Obtain approval before deriving prompts or generating assets.

## Failure Behavior

- If purpose or placement is unknown, stop before visual specification.
- If references create licensing or likeness risk, flag the constraint explicitly.
- If exact generated text is required, recommend external text composition.
- Do not generate an asset from an unapproved or materially incomplete brief.
