# Phase 1: B2C Programmatic SEO Pivot Strategy

This document synthesizes the strategic reports, brainstorming sessions, and our current infrastructure to map out the exact Phase 1 execution for the B2C pivot.

## 1. Infrastructure Alignment & Data Sourcing

*   **Routing Engines (Zero Variable Cost):** We use our existing VPS running **OSRM** (Open Source Routing Machine) for precise driving routes/isochrones and **MOTIS** (Multi-Objective Traffic Information System) for complex public transit logic. These self-hosted tools allow us to compute millions of routes at zero marginal cost.
*   **Timetable & Cost Logic (Dual API Approach):** 
    *   **The Default Live API:** The interactive "Where are you travelling from?" widget on the site uses the standard EndMile API (powered by live OJP prices and HMRC business driving costs). It computes exact live data for user queries.
    *   The Backend Matrix Scripting API: For the pre-computed static regional tables, we use a private backend script/API that swaps OJP out for our zero-variable-cost MOTIS train provider. This computes static routes en masse (with leisure-focused MPG driving costs) without incurring external API fees. (See Matrix API Usage for payload details).
        *   **[PARTIAL] Train Fares:** MOTIS does not natively return ticket prices. A static fare matrix (`data/railway/b2c_train_fares.json`) covering ~500 UK city pairs exists, but generated venue routes expose exact National Rail CRS station pairs (for example `BHM -> BMH`). The per-venue matrix generator now replaces B2C train estimates with exact static fares when those station pairs exist. After the full matrix run, run `scripts/batch-router/extract-missing-fares.mjs`, fill the missing exact CRS pairs, then run `scripts/batch-router/inject-scraped-fares.mjs`.
*   **Venue & Parking Data (The Anchor):** The true unique value is origin-independent venue logistics. We will research and scrape site-specific parking data (NCP, Q-Park, municipal data, park & rides) and precise walking distances from stations. This static data forms the foundation of every page.

### B2C Routing Modes (The Provider Strategy)
To complement the data and provide actionable comparisons, the B2C widget and batch processor will support the following tailored routing modes:
*   **Public Transit**: Train only, Bus only.
*   **Multimodal Transit**: Drive + Train, Bus + Train.
*   **Drive to Park & Ride**: Driving to a predefined suburban park and ride site, then taking a bus/metro to the venue.
*   **Drive to City Parking (NEW)**: Driving to one of the scraped city centre car parks, then walking or taking local transit to the final venue. This serves as our primary driving recommendation since it uses real, actionable parking data and provides true "information gain."
*   **Direct Drive**: Kept as a baseline comparison ("drive the whole way"), but scaled back in focus for B2C since we do not have guaranteed on-site parking availability for every individual venue door.

## 2. Target Venue Categories (The Niche Strategy)

We will target high-anxiety, unfamiliar, or high-friction destinations. We will apply strict **thresholds** to our scraping to ensure we don't pollute the site with low-friction, everyday places (e.g., small pubs, cafes, or local restaurants).

### Venue Selection Thresholds
A venue must meet at least one of these criteria to be included:
1.  **Capacity Threshold:** Event venues must have a capacity of **> 1,500 people**. (This eliminates places like Hyde Park Book Club, which only holds ~100-200 people, where parking is trivial side-street parking).
2.  **Friction Threshold:** The destination is a rare, high-stress visit where people are willing to research parking in advance (e.g., Hospitals, Jury Duty).
3.  **Dedicated Infrastructure:** The venue has official, paid parking structures.

### The Refined Target List
*   **High Friction / High Value:** Court venues (jury service/hearings), Major Hospitals & Medical Centres, Passport Offices & Embassies (highly stressful, unfamiliar visits), Business parks / Single-employer HQs (interviews, site visits).
*   **Medium Competition (High Volume, High Capacity):** Universities, Conference centres (NEC, ExCeL), Racecourses, Stadiums/Arenas (capacity > 1,500), Major Theatres (e.g., West End, regional grand theatres), Large Retail villages.
*   **Avoid:** Cruise/Ferry terminals, Park & Rides (these are transit hubs used for routing, not the final destination), Prisons, Small music venues/bars (under capacity threshold), Airports, Theme parks.

## 3. Core Defense Against "Thin Content" (Google Penalties)

Google's Helpful Content Update aggressively penalizes programmatic sites that simply swap location names. Our defense is **Information Gain**—synthesizing disparate data points into actionable logistical conclusions.

