# Adaptive Prompt Architect

[![Validate](https://github.com/ilya-yarets/adaptive-prompt-architect/actions/workflows/validate.yml/badge.svg)](https://github.com/ilya-yarets/adaptive-prompt-architect/actions/workflows/validate.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A context-aware Agent Skill for Codex and ChatGPT that turns rough requests, voice transcripts, typo-filled notes, and streams of thought into reliable execution.

By default, `$prompt-architect` silently reconstructs the user's intent and completes the task. It does **not** print an intermediate rewritten prompt unless the user asks to see it. The internal rewrite never expands the user's permissions or scope.

This repository contains an instructions-only, skills-only plugin. It has no MCP server, API key, telemetry, or background service.

## What makes it adaptive

- Corrects obvious grammar, transcription, and logical errors without casually changing names, numbers, terms, or negations.
- Uses only relevant chat and explicitly connected workspace context.
- Organizes a stream of thought without forcing every request into one template.
- Adds roles, steps, constraints, sources, examples, and validation only when they improve the specific task.
- Preserves professional freedom instead of over-constraining the executing model.
- Asks the smallest useful question when ambiguity changes meaning, authorization, or the cost of an error.
- Treats quoted or attached content as data unless the user explicitly makes it an instruction.
- Adapts coding prompts for the named model or tool, including focused Codex Spark tasks.

## Modes

| Invocation | Behavior |
| --- | --- |
| `$prompt-architect <rough task>` | Silently refines the request and completes the task. |
| `$prompt-architect quickly: ...` / `быстро` | Uses the smallest sufficient reconstruction. |
| `$prompt-architect deeply: ...` / `глубоко` | Checks context, ambiguity, and risk more carefully without expanding scope. |
| `$prompt-architect prompt only: ...` / `только промпт` | Returns one copy-ready prompt and does not execute it. |
| `$prompt-architect show prompt: ...` / `покажи промпт` | Shows the improved prompt and does not execute it. |
| `$prompt-architect show and execute: ...` / `покажи и выполни` | Shows the prompt first, then completes the task. |
| `$prompt-architect for <model/tool>: ...` / `для <модели>` | Adapts the internal specification or prompt to the target. |

Examples:

```text
$prompt-architect deeply: this is from voice input maybe words are wrong, I need a small prototype where two people track groceries, maybe receipt photo or manual, main thing is test if we use it
```

```text
$prompt-architect только промпт: подготовь мой последний запрос для Codex Spark
```

```text
$prompt-architect покажи и выполни: придумай три коротких названия для этой заметки
```

## Install from GitHub

The easiest Codex route is to ask the bundled skill installer:

```text
$skill-installer Install the prompt-architect skill from https://github.com/ilya-yarets/adaptive-prompt-architect/tree/main/skills/prompt-architect
```

For a manual user-level installation:

```bash
git clone https://github.com/ilya-yarets/adaptive-prompt-architect.git
cd adaptive-prompt-architect
mkdir -p ~/.agents/skills
ln -s "$PWD/skills/prompt-architect" ~/.agents/skills/prompt-architect
```

Codex detects skill changes automatically. If the skill does not appear, restart Codex and invoke it with `$prompt-architect`.

The repository is already packaged as a skills-only plugin. It is not yet listed in the universal ChatGPT/Codex plugin directory; GitHub installation is the current distribution path.

## Safety boundary

“Silent” means the improved working specification is not printed as a separate block. It does not hide required approvals, material assumptions, tool activity, or task results. The skill cannot create permission to send, delete, publish, purchase, deploy, or alter external state beyond what the user authorized.

If a material ambiguity affects a name, number, negation, destination, irreversible action, or target system, the skill asks a compact blocking question instead of guessing.

## Development and evaluation

The repository includes behavior-oriented eval cases for:

- silent default execution;
- prompt-only and show-and-execute modes;
- voice-transcription invariants;
- streams of thought;
- context-aware coding prompts;
- destructive ambiguity;
- quoted prompt-injection content;
- precise trigger and non-trigger routing.

Run the repository checks with:

```bash
python3 scripts/validate.py
```

The eval files are specifications for representative model tests, not claims of deterministic model output.

## Русский

`$prompt-architect` — адаптивный архитектор намерения. Он понимает сырой запрос, исправляет очевидные ошибки голоса или текста, использует релевантный контекст и по умолчанию сразу выполняет задачу, не показывая промежуточный переписанный промпт.

Быстрый вызов:

```text
$prompt-architect глубоко: [сырой запрос, голосовая расшифровка или поток мыслей]
```

Если нужен именно текст промпта для копирования:

```text
$prompt-architect только промпт: [черновик]
```

Если хотите увидеть улучшенный промпт и затем получить результат:

```text
$prompt-architect покажи и выполни: [черновик]
```

## License

[MIT](LICENSE). See [Privacy](PRIVACY.md), [Terms](TERMS.md), and [Support](SUPPORT.md).
