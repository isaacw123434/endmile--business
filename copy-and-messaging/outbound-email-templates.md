# Outbound Email Sequences & Sniper Templates Catalogue

*Authoritative template catalogue synchronized with `C:\Users\isaac\Documents\endmile\endmile_master_pipeline.xlsx` (Sheet 3: `Email Templates & Referrers`) and `scripts/outreach/send_app_outreach.py`.*

---

## 1. Quick Template Selector & Routing Matrix

| Template Code | Template Name | Target Recipient / Inbox | Hook / Angle | Word Count |
|---|---|---|---|---|
| **`DIRECT_SCRATCHPAD`** | Direct Operations Scratchpad Pitch | Direct Operations & Named Leads (`operations@`, `projects@`) | 10-Minute Travel Juggling vs 10-Second Pre-Trip Tool | 85 words |
| **`DIRECT_RECHARGE`** | Direct Project Recharges & Margin Defense | Finance, Commercial Leads, Quantity Surveyors (`finance@`, `commercial@`) | Backing up HMRC 55p mileage against AP pushback | 95 words |
| **`INFO_REF_A`** | Info Desk Referral A (Founder Discovery Ask) | General Front Desk / Triage (`info@`, `hello@`, `enquiries@`) | Pre-revenue engineer asking 2 quick questions (Disarming) | 38 words |
| **`INFO_REF_B`** | Info Desk Referral B (Multi-Tab Time Saver) | General Front Desk / Triage (`info@`, `hello@`, `enquiries@`) | Operational time saver for client travel planning | 50 words |
| **`INFO_REF_C`** | Info Desk Referral C (55p Mileage Dispute) | General Front Desk / Triage (`info@`, `hello@`, `enquiries@`) | Backing up client expense disputes and travel invoices | 45 words |
| **`INFO_REF_D`** | Info Desk Referral D (Gatekeeper Forward) | High-volume busy reception inboxes (`info@`, `hello@`) | Frictionless forward request (Zero pitch) | 28 words |
| **`FOLLOWUP_DIRECT_1`** | Direct Follow-Up (+3 to 4 Days) | Direct Operations & Named Leads | Zero-friction sandbox link pre-configured for their HQ corridor | 55 words |
| **`FOLLOWUP_INFO_1`** | Info Desk Follow-Up (+4 Days) | General Front Desk / Triage | Polite reminder / routing request | 32 words |
| **`THEATRE_VISIT_A`** | Theatre Variant A: Interactive Visit Planner | General Managers, Marketing, Visitor Services | Replaces static paragraphs with 1-line interactive trip planner + visual mockup | 82 words |
| **`THEATRE_ACCESS_B`** | Theatre Variant B: Step-Free Transit Clarity | Box Office, Access Officers, Visitor Experience | Step-free rail routes and Blue Badge parking certainty | 80 words |
| **`GIG_CURFEW_A`** | Live Music Variant A: Post-Curfew Return Transit | Operations Managers, Venue Promoters | Out-of-town fans checking last train/bus departures home before traveling | 81 words |
| **`MUSEUM_PLANNER_A`** | Urban Museum Variant A: Transit vs Driving Clarity | Visitor Services, Operations Managers | Comparing driving + parking against direct train routes on mobile | 83 words |
| **`HERITAGE_RURAL_B`** | Rural Heritage Variant B: Mainline Rail-to-Gate Links | Commercial Directors, Head of Visitor Services | Connecting mainline rail with local buses/taxis for car-free tourists | 79 words |
| **`ATTRACT_FAMILY_A`** | Family Attraction Variant A: Instant Trip & Parking Planning | Operations Directors, Visitor Operations | Instant home-to-gate driving times, parking, and transit in one tool | 84 words |
| **`THEATRE_SCOPE3_A`** | Arts NPO Variant A: Passive Julie's Bicycle Scope 3 | Sustainability Officers, Operations Directors | Replacing 3-4% post-show survey guesswork with real trip query telemetry | 86 words |
| **`VENUE_INFO_REFERRAL`** | Venue Front-Desk Disarming Referral | General Venue Inboxes (`info@`, `hello@`, `boxoffice@`) | Disarming engineer ask pointing to visitor ops or website manager | 44 words |

