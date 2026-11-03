# Poligent

Poligent tracks German federal **labor-law legislation while it is still going through parliament** and answers one question: *could this affect me?*

You describe your situation once, for example as an employee working shifts or as a freelancer who is also a parent. Poligent then assesses the bills in progress in the Bundestag against that description. Each answer cites the official documents it relies on and states clearly how open the outcome still is.

> **Status:** design phase. See [PROJECT_BRIEF.md](PROJECT_BRIEF.md).

## How it works

1. **Ingest.** Poligent fetches labor-law bills from the Bundestag's [DIP API](https://dip.bundestag.de/über-dip/hilfe/api). It maps their raw status to a small set of legislative states and embeds the key documents.
2. **Retrieve.** It combines structured and semantic search over one Postgres + pgvector store.
3. **Assess.** For each bill, an LLM decides *relevant*, *possibly relevant* or *not relevant* for your profile. It must give its reasoning and cite the passages it relies on.

## Stack

| Layer | Technology |
|---|---|
| Frontend | Vue, Vuetify |
| Backend | Java, Quarkus, LangChain4j |
| Database | PostgreSQL with pgvector |
| Tracing | Langfuse |
| Tooling | Nx, Docker Compose |

Everything runs locally in Docker. The only external calls go to the DIP API and to the LLM and embedding provider.

## Docs

- [PROJECT_BRIEF.md](PROJECT_BRIEF.md) covers scope, architecture and next steps.
- [GLOSSARY.md](GLOSSARY.md) defines the domain terms.
- [docs/adr/](docs/adr/) records the architecture decisions.

## Limitations

- **Not legal advice.** Poligent is an informational aid only.
- **Coverage:** federal law only. It does not cover state or EU law, or ministry drafts that have not yet reached parliament.
- **Completeness:** relevance is a best-effort LLM assessment. Poligent cannot promise that you will never miss a change that affects you.
- **Data:** traces of the questions and profiles you enter are stored locally, in Langfuse.
