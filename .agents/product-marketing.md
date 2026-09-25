# Product Marketing Context

*Last updated: 2026-09-25*

## Related Research Sources
- **Customer feedback and conversation log:** `.agents/customer-feedback.md`
- **Current roadmap and validation priorities:** `.agents/roadmap.md`
- **Brand, design, and asset context:** `.agents/brand-context.md`
- **Published, planned, and draft content:** `.agents/content-log.md`
- **Product and marketing decisions:** `.agents/decisions.md`
- Future AI work on launch, copywriting, CRO, customer research, cold email, sales enablement, onboarding, ads, and content strategy should read the customer feedback log before making claims about customer pain, proof, personas, or messaging.
- Treat `.agents/product-marketing.md` as the positioning summary and `.agents/customer-feedback.md` as the raw evidence and voice-of-customer source.
- Treat `.agents/content-log.md` as the source of truth for published posts, planned posts, draft posts, and source-data-only content ideas.

## Product Overview
**One-liner:** EndMile powers UK multimodal door-to-door journey intelligence, destination arrival guides, and embeddable venue travel planners.

**What it does:** EndMile brings trains, driving, parking tariffs, Park & Ride, taxis, and local transit into one unified decision engine. It calculates the real Total Journey Cost (fuel, parking fees, rail fares, congestion charges, time, and carbon) and generates both consumer arrival guides and embeddable "Plan Your Visit" widgets for venues.

**Product category:** UK multimodal routing engine, destination arrival guides (B2C pSEO), embeddable venue travel widgets (B2B SaaS), travel intent DaaS.

**Product type:** Embeddable B2B SaaS widget, Programmatic SEO Guide (`guide.endmilerouting.co.uk`), and REST/Streaming Routing API.

**Business model & Unit Economics (Real Rate Cards):**
1. **B2B SaaS Subscriptions**: Embeddable "Plan Your Visit" interactive widgets for UK theatres, stadiums, event centres, arenas, and universities at £29–£99/month.
2. **B2C Programmatic SEO Monetisation (Based on 38,000 Published Venue Pages)**:
   - **Google AdSense / Programmatic Ads**: Category Travel & Transportation (EMEA) baseline ~$3.16 RPM (~£2.50 RPM). Yields ~£409/mo at 164k monthly pageviews (conservative 3.6 visits/page/mo).
   - **JustPark Parking Affiliate (Awin advertiser 6188)**: 
     - 20.00% CPA for new customer bookings
     - 5.00% CPA for existing customer bookings (blended ~9.5% on £15 avg basket = ~£1.43/booking)
     - £7.50 space listing bounty. Yields ~£143/mo conservative.
   - **Trainline Rail Affiliate (Partnerize)**:
     - 0.50% CPA default ticket rate (on £45 avg basket = ~£0.23/ticket)
     - 20.00% CPA for UK Railcard new customers (£6.00 on £30 card)
     - 7.00% CPA for UK Railcard existing customers (£2.10 on £30 card)
     - 2.00% CPA for Flixbus. Yields ~£34/mo conservative.
   - **Conservative Net Profit (38k pages @ 3.6 visits/page/mo)**: **~£535/month net profit** (~£6,430/yr at >91% margin after £50/mo VPS costs).
   - **Moderate Growth (7.5 visits/page/mo)**: **~£1,167/month net profit** (~£14,000/yr).
   - **Optimised (Premium Ad Network @ £14 RPM + 7.5 visits/page/mo)**: **~£4,500+/month net profit** (~£54,000/yr).
3. **Data-as-a-Service (DaaS)**: Retained anonymised UK travel search intent telemetry for transport and parking planners.

## Target Audience
**Primary B2B Target:** UK venue managers, event operations leads, theatre directors, stadium logistics teams, and university visitor management.
**Primary B2C Target:** UK event-goers, hospital visitors, jury/court attendees, stadium fans, and regional travellers seeking accurate door-to-door travel and parking options.

**Decision-makers (B2B):** Venue managers, marketing heads, operations directors looking to eliminate attendee parking confusion and reduce "how do I get there?" customer support tickets.

**Primary use cases:**
- **For Venues (B2B)**: Embedding a live, interactive "Plan Your Visit" widget on the venue website that routes visitors from anywhere in the UK, calculates driving vs rail costs, and highlights preferred car parks and Park & Ride hubs.
- **For Consumers (B2C)**: Finding verified, hyper-local arrival guides with exact parking tariffs, station walks, and regional comparison matrices before visiting high-friction UK destinations.
- **For Travel Decision Making**: Comparing full door-to-door cost (driving + parking vs rail + last mile) before committing to a journey.

