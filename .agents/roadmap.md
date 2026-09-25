# Roadmap

*Last updated: 2026-08-15*

This is the current AI-readable product and go-to-market roadmap. Durable feature plans live in `docs/new-features/` and B2C pivot strategy in `docs/b2c-pivot/`.

## Current Position

EndMile has evolved from a pure consumer journey comparison prototype into a dual-engine commercial platform powered by a self-hosted multimodal routing backend (OSRM, MOTIS, National Rail OJP, UK parking tariffs, and streaming Fastify API):

1. **B2B Team Logistics & Pre-Trip Travel Justification Platform (`app.endmilerouting.co.uk`)**:
   - **Enterprise 2-Page Pre-Trip PDF**: Page 1 Financial & Tax Audit Shield (HMRC 55p AMAP vs direct drive modal comparison, UK VAT 1/6 fuel reclaim under VIT55400, client recharge table, DEFRA 2026 / ISO 14083 carbon reporting) + Page 2 Operational Itinerary (transit timeline with transfer buffer callouts, QR code deep-link, and SHA-256 tamper-evident integrity hash).
   - **Sequential Multi-Event Calendar (.ics)**: Direct browser download of RFC 5545 calendar with per-leg departure alarms (`VALARM`).
   - **Zero-Login Route Snapshot**: Short 8-char share tokens (`/#/s/:token`), anchored desktop menu, and responsive 2-column desktop layout.
2. **B2C Programmatic SEO Engine (`guide.endmilerouting.co.uk`)**: 57k+ eligible UK venues, generating static arrival guides, precomputed regional route matrices, and dynamic live planning widgets. Monetised via parking referrals (JustPark/Awin), train ticket referrals (Trainline/Partnerize), and future display ads.
3. **B2B 'Plan Your Visit' Embeddable Widget SaaS**: The live streaming route planner packaged as an embeddable JS widget for UK theatres, arenas, stadiums, event centres, museums, and universities to solve attendee travel/parking inquiries for £29–£99/month.
4. **Data-as-a-Service (DaaS) Search Telemetry**: Continuous recording of anonymised destination, origin, and mode selection queries in Postgres to build an aggregated UK travel intent dataset for future commercialisation with transport and parking planners.

## Current Focus

Maximize near-term revenue and profitability through the focused three-track strategy:
1. **Track 1 (B2B Pro Planner & Coordinator Dispatch SaaS — £19–£49/mo)**: Package the pre-trip route planning engine into a high-WTP **Pre-Trip Travel Cost Justification & Dispatch Workspace** for UK consultancies and logistics coordinators (e.g. Dorset Software).
2. **Track 2 (B2B 'Plan Your Visit' Venue Widget SaaS — £19–£49/mo)**:
   - **Market Demarcation**: Bypassed 5-figure enterprise tenders (leaving TfGM/arenas to YST); attacking the unserved 99% mid-market.
   - **Prospect Pipeline**: Mined 111k OSM dataset and extracted **4,992 qualified unserved UK venues** with verified websites (954 theatres, 2,418 museums/galleries, 1,197 attractions, 423 universities) into `data/venues/unserved_prospects.csv`.
   - **Active Sales Execution**: Founder is actively working through the structured CSV in Excel, finding named operational decision-makers (Head of Visitor Experience / Operations Director) on LinkedIn and venue staff directories, and executing personalized sniper outreach (10–15/day) using the modular cold email copy in `docs/product/venue-widget-outbound-playbook.md`.
3. **Track 3 (B2C Compounding Passive Income)**: Expand B2C programmatic SEO venue coverage in batches (350 -> 1,000 -> 3,000) earning parking and rail affiliate commissions.

## Now (Phase 3: B2B Pro Monetization, Co-Branded Enterprise Customization & Admin Dashboard Linkage)

