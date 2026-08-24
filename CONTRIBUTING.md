# Contributing

Focused bug fixes, behavior evals, documentation improvements, and well-scoped prompt-design proposals are welcome.

1. Create a feature branch and keep the change focused.
2. Use synthetic or redacted examples. Never include secrets, private transcripts, or personal workspace data.
3. Preserve user intent, authorization boundaries, and ordinary useful behavior. Prefer a short shared invariant or targeted eval over repeated instructions.
4. Keep shared behavior in the canonical `SKILL.md`; add host-specific metadata only when a host requires it.
5. Run `python3 scripts/validate.py` and include the result in the pull request.
6. Explain the problem, the smallest proposed change, behavior or compatibility risk, and how to roll it back.

Report security issues privately through [SECURITY.md](SECURITY.md), not in a public issue.
