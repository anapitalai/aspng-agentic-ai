# Project Guidelines

# ASPNG Agentic AI
- Agentic AIs using python copilot SDK in the field of Surveying, GIS, Cloud native GIS and GNSS.

## Scope
- This workspace is intended for surveying and GIS agents built with the Copilot SDK.
- Treat the repository as a greenfield project until code or docs establish stronger conventions.
- Do not invent build, test, or deploy commands that are not present in the workspace.

## Available Custom Agents
- [Survey Solution Architect](.github/agents/survey-solution-architect.agent.md): designs surveying workflows, parcel and boundary orchestration, and Copilot SDK flow decomposition.
- [GIS Workflow Engineer](.github/agents/gis-workflow-engineer.agent.md): implements spatial ETL, transformations, geoprocessing logic, and GIS tool integrations.
- [Spatial QA Reviewer](.github/agents/spatial-qa-reviewer.agent.md): reviews geometry correctness, topology quality, CRS consistency, and attribute completeness.
- [GNSS Workflow Engineer](.github/agents/gnss-workflow-engineer.agent.md): builds GNSS pipelines for RTK or PPK processing, quality checks, and datum-aware outputs.
- [Cloud Native GIS Engineer](.github/agents/cloud-native-gis-engineer.agent.md): designs and implements cloud-scale GIS services, data pipelines, and observability-aware spatial systems.

## Architecture
- Prefer a separation between domain workflows, SDK orchestration, and spatial data utilities.
- Keep survey logic, coordinate reference system handling, and GIS transforms in explicit modules rather than embedding them in prompts.
- Isolate external integrations such as PostGIS, GDAL, field data APIs, or map services behind narrow tool adapters.

## Domain Rules
- Require the coordinate reference system, units, and source datum to be explicit before transforming or validating geometry.
- Preserve geometry provenance: record source files, survey dates, control assumptions, and transformation steps when code or docs create them.
- Flag legal or regulatory assumptions instead of fabricating authoritative cadastral or boundary outcomes.
- Prefer open geospatial formats such as GeoJSON, WKT, CSV with coordinates, and documented EPSG codes unless the repo defines another standard.

## Implementation Conventions
- Favor typed interfaces for features, observations, traverses, parcels, and QA findings.
- Keep prompt text small; put repeatable behavior in code, tests, or reusable SDK tools.
- When bootstrapping, prefer directories such as `src/agents/`, `src/workflows/`, `src/tools/`, `src/spatial/`, `docs/`, and `tests/`.
- Add sample data and fixtures that exercise coordinate transforms, linework closure, parcel topology, and field import edge cases.

## Validation
- Validate geometry with deterministic checks before presenting conclusions to users.
- Prefer tests for CRS conversion, distance and bearing calculations, polygon validity, topology overlaps, and missing attributes.
- If the workspace does not yet contain executable checks, state that gap plainly instead of claiming validation ran.

## Documentation
- Link future process details from `docs/` rather than duplicating them here.
- When introducing a new survey or GIS workflow, document required inputs, CRS expectations, tolerances, and output schema near the code.


## Context Files

Read the following to get the full context of the project:

- @context/project-overview.md
- @context/coding-standards.md
- @context/ai-interaction.md
- @context/current-feature.md