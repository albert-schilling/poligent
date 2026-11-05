# Poligent

Tracks German federal labor-law Procedures while they are still in progress, and tells a person whether one may affect their Profile. See [`README.md`](README.md).

## Where decisions live

Read the relevant source before you design anything; decisions are already made there.

- [`GLOSSARY.md`](GLOSSARY.md): the domain terms. Use them in code, tests, commits and pull requests, and avoid the words it lists under _Avoid_.
- [`docs/adr/`](docs/adr/): architecture decisions.
- [`PROJECT_BRIEF.md`](PROJECT_BRIEF.md): scope, architecture and next steps.

## Conventions

`./scripts/validate.sh` runs what CI runs. A Stop hook runs it at the end of every agent turn and keeps the turn going while it fails.

- [`docs/conventions/tooling.md`](docs/conventions/tooling.md): commands, and tool behaviour that has surprised us. Read it before you run, configure or debug a tool.
- [`docs/conventions/code.md`](docs/conventions/code.md): project layout, comments and config files. Read it before you write code or config.
- [`docs/conventions/pull-requests.md`](docs/conventions/pull-requests.md): size, tests, workflow files and the harness log. Read it before you commit, push or open a pull request.
- [`docs/conventions/issues-and-records.md`](docs/conventions/issues-and-records.md): the issue template, labels, and how decision records name tools. Read it before you write an issue or a decision record.

## Agent skills

### Issue tracker

Issues live in GitHub Issues for `albert-schilling/poligent` (via the `gh` CLI). See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`. The Factory adds `friction` and `pre-existing`; see [`docs/conventions/issues-and-records.md`](docs/conventions/issues-and-records.md).

### Domain docs

Single-context: one `GLOSSARY.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