---

## 2. Consultancy App Direct Outreach (Named Leads & Operations Desks)

### `DIRECT_SCRATCHPAD`
**Subject:** `{Company}'s travel planning`  
**When to Use:** Named practice leads, travel coordinators, or specific operations/delivery inboxes (`operations@`, `projects@`, `travel@`, `office@`).

```text
{Good morning / Good afternoon} {ContactName},

When your consultants head out to client sites (like {TravelCorridor}), does someone on operations still spend 10 minutes juggling Google Maps, Trainline, and station parking to find the fastest and cheapest door-to-door route?

I built EndMile as a quick scratchpad for UK consultancies. It stacks up driving (at HMRC 55p/mile) against train fares, station parking, and destination taxis side-by-side in 10 seconds.

Happy to send over a 30-second preview of how it works for {HQCity} corridors if helpful?

Best,
Isaac
Founder, EndMile
isaacw@endmilerouting.co.uk

No worries at all if this isn't relevant to your team.
```

### `DIRECT_RECHARGE`
**Subject:** `Client travel recharges`  
**When to Use:** Cost consultants, quantity surveyors, project managers, or finance contacts managing client billing.

```text
{Good morning / Good afternoon} {ContactName},

When {Company}'s consultants travel to client sites, do your finance or project leads ever run into pushback from client accounts payable over HMRC 55p mileage or taxi expenses?

We've found many UK consultancies lose 1–5% of travel recharges simply because clients look up a superficial £50 train ticket and dispute a £110 car journey, ignoring station parking and taxi legs.

We built EndMile to calculate the true door-to-door comparison before consultants travel, generating a 1-page Pre-Trip Cost Justification PDF to attach directly to client invoices.

Would it be helpful to see a sample justification report for {HQCity} routes?

Best,
Isaac
Founder, EndMile
isaacw@endmilerouting.co.uk

No worries at all if this isn't relevant to your team.
```

### `FOLLOWUP_DIRECT_1`
**Subject:** `Re: {Company}'s travel planning`  
**When to Use:** Send 3–4 business days after `DIRECT_SCRATCHPAD` if no response.

```text
{Good morning / Good afternoon} {ContactName},

Just following up on this — know you're busy coordinating client dispatches.

We set up a quick 1-click test link with {HQCity} corridors pre-configured: https://endmilerouting.co.uk

No login or download needed — feel free to test your team's next client route and see if it cuts your planning time down from 15 minutes to 30 seconds.

Best,
Isaac
Founder, EndMile
isaacw@endmilerouting.co.uk
```

---

## 3. General Front-Desk Inboxes (`info@`, `hello@`, `enquiries@`, `contact@`) — Front-Desk Referral Variations

> [!IMPORTANT]
> **Salutation & Formatting Rules:**
> 1. **Time-Aware Salutation:** Use `Good morning,` (before 12:00) or `Good afternoon,` (after 12:00). Never use informal "Hi team," or "Hi there,".
> 2. **Capitalized Subject Lines:** NEVER start subject lines in lowercase. Always capitalize the first word (e.g. `Quick question - travel coordination`).
> 3. **Zero Links in Email 1:** Omit raw `https://` URLs from Email 1 to ensure 100% spam inbox deliverability without triggering ATP Safe Links scanner.
> 4. **Natural Human Opt-Out:** Always use natural conversational sign-offs (e.g. `No worries at all if this isn't relevant to your team.`) instead of robotic `reply 'unsubscribe'` keywords.

### `INFO_REF_A` (Variant A: Founder Discovery Ask)
**Subject:** `Quick question - travel coordination`  
**Word Count:** 38 words  
**Strategy:** Extremely disarming; gatekeepers forward directly to Ops.

