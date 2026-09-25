# Analytics & Telemetry CLI Runbook

How to use EndMile's command-line analytics tools to pull live business metrics from Google Analytics 4 (GA4), Google Search Console (GSC), Bing Webmaster Tools, and the production VPS PostgreSQL database.

---

## 1. Overview of Analytics CLIs

Located in `scripts/analytics/`:

| Script | Primary Use | Data Sources |
|---|---|---|
| [`guide-performance.mjs`](../scripts/analytics/guide-performance.mjs) | B2C Venue Guide & Widget traffic, Search Console impressions, Bing indexing, venue searches, OJP costs | GA4, GSC API, Bing Webmaster API, VPS Postgres (`endpoint_calls`) |
| [`app-performance.mjs`](../scripts/analytics/app-performance.mjs) | Flutter app acquisition channels, popular corridors, search failure rates, B2B TCO savings | GA4, VPS Postgres (`endpoint_calls`), GSC, Bing |
| [`submit-indexnow.mjs`](../scripts/analytics/submit-indexnow.mjs) | Instantly submit new venue guide URLs to Bing/Yandex search engines | IndexNow API |

---

## 2. Configuration & Default Properties

The CLIs are pre-configured with default IDs:
- **GA4 Property:** `properties/531529105`
- **Search Console Site URL:** `sc-domain:endmilerouting.co.uk`
- **Bing Site URL:** `https://guide.endmilerouting.co.uk/` (Guide) / `https://endmilerouting.co.uk/` (App)
- **Bing API Key:** `f9541b772ec346ea816b0395881232e0`
- **VPS Host:** `deploy@155.133.23.54` (Database: `endmile`, Container: `postgres`)

---

## 3. Running Guide & Widget Analytics (`guide-performance.mjs`)

### A. Local Run (Bing + Fixtures or Fallback)
```bash
node scripts/analytics/guide-performance.mjs --days 28 --surface guide --markdown
```

### B. Production Live Run (Direct DB Query via SSH)
To pull live `endpoint_calls` records directly from the VPS PostgreSQL container:
```bash
node scripts/analytics/guide-performance.mjs --days 7 --surface guide --ssh-db deploy@155.133.23.54 --markdown
```

### C. Filtering by Specific Venue
```bash
# Check searches and conversions for a specific venue (e.g. Ripon Cathedral)
node scripts/analytics/guide-performance.mjs --venue-id 21285244 --days 30 --markdown
```

### Key Metrics Reported:
- **Total Guide Pageviews & Unique Visitors**
- **Widget Conversion Rate:** Percentage of venue page visitors who performed a live route search.
- **Top Search Corridors:** Which cities visitors are traveling from.
- **OJP API Cost Incurred:** Total pounds/pence spent serving widget searches for that venue.

---

## 4. Running App & Routing Analytics (`app-performance.mjs`)

### A. Bounded 28-Day Channel Breakdown
```bash
node scripts/analytics/app-performance.mjs --days 28 --markdown
```

### B. Production Query over SSH
```bash
node scripts/analytics/app-performance.mjs --days 7 --ssh-db deploy@155.133.23.54 --markdown
```

### C. Corridor & Tenant Filtering
```bash
# Filter for a specific corridor (e.g., Leeds)
node scripts/analytics/app-performance.mjs --days 28 --corridor "Leeds" --markdown

# Filter for a specific B2B corporate tenant
node scripts/analytics/app-performance.mjs --days 28 --tenant-id "00000000-0000-0000-0000-000000000000" --markdown
```

### Key Metrics Reported:
1. **Acquisition Channels:** Traffic split across Direct, LinkedIn Campaigns, Google Organic, Bing Organic, AI Engine Citations (ChatGPT/Perplexity), and B2C Guide CTAs.
2. **Search Reliability:** Total searches, % HTTP 200 success, % 0-result gap, % errors/timeouts.
3. **Corridor Frequency & Quality:** Top origin $\to$ destination pairs with median response time.
4. **Value Realization:** Total £ in TCO travel savings identified vs direct driving and total kg of CO2 saved.

---

## 5. Automated Tests

Run the test suite to verify argument parsing and data transformations:

```bash
npm run test:analytics
# or
node --test scripts/analytics/*.test.mjs
```
