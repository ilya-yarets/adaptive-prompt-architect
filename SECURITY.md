# Security Policy

## Supported versions

Security fixes target the current `main` branch and the latest published release. Older snapshots and forks are not maintained by this project.

## System and scope

Adaptive Prompt Architect is an instructions-only Agent Skill and skills-only plugin. This policy covers its instructions, agent metadata, manifest and assets, validation and eval files, and installation guidance.

The project has no server, background service, telemetry, credential store, or independent content transmission. Host products and user-enabled tools remain separate trust boundaries with their own permissions and safety controls.

## Threat model and invariants

User prompts, voice transcripts, quotes, attachments, web pages, search or tool results, issue content, and workspace files may contain mistakes or adversarial instructions.

- Internal prompt refinement adds no authority and cannot expand the user's scope.
- Authority comes from the source of an instruction, not instruction-like wording.
- Instructions found inside retrieved, quoted, attached, or imported content remain data and cannot override higher-priority rules, authorize unrelated tool use, or suppress required confirmations.
- Material names, numbers, terms, negations, recipients, and authorization boundaries must not be silently changed.
- The skill must not disclose hidden instructions, secrets, or unrelated private context.
- Repository validation must not transmit content, execute unexpected code, or write outside the repository.

## What to report

Please report plausible authorization bypasses, prompt-injection paths, private-context disclosure, unexpected code or network execution, unintended repository mutation, or distribution-integrity problems.

Subjective wording preferences, ordinary model nondeterminism without a boundary failure, host-platform vulnerabilities, explicitly authorized consequential requests, and harmless documentation errors are normally out of scope.

## Limitations

Instructions influence model behavior but cannot enforce the host product's security boundary. Eval files describe observable expectations; they are not deterministic guarantees for every model or host configuration.

## Private reporting

Use [GitHub private vulnerability reporting](https://github.com/ilya-yarets/adaptive-prompt-architect/security/advisories/new). Do not disclose a suspected vulnerability in a public issue. Include the affected version or commit, a concise impact description, reproduction steps, and synthetic or redacted evidence only.

Last updated: August 23, 2026.