```text
{Good morning, / Good afternoon,}

Could you point me to whoever looks after consultant travel or expenses at {Company}?

I'm an independent UK software engineer building a tool to cut down the time consultancies spend planning client travel and comparing HMRC 55p mileage. Just wanted to ask them 2 quick questions about how they currently handle it.

Best,
Isaac
Founder, EndMile
isaacw@endmilerouting.co.uk

No worries at all if this isn't relevant to your team.
```

### `INFO_REF_B` (Variant B: Multi-Tab Time Saver)
**Subject:** `{Company}'s travel planning`  
**Word Count:** 50 words  
**Strategy:** Concrete operational time saver; receptionist forwards to travel planner.

```text
{Good morning, / Good afternoon,}

Quick question — who at {Company} coordinates travel when consultants head out to client sites (like {TravelCorridor})?

I put together a simple tool for UK consultancies that works out driving mileage against train fares, parking, and taxis in 10 seconds, instead of jumping between 3 tabs.

Worth passing this over to whoever handles travel for your team?

Best,
Isaac
Founder, EndMile
isaacw@endmilerouting.co.uk

No worries at all if this isn't relevant to your team.
```

### `INFO_REF_C` (Variant C: HMRC 55p Mileage Dispute)
**Subject:** `Consultant travel expenses`  
**Word Count:** 45 words  
**Strategy:** Commercial angle; routes to Practice Manager or Accounts.

```text
{Good morning, / Good afternoon,}

Could you point me to whoever manages travel expenses or project recharges at {Company}?

I put together a simple tool for UK consultancies to help back up HMRC 55p mileage against rail costs when clients question travel invoices.

Who would be best to speak with about that?

Best,
Isaac
Founder, EndMile
isaacw@endmilerouting.co.uk

No worries at all if this isn't relevant to your team.
```

### `INFO_REF_D` (Variant D: Ultra-Short Gatekeeper Forward)
**Subject:** `Quick referral - operations / travel`  
**Word Count:** 28 words  
**Strategy:** Zero friction, zero sales pitch; pure receptionist routing request.

```text
{Good morning, / Good afternoon,}

Could you point me in the right direction? Who at {Company} coordinates travel planning or expenses for consultants travelling to client sites?

Thanks so much,
Isaac
Founder, EndMile
isaacw@endmilerouting.co.uk

No worries at all if this isn't relevant to your team.
```

### `FOLLOWUP_INFO_1`
**Subject:** `Re: Quick question - travel coordination`  
**Word Count:** 32 words  
**When to Use:** Send 4 business days after `INFO_REF_A/B/C/D` if no reply.

```text
{Good morning, / Good afternoon,}

Following up briefly on this — did you know who would be the best person to speak with regarding consultant travel or operations at {Company}?

Much appreciated,
Isaac
Founder, EndMile
isaacw@endmilerouting.co.uk
```

---

## 4. B2B Venue Travel Widget Outreach: Grounded, Visual & High-Converting Templates

> **Strategic Operating Rules & Core Principles:**
> 1. **Never use the "parking tickets" or "box office parking questions" angle:** Visitors don't email box offices asking about parking, and venues don't care if someone gets a parking fine on a public street. It is an artificial, unconvincing pitch.
> 2. **Never claim complex enterprise features we don't have:** We don't have EV charger reservation systems or direct municipal grant integrations like YST. Don't pretend to be an enterprise mobility consultant.
> 3. **The Real Value Proposition:** 
>    - Most visitors check directions on a phone. Current venue visit pages are walls of static text that force visitors to copy postcodes, bounce to Google Maps, check Trainline, and leave the venue's site.
>    - EndMile is a **clean, 1-line embedded trip planner** that lets visitors enter their origin and instantly see their exact options (train timetables, station walking routes, driving times, and verified local car parks) directly on the venue's visit page.
>    - The **Playwright mock screenshot** of *their own website* is our greatest sales asset. It proves personal founder effort and lets the prospect immediately see how seamless it looks.
> 4. **Tone & Constraints:** Under 90 words, natural British phrasing, time-sensitive salutations (`Good morning,` / `Good afternoon,`), sentence-case subject lines, and disarming interest-based asks.

