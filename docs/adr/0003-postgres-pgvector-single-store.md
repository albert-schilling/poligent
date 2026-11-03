# Single Postgres + pgvector store for relational and vector data

Legislative data has structured relationships (a Procedure, its Procedure steps and its Printed papers) and also needs semantic search over text chunks. We keep both in one PostgreSQL instance with the pgvector extension, not a relational database next to a dedicated vector database. This means one system to run locally, and structured and semantic filters can be combined in a single SQL query, for example "labor-law procedures changed in the last 7 days, ranked by similarity to the question".

## Considered Options

- **A dedicated vector database (Qdrant, Weaviate and similar).** Rejected because, at this corpus size, the second system to operate and keep in sync outweighs its query performance.