## Personas
| Persona | Cares about | Challenge | Value we promise |
|---------|-------------|-----------|------------------|
| Venue / Operations Manager | Reducing parking chaos, attendee delays, customer support calls | Static "How to Find Us" text pages leave visitors confused about parking and transit | Drop-in interactive "Plan Your Visit" widget that answers all travel questions |
| Event / Stadium Director | Visitor experience, VIP/accessible transport, sustainability goals | Attendees arrive late or park illegally in local residential streets | Promotes public transit, Park & Ride, and designated parking with live routing |
| Event Goer / Visitor | Finding the cheapest/easiest way to reach a venue without parking fines | Unsure whether to drive or take the train; doesn't know local parking fees | Complete door-to-door cost, time, parking, and transit comparison in one view |
| Corporate Travel / Transport Planner | Understanding real door-to-door travel tradeoffs | Tools only show single legs (train-only or drive-only) | Full multimodal journey cost and carbon intelligence |

## Problems & Pain Points
**Core problem:** UK business journey planning is fragmented. Employees have to stitch together separate apps for maps, trains, taxis, buses, driving costs, and carbon.

**Why alternatives fall short:**
- Google Maps does not show the full business cost of a journey.
- Trainline helps with the train leg but not the door-to-door route.
- Citymapper is useful in cities but not for intercity business travel.
- Expense systems usually see the cost after travel, not before route selection.

**What it costs them:** Hidden expenses, wasted planning time, weak policy visibility, hard-to-compare route choices, and incomplete Scope 3 travel data.

**Emotional tension:** Travel teams and employees are asked to make better travel choices with incomplete information.

## Competitive Landscape

### 1. Corporate Pre-Trip Travel Justification (B2B SaaS)
- **Direct:** Corporate travel planning and expense tools (Concur, TravelPerk, Navan) - focused on booking, approval, or post-trip expense claims rather than pre-travel door-to-door multimodal comparison or client recharge dispute prevention.
- **Secondary:** Google Maps, Trainline, Citymapper, taxi apps, and public transport planners - useful for individual legs but blind to full HMRC mileage, VAT fuel recovery, and door-to-door TCO.
- **Indirect:** Manual comparison in spreadsheets or employees choosing habitual routes - flexible, but inconsistent and hard to govern.

### 2. Venue Travel Widget Market (B2B SaaS)
- **Enterprise Incumbent (You. Smart. Thing. / YST):**
  - Focuses on 5-figure enterprise tenders: Combined Authorities (TfGM Bee Network full-page iframe), Premier League / Tier 1 Arenas (Co-op Live, CBS Arena, Headingley, Wimbledon).
  - High friction rate card (G-Cloud 14): £750/day dev rate, ~3-day (£2,250) minimum single-location setup, £0.10/SMS. Heavy 600px desktop iframes forced cultural clients (Ashmolean, Pitt Rivers) to drop embeds and use plain outbound text links.
- **The EndMile Strategic Demarcation & Positioning:**
  - We do NOT compete for enterprise transport authority tenders.
  - We target the **unserved 99% mid-market (4,992 UK cultural & visitor venues)** with NO widget installed.
  - Wedge: £0 setup fee, 2-minute 1-line embed, self-serve £19–£49/month on corporate credit card, lightweight mobile-first layout, and automated Julie's Bicycle Scope 3 carbon exports for Arts Council England (ACE) NPOs.
- **Active Go-To-Market Execution:**
  - Founder is actively working through `data/venues/unserved_prospects.csv` in Excel, finding named operational decision-makers (Head of Visitor Experience / Operations Director) via website staff directories and LinkedIn, and executing personalized sniper outreach (10–15/day) using [`sales-and-marketing/venue-widget-outbound-playbook.md`](sales-and-marketing/venue-widget-outbound-playbook.md).

## Differentiation
**Key differentiators:**
- Door-to-door UK routing across trains, taxis, buses, and driving.
- Total cost view including fares, fuel, parking, congestion charges, and time value.
- Journey risk as part of the route comparison, not an afterthought.
- Carbon impact shown per route for business travel reporting.
- Route comparison views for recommended, earliest arrival, and cheapest options.

**How we do it differently:** EndMile treats business travel as a full journey decision rather than a single-mode route or booking action.

**Why that's better:** Teams can compare the trade-offs that matter before anyone travels: cost, time, risk, and carbon.

**Why customers choose us:** They need a clearer pre-travel decision layer than consumer mapping, rail booking, or expense tools provide.

## Objections
| Objection | Response |
|-----------|----------|
| We already use Google Maps or Trainline. | Those tools help with parts of the journey. EndMile compares the whole business trip, including first mile, last mile, hidden costs, risk, and carbon. |
| Employees can work this out themselves. | They can, but it takes multiple apps and creates inconsistent choices. EndMile makes the trade-offs visible in one search. |
| We only need the fastest route. | The fastest route is not always the best business route once cost, risk, and Scope 3 impact are included. |

**Anti-persona:** Pure leisure travellers looking only for a consumer trip planner or booking app.

