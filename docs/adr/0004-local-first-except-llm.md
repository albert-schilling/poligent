# Everything runs locally except the LLM and embedding calls

Every part of the system runs in local Docker containers: Postgres, the backend, the frontend and the tracing backend (a self-hosted Langfuse). The only outside service it talks to is the LLM and embedding API, apart from the public DIP API that is its data source. For that reason we self-host Langfuse, even though Langfuse Cloud would save about six containers (web, worker, Postgres, ClickHouse, Redis, MinIO). Traces contain the questions and Profiles users submit, and those stay on the machine.