### The Uniqueness Ratio (QA Publishing Logic)
To prevent indexing bloat and algorithmic penalties, the backend must run a uniqueness check before publishing any generated page.
# Phase 1: B2C Programmatic SEO Pivot Strategy

This document synthesizes the strategic reports, brainstorming sessions, and our current infrastructure to map out the exact Phase 1 execution for the B2C pivot.

## 1. Infrastructure Alignment & Data Sourcing

*   **Routing Engines (Zero Variable Cost):** We use our existing VPS running **OSRM** (Open Source Routing Machine) for precise driving routes/isochrones and **MOTIS** (Multi-Objective Traffic Information System) for complex public transit logic. These self-hosted tools allow us to compute millions of routes at zero marginal cost.
*   **Timetable & Cost Logic (Dual API Approach):** 
    *   **The Default Live API:** The interactive "Where are you travelling from?" widget on the site uses the standard EndMile API (powered by live OJP prices and HMRC business driving costs). It computes exact live data for user queries.
    *   The Backend Matrix Scripting API: For the pre-computed static regional tables, we use a private backend script/API that swaps OJP out for our zero-variable-cost MOTIS train provider. This computes static routes en masse (with leisure-focused MPG driving costs) without incurring external API fees. (See Matrix API Usage for payload details).
        *   **[PARTIAL] Train Fares:** MOTIS does not natively return ticket prices. A static fare matrix (`data/railway/b2c_train_fares.json`) covering ~500 UK city pairs exists, but generated venue routes expose exact National Rail CRS station pairs (for example `BHM -> BMH`). The per-venue matrix generator now replaces B2C train estimates with exact static fares when those station pairs exist. After the full matrix run, run `scripts/batch-router/extract-missing-fares.mjs`, fill the missing exact CRS pairs, then run `scripts/batch-router/inject-scraped-fares.mjs`.
*   **Venue & Parking Data (The Anchor):** The true unique value is origin-independent venue logistics. We will research and scrape site-specific parking data (NCP, Q-Park, municipal data, park & rides) and precise walking distances from stations. This static data forms the foundation of every page.

### B2C Routing Modes (The Provider Strategy)
To complement the data and provide actionable comparisons, the B2C widget and batch processor will support the following tailored routing modes:
*   **Public Transit**: Train only, Bus only.
*   **Multimodal Transit**: Drive + Train, Bus + Train.
*   **Drive to Park & Ride**: Driving to a predefined suburban park and ride site, then taking a bus/metro to the venue.
*   **Drive to City Parking (NEW)**: Driving to one of the scraped city centre car parks, then walking or taking local transit to the final venue. This serves as our primary driving recommendation since it uses real, actionable parking data and provides true "information gain."
*   **Direct Drive**: Kept as a baseline comparison ("drive the whole way"), but scaled back in focus for B2C since we do not have guaranteed on-site parking availability for every individual venue door.

## 2. Target Venue Categories (The Niche Strategy)

We will target high-anxiety, unfamiliar, or high-friction destinations. We will apply strict **thresholds** to our scraping to ensure we don't pollute the site with low-friction, everyday places (e.g., small pubs, cafes, or local restaurants).

### Venue Selection Thresholds
A venue must meet at least one of these criteria to be included:
1.  **Capacity Threshold:** Event venues must have a capacity of **> 1,500 people**. (This eliminates places like Hyde Park Book Club, which only holds ~100-200 people, where parking is trivial side-street parking).
2.  **Friction Threshold:** The destination is a rare, high-stress visit where people are willing to research parking in advance (e.g., Hospitals, Jury Duty).
3.  **Dedicated Infrastructure:** The venue has official, paid parking structures.

### The Refined Target List
*   **High Friction / High Value:** Court venues (jury service/hearings), Major Hospitals & Medical Centres, Passport Offices & Embassies (highly stressful, unfamiliar visits), Business parks / Single-employer HQs (interviews, site visits).
*   **Medium Competition (High Volume, High Capacity):** Universities, Conference centres (NEC, ExCeL), Racecourses, Stadiums/Arenas (capacity > 1,500), Major Theatres (e.g., West End, regional grand theatres), Large Retail villages.
*   **Avoid:** Cruise/Ferry terminals, Park & Rides (these are transit hubs used for routing, not the final destination), Prisons, Small music venues/bars (under capacity threshold), Airports, Theme parks.