## Switching Dynamics
**Push:** Frustration with switching between apps, hidden travel costs, weak pre-travel visibility, and manual carbon reporting.

**Pull:** One route comparison that shows cost, time, risk, and CO2 before the journey.

**Habit:** Employees default to familiar tools or past route choices.

**Anxiety:** Teams may worry whether a new planning layer is accurate enough for real travel decisions.

## Customer Language
**How they describe the problem:**
- "Planning a UK journey should not take 3 apps."
- "Google Maps doesn't tell you the full cost."
- "Trainline can't get you to the station."
- "Citymapper won't take you intercity."

**How they describe us:**
- "EndMile helps businesses plan UK travel by comparing routes by true door-to-door cost, time, journey risk and carbon impact."
- "EndMile does."

**Words to use:** Door-to-door, real cost, UK business travel, journey risk, carbon, Scope 3, compare, before employees travel, route trade-offs, first mile, last mile.

**Words to avoid:** Consumer-only positioning, fastest-only messaging, vague sustainability claims without route-level proof.

**Glossary:**
| Term | Meaning |
|------|---------|
| Door-to-door cost | The full cost of the journey, including first mile, last mile, fares, driving, parking, congestion, and other travel costs. |
| Journey risk | A route's exposure to fragile transfers, delay risk, walking pressure, and connection uncertainty. |
| Scope 3 business travel | Indirect emissions from employee business travel that organisations may need to measure and report. |
| Smart Swap | EndMile feature for changing first or last-mile legs and seeing the exact cost and time difference. |

## Brand Voice
**Tone:** Direct, practical, business-focused.

**Style:** Clear contrasts, plain language, concrete route trade-offs, low fluff.

**Personality:** Useful, precise, pragmatic, transparent.

## Proof Points
**Metrics:**
- 3,000+ route combinations per search.
- DEFRA 2026 carbon basis stated on the landing page.

**Customers:** Not yet specified.

**Testimonials:**
> Not yet available.

**Value themes:**
| Theme | Proof |
|-------|-------|
| Complete journey comparison | Trains, taxis, buses, and driving compared side by side. |
| Cost control | Fares, fuel, parking, congestion charges, and time value included before travel. |
| Sustainability reporting | CO2 per route and Scope 3 positioning. |
| Lower planning friction | Launch copy frames the problem as replacing three-app journey planning. |

## Launch Assets
**Website:** https://endmilerouting.co.uk

**LinkedIn launch image:** `C:/Users/isaac/OneDrive/Documents/EndMile/linkedinphoto.png`

**LinkedIn business page:** EndMile Routing

**LinkedIn page URL:** Not yet recorded in this document.

**LinkedIn page current state:** The business page currently has 9 followers, is listed as Software Development, Leeds, and 0-1 employees. The founder has not yet applied suggested profile-copy edits, so future AI users should treat the wording below as the live public context unless told otherwise.

**LinkedIn page headline/tagline:** EndMile helps businesses compare door-to-door UK travel routes by cost, time, risk and carbon.

**LinkedIn page overview:**
```text
EndMile helps businesses plan UK travel by comparing routes by true door-to-door cost, time, journey risk and carbon impact.

Instead of showing only the fastest route, EndMile brings together trains, taxis, buses and driving, then factors in fares, fuel, parking, congestion charges, time value and CO2. The result is a clearer view of the real cost of each journey before employees travel.

EndMile is built for corporate travel teams that need better cost control, policy visibility and Scope 3 business travel reporting.
```

**LinkedIn launch image context:** Screenshot-style product visual showing a Ripon HG4 to West Jesmond journey, a recommended multimodal route, £28.11 cost, 1h 46m duration, drive/train/local transit legs, "Low Risk", "Saves 61% CO2 vs driving", and "Top Choice". It supports the message that EndMile compares route trade-offs rather than showing a single travel mode.

**Recommended image use:** Reuse the launch image selectively. For follow-up posts, prefer simple journey-breakdown graphics or product screenshots that prove a specific point: full journey components, cost comparison, carbon comparison, or risk comparison.

**LinkedIn post copy:**
```text
PLANNING A UK JOURNEY SHOULD NOT TAKE 3 APPS.

Google Maps doesn't tell you the full cost.
Trainline can't get you to the station.
Citymapper won't take you intercity.

EndMile does.

Link in comments.
```

## LinkedIn Post Log
Historical copy is retained here for positioning context. Use `.agents/content-log.md` as the source of truth for current published, planned, draft, and source-data-only content status.

### 2026-05-20 - Business page launch post
**Channel:** EndMile Routing LinkedIn business page.

**Image:** `C:/Users/isaac/OneDrive/Documents/EndMile/linkedinphoto.png`

