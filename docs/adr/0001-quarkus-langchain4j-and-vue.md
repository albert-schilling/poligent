# Quarkus + LangChain4j backend and Vue + Vuetify frontend

The original brief planned a TypeScript stack: Next.js, tRPC, and either the Vercel AI SDK or TanStack AI. We use Java with Quarkus and the `quarkus-langchain4j` extension in the backend, and Vue with Vuetify in the frontend. This is a deliberate choice of preferred stack, not a technical necessity. LangChain4j gives us structured output, tool calling, an embedding-store abstraction and a provider-neutral model interface, which covers the "avoid vendor lock-in" goal.

## Consequences

- We lose end-to-end type safety through tRPC. Instead, the backend publishes an OpenAPI spec (SmallRye OpenAPI) and the frontend generates its typed client from it. Chat responses stream over SSE.
- There are two languages to maintain, which [ADR 0002](0002-nx-with-gradle.md) addresses at the tooling level.
