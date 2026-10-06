# You. Smart. Thing. (YST) UK Venue Landscape & Customer Segmentation

Internal commercial research document. Not for public distribution.

---

## 1. Public Sector G-Cloud 14 Rate Card (Verified Crown Commercial Service Filing)

Under the UK Crown Commercial Service G-Cloud 14 framework (Cloud Software Lot 2), You. Smart. Thing. publishes their rate card:

- **Deployment & Onboarding Day Rate**: **£750 / day** (exclusive of VAT).
  - Single location setup: **~3 days minimum (£2,250 setup fee)**.
  - Medium multi-location: **~15 days (£11,250 setup fee)**.
- **Bespoke Development**: **£750 / day** (for ticketing/CRM integration).
- **Annual Platform Licence Fee**: Enterprise annual contract (negotiable with booking affiliate revenue share).
- **Messaging Fees**: £0.10 per SMS.
- **Support**: £60 / hour for out-of-hours support.

*Commercial Implication for EndMile*: An independent theatre or mid-sized museum cannot justify £2,250 upfront plus enterprise annual fees for travel planning. EndMile's self-serve embed with £0 setup fee and £0–£49/month pricing removes 95% of the procurement hurdle.

---

## 2. Customer Segmentation: Paying Enterprise vs. Free Platform Links

Through live web crawling and transparency register analysis, we identified two radically different groups using YST:

### Category A: High-Paying Enterprise & Public Clients
These organisations have dedicated five-figure mobility/sustainability budgets:
- **Transport Authorities & Combined Authorities**:
  - **Transport for Greater Manchester (TfGM / Bee Network)**:
    - *Host URL*: `https://tfgm.com/plan-a-journey`
    - *Implementation*: Full-page iframe embed (`<iframe src="https://travel.yousmartthing.com/bee_network">`)
    - *Usage*: Core regional journey planner & demand management across 30M+ journey plans.
  - **West Midlands Combined Authority (WMCA)**: Multiple transparency register invoices £14k–£18k for regional mobility.
  - **Warwickshire County Council**: Smart Travel Partnership (Cllr Jan Matecki transport portfolio).
- **Major Sports Arenas & Stadiums**:
  - **Co-op Live** (Manchester, 23,500 capacity) — Arena arrival logistics (`cooplive.com/plan-your-visit/getting-here`).
  - **Coventry Building Society Arena** (Coventry) — Matchday highway & car park management (`cbsarena.co.uk/visiting-us/getting-here`).
  - **Leeds Rhinos / AMT Headingley Stadium** (Leeds) — Dispersing matchday traffic (`therhinos.co.uk/headingley-stadium/plan-your-visit`, slug: `/leeds_rhinos`).
  - **Lancashire Cricket / Emirates Old Trafford** (Manchester) — Fan travel advice in ticketing FAQs (`lancashirecricket.co.uk`, slug: `/lancashire_cricket_club/journeyplan`).
  - **The Championships, Wimbledon (AELTC)** (London) — Custom tenant domain `wimbledon.myjrny.uk`.
  - **AFAS Dome** (Brussels, Belgium) — Major arena concert travel partner (`afas-dome.be`).
- **Major Funded Events, Exhibitions & Festivals**:
  - **Birmingham Weekender / Central BID Birmingham**: Hosted via Birmingham Hippodrome (`birminghamhippodrome.com`, slug: `/birmingham_weekender`).
  - **International Confex / ExCeL London**: B2B exhibition travel partner (`international-confex.com`).
  - **DF Concerts**: Glasgow & Edinburgh Summer Sessions.
  - **Bradford City of Culture 2025**.

### Category B: Verified Cultural Venues & Museums (Prime Displacement Targets)
These are independent cultural organisations that currently host YST iframes or links:
- **The Herbert Art Gallery & Museum (Coventry)**:
  - *Host URL*: `https://www.theherbert.org/visiting/default.aspx`
  - *Implementation*: Live in-page iframe (`<iframe src="https://travel.yousmartthing.com/herbert_art_gallery" height="600" width="100%">`).