- **Stripe Billing & Subscription Engine (`packages/server/`)**:
  - Add `stripe` SDK to Fastify backend (`packages/server/src/interface/routes/billing-routes.ts`).
  - Configure Pro Planner (£19/mo solo coordinator) and Teams (£49/mo up to 3 seats) products.
  - Implement checkout sessions (`POST /billing/checkout-session`), Stripe Customer Portal sessions (`POST /billing/portal-session`), and secure webhook handlers (`POST /billing/webhook`).
  - Apply database migration `025-tenant-subscription-and-branding.sql` for tenant plan, subscription status, seat limits, and branding settings.
- **In-App Quota Paywall & Upgrade Flow (`packages/app/`)**:
  - Enforce 3-lifetime PDF export limit for free users; trigger `UpgradePaywallModal` on the 4th export attempt presenting the £19/mo Pro Planner and £49/mo Teams tiers with client dispute prevention copy.
- **Co-Company Logo Header Addition (White-Label & Co-Branding)**:
  - Add corporate co-branding to `PreTripPdfAuditPage` and `PreTripPdfItineraryPage`: render `[EndMile Logo] | [Client Logo]` with `"Prepared by [Company Name] for Client [Client Code]"`.
  - Add server logo upload endpoint (`POST /tenants/logo`) supporting PNG/SVG storage and public URL persistence.
  - Co-brand `SharedJourneyBanner` on web snapshots with `"Dispatched by [Company Name]"`.
- **Admin Dashboard Linkage (`packages/admin_portal/` & `packages/server/`)**:
  - Wire Flutter Admin Portal to live Fastify API (retire mock settings repository).
  - Enable company profile editing and drag-and-drop logo upload with live preview.
  - Add Billing & Subscription management tab with current plan badge and Stripe Customer Portal link.
  - Enable tenant-wide mileage preset configuration (`55p/mile` HMRC AMAP, `45p/mile` legacy) synced automatically to coordinator mobile/web client apps.
- **Customer Value-Proof Delivery**:
  - Send Paul Hardy (`logistics@dorsetsoftware.com`) the tangible 2-page sample PDF branded with Dorset Software and Poole HQ origin corridors.

## Next

- **Outbound to UK Regional Consultancies**:
  - Target 20–30 Operations Managers / Logistics Coordinators at UK IT, engineering, and environmental consultancies (10–100 employees) with the "client travel recharge dispute prevention" pitch.
- **High-Intent B2B SEO Landing Pages**:
  - Create targeted tools & landing pages: *"HMRC 55p Business Mileage vs Train Cost Calculator"*, *"Client Travel Recharge Justification Template"*.
- **B2B Venue Widget Outreach**:
  - Direct outreach to mid-tier UK theatres, stadiums, and event organizers offering free trial of the "Plan Your Visit" embed.

## Later

- **Coordinator Dispatch Board (`/dispatches`)**:
  - Dedicated desktop dispatch management screen in the app for managing 20+ active consultant deployments, reverse route duplication, and batch client invoice exports.
- **Accounting Reconciliation Export**:
  - CSV / Xero / Sage batch export for monthly client travel recharge invoicing.
- **Venue Widget Self-Serve Onboarding**:
  - Self-serve portal for venue managers to customize colors, preferred car parks, and notices.
- **UK Travel Demand Data-as-a-Service (DaaS)**:
  - Aggregate retained search intent telemetry into quarterly reports for transport and parking operators.

## Not Now

- Broad paid ad campaigns.
- Firm personas based only on the current survey sample.
- Enterprise compliance, ROI, or savings claims without proof.
- Carbon-only positioning.
- Generic multi-stop trip planning.
- A separate marketing repo.
- Fully dynamic no-code policy builders.
- Building sustainability, finance, travel operations, travel agent, or API product paths before feedback selects the first wedge.
- Building multiple portals at once.
- Reworking infrastructure for hypothetical enterprise scale before a wedge and pilot path are clear.

## Product Priority From Existing Feature Plans

The current durable feature-planning order is:

