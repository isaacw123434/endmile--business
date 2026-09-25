---
name: endmile-app-performance
description: Analyze EndMile App, web planner, and core multimodal routing performance using first-party Postgres telemetry, GA4 acquisition channels (Direct, LinkedIn, Organic Search, AI Referrals, Guide CTAs), GSC/Bing, search success rates, popular corridors, and B2B TCO savings. Use when asked how the Flutter app or web planner is performing, where app users came from, which corridors are searched or failing, or tenant adoption and ROI.
---

# EndMile App & Core Routing Performance

## Overview

Use this skill for first-party app and core journey planner performance analytics. It covers traffic acquisition channels (Direct, LinkedIn, Google/Bing, AI search citations, Guide widget CTAs), search success rates, popular corridors, engine latency (OJP/MOTIS/OSRM), user cohort retention, and B2B Total Cost of Ownership (TCO) savings.

## First Read

Read these files before answering app performance or routing reliability questions:

- `docs/product/search-and-user-logs.md`
- `docs/architecture/server-routing-architecture.md`
- `docs/product/b2b-pretrip-pdf-justification-and-dispatch.md`

For code-level inspection, start with:

- `scripts/analytics/app-performance.mjs`
- `packages/server/src/interface/plugins/request-tracker.ts`
- `packages/server/src/infrastructure/tracking/in-memory-api-call-tracker.ts`
- `packages/server/src/infrastructure/database/migrations/003-journey-analytics.sql`

## Key Questions Answered

1. **Traffic Acquisition & Channel Sources:** Where did visitors/commuters come from? (Direct, LinkedIn campaigns, Google/Bing organic search, AI search engine citations like ChatGPT/Perplexity, B2C Guide Live Widget CTAs, or corporate invite emails).
2. **Search Success & Reliability:** Did searches succeed (HTTP 200 with valid journeys), return 0 results (timetable/corridor gap), or error/time out?
3. **Corridor Quality:** Which UK origin $\to$ destination pairs are most frequently searched, and which ones have high latency or zero-result rates?
4. **User Retention & Tenant Health:** How many active users are returning weekly? How many belong to corporate B2B tenants vs individual commuters?
5. **Value Realisation:** How many £ in TCO travel savings and kg of CO2 were identified vs direct driving? How many users saved routes or set up disruption alerts?

## CLI Workflow

Run the checked-in CLI for joined analysis:

```bash
# Bounded 28-day markdown summary across all channels and search telemetry
node scripts/analytics/app-performance.mjs --days 28 --markdown

# Production query via SSH to the VPS Postgres container
node scripts/analytics/app-performance.mjs --days 7 --ssh-db deploy@155.133.23.54 --markdown

# Filter by a specific corporate tenant
node scripts/analytics/app-performance.mjs --days 28 --tenant-id <tenant-uuid> --markdown

# Filter by specific corridor
node scripts/analytics/app-performance.mjs --days 28 --corridor "Leeds" --markdown
```

### Useful Flags

- `--from YYYY-MM-DD`, `--to YYYY-MM-DD`, or `--days N` (default 28)
- `--tenant-id <id>`: Filter metrics for a specific B2B corporate tenant
- `--corridor <substring>`: Filter popular corridors by city/station name
- `--limit <N>`: Number of table rows to display (default 15)
- `--ssh-db deploy@155.133.23.54`: Query production PostgreSQL via the VPS Docker Compose stack
- `--google-cloud-config <path>`: Local Google Cloud ADC config directory (e.g. `C:\Users\isaac\.gcloud-endmile-analytics`)
- `--gsc-google-cloud-config <path>`: Separate GSC ADC config (e.g. `C:\Users\isaac\.gcloud-endmile-gsc`)
- `--ga4-google-cloud-config <path>`: Separate GA4 ADC config (e.g. `C:\Users\isaac\.gcloud-endmile-analytics`)
- `--ga4-property <id>`: Defaults to `properties/531529105`
- `--site-url <url>`: Defaults to `sc-domain:endmilerouting.co.uk`
- `--json` or `--markdown`
- `--fixture-dir <dir>`: Run offline against saved JSON fixtures for automated testing

## Data Privacy & Guardrails

- **Client Hashing:** `client_id` in `endpoint_calls` is a daily-salted hash. Never commit or log raw client IP addresses.
- **Coordinates:** Public analytics aggregates round coordinates or use station/city names. Never expose exact residential coordinates.
- **Money:** Always compute and display financial calculations derived from integer pence.
- **Multi-Tenancy:** Keep tenant metrics segregated using tenant IDs.

## Validation

To run unit and fixture test suites:

```bash
node scripts/analytics/app-performance.test.mjs
```