---

### 4.1 The Core Tested Templates (By Sector & Use Case)

#### Subtype 1A: Theatres, Arts Centres & Concert Halls

##### `THEATRE_VISIT_A` (Variant A: Interactive Trip Planning vs Static Text)
**Subject:** `Visitor directions for {VenueName}`  
**Word Count:** 82 words  
**Target:** General Managers, Marketing Directors, Visitor Services Managers.  
**Strategy:** Addresses the mobile visitor experience where patrons have to read through static paragraphs and jump between navigation apps to plan arrival times.

```text
{Good morning / Good afternoon} {ContactName},

Looking at {VenueName}'s "Getting Here" page, visitors planning their trip currently have to read through static text and jump between map apps and train timetables to figure out their route.

We built EndMile as a lightweight, 1-line trip planner for UK venues. Ticket holders simply type their postcode and instantly get door-to-door transit times, station walks, and car parks directly on your page.

I mocked up how it looks on {VenueName}'s actual visit page (screenshot attached). Would you be open to trying a live preview?

Best,
Isaac
Founder, EndMile
isaacw@endmilerouting.co.uk

No worries at all if this isn't relevant to your team.
```

##### `THEATRE_ACCESS_B` (Variant B: Step-Free Transit & Accessible Arrival Clarity)
**Subject:** `Accessible travel guidance for {VenueName}`  
**Word Count:** 80 words  
**Target:** Access Officers, Box Office Managers, Head of Visitor Services.  
**Strategy:** Addresses accessibility uncertainty by showing step-free rail options and accessible car park locations upfront.

```text
{Good morning / Good afternoon} {ContactName},

When patrons with accessibility requirements plan a visit to {VenueName}, how easy is it for them to see step-free public transport and accessible parking options on your site?

Generic map links don't clarify accessible station exits or walking distances.

We built EndMile to embed a clean trip planner on your visit page, highlighting verified step-free transit routes and Blue Badge parking in one place.

I attached a quick mockup showing how it sits on your website. Would this be useful for {VenueName}?

Best,
Isaac
Founder, EndMile
isaacw@endmilerouting.co.uk

No worries at all if this isn't relevant to your team.
```

---

#### Subtype 1B: Music Venues, Gig Spaces & Late-Night Halls

##### `GIG_CURFEW_A` (Variant A: Post-Gig Public Transit & Last Train Timing)
**Subject:** `Getting home from {VenueName}`  
**Word Count:** 81 words  
**Target:** Operations Managers, Venue Promoters, General Managers.  
**Strategy:** Targets out-of-town gig-goers worried about post-11 PM return trains, giving them return transit times directly when checking event details.

```text
{Good morning / Good afternoon} {ContactName},

For evening gigs finishing after 10:30 PM at {VenueName}, do attendees travelling in from surrounding towns often struggle to check return train and bus times in advance?

We built EndMile as a simple, 1-line trip planner for UK live venues. It lets ticket buyers check their exact route home—including last rail departures and station walking times—right on your event pages.

I attached a mockup showing how it looks on your site. Happy to share a live preview if helpful?

Best,
Isaac
Founder, EndMile
isaacw@endmilerouting.co.uk

No worries at all if this isn't relevant to your team.
```

---

#### Subtype 2A: Urban Museums, Galleries & Heritage Properties

##### `MUSEUM_PLANNER_A` (Variant A: Transit vs Driving Clarity)
**Subject:** `Travel directions for {VenueName}`  
**Word Count:** 83 words  
**Target:** Head of Visitor Experience, Commercial Directors, Operations Managers.  
**Strategy:** Helps day visitors compare driving and parking against direct train routes in one tap on mobile.