## 3. Core Defense Against "Thin Content" (Google Penalties)

Google's Helpful Content Update aggressively penalizes programmatic sites that simply swap location names. Our defense is **Information Gain**—synthesizing disparate data points into actionable logistical conclusions.

### The Uniqueness Ratio (QA Publishing Logic)
To prevent indexing bloat and algorithmic penalties, the backend must run a uniqueness check before publishing any generated page.
$$ Uniqueness\ Ratio = \frac{Unique\ Fields\ Count}{Total\ Fields\ Count} $$
**Rule:** A page is only published if it passes the composite publish-readiness gate. The gate combines routing density, transport-column coverage, generated content, FAQ depth, semantic fact count, and OSM/master provenance instead of relying on one hard fact-count threshold.

## 4. UX/UI & Page Structure Blueprint

The page layout must appease the user, hold retention, and satisfy search engine crawlers with server-rendered content.

1.  **Arrival Guide (The Anchor):** Server-rendered details about official parking options, capacities, advertised costs, and precise station walk times. This provides immediate Information Gain based on factual, scraped data. Parking affiliate links belong exactly here as alternatives.
2.  **The Interactive "Hook" (Above the Fold):** A simple "Where are you travelling from?" postcode/town box. Do not force geolocation, offer it as an optional shortcut. When used, the live API calculates the exact door-to-door route.
3.  **Retention Mechanics (Interactive Sliders):** To maximize "Time on Page", include interactive toggles alongside the data tables and live widget. For example: a "Number of Passengers" toggle, "Adjust Vehicle MPG" slider, and a "Business vs Leisure" toggle (HMRC rates vs MPG fuel costs). Both the static tables and the live widget must be dynamically recalculable purely on the client side (using `baseParkingCost`, `distanceMetres`, and `baseTrainFare` embedded in the dataset/API response).
4.  **Regional Origin Table (Server-rendered Data):** A static table showing pre-calculated drive/train times from 4-6 common regional origins using the Backend Matrix API. This gives Google crawler real content and catches generic search intent.
5.  **Last Leg Interactive Map:** Each venue page will display a map highlighting the final "last mile" leg of the journey (e.g., walking path from the closest train station, bus station, or city car park to the venue doors) by decoding the `encodedPolyline` supplied by the backend routing API.
6.  **Authentic FAQs:** Real questions scraped from sources like TripAdvisor, rather than generic templated Q&As.
7.  **Affiliate Links & Monetization Placement:**
    *   **Parking Affiliates (JustPark via Awin):** Placed in parking CTAs around the Arrival Guide, regional matrix, and live widget results. Present official/static parking data neutrally, then offer a clearly disclosed "pre-book parking" action. Phase 1 uses verified venue-to-JustPark destination mappings where available and falls back to the generic JustPark parking page; it does not claim live JustPark availability or scrape JustPark inventory.
    *   **Ticketing Affiliate (Trainline via Partnerize):** Placed inside the "Regional Origin Table" and the output of the "Interactive Postcode Tool" (for example, a clearly disclosed "Buy tickets on Trainline" link next to the calculated train time). Track the product category so commission reporting can distinguish standard bookings, railcards, and rail passes.
    *   **Display Ads:** Premium networks (Setupad/MonetizeMore) for sticky sidebars.

### Verified Affiliate & Media Rate Cards

#### 1. JustPark Awin Rate Card (Advertiser 6188)
*Snapshot recorded 2026-08-15:*
- **Bookings by new customers:** 20.00%
- **Bookings by existing JustPark customers:** 5.00%
- **Space Listings:** GBP 7.50
- **Default rate:** 5.00%
- *Average basket: £15.00 $\to$ Blended commission ~£1.43 / booking (assumes 70% existing / 30% new).*

#### 2. Trainline Partnerize Rate Card
*Snapshot recorded 2026-08-15:*
| Campaign configuration | CPA rate | Notes / Example Payout |
|---|---:|---|
| UK Railcard — new customer | 20.00% | ~£6.00 payout on £30 1-yr railcard |
| UK Railcard — existing customer | 7.00% | ~£2.10 payout on £30 1-yr railcard |
| EU Railcard — new customer | 20.00% | Active |
| EU Railcard — existing customer | 7.00% | Active |
| FlixBus | 2.00% | Active |
| Eurail / Swiss Pass | 4.00% | Active |
| Interrail Pass | 2.50% | Active |
| Pass Rail (France) | 1.45% | Active |
| Season Tickets | 0.00% | Active (`0% Commission Season`) |
| Default (Standard Train Tickets) | 0.50% | ~£0.23 payout on £45 avg return basket |

