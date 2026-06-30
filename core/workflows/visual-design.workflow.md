# Visual Design Workflow

## Purpose

Plan, implement, and review user-interface and image work against explicit design,
responsive, accessibility, state, and asset requirements.

## When to Use

- Designing or restructuring a screen, flow, or reusable component.
- Implementing UI from an approved brief or component specification.
- Performing scoped visual, responsive, or accessibility polish.
- Reviewing screenshots or establishing visual regression coverage.
- Planning icons, banners, illustrations, or other image assets.

## Inputs

- Product goal, target users, and acceptance criteria.
- Existing design system, tokens, components, and content conventions.
- Current implementation and representative application states.
- Target viewports, input methods, browsers, and accessibility requirements.
- Reference images, brand constraints, required asset sizes, and text policy.

## Required Agents

- `ui-architect`: defines hierarchy, components, states, and responsive behavior.
- `implementer`: builds approved UI changes.
- `visual-qa-reviewer`: compares rendered results with the specification.
- `accessibility-reviewer`: checks semantics, keyboard use, focus, and contrast.

Use `asset-director` for image work and `test-runner` for interaction or visual
regression coverage.

## Commands

- `/ui-brief`: define user goal, hierarchy, states, and constraints.
- `/design-system-audit`: inventory reusable tokens and components.
- `/component-spec`: define API, variants, states, and accessibility behavior.
- `/build-ui-from-spec`: implement an approved design specification.
- `/ui-polish-pass`: correct scoped visual inconsistencies without redesigning.
- `/responsive-pass`: verify behavior across defined viewport ranges.
- `/accessibility-pass`: inspect semantics, focus, input, and contrast.
- `/screenshot-review`: review rendered evidence against the brief.
- `/visual-regression-setup`: add stable, intentional visual coverage.
- `/image-brief`: define purpose, composition, constraints, and deliverables.
- `/generate-image-prompts`: derive prompts from an approved image brief.
- `/asset-pack-plan`: specify variants, dimensions, formats, names, and alt text.

## Procedure

1. Define the user task, changed surface, success criteria, and explicit non-goals.
2. Audit existing tokens, components, layout patterns, assets, and content before
   creating new design primitives.
3. Produce a UI or image brief covering hierarchy, content, interaction, states,
   responsive behavior, accessibility, and constraints.
4. For components, define inputs, variants, state transitions, error behavior,
   keyboard behavior, and composition boundaries.
5. Establish representative states: loading, empty, error, success, disabled,
   hover, focus, active, long content, and constrained viewport where relevant.
6. Implement the approved specification using existing tokens and components.
   Keep polish changes scoped and avoid unrelated redesign.
7. Render at defined viewports and capture consistent screenshots for comparison.
8. Review hierarchy, spacing, alignment, overflow, typography, contrast, focus,
   interaction states, and content resilience.
9. Test keyboard and semantic behavior, then run relevant component, interaction,
   accessibility, and visual-regression checks.
10. Report the specification implemented, evidence reviewed, deviations, checks,
    and remaining risks.

For image work, approve an image brief before prompt generation or asset creation,
then review outputs against composition, safe area, text, size, and brand rules.

## Rules

- Use existing design tokens and components before introducing new ones.
- Do not add arbitrary colors, type sizes, spacing values, or breakpoints.
- Do not treat a single desktop screenshot as responsive verification.
- Preserve semantic structure, keyboard access, visible focus, and readable contrast.
- Avoid broad redesign during a polish, responsive, or accessibility pass.
- Use realistic long, empty, loading, error, and disabled states where applicable.
- Do not approve generated image text without inspecting its accuracy.
- Every meaningful image needs a filename plan, dimensions, format, and alt-text
  decision; decorative images should be identified as such.
- Visual snapshots are reviewed artifacts, not automatic proof of correctness.

## Outputs

- UI brief, component specification, or image brief.
- Reuse decisions for tokens, components, and assets.
- Implemented UI or generated asset set when authorized.
- Viewport and state coverage matrix.
- Screenshot review with prioritized visual and accessibility findings.
- Verification commands, evidence, deviations, and remaining risks.

## Verification

- Render all required states at representative narrow and wide viewports.
- Check for overflow, clipping, reflow, content expansion, and touch target issues.
- Verify keyboard order, focus visibility, labels, semantics, and error association.
- Run automated accessibility and visual checks where configured, then perform
  manual review for issues automation cannot establish.
- Compare screenshots against the approved brief rather than subjective polish.
- Inspect asset dimensions, format, transparency, safe areas, text, and alt text.

## Failure Modes

- If no brief or acceptance criteria exists, stop implementation after producing a
  proposed brief unless exploratory work was explicitly requested.
- If design tokens or component ownership are unclear, document the conflict before
  adding a competing primitive.
- If representative data or states are unavailable, use labeled fixtures and list
  the unverified production states.
- If rendering or browser access is unavailable, do not claim visual verification;
  provide exact viewports, states, and steps still required.
- If accessibility conflicts with a visual requirement, treat accessibility as a
  blocker and surface the product decision needed.

## Provider Notes

Provider adapters may use browser, screenshot, accessibility, or image-generation
tools, but the brief remains the controlling input. Tools must not broaden the
approved visual scope. Store reproducible prompts and asset metadata when assets
are generated, and distinguish automated findings from manual visual judgment.