1. Policy guardrails and tenant configuration.
2. Time-window search.
3. Saved-route PDF reports.
4. Group travel coordination.

Reason: these move EndMile from a route search tool toward a corporate travel decision system.

## Shared Platform Roadmap

These foundations are useful across all plausible B2B wedges and can be planned before a final wedge is chosen.

### Phase 0 - Current Demo/MVP

Purpose: prove the route comparison engine and collect feedback.

Current shape:

- Consumer-facing app experience.
- Search and compare route options.
- Personal preferences, not company policy.
- Live on-the-day tracker.
- Saved route foundations.
- Admin portal mocks.

### Phase 1 - Product Quality Foundation

Purpose: make the current app reliable enough to extend into B2B workflows.

Work:

- Improve Flutter UI code structure and state management.
- Reduce brittle widget/provider patterns.
- Make route detail, saved routes, Smart Swap, and live tracking easier to maintain.
- Improve feedback capture around searches, route views, swaps, saves, and live tracker usage.
- Clarify MVP/demo language in product and marketing copy.

Decision rule: stay focused on quality and observability. Do not build wedge-specific features yet.

### Phase 2 - Market Feedback And Wedge Selection

Purpose: choose the first B2B wedge based on real demand, not assumptions.

Feedback targets:

- Sustainability teams.
- Finance teams.
- Travel managers and operations leaders.
- Universities and public-sector departments.
- Event organisers and venues.
- Business parks and regional offices.
- Consultants and client-facing professionals.
- Travel agents or managed travel service providers.
- Potential API consumers.

Questions to answer:

- Who feels the pain strongly enough to change behaviour?
- Who has budget or influence?
- Which route comparison proof creates the strongest reaction: carbon, cost, risk, policy, live tracking, or reporting?
- Does the buyer want a dashboard, a workflow tool, an API, or just better evidence for decisions?
- What existing system would EndMile need to integrate with?

Decision rule: pick one primary wedge before building wedge-specific product, landing pages, or sales collateral.

### Phase 3 - Shared B2B Foundation

Purpose: build the common B2B substrate after feedback confirms the product should move beyond the demo/MVP.

Work:

- Tenant onboarding and company profile.
- Role model: traveller, manager, finance admin, sustainability admin, travel admin, tenant owner, travel agent, platform admin.
- Company policy model and policy versioning.
- Admin portal foundation backed by real APIs.
- SSO-ready auth, then Google Workspace and Microsoft Entra ID.
- Audit logs for policy, reports, exports, and admin actions.
- Report storage and export jobs.
- Saved/shared journey evidence.
- Domain and subdomain plan:
  - app product domain for traveller experience.
  - admin product domain for company portal.
  - API product domain for external consumers.
  - tenant or campaign landing pages once wedge is selected.

Decision rule: build only what supports the chosen wedge plus obvious shared infrastructure.

## Candidate Wedges and Revenue Engines

### 1. Active Primary B2B Wedge: 'Plan Your Visit' Event & Venue Widgets (SaaS)

Hypothesis: UK event venues, theatres, stadiums, arenas, museums, and universities suffer from customer parking confusion, traffic complaints, and support inquiries. They will pay £29–£99/month for a live, branded interactive arrival planner embedded on their "How to Find Us" page.

Value proposition:
- Eliminates visitor arrival confusion and traffic congestion around the venue.
- Provides door-to-door multimodal transit and parking routes from anywhere in the UK.
- Generates affiliate revenue (JustPark / Trainline) inside the venue's own website.
- 2-line embed snippet installation (`<script src=".../widget.js" data-venue="id"></script>`).

### 2. Active Scale Engine: B2C Programmatic Arrival Guides & Affiliate Arbitrage

Hypothesis: Thousands of people search for `how to get to [Venue]`, `[Venue] parking`, and `nearest station to [Venue]` every month. 