#### 3. Display Ads (Google AdSense Baseline)
- Category: Travel & Transportation (EMEA).
- Official AdSense benchmark: 50,000 monthly page views $\approx$ $1,900 / year (~$3.16 RPM / ~£2.50 RPM).

---

### Conservative Financial Model (38,000 Published Venue Pages)

Based on a conservative long-tail distribution across 38k UK venue arrival guides (~3.6 visits/page/mo = ~136.4k visits / ~163.7k pageviews/mo):

| Revenue Stream | Basis / Conversion Assumptions | Monthly Revenue | Annual Revenue |
| :--- | :--- | :---: | :---: |
| **Google AdSense Ads** | 163.7k pageviews @ £2.50 RPM | **£409.25** | £4,911.00 |
| **JustPark Parking (Awin)** | 81.8k driving visits $\to$ 3.5% CTR $\to$ 3.5% CVR (100 bookings @ £1.425 blended) | **£142.90** | £1,714.80 |
| **Trainline Rail (Partnerize)** | 40.9k rail visits $\to$ 3.0% CTR $\to$ 5.0% CVR (61 bookings @ £0.225 ticket + £19.89 railcards) | **£33.71** | £404.50 |
| **TOTAL GROSS REVENUE** | **Combined 38,000 page conservative estimate** | **£585.86 / mo** | **£7,030.30 / yr** |
| Infrastructure (VPS Hosting) | Fixed monthly server cost | -£50.00 / mo | -£600.00 / yr |
| **NET OPERATING PROFIT** | **Net margin: 91.5%** | **£535.86 / mo** | **£6,430.30 / yr** |

*Growth & Optimization Potential:*
- **Moderate Traffic Case (7.5 visits/page/mo = ~340k PV)**: **~£1,167/month net profit** (~£14,000/yr).
- **Premium Ad Network Tier (Mediavine Journey/Setupad @ £14 RPM on 340k PV)**: **~£4,500+/month net profit** (~£54,000/yr).

## 5. Technical Roadmap & Execution Plan

Based on a detailed analysis of the existing monorepo (`@endmile/server`, `@endmile/landing`), here is the comprehensive end-to-end process required to launch the B2C programmatic SEO strategy:

### A. Advanced Data Acquisition Pipeline
1.  **Venue Discovery & Enrichment (The "Information Gain" Engine):**
    *   **[DONE] Seed List Generation:** Build an automated scraper to pull a comprehensive list of "High Friction" UK venues (Hospitals, Arenas, Universities, Courts) rather than manually curating them. The master venue list is generated.
    *   **Enrichment Script:** Build an automated pipeline (e.g., using an LLM via the Gemini API) to crawl official venue arrival pages, TripAdvisor, and Reddit to extract *non-obvious* transit advice (e.g., "Don't use the South Entrance on match days," or "The walking path from the station is unlit at night"). 
2.  **[DONE] Parking Scraper Microservices (`scripts/scrapers`):** 
    *   Completed scraping city centre parking providers (NCP, Q-Park, CitiPark, APCOA, local councils). Data extracted and merged into static JSON.

### B. Monorepo Server Modifications (`@endmile/server`)
*Adapting the existing Fastify API for the B2C widget.*

#### What `plan-journey.ts` Already Builds (All Modes Below Are Live)
The existing `plan-journey.ts` orchestration engine already supports all of our core B2C modes in parallel. No routing logic needs to be invented from scratch:
*   **Direct Transit** (`generateProviderLegs` -> MOTIS): Bus only, Train only, direct point-to-point.
*   **Multimodal Transit** (first-mile/last-mile hub architecture): Walk -> Train -> Walk, Bus -> Train -> Walk, Drive (to local station) -> Train -> Walk, etc.
*   **Park & Ride** (`generateParkAndRideJourneys`): Drive to a predefined suburban P&R site -> bus/metro into city. Uses `park-and-ride/sites.json` as the hub source. Applies parking cost + buffer.
*   **Direct Drive** (`generateDirectDrive` -> OSRM): Full origin-to-destination driving baseline. Currently gated behind a `MIN_DIRECT_DRIVE_METRES` threshold (>=10 km) and scaled back for B2C.

