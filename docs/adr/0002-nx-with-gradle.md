# Nx monorepo, with Gradle instead of Maven for the backend

The repo is an Nx monorepo that holds the backend, the frontend and the eval suite, so one task graph covers build, test and eval, and CI can use `nx affected` and caching. Nx only understands Java builds natively through the official `@nx/gradle` plugin. For that reason the Quarkus backend uses Gradle (Kotlin DSL), even though Maven is the Quarkus default and what most of its docs show.

## Considered Options

- **Maven with Nx `run-commands` wrappers or a community plugin.** Rejected because task inputs and caching would need to be configured by hand and would be brittle.
- **No Nx (pnpm workspaces plus a Makefile).** Simpler at 2–3 projects, but gives up the task graph and the CI story.
