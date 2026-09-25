# Operations & Infrastructure Guide

Operational runbooks, hosting configurations, server costs, routing queries, and analytics CLI execution.

## Operations Manuals

| Manual | Topic & Contents |
|---|---|
| [`vps-access-and-operations.md`](vps-access-and-operations.md) | **Production VPS Specifications & Management:** Contabo Cloud VPS 30 specs, SSH access credentials, Docker Compose stack (Caddy, Fastify, Postgres, Redis, OSRM, MOTIS), log viewing, service restarts, and health checks. |
| [`infrastructure-costs-and-economics.md`](infrastructure-costs-and-economics.md) | **Cloud Economics & Unit Costs:** Exact monthly burn (~£37–£50/mo), Contabo VPS breakdown (£16.00/mo), National Rail OJP API unit economics (£0.00042/call ~2.19p/search), caching ROI, and scaling cost projections. |
| [`how-to-query-routes.md`](how-to-query-routes.md) | **Query Recipes for Routing Engines:** Step-by-step instructions for testing production routes via `curl` on the public SSE stream, internal MOTIS queries (port 8080), OSRM queries (ports 5000/5001), and batch matrix tools. |
| [`analytics-and-telemetry-cli.md`](analytics-and-telemetry-cli.md) | **Guide & App Analytics CLI Runbook:** How to run `guide-performance.mjs` and `app-performance.mjs` to fetch metrics from GA4 (`properties/531529105`), Google Search Console (`sc-domain:endmilerouting.co.uk`), Bing, and the production VPS PostgreSQL database via SSH. |
| [`maintenance-and-rebuilds.md`](maintenance-and-rebuilds.md) | **Routine Maintenance Schedules:** Mandatory weekly TNDS GTFS rebuild procedure, yearly OSRM road graph rebuilds, DEFRA greenhouse gas conversion factor updates, and CI/CD GitHub Actions deploy flows. |