Value proposition:
- Hyper-local destination arrival guides backed by real UK parking tariffs, rail fares, and precomputed regional matrices.
- High-margin monetization via JustPark parking referrals (Awin), Trainline rail tickets (Partnerize), and future display ads.
- Zero marginal cost per visitor, compounding over time as search engines index 5k–50k pages.

### 3. Active B2B App Wedge: Team Logistics & Pre-Trip Itinerary Workspace (£19–£49/mo)
*Master Specification: [`docs/product/b2b-pretrip-pdf-justification-and-dispatch.md`](../docs/product/b2b-pretrip-pdf-justification-and-dispatch.md)*

Hypothesis: Logistics coordinators, project managers, and consulting/field service firms (e.g. Dorset Software) dispatch consultants across the UK and need to calculate, compare, and justify door-to-door travel costs (HMRC 55p mileage + parking vs rail + taxis) before journeys happen to prevent client billing disputes and margin leakage.

Value proposition:
- Eliminates manual cross-checking across Google Maps, RAC mileage calculators, Parkopedia, and National Rail.
- **Client Billing Margin Protection & 1-Page PDF Cost Justification**: One-click professional summary pre-emptively proving door-to-door TCO to client AP auditors, attached to client recharge invoices (preventing 1–5% EBTA margin leakage).
- **Zero-Login Consultant Mobile Dispatch**: Clean mobile web itinerary (`/itinerary/[shareToken]`) with calling points, station parking SatNav postcodes, and calendar export.
- **Company Mileage & Rate Presets**: Custom HMRC mileage rates (statutory 55p/25p AMAP, legacy 45p, EV tariffs) and corporate parking rules.
- **Saved Team Route Templates**: Reusable templates for recurring client deployments (e.g. Poole $\to$ Birmingham, Poole $\to$ Manchester, Poole $\to$ London).

### 4. Long-Term Asset: UK Travel Demand Data-as-a-Service (DaaS)

Hypothesis: Retained search query logs (origin postcodes, destination venues, transport mode preferences) form an aggregated UK travel intent dataset that can be sold to transport authorities, parking operators, and outdoor media planners once query volume reaches critical mass.

---

### Secondary / Exploratory Wedges (On-Demand)

### Sustainability Teams

Hypothesis: sustainability teams need proactive carbon reduction, not only annual or retrospective reporting.

Value proposition:

- Help teams reduce business travel carbon before travel decisions are made.
- Compare route-level carbon alongside cost, time, and journey risk.
- Identify where rail, mixed-mode, or different departure choices reduce emissions without creating unacceptable time or risk.
- Move beyond annual carbon reports by showing lower-carbon choices at the point of planning.

Potential product:

- Carbon dashboard by employee, department, route, office, project, or period.
- Scope 3 Category 6 business travel reporting.
- Mode split and direct-drive comparison.
- Carbon reduction opportunities before trips happen.
- Carbon evidence exports and audit notes.
- Tenant settings for carbon targets or budgets.

Risks:

- Sustainability may not own travel behaviour or purchasing.
- Carbon may be a secondary concern behind cost, policy, and convenience.
- Claims need proof and clear data caveats.

### Finance And Expense Teams

Hypothesis: finance teams care about reducing business travel cost before driving, parking, taxis, and mileage claims become expenses.

Value proposition:

- Reduce avoidable travel cost by comparing full door-to-door cost before travel.
- Make driving, mileage, parking, ULEZ, congestion, taxi, rail, and time-cost trade-offs visible.
- Provide expense evidence and policy context before claims are submitted.
- Show where alternatives to driving save money or where driving is genuinely justified.

Potential product:

- Travel cost dashboard by employee, department, office, project, route, or period.
- Mileage, parking, taxi, fare, and surcharge breakdowns.
- Expense-ready route reports.
- Policy caps, warnings, and approval states.
- Export to finance or expense systems later.
- Cost reduction insights versus direct driving or habitual routes.

Risks:

- Finance may only care after expenses are incurred unless policy and approval workflows are strong.
- Savings claims need real usage proof.
- Integration expectations may increase quickly.

### Travel Operations And Policy Teams

Hypothesis: travel or operations teams need a decision layer that helps employees choose policy-compliant, practical routes before booking or travelling.

Value proposition:

- Compare route options against company policy, cost, time, risk, and carbon.
- Reduce inconsistent employee decisions and manual travel guidance.
- Support repeated routes, shared routes, and route evidence.
- Use live tracker data to support on-the-day confidence.

Potential product:

- Company travel policy guardrails.
- Admin-managed preferred modes, cost caps, taxi rules, parking rules, and approval thresholds.
- Employee traveller app with company policy applied.
- Saved route templates for common journeys.
- Live tracking for saved routes.
- Manager approval and exception workflows later.

Risks:

- Existing travel management platforms may already own some workflow.
- Procurement cycles may be longer.
- Policy complexity can grow quickly.

### Travel Agents And Managed Service Providers

Hypothesis: travel agents or travel service providers can use EndMile as a workflow tool to compare routes faster for client companies.

Value proposition:

- Speed up route comparison work for people arranging business travel for others.
- Let agents create evidence-backed route options for clients.
- Support multiple client workspaces and branded reports.
- Reduce manual comparison across maps, rail, taxi, parking, and carbon tools.

Potential product:

- Multi-client workspace.
- Fast route comparison and saved client routes.
- Branded PDF or shareable reports.
- Client-specific preferences or policy profiles.
- Notes, quotes, and handoff links.
- Batch route comparison for repeated client journeys later.

Risks:

- Travel agents may need booking integration, which is not the current product.
- Workflow expectations may differ from corporate self-service.
- Multi-client permissions add complexity.

### API Platform

Hypothesis: other platforms need route-level cost, carbon, risk, and first/last-mile intelligence without building the routing engine themselves.

Value proposition:

- Provide routing, cost, carbon, and journey-risk intelligence as an API.
- Serve expense platforms, sustainability platforms, event platforms, travel tools, and internal corporate systems.
- Let partners embed EndMile's decision layer into existing workflows.

Potential product:

- API keys and developer docs.
- Route comparison endpoint.
- Carbon and cost calculation endpoint.
- Policy evaluation endpoint later.
- Usage limits, rate limits, logs, billing, and status page.
- Webhooks or batch jobs later.

Risks:

- API customers expect reliability, docs, support, versioning, and clear SLAs.
- Monetisation may take longer than self-serve product validation.
- Public API increases security and abuse surface.

## Infrastructure Themes

Plan for these as B2B foundations, but sequence them after product quality and feedback.

- Domains and subdomains for app, admin, API, status, and wedge-specific landing pages.
- Tenant isolation, RLS, and tenant-aware background jobs.
- Role-based access control.
- SSO-ready auth, then Google Workspace and Microsoft Entra ID.
- Audit logging for tenant admin actions.
- Report generation and authenticated file storage.
- API key management and rate limiting.
- Usage analytics for product, API, and tenant activity.
- Billing-ready usage metering.
- Data retention and privacy controls.
- Monitoring, uptime status, and incident process for business customers.

## Success Signals

- Five people test one real route.
- Three testers say EndMile exposed something they would otherwise have checked manually.
- Someone asks for repeated journeys, teams, policy, exports, reports, approvals, or shared planning.
- A target segment describes the problem in their own words without prompting.
- A B2B buyer or operator asks how this would work for their company, team, clients, reports, expenses, policy, or API.
- Feedback clearly favours one wedge over the others.

## Risk Signals

- People like the idea but do not test a real route.
- Feedback centres only on leisure travel or generic mapping.
- Prospects care only about booking tickets, not comparing route decisions.
- Carbon is interesting but not urgent enough to drive action.
- Every segment likes a different part, but none shows urgency.
- Wedge-specific requests arrive before the shared app quality and tenant foundations are ready.