#### [DONE] Drive to City Parking + Walk/Transit
A new generator `generateDriveToCityParkingJourneys` has been added to `plan-journey.ts`:
*   **Hub Source:** Loads scraped city centre car parks from `data/city_parking/parking.json`, filtered to those within a configurable radius of the destination venue.
*   **Drive Leg:** OSRM route from user origin -> chosen city car park.
*   **Parking Cost:** Injects the scraped `basePrice` from the JSON directly onto the drive leg cost.
*   **Last-Mile Leg:** Walk or short local transit from car park -> venue doors.
*   **Prioritisation:** This mode is surfaced as the primary driving recommendation on B2C pages, above Direct Drive, since we have real, verified parking data backing it.

#### [DONE] Request-Scoped Train Planner / Dual Routing
*   Concurrent initialization of `OjpTrainPlanner` (live National Rail timetables and ticket prices for standard routing) and `MotisTrainPlanner` (zero-marginal-cost static timetable datasets on port 8081 for B2C matrix routing).
*   Requests are dynamically routed request-scopedly via `DelegatingTrainPlanner` based on the `routingProfile` parameter (`default` vs `b2c_matrix`).

#### Remaining Server Tasks
1.  **Live Widget Endpoint Hookup:** The B2C live widget calls the production streaming journey endpoint (`POST /journeys/search/stream`) with `routingProfile: "default"` and `includeCityParking: true`, after resolving the user's origin via `/autocomplete` and `/places/:placeId`. The older `GET /api/public/v1/routes/compare` route exists as a public REST wrapper, but it is not the implemented live-widget path.
2.  **Cost Estimation Engine:** Keep live-widget cost logic on the default API path (live OJP fares and HMRC/business defaults), while client-side B2C controls can recalculate display prices from returned distance, parking, passenger, MPG, and purpose metadata.
3.  **CORS & Security:** Ensure the production API allow-list and Cloudflare/WAF rules include the consumer subdomain for `/autocomplete`, `/places/:placeId`, and `/journeys/search/stream` before launch.

### C. The Batch Processing Pipeline (OSRM & MOTIS)
*Generating the pre-computed static regional data.*

1.  **The Origin Matrix:** Compile a static list of the ~500 most populous UK towns and cities with their exact geographical centroids (loaded from `data/city_parking/city_centres.json`).
2.  **Nearby City Selection (NEW focus):**
    *   Write an algorithm/script to identify the **5 closest cities** from our Origin Matrix to any target destination venue based on coordinate distance (e.g. Haversine).
3.  **[DONE] Batch Routing Script (`scripts/batch-router/generate-venue-matrix.mjs`):**
    *   A Node.js worker that iterates over the `master_venues.json`. With the current selector, `generate-venue-matrix.mjs --limit 0` reported 57,409 qualifying matrix-eligible venues out of 111,233 total master venues on 2026-08-10.
    *   Inject the scraped parking data into the static "Arrival Guide".
    *   Port the Vanilla JS interactive logic into a client-side reactive component (e.g., React/Preact/Svelte) that hits the new public Fastify API endpoints, passing the `includeCityParking: true` flag to display useful parking alternatives with pricing.
    *   Build client-side sliders (passengers, MPG, business vs leisure) that dynamically update prices in the browser using the returned metadata.
    *   Integrate a map component to highlight the final last-mile leg using the encoded polyline.
4.  **SEO Best Practices & Sitemaps (NEW focus):**
    *   Ensure proper structured data schemas (FAQ, Organization, LocalBusiness/Venue) are present.
    *   Implement title tags, meta descriptions, unique page ratio validation, and clean hierarchical headings (`<h1>` to `<h3>`).
    *   Generate a dynamic `sitemap.xml` for all programmatic B2C venue pages.
5.  **The Uniqueness Gatekeeper:** Run the publish gate during the final Astro build after matrix data, exact train fares, parking/last-mile data, and generated content have all been injected. If a venue page lacks enough routed origins, fare coverage, parking/last-mile detail, or venue-specific copy, `getStaticPaths()` omits it and the sitemap excludes it.
6.  **JustPark/Awin Affiliate Layer:** The B2C site reads `data/affiliates/parking_destinations.json` at build time. Mapped venues use a verified JustPark destination URL; unmapped venues use `https://www.justpark.com/uk/parking/`. The generated outbound URL uses `https://www.awin1.com/cread.php?awinmid=6188&awinaffid=3016279&clickref=venue_<venueId>&ued=<encoded JustPark URL>`. Do not generate JustPark slugs by assumption. Future improvement is a richer resolver hierarchy (exact venue, postcode/area, city, generic) or an authorised JustPark partner feed/API.

