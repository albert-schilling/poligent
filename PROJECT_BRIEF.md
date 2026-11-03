# Project Brief: Poligent

Domain terms are defined in [GLOSSARY.md](GLOSSARY.md), and architectural decisions are recorded in [docs/adr/](docs/adr/).

## Purpose

Poligent is a portfolio project for AI engineering roles. It shows RAG, agentic workflows, prompt engineering and MLOps applied to a real, narrowly scoped problem.

## Core idea

Poligent tracks German federal **labor-law Procedures while they are still in progress**, not only laws that have already been enacted. It answers whether a Procedure may affect a person's **Profile**, and it is explicit about how uncertain that is: an open Legislative state means the outcome is not yet decided, and nothing it says is legal advice.

Existing tools, such as gesetze-im-internet.de and buzer.de, search enacted law. Tracking Procedures that are still in progress, matched to a person, is a use case those tools leave open, and it calls for an agentic pipeline instead of a single RAG lookup.

## Scope (v1)

- **In scope**: Procedures of type Gesetzgebung in Electoral term 21, limited to labor-law Procedures.
- **Out of scope**: enacted-law paragraphs from gesetze-im-internet.de, ministry drafts (Referentenentwürfe), earlier Electoral terms, state, EU and international law, user accounts and notifications.

## Data source: DIP API

The DIP API is at `https://search.dip.bundestag.de/api/v1`, with its spec at `/openapi.yaml`. The facts below were checked against spec v1.5.

- **Authentication**: every request needs `Authorization: ApiKey <key>`, or the `?apikey=` query parameter. The public key can rotate.
- **Pagination**: cursor-based, with at most 100 items per page (10 for `*-text` endpoints). Paging is finished when the cursor stops changing.
- **Filters**:
  - `f.wahlperiode`, `f.vorgangstyp`.
  - `f.sachgebiet` and `f.deskriptor` combine with AND, so each value needs its own query.
  - `f.aktualisiert.start` supports incremental sync.
- **Enactment data**: `verkuendung[]` and `inkrafttreten[]` are structured fields.
- **Free-text fields**: `beratungsstand` (the DIP status) and `sachgebiet` are free strings with no fixed list of values.
- **Full text**: available from `/drucksache-text`.
- **Rate limits**: none are published, so we poll conservatively.
- **Copyright**: Printed papers are official works (amtliche Werke). We may process them internally, but we only quote them briefly with a source and never alter them.

## Architecture

1. **Ingestion**: a scheduled job inside the backend.
   - First it backfills the whole Electoral term, then it runs a daily incremental sync.
   - It selects labor-law Procedures by the union of single-value Sachgebiet and deskriptor queries.
   - A new Procedure step is recorded as a Status change.
   - It fetches the full text of Key documents, chunks it and embeds the chunks.
2. **State mapping**: the DIP status is mapped to a Legislative state through a versioned, tested config.
   - Unmapped values become `UNKNOWN`.
   - A filled `verkuendung` always means `ENACTED`, and Entry into force dates are always shown.
3. **Chat**:
   - The backend retrieves Procedures and chunks using structured and semantic search together.
   - It produces a Relevance assessment against the Profile: a Verdict, its reasoning and the citations it relies on, with no numeric confidence.
   - Answers are grounded only in retrieved text, and there is an explicit "nothing found" answer.
   - Chat is multi-turn but not persisted.
   - Answers follow the UI language, and quotes stay in the German original.
4. **UI**:
   - A list of Procedures showing each one's Legislative state and a "changed since your last visit" highlight, plus a detail view for each Procedure.
   - The chat cites Procedures, and a Procedure's detail view can open the chat about it.
   - The Profile is stored in the browser.

**Data model (draft)**:
- `procedures`, `procedure_steps` and `printed_papers` hold the structured DIP data.
- `chunks` holds the text plus its pgvector embedding and references the Procedure and Printed paper it came from.
- `sync_state` holds the incremental-sync high-water mark.

## Stack

| Layer | Choice |
|---|---|
| Monorepo | Nx (pnpm, Gradle via `@nx/gradle`), see [ADR 0002](docs/adr/0002-nx-with-gradle.md) |
| Frontend | Vue, Vuetify, Vite, vue-i18n (German and English); typed client generated from OpenAPI |
| Backend | Java with Quarkus: REST with OpenAPI, SSE, Scheduler, Hibernate Panache, Flyway; see [ADR 0001](docs/adr/0001-quarkus-langchain4j-and-vue.md) |
| AI | Quarkus LangChain4j with OpenAI for chat and embeddings; Azure OpenAI is the documented switch |
| Database | PostgreSQL with pgvector, see [ADR 0003](docs/adr/0003-postgres-pgvector-single-store.md) |
| Observability | OpenTelemetry sent to a self-hosted Langfuse |
| Runtime | Docker Compose, everything local except LLM calls; see [ADR 0004](docs/adr/0004-local-first-except-llm.md) |
| CI | GitHub Actions: `nx affected` lint, test and build against recorded DIP responses; eval runs on manual trigger or PR label |

## Evaluation (`eval/`)

Built before the retrieval code and run with `nx eval`.
- **Retrieval**: 15–20 questions, each with the Procedures it should find, scored as Recall@k.
- **Relevance assessment**: about 10 labelled (Profile, Procedure) → Verdict cases, scored as exact agreement.
- Scores are recorded in Langfuse.

## Next steps

- [ ] Extend `explore_dip_states.py` to also count `sachgebiet` and `deskriptor` values, then run it against Electoral term 21.
- [ ] Use those results to write the labor-law filter values and the DIP status → Legislative state mapping.
- [ ] Set up the Nx monorepo, the Compose stack (Postgres with pgvector, Langfuse) and the Quarkus and Vue skeletons.
- [ ] Build the eval set.
- [ ] Build the DIP client, with recorded fixtures for tests.
- [ ] Spike: check whether Langfuse displays LangChain4j's `gen_ai.*` spans as LLM calls.
