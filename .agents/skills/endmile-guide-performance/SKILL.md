---
name: endmile-guide-performance
description: Analyze EndMile Guide and B2C performance using API source attribution, endpoint_calls, GA4, and Google Search Console. Use when asked whether journey/search traffic came from the Flutter app, Guide live widget, matrix CLI, or agent CLI; when running scripts/analytics/guide-performance.mjs; or when combining server telemetry with GA4/GSC for SEO, widget, CTA, affiliate-click, latency, cache, or OJP-cost analysis.
---

# EndMile Guide Performance

## Overview

Use this skill for first-party Guide/B2C analytics and request-source attribution. It covers the server telemetry fields, privacy rules, CLI workflow, and the docs/code files to read before making claims.

## First Read

Read these files before answering attribution or Guide analytics questions:

- `docs/product/search-and-user-logs.md`
- `docs/b2c-pivot/README.md`
- `docs/b2c-pivot/phase_2_b2c_site_architecture.md`

For code-level inspection, start with:

- `packages/server/src/interface/utils/request-source-attribution.ts`
- `packages/server/src/interface/plugins/request-tracker.ts`
- `packages/server/src/infrastructure/database/migrations/022-endpoint-source-attribution.sql`
- `scripts/analytics/guide-performance.mjs`

## Source Attribution

New `endpoint_calls` rows carry telemetry-only fields:

| Caller | `client_surface` | `client_feature` | `source_kind` | `source_id` |
|---|---|---|---|---|
| Flutter app journey search | `app` | `journey_search` | `none` | `NULL` |
| Guide venue live widget | `guide` | `live_widget` | `venue` | Venue ID |
| Matrix generator CLI | `matrix_cli` | `matrix_batch` | `none` | `NULL` |
| Future agent analysis CLI | `agent_cli` | `analysis` | `none` | `NULL` |
| Absent or invalid attribution | `unknown` | `unknown` | `none` | `NULL` |

Treat `X-EndMile-*` headers as telemetry only. Never use them for authentication, tenancy, pricing, permissions, or security decisions.

Do not capture PII in attribution fields. `X-EndMile-Source-Id` is a venue ID for Guide live-widget searches only; do not put postcodes, raw coordinates, full URLs, emails, or user identifiers there.

## CLI Workflow

Prefer the checked-in CLI for joined analysis:

```bash
node scripts/analytics/guide-performance.mjs --days 28 --surface guide --markdown
node scripts/analytics/guide-performance.mjs --days 7 --surface guide --ssh-db deploy@155.133.23.54 --markdown
```

Useful flags:

- `--from YYYY-MM-DD`, `--to YYYY-MM-DD`, or `--days N`
- `--surface app|guide|matrix_cli|agent_cli|unknown`
- `--venue-id <id>`
- `--page <url-or-path-substring>`
- `--venue-data <path>` to resolve venue IDs to names; defaults to `data/venues/master_venues.json`
- `--google-cloud-config <path>` to run `gcloud` against the EndMile analytics ADC config
- `--gsc-google-cloud-config <path>` to use a separate Search Console ADC config
- `--ga4-google-cloud-config <path>` to use a separate GA4 ADC config
- `--query <substring>` to filter search queries by keyword (e.g. `--query "park"`)
- `--limit <N>` number of rows to display in tables (defaults to 15)
- `--bing-api-key <key>` Bing Webmaster API key; defaults to `BING_API_KEY` env or EndMile key `f9541b772ec346ea816b0395881232e0`
- `--bing-site-url <url>` Bing site URL; defaults to `https://guide.endmilerouting.co.uk/` (or `https://endmilerouting.co.uk/` for `--surface app`)
- `--no-bing` to disable Bing API queries
- `--json` or `--markdown`
- `--ssh-db deploy@155.133.23.54` to query production Postgres through the VPS Docker Compose stack
- `--fixture-dir <dir>` for offline fixture tests

Inputs and defaults:

- Postgres: prefer `ANALYTICS_DATABASE_URL`; fall back to `DATABASE_URL`; use `--ssh-db deploy@155.133.23.54` for the production VPS when no local tunnel or public read-only URL exists.
- GSC site: defaults to `sc-domain:endmilerouting.co.uk`.
- Bing site: defaults to `https://guide.endmilerouting.co.uk/` with Bing API key `f9541b772ec346ea816b0395881232e0`.
- GA4 property: defaults to `properties/531529105`.
- Google auth: use `GOOGLE_ACCESS_TOKEN` or `gcloud auth application-default print-access-token`; direct CLI tokens need both `https://www.googleapis.com/auth/webmasters.readonly` and `https://www.googleapis.com/auth/analytics.readonly`.
- Local EndMile auth: prefer `--google-cloud-config C:\Users\isaac\.gcloud-endmile-analytics` when running from this workstation. If that token reports insufficient scopes, do not use the default Google Cloud SDK OAuth client for GA4. Google can block `analytics.readonly` on the default client with "This app is blocked". Create/download an EndMile-owned OAuth **Desktop app** client JSON from the Google Auth Platform Clients page for `absolute-cipher-381419`, save it outside the repo as `C:\Users\isaac\.gcloud-endmile-analytics\endmile-oauth-client.json`, and refresh ADC with:

```text
https://console.cloud.google.com/auth/clients?project=absolute-cipher-381419
```

```bash
gcloud auth application-default login --client-id-file=C:\Users\isaac\.gcloud-endmile-analytics\endmile-oauth-client.json --scopes=https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/analytics.readonly,openid,https://www.googleapis.com/auth/userinfo.email
```

For `--surface guide`, the CLI filters GSC and GA4 to `guide.endmilerouting.co.uk` unless a more specific `--page` filter is supplied.

When reporting Guide live-widget rows, resolve `source_id` through `data/venues/master_venues.json` and use venue names in human-facing analysis. Keep the ID only as a parenthetical trace key, for example `Leicester Magistrates' Court (130231837)`, not `Venue 130231837`.

The report covers GSC clicks, impressions, CTR, and position by page/query; GA4 page views and events; API searches by surface, p50/p95 latency, cache hit rate, OJP calls/cost; and opportunity rows such as high-impression low-CTR pages, pages with views but no widget starts, widget errors, and high-cost or slow API pages.

## Analysis And Recommendations

Do not stop at raw GA4/GSC tables. After collecting data, give prioritized recommendations using this order:

1. **Measurement confidence**: State which sources worked and which account/config was used. For the current local setup, GSC uses `C:\Users\isaac\.gcloud-endmile-gsc` as `isaacmwilloughby@gmail.com`; GA4 uses `C:\Users\isaac\.gcloud-endmile-analytics` as `isaacw@endmilerouting.co.uk`.
2. **SEO acquisition**: Lead with GSC and Bing Webmaster Tools totals. Bing Webmaster API provides live daily rank and traffic, queries, landing pages, and indexed page crawl stats. Query+page GSC rows can undercount because Search Console anonymizes or withholds some query rows, so do not treat query+page totals as the canonical SEO total if page-only totals disagree. Compare Bing vs Google trends to detect bot crawl divergences early.
3. **Widget funnel**: Calculate the Guide funnel from GA4:
   - `page_view`
   - `live_widget_view`
   - `live_widget_start`
   - `live_search_start`
   - `live_search_complete`
   - `live_search_error`
   - `route_card_select`
   - `affiliate_click`
   - `cta_click` / `app_cta_click`
4. **Funnel interpretation**:
   - Low `live_widget_view / page_view`: improve widget visibility above the fold, add clearer route-planner affordance, or reduce layout friction.
   - Low `live_widget_start / live_widget_view`: improve origin input placeholder/copy, autocomplete suggestions, and first interaction affordance.
   - High `live_search_error / live_search_start`: inspect affected pages and API telemetry before scaling traffic.
   - `live_search_complete` lower than first-party Guide API searches or vice versa: reconcile GA4 consent/blocking, frontend event emission, and endpoint attribution.
   - Affiliate clicks with very few completed searches: check whether static affiliate CTAs are doing the work, and separate static CTA performance from live route-card monetization.
5. **API health**: Use first-party `endpoint_calls` for Guide live-widget searches, not GA4, when judging real API usage, latency, and cache hit rate. Resolve venue IDs to names in all human-facing recommendations.
6. **Cost caveat**: `api_calls` does not currently carry `client_surface`, so global OJP call counts and estimated cost must not be attributed to Guide unless the code has since added source attribution to `api_calls`.
7. **Action format**: End with 3-5 concrete next actions, ordered by likely impact. Tie each action to a specific metric or page group.