### E. API Resilience & MOTIS Resolution
*During the execution of Phase 1, we encountered significant resilience issues when routing via MOTIS.*

1. **CRS to TIPLOC Translation Bug**: 
   * **Issue:** MOTIS expects `TIPLOC` station codes, but our internal system operates strictly on National Rail `CRS` codes. The `CrsLookup` service was missing reverse translation methods (`resolveTiploc` and `resolveCrsFromTiploc`), causing the production server to fail its TypeScript build and silently fail during routing.
   * **Resolution:** We implemented comprehensive CRS-to-TIPLOC mapping in `InMemoryCrsLookup`, allowing the `MotisTrainPlanner` to correctly format queries and decode responses.
2. **Missing Modes**: 
   * **Issue:** Our payload to MOTIS only requested `routeType: 0` (High Speed/Long Distance). It failed to find regional routes because it omitted `routeType: 2` (Regional Rail).
   * **Resolution:** We injected `REGIONAL_RAIL` and `routeType: 2` into the query payload, allowing MOTIS to return local and regional train itineraries.
3. **Silent Failures**:
   * **Issue:** Empty arrays from MOTIS were silently swallowed, making debugging impossible.
   * **Resolution:** Added explicit `errMessage` logging to the `MotisTrainPlanner` to surface issues with the proxy or payload.
4. **Coordinate Fallback for Train Stations (Origin Snapping)**:
   * **Issue:** The `b2c_matrix` routing profile sent raw lat/lon coordinates to MOTIS for the origin. While this works for OSRM, MOTIS v5 strictly requires exact `StopId` (station code) strings to successfully return journeys, otherwise it throws `noJourneysFound`.
   * **Resolution:** We updated the `plan-journey.ts` orchestration layer to look up the nearest 5 rail hubs from the `CrsLookup` service for the origin coordinates, injecting the mapped `StopId` values into MOTIS.
5. **London Park & Tube Unlock**:
   * **Issue:** Generating matrix routes towards London venues was timing out and breaking the batch pipeline due to complex TfL (Transport for London) routing constraints.
   * **Resolution:** TfL Park & Tube server routing is now validated. London destination venues are eligible in `generate-venue-matrix.mjs`; routes use verified Saba/TfL station car parks, rail-style TfL onward modes, positive TfL Journey Planner fares, and preserved walk/transit geometry.
   * **Operational note:** London/M25 cities remain excluded as matrix origin rows so London venue pages compare useful inbound regional origins rather than local London-to-London trips.
6. **MOTIS Queue Health Backoff**:
   * **Issue:** Large matrix batch runs could overwhelm the MOTIS engine, leading to timeouts and dropped routes.
   * **Resolution:** Added a MOTIS queue health check endpoint and integrated a backoff mechanism into the batch CLI to pause processing when MOTIS is saturated.

The API is now verified on the VPS, successfully generating multileg journeys (walking -> train -> walking) and Park & Ride journeys (drive -> tram) using live MOTIS datasets at zero marginal cost.

### F. Implementation Learnings and Open Issues

**1. Resolved: MOTIS Station Code Mapping**
During implementation, we discovered that MOTIS returns `TIPLOC` stop codes for intermediate train legs rather than National Rail `CRS` codes. This caused the planner to crash when attempting to map stops. We implemented `resolveCrsFromTiploc` in `InMemoryCrsLookup` to correctly map MOTIS `TIPLOC` codes to `CRS` codes.

**2. Resolved: Train Planner Interface Mismatch (Zero Trains Returned)**
We resolved the interface mismatch by implementing request-scoped train routing. In `composition-root.ts`, both OJP and MOTIS train planners are concurrently initialized. The `DelegatingTrainPlanner` maps constraints dynamically: standard routing (`routingProfile === 'default'`) is sent to `OjpTrainPlanner` (via `CachedTrainPlanner`), returning full timetables and fares. Matrix routing (`routingProfile === 'b2c_matrix'`) is sent to `MotisTrainPlanner` (port 8081). This guarantees that standard searches (e.g. on the Flutter app) successfully return trains, while B2C matrix routing runs at zero marginal cost.

### G. Remaining TODOs (Next Steps)