**Copy:**
```text
PLANNING A UK JOURNEY SHOULD NOT TAKE 3 APPS.

Google Maps doesn't tell you the full cost.
Trainline can't get you to the station.
Citymapper won't take you intercity.

EndMile does.

Link in comments.
```

**Tone notes:** Short, direct, contrast-led, intentionally punchy. Uses all-caps headline for emphasis, then three competitor contrasts, then a two-word brand answer. This is the clearest current expression of the launch message.

### 2026-05-20 - Personal founder post resharing the business page
**Channel:** Founder's personal LinkedIn profile.

**Purpose:** Explain the problem more fully, add founder context, and ask for early testers.

**Copy:**
```text
Planning a business trip in the UK means bouncing between Google Maps, Trainline, and a parking website, then doing the maths yourself. Nobody shows you the full picture before you leave.

On the side, I've developed an early version that solves this issue which combines rail, driving, parking, taxis, walking, P&R, and local transit so you can see the real cost and carbon footprint before you travel, not just one leg of it, and not after the fact. 

Link is in the comments

I'm looking for early testers, particularly business travellers, event organisers, sustainability leads, and universities or business parks looking to improve travel planning.

Please get in touch with any thoughts.
```

**Tone notes:** Founder-led, practical, candid, early-stage, and direct. The founder is comfortable saying the product is an early version and asking plainly for feedback. Future posts should preserve this useful early-tester feel rather than sounding like polished enterprise advertising.

### Draft follow-up post - not yet posted
**Status:** Suggested copy only. Do not treat as already published.

**Recommended image:** A simple journey-breakdown graphic or a product screenshot, not necessarily the original launch image.

**Copy:**
```text
A business journey is not just "train vs car".

It is:

Home -> station
Parking or taxi
Train fare
Connection risk
Arrival station -> destination
Time lost
CO2 impact
Expense policy fit

Most tools show one piece of that. EndMile compares the full door-to-door journey before you travel.

Looking for early testers in UK business travel.
```

**Posting guidance:** Best posted from the founder's personal profile first for reach, then reshared from the EndMile Routing business page. Put the product link in the first comment when optimizing for LinkedIn reach.

### Planned next-week post - 2026-05-27
**Status:** Planned draft. Do not treat as already published until confirmed.

**Channel:** Founder's personal LinkedIn profile first, then repost from EndMile Routing.

**Goal:** Move from launch announcement to customer discovery. The post should attract business travellers and people who plan staff travel by asking how they currently compare awkward multi-leg journeys.

**Recommended image:** Use a simple journey-breakdown image rather than the original launch screenshot. Suggested visual structure:
```text
Home -> station -> train -> connection -> taxi/bus/walk -> destination

Cost | Time | Risk | CO2
```

**Copy:**
```text
The part of business travel planning that surprised me most:

The hard bit is not always booking the train.

It is working out the full journey before you commit:

Home -> station
Parking or taxi
Train fare
Connection risk
Arrival station -> destination
Time lost
CO2 impact
Expense policy fit

One person in my early research described the pain as:

"Co-ordinating timings and trying to get the shortest wait between connections."

That is exactly the problem I am trying to solve with EndMile.

It compares UK business journeys by full door-to-door cost, time, risk and carbon, before you travel.

If you regularly plan UK work trips, I would be grateful for your honest answer:

How do you compare these options today?
```

**First comment:**
```text
I am looking for early testers who plan or take UK business journeys.

Try EndMile here: https://endmilerouting.co.uk

If you test one real route you have travelled recently, I would be grateful for blunt feedback.
```

**Posting guidance:** Post midweek in the morning, ideally Wednesday 2026-05-27 between 08:00 and 10:00 UK time. Spend 20 minutes before posting commenting on posts by target people, then reply quickly to any comments during the first hour.

## LinkedIn Messaging Rules
- Lead with the practical pain: business travel planning currently takes too many apps and too much manual comparison.
- Use sharp contrasts against partial tools, especially Google Maps, Trainline, Citymapper, parking websites, taxi apps, and expense systems.
- Keep the offer grounded in real route decisions: full door-to-door cost, time, journey risk, and carbon before travel.
- Ask for early testers openly. The launch stage is early access, not mature enterprise procurement.
- Avoid sounding like a generic sustainability tool. Carbon matters, but it should sit beside cost, time, and risk.
- Avoid overclaiming accuracy, savings, or compliance before proof is collected.
- Strong CTA language: "Try EndMile", "Looking for early testers", "Try one real journey", "Tell me how you make this decision today".
- Link placement for LinkedIn: usually "Link in comments" in the post body, followed by the website URL in the first comment.

## Goals
**Business goal:** Establish EndMile as the business travel route comparison layer for UK organisations.

**Conversion action:** Get visitors to plan or compare a journey in the web app or install the mobile app.

**Current metrics:** LinkedIn page has 9 followers and is listed as software development in Leeds with 0-1 employees.
