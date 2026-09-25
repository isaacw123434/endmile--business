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
