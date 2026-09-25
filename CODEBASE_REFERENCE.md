# Codebase Reference & Technical Bridge

This document bridges this business repository (`endmile--business`) to the technical application codebase (`endmile-1`).

---

## 1. Codebase Location & Remote

| Attribute | Path / Identifier |
|---|---|
| **Local Absolute Path** | `c:\Users\isaac\Videos\files too big for onedrive\github\endmile-1` |
| **Relative Path** | `../endmile-1` |
| **GitHub Repository** | [`https://github.com/isaacw123434/endmile`](https://github.com/isaacw123434/endmile) |
| **Default Branch** | `main` |

---

## 2. Monorepo Package Directory & Responsibilities

The software is structured as a pnpm monorepo in `../endmile-1`:

```text
../endmile-1/
├── packages/
│   ├── server/             # TS Fastify Backend API (api.endmilerouting.co.uk)
│   ├── b2c_site/           # Astro Programmatic SEO Guide & Widget (guide.endmilerouting.co.uk)
│   ├── app/                # Flutter Mobile & Web Client (app.endmilerouting.co.uk)
│   ├── admin_portal/       # Flutter Web B2B Enterprise Portal
│   └── landing/            # Astro Marketing Landing Site (endmilerouting.co.uk)
├── scripts/
│   ├── analytics/          # Performance & telemetry reporting CLIs
│   ├── batch-router/       # Venue matrix generator & fare extraction
│   └── scrapers/           # OSM data extraction and hazard scrapers
└── data/
    ├── venues/             # Master UK venue database (91MB JSON)
    └── b2c/                # Pre-computed venue matrices and fares
```

---

## 3. Production Deployments & URLs

| Surface | URL | Deployment Platform | Underlying Package |
|---|---|---|---|
| **API Backend** | `https://api.endmilerouting.co.uk` | Contabo VPS (Docker, Caddy reverse proxy) | `packages/server` |
| **B2C Guide & Live Widget** | `https://guide.endmilerouting.co.uk` | Cloudflare Pages / Static Hosting | `packages/b2c_site` |
| **End-User Web Planner** | `https://app.endmilerouting.co.uk` | Contabo VPS (Nginx container via Caddy) | `packages/app` |
| **Public Marketing Site** | `https://endmilerouting.co.uk` | Cloudflare Pages / Static Hosting | `packages/landing` |

---

## 4. Business-to-Code Implementation Bridge

When business, commercial, or marketing strategies in this repository require code updates, reference this mapping:

| Business Need | Where to Implement in Code (`../endmile-1`) | Key Files |
|---|---|---|
| **Update SaaS Pricing or Tiers** | `packages/landing/`, `packages/app/` | `packages/landing/src/pages/pricing.astro`, `packages/app/lib/features/subscription/` |
| **Modify Venue Widget Embed Code** | `packages/b2c_site/` | `packages/b2c_site/src/components/b2c/LiveWidget.astro` |
| **Tweak Pre-Trip Cost Justification PDF** | `packages/server/`, `packages/app/` | `packages/server/src/application/use-cases/generate-trip-pdf.ts`, `packages/app/lib/features/reports/` |
| **Add New Venue or Regenerate Matrix** | `scripts/batch-router/` | `scripts/batch-router/generate-venue-matrix.mjs` |
| **Update HMRC AMAP Mileage Rates** | `packages/server/` | `packages/server/src/domain/entities/tco-policy.ts` |
| **Adjust OJP API Concurrency or Cache** | `packages/server/` | `packages/server/src/infrastructure/external/national-rail/cached-train-planner.ts` |
| **Update Scope 3 DEFRA Carbon Factors** | `data/` | `data/defra-emission-factors-2026.json` |

---

## 5. Working with Both Repositories

- Use **`endmile--business`** for strategic planning, competitor research, sales copywriting, outbound prospect targeting, running performance telemetry CLIs, and financial modeling.
- When an AI agent needs to inspect or edit application code, navigate to `../endmile-1`.
- Always follow the strict Clean Architecture rules and pre-commit checks documented in `../endmile-1/AGENTS.md` before making code changes in that repository.