With the B2C routing engine deployed and the matrix data pipeline passing small production test batches (`generate-venue-matrix.mjs --limit 10`, `--limit 11`, and a hotel `--limit 20` smoke run), the next step is the full data run, fare backfill, content enrichment, and final Astro publish gate.

- [ ] **Deploy B2C Site Infrastructure:** The VPS-hosted `b2c-site` Docker image, Caddy host for `guide.endmilerouting.co.uk`, deploy wiring, API CORS allow-list, and SSG cookie/GA4 consent wrapper are in place. Remaining before sign-off: add GitHub secret `GA4_MEASUREMENT_ID=G-EW6G2GYXJE`, redeploy the B2C image so the static build includes the stream ID, verify GA4 events in DebugView/Realtime, and update terms/privacy/cookies copy for B2C GA4, affiliate links, Google Places/autocomplete, live route searches, and the root landing PostHog-vs-GA4 wording mismatch.
- [ ] **Run Full Matrix Pipeline:** Execute the matrix generation script across the current post-London-unlock qualifying venue set to populate the `data/b2c/venues/` directory. The CLI is resumable and skips existing venue files unless `--force` is used.
- [x] **Implement TfL Park & Tube Before London Matrix Expansion:** London destinations are now eligible after server routing produced realistic Park & Tube rows from verified outer London / TfL station car parks, positive live TfL Journey Planner fares, and Tube/Elizabeth line/DLR/Overground transfer legs.
- [ ] **Extract and Inject Exact Train Fares:** Run `scripts/batch-router/extract-missing-fares.mjs`, fill exact CRS-pair fares into `data/railway/b2c_train_fares.json`, then run `scripts/batch-router/inject-scraped-fares.mjs`.
- [ ] **Content Enrichment:** Run the separate Gemini/content pipeline after matrix and fare injection so the final pages have venue-specific qualitative content.
- [ ] **Astro SSG Build:** Use the dedicated `packages/b2c_site` package to build the B2C homepage, region hubs, city hubs, and venue pages from generated JSON files in `data/b2c/venues/`.
- [DONE] **Final Data Gatekeeping:** `validateVenueData()` now applies the composite publish-readiness gate during `getStaticPaths()` and sitemap generation, while `scripts/batch-router/audit-publish-readiness.mjs` writes `data/b2c/publish_readiness_report.json` and `data/b2c/publish_candidates.txt` so expansion beyond `published_venues.txt` stays deliberate.
- [ ] **Build the Regional Origin Table Component:** Create the static UI table directly mapping the JSON data (directDrive, driveToCityPark, parkAndRide, trainWalk) into comparison columns.
- [ ] **Build the Arrival Guide Component:** Create a static UI component displaying the scraped official parking options, prices, and precise walk times.
- [ ] **Client-Side Widget Integration:** Port the Vanilla JS interactive "Where are you travelling from?" tool into a reactive framework (e.g., React/Preact/Svelte) and embed it on the Astro page to hit the live API endpoints.
- [ ] **Map & Polyline UI:** Integrate a map component to decode and render the `encodedPolyline` for the final last-mile walk/transit leg.
- [ ] **SEO / AI-SEO Layer:** Generate `sitemap.xml`, `robots.txt`, canonical URLs, title/meta descriptions, JSON-LD, and static extractable content for search engines and AI answer engines.

---

## 6. Traffic & Monetization Projections (AdSense)

Based on Google AdSense estimates for the UK Travel/Transport sector, we can project potential earnings for Phase 1. 

**AdSense Baselines (Estimated UK averages):**
- 50,000 page views per month ≈ $1,900 yearly earnings
- 10,000,000 page views per month ≈ $390,000 yearly earnings
*(This scales highly linearly at roughly $0.038 - $0.039 yearly earnings per monthly view).*

**Phase 1 Projections (57,409 Matrix-Eligible Venues):**
- **Qualifying Venues Generated:** 57,409
- **Conservative Traffic Estimate:** 50 organic views per venue per month
- **Total Monthly Page Views:** 2,870,450

**Calculation:**
- `(2,870,450 / 10,000,000) * $390,000 = $111,947 yearly earnings`
- Converted to GBP (~0.78 exchange rate): **£87,300 yearly passive income.**

This does *not* include affiliate conversions from parking partners or Trainline through Partnerize, which will run concurrently alongside display ads. Apply the category-specific Trainline rates above rather than a single blended commission assumption when producing affiliate forecasts.