```text
{Good morning / Good afternoon} {ContactName},

Taking a look at the visitor guide on {VenueName}'s website, day visitors currently have to sort through multiple transport bullet points to compare driving vs public transit.

We built EndMile to give visitors an interactive door-to-door trip planner directly on your "Visit" page. Visitors enter their starting point and get live train times, walking routes, and official car parks side-by-side.

I mocked up how this looks on {VenueName}'s visit page (attached). Worth sending over a quick preview link to test?

Best,
Isaac
Founder, EndMile
isaacw@endmilerouting.co.uk

No worries at all if this isn't relevant to your team.
```

##### `HERITAGE_RURAL_B` (Variant B: Connecting Mainline Rail to Rural Heritage)
**Subject:** `Car-free visitor routes to {VenueName}`  
**Word Count:** 79 words  
**Target:** Commercial Directors, Head of Visitor Services.  
**Strategy:** Bridges the gap between mainline train stations and local connecting buses or taxis for non-driving visitors.

```text
{Good morning / Good afternoon} {ContactName},

For tourists and visitors without a car, how easily can they work out how to reach {VenueName} via public transport from the nearest train station?

Many visitors assume historic sites are inaccessible without driving unless connecting bus routes or station taxis are clearly laid out.

EndMile embeds a 1-line route planner connecting mainline rail arrivals with local onward travel directly on your website.

Attached is a quick mockup of how it looks. Would a preview be of interest?

Best,
Isaac
Founder, EndMile
isaacw@endmilerouting.co.uk

No worries at all if this isn't relevant to your team.
```

---

#### Subtype 3A: Visitor Attractions, Zoos & Wildlife Parks

##### `ATTRACT_FAMILY_A` (Variant A: Pre-Trip Family Journey Planning)
**Subject:** `Visitor trip planning for {VenueName}`  
**Word Count:** 84 words  
**Target:** Head of Visitor Operations, General Managers, Marketing Leads.  
**Strategy:** Simplifies family journey planning by replacing text descriptions with an instant interactive route and parking tool.

```text
{Good morning / Good afternoon} {ContactName},

Looking at the arrival advice on {VenueName}'s website, families planning a day out currently have to manually cross-reference driving routes, parking advice, and train connections across different tabs.

We built EndMile as an embeddable visit planner. Families simply enter their home town or postcode to see their exact driving time, car park locations, or public transit options in one place.

I went ahead and mocked up how it looks on your visit page (attached). Worth seeing a 30-second live preview?

Best,
Isaac
Founder, EndMile
isaacw@endmilerouting.co.uk

No worries at all if this isn't relevant to your team.
```

---

#### Subtype 4A: Arts Council England (ACE) NPOs & Green Book Venues

##### `THEATRE_SCOPE3_A` (Variant A: Audience Travel Scope 3 Carbon Telemetry)
**Subject:** `Audience travel reporting for {VenueName}`  
**Word Count:** 86 words  
**Target:** Sustainability Leads, Operations Directors, Executive Directors (NPOs only).  
**Strategy:** Focuses purely on replacing low-response post-show email surveys with passive journey query telemetry for Julie's Bicycle reporting.

```text
{Good morning / Good afternoon} {ContactName},

For {VenueName}'s annual Julie's Bicycle environmental reporting, how does your team currently collect audience travel data?

Audience travel usually represents the vast majority of a cultural venue's footprint, yet most venues rely on post-show surveys with very low response rates.

EndMile embeds a 1-line journey planner on your visit page that passively logs travel modal splits and estimated passenger mileage as visitors plan their journey.

I attached a mockup showing how it sits on your site. Would a sample carbon export be of interest?

Best,
Isaac
Founder, EndMile
isaacw@endmilerouting.co.uk

No worries at all if this isn't relevant to your team.
```

