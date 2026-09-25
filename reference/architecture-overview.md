# High-Level System Architecture & Multimodal Pipeline

Architectural reference explaining EndMile's software design, routing engine coordination, and data flows.

---

## 1. System Overview & The Multimodal Pipeline

EndMile is a multimodal travel decision engine for Great Britain. It optimizes routes based on **Total Cost of Ownership (TCO)**, travel time, interchange risk, and carbon emissions rather than just raw travel duration.

### Core Routing Stack

```
               ┌────────────────────────────────────────────────────────┐
               │              Client User / Widget / API                │
               └──────────────────────────┬─────────────────────────────┘
                                          │
                                          ▼
               ┌────────────────────────────────────────────────────────┐
               │           Fastify API Server (packages/server)         │
               │            Clean Architecture (Domain Driven)          │
               └───────┬──────────────┬──────────────┬───────────┬──────┘
                       │              │              │           │
                       ▼              ▼              ▼           ▼
                 ┌──────────┐   ┌──────────┐   ┌──────────┐ ┌─────────┐
                 │   OSRM   │   │  MOTIS   │   │ National │ │   TfL   │
                 │ Driving  │   │ Transit  │   │ Rail OJP │ │ Unified │
                 │ & Cycles │   │  Engine  │   │ Train +  │ │ London  │
                 │ (Local)  │   │ (Local)  │   │  Fares   │ │ Transit │
                 └──────────┘   └──────────┘   └──────────┘ └─────────┘
```

1. **First / Last Mile (OSRM):** Self-hosted Open Source Routing Machine running on the VPS calculates driving or cycling routes from the user's origin to nearby train stations, or from arrival stations to final destinations.
2. **Intercity Middle Leg (National Rail OJP):** National Rail Online Journey Planner API provides train timetables, calling points, platform numbers, and regulated fares across Great Britain.
3. **Regional Transit (MOTIS):** Self-hosted C++ timetable routing engine running on the VPS with GB Traveline National Dataset (TNDS) GTFS data provides buses, trams, light rail, and ferries.
4. **London Transit (TfL Unified API):** Direct integration with Transport for London API for Underground, Overground, DLR, and Elizabeth Line routing.
5. **The Smart Swap Algorithm:** Evaluates combinations (e.g. drive 15 minutes to an out-of-town park-and-ride station with cheaper parking, take express rail, then walk 5 minutes) and compares True TCO vs direct driving.

---

## 2. Monorepo Package Map (in `endmile-1`)

The technical codebase is organized as a pnpm monorepo:

| Package | Technology | Role & Deployment |
|---|---|---|
| [`packages/server`](../../endmile-1/packages/server) | TypeScript, Fastify, PostGIS, Redis | Core routing API, scoring algorithms, telemetry, auth. Deployed to Contabo VPS (`api.endmilerouting.co.uk`). |
| [`packages/b2c_site`](../../endmile-1/packages/b2c_site) | Astro, Tailwind, TypeScript | Programmatic venue guide pages and live interactive widget. Deployed to Cloudflare Pages (`guide.endmilerouting.co.uk`). |
| [`packages/app`](../../endmile-1/packages/app) | Flutter (Dart), Riverpod | End-user mobile app (Android/iOS) and web planner client (`app.endmilerouting.co.uk`). |
| [`packages/admin_portal`](../../endmile-1/packages/admin_portal) | Flutter Web (Dart) | B2B enterprise admin dashboard for travel dispatchers and corporate travel buyers. |
| [`packages/landing`](../../endmile-1/packages/landing) | Astro, Tailwind | Public marketing site, pricing, and B2B product showcase (`endmilerouting.co.uk`). |

---

## 3. Clean Architecture Layers (Server)

The server enforces strict inward-only dependencies:
- **Domain:** Entities (Journey, RouteLeg, TCOEstimate, CarbonMetric), domain failures (`neverthrow` Result types). Zero dependencies on frameworks or libraries.
- **Application:** Use cases (`PlanJourney`, `CalculateTCO`, `ScoreRoutes`). Orchestrates domain logic.
- **Infrastructure:** Adapters (`OsrmDrivingClient`, `MotisClient`, `NationalRailOjpClient`, `PostgresJourneyRepository`, `RedisSearchCache`).
- **Interface / Presentation:** Fastify route controllers, Server-Sent Events (SSE) streaming handlers, Zod schema validation.