For the current first successful joined run over 2026-07-25 to 2026-08-21, the important GA4 funnel facts were:

- `page_view`: 96
- `live_widget_view`: 28
- `live_widget_start`: 4
- `live_search_start`: 6
- `live_search_complete`: 3
- `live_search_error`: 4
- `route_card_select`: 13
- `affiliate_click`: 5
- First-party Guide API searches: 3, across `Leicester Magistrates' Court (130231837)`, `Royal Armouries (78431237)`, and `Henry Moore Institute (78507133)`.

The default recommendation from that pattern is: improve the widget start rate before scaling pages, investigate live-search errors, keep CTR work focused on pages already receiving impressions, and do not attribute global OJP costs to Guide.

## MCP And External Data

Use MCP paths for agent-assisted exploration when available, especially connected GSC. Treat the CLI as the canonical repeatable path for analysis. GA4 direct access uses the official Data API; local GA4 MCP setup can supplement it when present.

If direct Search Console auth is missing the required scope, use the connected GSC MCP for SEO rows and use the CLI/SSH path for Postgres and GA4 checks. Keep MCPs separate from the CLI because MCP connections are agent-session state, while the CLI should remain runnable from a shell or cron.

## Google Advanced Protection Auth Gate

If GA4 or Search Console OAuth setup fails because the Google account is enrolled in Advanced Protection, stop before retrying tokens or changing CLI code. Open the Advanced Protection page for the user and ask them to unenroll first:

```text
https://myaccount.google.com/u/0/advanced-protection/onboarding?hl=en-GB&rapt=AEjHL4OHB1yft33DzsHsTUf5sbzXycYdMCt-sRaMw8SAZJYtL6AspOZejqTFYTFC87c_ZGUFOaHXu7eVNsWq-H0HOStAZOJgX_YKH_x06edCW4Ki9wPVImY
```

After the user confirms Advanced Protection is off, rerun the scoped ADC setup with an EndMile-owned OAuth Desktop client JSON. Do not retry the default `gcloud` client if Google shows "This app is blocked".

```bash
gcloud auth application-default login --client-id-file=C:\Users\isaac\.gcloud-endmile-analytics\endmile-oauth-client.json --scopes=https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/analytics.readonly,openid,https://www.googleapis.com/auth/userinfo.email
```

Then verify the CLI with:

```bash
node scripts/analytics/guide-performance.mjs --days 1 --surface guide --ssh-db deploy@155.133.23.54 --gsc-google-cloud-config C:\Users\isaac\.gcloud-endmile-gsc --ga4-google-cloud-config C:\Users\isaac\.gcloud-endmile-analytics --markdown
```

If Search Console succeeds but GA4 returns `User does not have sufficient permissions for this property`, inspect GA4 Admin account summaries for the authenticated user before changing OAuth again. If the only returned property is the old Bolivia property (`properties/520442532`) and EndMile (`properties/531529105`) is missing, the OAuth setup is working but the signed-in Google user does not have GA4 access to EndMile. Add the authenticated user to the EndMile GA4 property/account, or rerun ADC with a Google account that already has access.

Current local split-account setup:

- GSC config: `C:\Users\isaac\.gcloud-endmile-gsc`, authenticated as `isaacmwilloughby@gmail.com`.
- GA4 config: `C:\Users\isaac\.gcloud-endmile-analytics`, authenticated as `isaacw@endmilerouting.co.uk`.
- Joined report command:

```bash
node scripts/analytics/guide-performance.mjs --days 28 --surface guide --ssh-db deploy@155.133.23.54 --gsc-google-cloud-config C:\Users\isaac\.gcloud-endmile-gsc --ga4-google-cloud-config C:\Users\isaac\.gcloud-endmile-analytics --markdown
```

Awin, Partnerize, and Google Ads are not v1 adapters in this repo. Mention them as future import/adapters unless code has since been added.

## Validation

For CLI-only changes, run:

```bash
node scripts/analytics/guide-performance.test.mjs
```

For attribution or client-header changes, run the relevant checks from `docs/guides/DEVELOPER_COMMANDS.md`, including server tests, B2C build/tests, and Flutter analyze/format where touched.