---

### 4.2 Universal Reception / Gatekeeper Referral

#### `VENUE_INFO_REFERRAL` (Disarming Peer Referral)
**Subject:** `Quick question - visitor directions`  
**Word Count:** 44 words  
**Target:** General inboxes (`info@`, `hello@`, `enquiries@`, `boxoffice@`).  
**Strategy:** Disarming, honest founder ask asking reception to route to whoever manages the website or visitor operations.

```text
{Good morning, / Good afternoon,}

Could you point me to whoever looks after visitor operations or manages the website at {VenueName}?

I'm an independent UK software developer who built an embeddable visit planner for UK venues, and wanted to share a 30-second preview of how it looks on {VenueName}'s site.

Best,
Isaac
Founder, EndMile
isaacw@endmilerouting.co.uk

No worries at all if this isn't relevant to your team.
```

---

## 5. Visual Mock Screenshot Outbound Workflow (DevTools Injection)

To convert cold venue directors at a significantly higher rate than generic text or abstract claims, EndMile generates **actual, high-resolution screenshots of the prospect's real visit/getting-here page with the EndMile journey planner seamlessly embedded into their website's DOM**.

### 5.1 How It Works End-to-End
1. **Automated Visit Page Discovery**: Playwright launches headless Chromium, navigates to the venue's domain, scans the navigation structure, and automatically discovers their dedicated `/getting-here`, `/your-visit`, `/directions`, or `/find-us` page.
2. **Cookie Notice Dismissal**: Automatically detects and dismisses cookie consent modals (OneTrust, Cookiebot, CivicUK, etc.) to keep the page clean and unobstructed.
3. **DevTools DOM Injection**: Injects a custom-styled, sector-specific EndMile Journey Planner card (`#endmile-mock-widget`) directly into their main content container:
   - Matches sector-specific routing (e.g. late curfew trains for gigs, Clean Air Zone alerts & Park & Ride for urban museums, bypass routing for zoos).
   - Injects immediately below their primary "Getting Here" H1/banner or directly above their static Google Map.
4. **Retina Viewport Framing**: Scrolls the page so the venue's logo, primary navigation, and page title are visible above the widget, capturing a crisp 1.5x retina PNG (`screenshots/venues/{VenueID}_{Slug}.png`).
5. **Dynamic Email Personalisation & Attachment**:
   - The CLI dispatcher (`send_venue_outreach.py --attach-screenshot`) attaches `{venue_slug}_travel_planner_mock.png` to the outgoing SMTP email.
   - The email body dynamically swaps its closing CTA from an abstract preview offer to:
     > *"I went ahead and mocked up how this looks on your actual visit page (see attached screenshot, or try it live at https://endmilerouting.co.uk/venue-widget/?url=...&venue=...). Worth exploring a 14-day free pilot for {VenueName}?"*

### 5.2 Standalone Screenshot CLI
```bash
# Generate a mock screenshot for any venue URL and sector:
python scripts/outreach/generate_venue_mock_screenshot.py --url https://www.oxfordplayhouse.com --name "Oxford Playhouse" --archetype theatre

# Generate for a specific VenueID in the master pipeline:
python scripts/outreach/generate_venue_mock_screenshot.py --venue-id 345886715

# Batch generate for top 5 approved venues:
python scripts/outreach/generate_venue_mock_screenshot.py --batch --limit 5
```

### 5.3 Automated Outbound Dispatch with Screenshot Attachments
```bash
# Preview emails with cached/auto-generated screenshots:
python scripts/outreach/send_venue_outreach.py --dry-run --limit 5 --variant A --screenshot

# Preview with email attachments enabled:
python scripts/outreach/send_venue_outreach.py --dry-run --limit 5 --variant B --attach-screenshot

# Live dispatch with screenshot attachments:
python scripts/outreach/send_venue_outreach.py --limit 5 --variant auto --attach-screenshot
```



