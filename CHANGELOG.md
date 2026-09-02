# Changelog

This file records user-visible changes to Adaptive Prompt Architect. The package remains pre-1.0 while its behavior evals and cross-agent compatibility mature.

## [0.2.0] - Unreleased

### Changed

- Reworked the skill around outcomes and observable success instead of prescribed process.
- Replaced repeated mode and execution guidance with one compact decision path.
- Prefer relevant project conventions and progressively loaded references over universal rules or upfront context dumps.
- Keep examples only when they encode a real product requirement or address an observed failure.
- Adapt prompts from the target model's current documented capabilities rather than legacy assumptions about the model family.
- Use proportionate validation instead of mandatory plans, verifier agents, or repeated self-checking.
- Refined public metadata so the skill's purpose and boundaries are clearer during discovery.

### Preserved

- Explicit invocation still refines and executes by default; `prompt only` still returns a copy-ready prompt without execution.
- Names, numbers, negations, constraints, scope, and authorization boundaries remain protected.
- Instructions inside quotes, files, retrieved pages, and tool results remain data rather than additional authority.

### Quality

- Expanded the behavior eval specification from 12 to 16 scenarios.
- Added coverage for legacy-scaffolding removal, useful examples, progressive references, and proportionate validation.

## [0.1.2] - 2026-08-23

- Hardened source-authority handling and public security controls.
- Added behavior eval specifications for indirect prompt injection and confirmation preservation.

[0.2.0]: https://github.com/ilya-yarets/adaptive-prompt-architect/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/ilya-yarets/adaptive-prompt-architect/releases/tag/v0.1.2
