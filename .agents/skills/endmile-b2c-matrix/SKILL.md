---
name: endmile-b2c-matrix
description: Work on EndMile B2C matrix generation, venue matrix CLI runs, city parking/Park & Ride timing, and train fare extraction/injection. Use when updating or validating scripts under scripts/batch-router, B2C pivot docs, or matrix API behaviour for venue pages.
---

# EndMile B2C Matrix

## Overview

Use this skill for the B2C programmatic SEO matrix workflow: generating venue route JSON, validating `routingProfile: 'b2c_matrix'`, extracting missing fare pairs, and injecting scraped Trainline fares.

## Workflow

1. Read `docs/b2c-pivot/AGENTS.md`, `docs/b2c-pivot/README.md`, `docs/b2c-pivot/execution_phases_and_progress.md`, and `docs/b2c-pivot/matrix-api-usage.md` before making claims about the matrix workflow.
2. Treat `docs/b2c-pivot/execution_phases_and_progress.md` and the `docs/b2c-pivot/README.md` "Current Launch State and Remaining Work" section as the source of truth for B2C domain, VPS, GA4, deploy, legal, Search Console, content, fare, stage gates, and publish-gate status. Read them before answering "what's left", "is deploy set up", or "what should we do next" questions.
3. Avoid Flutter/Dart packages unless the task explicitly touches app UI. The B2C matrix work is primarily server routing, `scripts/batch-router`, `data/b2c`, `data/railway`, and B2C pivot docs.
4. Do not start a local Node dev server or use `pnpm dev` for VPS-backed matrix validation. Use tests, committed code, deployed API endpoints, and the batch CLI against the intended deployed API.
5. Keep B2C-only behaviour scoped to the existing `routingProfile: 'b2c_matrix'` and `includeCityParking` request constraints. Do not introduce a second B2C flag.
6. Treat generated venue JSON as data output. Stage it only when the user explicitly wants generated batch files in the PR.

## Matrix CLI

Use:

```bash
node scripts/batch-router/generate-venue-matrix.mjs --limit 10
node scripts/batch-router/generate-venue-matrix.mjs --type hotel
node scripts/batch-router/generate-venue-matrix.mjs --id 21285244 --force
node scripts/batch-router/generate-venue-matrix.mjs --ids 21285244,13939651 --force
```

Default resume behaviour skips already-generated venue files only when they pass the matrix shape validator. A valid matrix has at least 4 clean routed origins with no stored error rows; 4/5 partial outputs are saved with the failed origin omitted so Astro renders a shorter regional table. Outputs with 0-3 usable origins are discarded for retry/backfill. Use `--force` only when deliberately regenerating an existing venue file.

Current production-safe defaults are `--concurrency 3 --origin-stagger-ms 200 --motis-queue-max 120 --motis-inflight-max 24 --motis-poll-ms 1000 --api-timeout-ms 45000 --origin-attempts 1`.
London destination venues are eligible after the 2026-08-21 TfL Park & Tube server validation. The CLI still excludes London/M25 cities as origin rows so venue matrices compare useful inbound regional cities.
London was historically excluded because of route fan-out and TfL data-quality gaps, not because MOTIS cannot route London. MOTIS can remain part of National Rail routing, but TfL Journey Planner is authoritative for TfL fares and Tube/DLR/Elizabeth/Overground geometry. Do not run broad London-inclusive batches until the server has a global TfL limiter below TfL's 500 requests/minute product cap, recommended at roughly 420-450 requests/minute with 429 `Retry-After` handling, and a CLI-readable TfL queue/pressure endpoint. Until that exists, London validation should use small smoke batches such as `--concurrency 1 --origin-stagger-ms 1000 --api-timeout-ms 90000 --origin-attempts 1`.
Each concurrent venue can start up to five origin requests. When admin key `ENDMILE_ADMIN_API_KEY` is present, adaptive MOTIS queue backoff uses the `/health/motis-queue` endpoint with a queue threshold of 120 and poll rate of 1000ms. The CLI excludes repeat-failing origin CRS values (`HEMEL`, `GRAVE`, `BRACK`, `CRAWL`, `STALB`, `HIGHW`, `WELWY`, `MAIDE`, `SLOUG`, `CHELM`) by default; use `--exclude-origin-crs none` only for diagnostic runs.
Production matrix API calls also require `ENDMILE_MATRIX_API_KEY` to match the server's dedicated `MATRIX_API_KEY`. This authorises `b2c_matrix` searches and exempts the controlled CLI from EndMile route limits without exposing the broader admin key.

CLI flags:

| Flag | Purpose |
|---|---|
| `--limit N` | Process only the first `N` selected venues. `--limit 0` verifies config without API calls. |
| `--id ID` / `--ids ID,ID` | Target exact eligible venue IDs. |
| `--type TYPE` / `--types TYPE,TYPE` | Target venue types such as `hotel` or `hotel,hospital`. |
| `--force` | Overwrite existing output files instead of resume-skipping them. |
| `--api URL` | Override the API base URL; use the deployed API for VPS-backed validation. |
| `--concurrency N` | Number of venues processed at once. Default is `3`. |
| `--origin-stagger-ms N` | Delay between origin requests inside one venue. Default is `200`. |
| `--motis-queue-max N` | Max MOTIS queue length before triggering backoff pause. Default is `120`. |
| `--motis-inflight-max N` | Max MOTIS inflight concurrency limit. Default is `24`. |
| `--motis-poll-ms N` | Backoff check poll interval when paused. Default is `1000`. |
| `--matrix-api-key-env NAME` | Environment variable containing the matrix API key. Default is `ENDMILE_MATRIX_API_KEY`. |
| `--venue-pause-ms N` | Delay after each venue finishes. Default is `0`. |
| `--api-timeout-ms N` | Per origin API request timeout. Default is `45000`. |
| `--origin-attempts N` | Attempts per origin for retryable failures. Default is `1`. |
| `--exclude-origin-crs CRS,CRS` | Override the default excluded origin CRS list; use `none` to include all origins. |

## Routing Semantics

- Direct drive: OSRM drive from origin coordinates to venue coordinates.
- Drive to city parking: OSRM drive from origin coordinates to a city-parking hub, then MOTIS/walking from the parking hub to the venue. For B2C matrix output, city parking last mile is walking only and allowed when the walk is 24 minutes or less.
- Park & Ride: OSRM drive to a configured Park & Ride site, then MOTIS transit/walk to the venue. For B2C matrix output, remove scheduled wait from the displayed static time; use drive time plus transit/walk sub-leg time.
- Transit geometry: the venue matrix CLI must preserve simplified `subLegs` from transit leg metadata so Astro maps can render walking access legs and bus/tram/metro vehicle legs with separate line styles. Regenerate venue JSON after CLI changes that affect subleg serialization.

## Fare Pipeline Architecture & Workflow

The EndMile B2C rail fare dataset (`data/railway/b2c_train_fares.json`) provides 100% pricing coverage across all 55,531 UK venue matrices without commercial OJP XML API costs through a multi-tier pipeline:

### 1. Multi-Tier Resolution Pipeline

1. **Tier 1: Direct Trainline Scraping (`price-missing-trainline-fares.mjs`)**
   - High-throughput parallel scraping (2 staggered workers, 25ms delay + jitter, auto-retry on HTTP 429/503).
   - Resolves structured JSON-LD and HTML price patterns across 2,895 station slugs with explicit London terminal and regional aliases.
2. **TfL Park & Tube Fares**
   - Do not regenerate static TfL zonal/contactless fares for Park & Tube routing.
   - The server TfL integration uses TfL Journey Planner fare data (`journey.fare.totalCost`) when returned; Park & Tube options without a positive TfL fare should be suppressed rather than shown as free.
   - Existing historical `tfl_*` entries in `data/railway/b2c_train_fares.json` are legacy matrix data, not the authoritative Park & Tube pricing path.
3. **Tier 3: Parallel MOTIS Composite Breakdown (`motis-fallback-pricer.mjs`)**
   - 10-worker parallel pool querying local MOTIS on VPS (`http://localhost:8081`) at ~120 pairs/sec.
   - Decomposes multi-operator transfer journeys into individual legs, verifying each sub-leg is priced before summing.
   - **Zero-Partial-Split Safety:** Never writes partial sums or guessed averages. Emits full sub-leg audit trails (`note: summed_from_motis_legs: A->B, B->C`).
4. **Tier 4: National Rail Regulated Mileage Tariff Fallback (`inject-all-remaining-mileage-fares.mjs`)**
   - For irreducible commuter lines and branch stations lacking static marketing discounts, calculates the official DfT distance-based regulated passenger rate using great-circle station coordinates:
     $$\text{Fare (pence)} = \max\left(280, 250 + \text{round}(\text{Distance in Miles} \times 24)\right)$$
   - Tagged as `source: 'national_rail_regulated_tariff'`.

### 2. End-to-End Execution Sequence

```bash
# 1. Extract unpriced station pairs from venue matrices
node scripts/batch-router/extract-missing-fares.mjs

# 2. Scrape direct Trainline market fares across missing pairs
node scripts/batch-router/price-missing-trainline-fares.mjs --concurrency 2 --delay-ms 25 --write

# 3. Decompose multi-leg routes with MOTIS fallback engine
node scripts/batch-router/motis-fallback-pricer.mjs --concurrency 10

# 4. Populate any remaining branch/commuter pairs with regulated mileage tariff
node scripts/batch-router/inject-all-remaining-mileage-fares.mjs

# 5. Verify and inject into venue JSON files
node scripts/batch-router/inject-scraped-fares.mjs --dry-run
node scripts/batch-router/inject-scraped-fares.mjs --write
```

### 3. Safety & Integrity Guarantees

- **Integer-Pence Strictness:** Every fare is stored strictly as integer pence in JSON matrices (`no floating-point money`).
- **Data Preservation:** Non-train routes, driving polylines, coordinates, car parks, and taxi costs are 100% preserved.
- **Idempotency:** A dry run immediately following `--write` reports 0 venues changed and 0 missing fares.