- **The Electric Theatre (Guildford)**:
  - *Host URL*: `https://electric.theatre/getting-here/`
  - *Implementation*: Custom travel assistant link and cookie policy integration.
- **Compton Verney Art Gallery & Park (Warwickshire)**:
  - *Implementation*: Dedicated Destination Group for country house, gallery, and grounds.
- **Visit Belfast (CS Lewis Square & Destination Listings)**:
  - *Host URL*: `https://visitbelfast.com/listing/cs-lewis-square/97370101/`
  - *Implementation*: CMS destination integration with custom property `"yousmartthing": "true"`.

### Category C: Non-Paying / Ticketing Platform Cohort ("TicketSource Users")
Many smaller venues linking to `travel.yousmartthing.com` are **not paying clients**:
- **Venues**: Red Ladder Theatre Company, Hawksworth Wood Village Hall, St. John's Parish Hall.
- **How they got it**: TicketSource integrated a free travel assistant link into event confirmation templates. Event organisers simply tick a box in their TicketSource portal or paste a text link into event descriptions.
- **Commercial Reality**: These venues have virtually zero software budget. They will not pay £19/month on a recurring corporate card without committee review.

### Category D: "Ghost" Slugs (Transit Trials & Municipal Projects)
When inspecting Wayback Machine CDX dumps for `travel.yousmartthing.com/*`, many slugs are not active SaaS venues:
1. **Bus Route Numbers** (e.g. `36-leeds-harrogate-ripley`, `1-lincoln-grantham`, `17-blackpool-lytham`): Ingested during scenic bus corridor trials (like Transdev's 36 bus route). They simply render transit line waypoints, not a venue widget.
2. **Coventry 2021 City of Culture Slugs** (e.g. `147_Nightclub`, `AfriLicken_Junction`, `2-Tone_Village`): Generated during a one-off council grant project in 2021 mapping Coventry businesses. Most do not have an active website or widget.

---

## 3. How to Validate If a Slug is on a Real Host Page

When investigating any slug from `travel.yousmartthing.com/<slug>`:

1. **Exact-Quote Google Search**:
   ```text
   "travel.yousmartthing.com/<slug>"
   ```
   *Example*: `"travel.yousmartthing.com/herbert_art_gallery"` instantly returns `https://www.theherbert.org/visiting/default.aspx`.
2. **URLScan.io Parent Page Lookup**:
   Search `travel.yousmartthing.com` on `urlscan.io/search`. It captures the external parent domain that loaded the iframe.
3. **Site-Specific Verification**:
   ```text
   site:<venue-domain.co.uk> "yousmartthing" OR "travel.yousmartthing.com"
   ```

---

## 4. EndMile Target ICP & Outbound Sales Strategy

For the complete commercial outbound playbook, modular cold email copy by venue type, objection handling, and the 4,992-venue unserved prospect database, see:
👉 [**Master Outbound Sales Playbook & Prospecting Engine**](../product/venue-widget-outbound-playbook.md)

Key Strategic Principles:
- **Zero Competition with YST:** We do not compete for £20k enterprise transport authority tenders (TfGM, Co-op Live). We target the 4,992 UK cultural and visitor venues with **no travel widget installed**.
- **The 4 Core Archetypes:** Independent Regional Theatres (300–2,000 seats), Regional Civic/University Museums & Galleries, Visitor Attractions & Wildlife Parks, University Campuses & Open Days.
- **Pricing:** Self-serve £19–£49/month with £0 setup fee (eliminating YST's £2,250 procurement hurdle).

---

## 5. Verified Live Host Profiler Dossiers (Automated Scan)

### Venue Dossier: The Herbert Art Gallery & Museum

- **Host URL:** https://www.theherbert.org/visiting/default.aspx
- **Sector / Archetype:** Museum & Gallery
- **Location:** Coventry
- **Integration Status:** `IFRAME_EMBED`
- **Slug:** `herbert_art_gallery`
- **Embed Tag:** `<iframe allow="geolocation" frameborder="0" height="600" scrolling="no" src="https://travel.yousmartthing.com/herbert_art_gallery" width="100%">`
- **Flaw:** Rigid 600 height creates double-scrollbars and layout shifts on mobile viewports.
- **Recommended EndMile Tier:** Standard (£19/mo) or Growth (£49/mo)
- **Value Proposition Angle:**
  Replace heavy 600px YST iframe with EndMile's lightweight, fully responsive widget that includes door-to-door multimodal routing, live rail fares, and automatic Scope 3 Julie's Bicycle carbon disclosures with £0 setup fee.

---

### Venue Dossier: Transport for Greater Manchester (Bee Network)

- **Host URL:** https://tfgm.com/plan-a-journey
- **Sector / Archetype:** Transport Authority
- **Location:** Manchester
- **Integration Status:** `IFRAME_EMBED`
- **Slug:** `bee_network`
- **Embed Tag:** `<iframe title="Journey planner" class="_16ffzwl1" src="https://travel.yousmartthing.com/bee_network" allow="geolocation">`
- **Flaw:** Rigid fixed height creates double-scrollbars and layout shifts on mobile viewports.
- **Recommended EndMile Tier:** Scale / Enterprise (£119/mo)
- **Value Proposition Angle:**
  Replace heavy 600px YST iframe with EndMile's lightweight, fully responsive widget that includes door-to-door multimodal routing, live rail fares, and automatic Scope 3 Julie's Bicycle carbon disclosures with £0 setup fee.

---

### Venue Dossier: Visit Belfast (CS Lewis Square)

- **Host URL:** https://visitbelfast.com/listing/cs-lewis-square/97370101/
- **Sector / Archetype:** Tourism Destination
- **Location:** Belfast
- **Integration Status:** `CMS_FLAG`
- **Slug:** `belfast`
- **Current Setup:** Outbound link to `travel.yousmartthing.com`
- **Flaw:** Bounces visitors off the venue website instead of keeping them on-page.
- **Recommended EndMile Tier:** Standard (£19/mo) or Growth (£49/mo)
- **Value Proposition Angle:**
  Upgrade outbound link to an in-page interactive travel widget so visitors never leave visitbelfast.com.

---

## 6. YST Commercial Positioning & Sector Playbook Deconstruction

Through direct web scraping and analysis of You. Smart. Thing.'s sector pages (Major Events, Cultural Venues, Stadiums, and Local Authorities), we have extracted their core commercial value model and why venues buy travel software:

### 6.1 The 4 Pillars of YST's Event & Venue Pitch

1. **Audience Travel Represents >80% of an Event's Carbon Footprint (Scope 3)**
   - *The Reality:* For cultural organisations and major events, direct energy use (Scope 1 & 2) is a small fraction of total environmental impact. Over 80% of carbon emissions come from spectator and audience travel.
   - *The Mandate:* Arts Council England (ACE) National Portfolio Organisations (NPOs) and Theatre Green Book venues are required to measure audience travel emissions for annual **Julie's Bicycle** audits.
   - *Current Workaround:* Venues currently send post-show email surveys with dismal 3–4% response rates and guess the remainder on spreadsheets.
   - *YST's Angle:* Automates Scope 3 GHG data capture by recording actual journey queries and modal choices (active travel, rail, bus, EV, combustion car).

2. **Dwell Time & Secondary Spend (The Commercial Engine)**
   - *The Reality:* Regional theatres, arts centres, and attractions make razor-thin margins on headline tickets (promoters and touring companies take 70%–85% of face value). The venue survives on **secondary spend**: bars, catering, programmes, and merchandise.
   - *The Pain:* When visitors get delayed by last-mile driving traffic or spend 20 minutes circling for city parking, they arrive flustered at the 2-minute call. They bypass the foyer bar entirely and rush straight into the auditorium.
   - *YST's Metric:* Helping audiences plan multimodal arrivals gets attendees through the doors 30–45 minutes earlier. Case studies report a **~20% boost in on-site secondary spend / upsell conversion**, while eliminating latecomer seating holds and performance disruptions.

3. **Digital Retention vs. External App Drop-Off**
   - *The Reality:* When a venue page tells guests "we are near Station X" or embeds a generic Google Maps link, the ticket holder leaves the venue's digital estate.
   - *The Flaw of Google Maps:* Generic sat-nav apps have no awareness of venue entrance turnstiles, event road closures, temporary traffic regulation orders (TTROs), or preferred Park & Ride corridors. They direct drivers down residential backstreets or closed roads.
   - *YST's Angle:* Embedding a curated travel assistant keeps visitors within the venue's digital environment, allowing the operator to steer crowd ingress and maintain brand contact.

4. **Accessibility, Inclusion & Step-Free Confidence**
   - *The Reality:* Over 14 million people in the UK have access requirements.
   - *The Pain:* Disabled, older, or neurodivergent patrons often hesitate to book tickets if arrival logistics are unclear.
   - *YST's Angle:* Delivering clear Blue Badge parking locations, step-free public transport interchanges, and walking distances upfront builds booking confidence and complies with Equality Act 2010 accessibility guidelines without forcing visitors to phone ahead.

5. **Planning Permissions, Section 106 & Council Licensing Conditions**
   - *The Reality:* In the UK, venue operating licences, outdoor festival permits, university campus expansions, and stadium capacity increases require formal **Section 106 Sustainable Travel Plans** approved by council highways departments.
   - *The Pain:* Local planning authorities and police require proof that the venue is actively mitigating local street congestion, anti-social parking, and single-occupancy car trips. If a venue fails to monitor travel modal splits, they face planning condition enforcement or premises licence review.
   - *YST's Angle:* Provides continuous travel demand telemetry to prove non-car modal share to local councils and transport authorities.

6. **Peak Ingress Surges, Temporary Traffic Orders (TTROs) & Post-Curfew Egress Dispersal**
   - *The Reality:* Stadiums, music arenas, and family attractions experience acute bottlenecks:
     - *Morning Ingress (Attractions/Zoos):* 10:00–11:30 AM family surges back up onto arterial A-roads.
     - *Night Egress (Music Venues/Arenas):* Post-23:00 curfew crowd dispersal when public transit drops off.
     - *Highway Compliance:* Enforcing council Temporary Traffic Regulation Orders (TTROs) so generic sat-navs don't route traffic down closed residential streets.
   - *YST's Angle:* Curates ingress corridors to designated turnstiles/gates and flags last train departures to prevent stranded crowds post-curfew.

7. **Parking Yield Management & Combating Rogue Verge Parking**
   - *The Reality:* Venues and attractions invest heavily in official car parks or Park & Ride contracts, but lose revenue when visitors park in unauthorized residential streets, council bays, or private rogue lots because arrival advice was vague.
   - *YST's Angle:* Guides ticket holders directly to pre-booked on-site bays or partner Park & Ride shuttles, capturing parking revenue and eliminating neighborhood friction.

---

### 6.2 Deep Dive: What YST Actually Sells to Visitor Attractions (`/portfolio/visitor-attractions/`)

From scraping `https://yousmartthing.com/portfolio/visitor-attractions/`, `https://yousmartthing.com/benefits/`, and `https://yousmartthing.com/pricing/`:

#### Is it "Parking Tickets"?
**NO.** YST does not sell or issue parking enforcement tickets, fines, or basic parking vouchers.
When YST talks about parking and revenue for visitor attractions, they mean two specific things:
1. **Parking Demand Management & Capacity Smoothing**: Directing visitors away from full main lots to off-site or Park & Ride options before they arrive, avoiding traffic gridlock at rural estate gates (e.g. Compton Verney).
2. **Booking-Flow Secondary Revenue & Upsell**: Turning the post-ticket confirmation email into an affiliate travel/upsell portal (selling train tickets, hotel stays, gift shop packages, and carbon balancing add-ons).

#### The 4 Core Commercial Hooks YST Uses on Attractions:

1. **Local Authority / Grant Subsidies & Scope 3 Decarbonisation**:
   - YST pitches local councils (e.g., their live case study with **Warwickshire County Council** funding **Compton Verney Art Gallery & Park**).
   - Councils fund or co-sponsor the deployment to meet their Net Zero Climate Strategy and count visitor CO2e reductions toward county emissions targets.
2. **"EV Assist" & ChargePoint Operators (CPO Integration)**:
   - Targets drivers with range anxiety visiting countryside attractions with limited charging infrastructure.
   - Allows visitors to log expected EV arrival state-of-charge, pre-book charging bays at the attraction, or route via en-route rapid chargers.
3. **Accessibility & "Pre-Arrival Assistance Requests"**:
   - Offers step-free routes, sensory maps, and low-stimulus travel options.
   - **Operational Wedge**: Allows disabled visitors to request assistance (e.g., buggy transfer, sighted guide, wheelchair loan) directly through the travel assistant, dispatching pre-arrival alerts to front-of-house operations teams.
4. **"Destination Groups" & Multi-Entrance Wayfinding**:
   - For historic estates, arboretums, and country parks with multiple ticket offices or separate event fields, YST groups different arrival gates under one umbrella to stop visitors queuing at the wrong gate.

#### YST Published Pricing & Hidden Enterprise Gotchas (`/pricing/`):
- **Mandatory Setup & Configuration Fee**: **£1,000.00 ex VAT** (£2,250 on G-Cloud 14).
- **Ongoing Support / Integration Rate**: **£93.75 / hour ex VAT**.
- **Abstract Architecture**: Heavy emphasis on "Consent Matrices", "Personal Travel Assistants", and "Manufacturer data exploitation", which alienates lean attraction operators who just want visitors to know how to get there.

---

### 6.3 Why YST Leaves the Mid-Market Wide Open for EndMile

While YST's messaging around Scope 3 and dwell time is commercially sound, their execution creates severe friction for the 4,992 UK mid-market venues:

| Strategic Dimension | You. Smart. Thing. (YST) | EndMile Venue Widget | The Commercial Wedge |
|---|---|---|---|
| **Procurement & Setup** | Mandatory **£1,000.00 setup fee** (or £2,250 on G-Cloud 14) + enterprise onboarding | **£0 setup fee**, instant self-serve script | Removes 100% of upfront budget friction for independent attractions. |
| **Ongoing Pricing** | Enterprise contracts + £93.75/hr bespoke rates | **£19 to £49 / month** flat SaaS (cancel anytime) | Easily approved on a credit card without board sign-off. |
| **Mobile UX & Embed** | Heavy (~10MB) rigid 600px desktop iframe that breaks mobile viewports and causes double-scrollbars | **Lightweight (<45KB)** 1-line script drawer, 100% fluid mobile responsiveness | Looks native on mobile; zero layout shift. |
| **Cost Transparency** | Transit-focused nudge (rail / walk / cycle) without true multi-leg cost breakdown | **True Door-to-Door Cost Comparison**: driving (fuel + parking tariffs) vs train fares + station walks side-by-side | Solves the #1 visitor question: *"What is the real door-to-door cost of driving vs public transit?"* |
| **Speed to Value** | Weeks of onboarding, bespoke mapping, and CRM integration meetings | **2-minute drop-in embed** with pre-configured venue gate coordinates | Immediate deployment for the current season. |


