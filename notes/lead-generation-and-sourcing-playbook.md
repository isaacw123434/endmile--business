# EndMile B2B Consultancy Lead Generation & Sourcing Playbook

**Author:** Isaac Willoughby & EndMile Business Brain  
**Date:** October 2026  
**Objective:** Scale and maintain a continuous, zero-bounce pipeline of 1,500–3,000+ UK consultancies and field service practices for the EndMile App, replacing guesswork with precision departmental targeting.

---

## 1. The Core Philosophy: Why "Who is Mark?" Matters

### The Problem with Statutory Directors
In public UK registries (Companies House), the registered "Officers" and "Directors" are legal and statutory roles. Very often, the person listed is:
* An external accountant or company secretary who incorporated the entity.
* A non-executive chairperson or silent financial investor.
* A senior partner who deals exclusively with equity and high-level client acquisition, completely detached from day-to-day project operations or travel expense claims.
* A founder who stepped back from operations 10 years ago.

**The Failure Mode:** When an outbound email arrives addressed to *"Hi Mark,"* pitching an operational tool for comparing train fares against mileage, Mark either ignores it as irrelevant spam or flags it. It feels disjointed, awkward, and AI-generated.

### The Winning Two-Pronged Architecture

Instead of guessing director names, EndMile deploys a precise two-pronged targeting architecture:

```
                                [Discovered Lead]
                                        │
                         Does it have a Named Contact
                       or Direct Operational Department?
                                ├── YES ──────────────┐
                                │                     │
                                ▼                     ▼
                       [Direct Department]     [Named Contact]
                      operations@, projects@,  arun.jardine@, peter@
                       travel@, logistics@     "Hi Arun / Peter"
                                │                     │
                                └──────────┬──────────┘
                                           ▼
                                [Direct Scratchpad Pitch]
                            Speaks directly to the 10-minute
                            multi-tab travel planning headache.
                                           │
                                ┌──────────┴──────────┐
                                │ (NO - General Desk) │
                                ▼
                       [Front Desk Triage]
                     info@, hello@, enquiries@
                                │
                                ▼
                    [Polite Founder Referral Ask]
                      Variant A (Founder Discovery Ask)
                      Variant B (Multi-Tab Time Saver)
                      Variant C (55p Mileage Dispute)
                    "Could you point me to whoever coordinates
                     consultant travel or expenses at [Company]?"
```

1. **Arm 1: Direct Operational Pitch (No Referral Ask):**
   * **Targets:** `operations@`, `projects@`, `travel@`, `logistics@`, `delivery@`, `office@`, `contracts@`, or named operational team members (e.g. `arun.jardine@nobleprog.co.uk`, `peter@yoursim.co.uk`).
   * **Message:** Addresses them directly (`Hi Arun,` / `Hi team,`). Directly attacks the friction: *"When your consultants head out to client sites, does someone spend 10 minutes juggling Google Maps, Trainline, and station parking...?"*
   * **Tone:** Peer-to-peer software engineer scratchpad utility.

2. **Arm 2: Front Desk Triage Referral (Never Pitch the Receptionist):**
   * **Targets:** `info@`, `hello@`, `enquiries@`.
   * **Message:** 38 to 50 words. Never sells to the receptionist. Asks a polite, human referral question: *"Could you point me to whoever looks after consultant travel or expenses at [Company]? Just wanted to ask them 2 quick questions..."*
   * **Why it converts:** Gatekeepers and office administrators are paid to route incoming inquiries to the right department. An authentic founder ask gets forwarded directly to the Operations Manager or Practice Lead.

---

## 2. Free UK Data Sources for Scaling the Pipeline

There is no need to buy expensive ZoomInfo, Apollo, or Hunter subscriptions that contain outdated data. The UK public sector and business registries provide the cleanest, richest free datasets:

### Source 1: Companies House Advanced Search API (Free & Real-Time)
* **API Endpoint:** `https://api.company-information.service.gov.uk/advanced-search/companies`
* **Authentication:** Free API key (`2f9f5eed-3be4-43aa-9761-353d9067fdc1`).
* **High-Travel Target SIC Codes:**
  * `62020` — IT Infrastructure & Cloud Consulting
  * `62012` — Bespoke Software & Digital Delivery
  * `71122` — Civil & Structural Engineering Consulting
  * `70229` — Management & Strategy Advisory
  * `71111` — Architectural & Site Design Services
  * `74909` — Specialist Environmental & Technical Advisory
  * `71129` — Other Engineering & Technical Consulting
  * `62090` — Other Information Technology Services
  * `71200` — Technical Testing, Inspection & Compliance
* **High-Travel Targeted Keyword Searches (`company_name_includes` across 32 Niches):**
  Companies that include these terms in their name almost universally have consultants, engineers, or project managers traveling to client locations:
  * **Project & Cost Management:** `project management`, `cost consultants`, `quantity surveyors`
  * **Engineering & Technical Infrastructure:** `building services`, `structural engineers`, `civil engineering`, `consulting engineers`, `geotechnical`, `ground engineering`, `highway engineering`, `transport planning`, `m&e consulting`, `fire safety engineering`, `acoustic consultants`, `environmental consultancy`, `ecological consultancy`
  * **Field Services & Commissioning:** `field service`, `commissioning`, `technical testing`
  * **IT, Cloud & Architecture Consulting:** `systems integration`, `cloud consultancy`, `cyber security consulting`, `data consultancy`, `software consultancy`, `digital transformation`, `managed it services`
  * **Management, Commercial & Strategy Advisory:** `management consultancy`, `business advisory`, `operational consulting`, `procurement consulting`, `planning consultancy`, `chartered surveyors`

### Source 2: Crown Commercial Service (CCS) & Gov.uk Digital Marketplace
* **What it is:** Public registers of all UK IT and management consultancies approved to deliver public sector services (G-Cloud, Digital Outcomes and Specialists, Management Consultancy Framework 3).
* **Why it's high intent:** Public sector consultancies MUST travel to government client sites (Whitehall, local councils, NHS trusts, regional agencies) and MUST strictly justify travel expenses against civil service guidelines.
* **Access:** Open CSV exports available on Gov.uk and Digital Marketplace supplier directory.

### Source 3: Procurement Policy Note (PPN) 06/21 — Carbon Reduction Plans
* **What it is:** Any UK company bidding for major government contracts must publish a public Carbon Reduction Plan detailing their Scope 3 Business Travel emissions.
* **Why it's gold:** These documents publicly disclose their exact business travel emissions, employee headcounts, and often the exact sustainability or operations director responsible for travel.

### Source 4: UK Professional Association Public Directories
* **Association for Consultancy and Engineering (ACE):** Public directory of UK engineering and infrastructure consultancies.
* **Management Consultancies Association (MCA):** Member directory of UK consulting practices.
* **Association for Project Management (APM):** Corporate partners directory.
* **Institution of Civil Engineers (ICE) & IStructE:** Registered consulting engineering firms.

---

## 3. The EndMile High-Yield Verification & Mining Engine

The automated miner (`scripts/outreach/mine_verified_leads.py`) transforms raw registry records into enriched, zero-bounce leads through a 6-layer watertight validation pipeline:

```
[Companies House API / Registry Record]
                  │
                  ▼
       1. Watertight Candidate Domain Generation
          • Full exact slug (w2projectmanagement.co.uk, jlprojectmanagement.com)
          • Multi-word brand slugs (wardellarmstrong.co.uk, wardell-armstrong.com)
          • Single-word brand protection: NEVER test raw single words on .co.uk/.com!
            Enforces industry suffixes: {word}consulting.co.uk, {word}pm.co.uk,
            {word}engineering.co.uk, {word}projects.co.uk, {word}-consulting.co.uk
            (Eliminates Foster's beer, Winter clothing, Ruby shoes, Connaught hotel collisions)
                  │
                  ▼
       2. Live DNS MX Verification (0% Bounce Gate)
          • Queries DNS MX servers with 1.5s timeout
          • Identifies provider (Microsoft 365, Google Workspace, Mimecast, 20i)
          • Rejects domains without active mail exchange infrastructure
                  │
                  ▼
       3. Live HTTP 200 & Anti-Parking Filter
          • Requires domain to respond with live HTTP 200 (apex or www)
          • Immediately rejects parked domains, domain sales landers (Sedo, GoDaddy, Dan),
            and host default pages ("Domain Default page", cPanel, Plesk, Nginx default)
          • Rejects consumer/hospitality businesses (beer, brewery, age gate, clothing, salon)
                  │
                  ▼
       4. Brand Confirmation & B2B Consulting Verification
          • Brand Word Match: company brand name words MUST appear in website content
          • B2B Indicator Match: site MUST contain at least 2 consulting/engineering terms
            (consult, engineer, project, client, advisory, management, survey, planning, etc.)
                  │
                  ▼
       5. Deep Web Crawling & Inbox Extraction
          • Crawls /team, /our-team, /people, /leadership, /contact, /contact-us, /about-us
          • Extracts mailto: links and published departmental emails
          • Discovers named staff (e.g. Arun, Peter, Imran, Jan)
                  │
                  ▼
       6. Outward Postcode Geo-Mapping & Fit Scoring
          • Extracts UK Postal District (e.g. 'B', 'BS', 'LS', 'M')
          • Maps to realistic client travel corridor:
            e.g. Leeds (LS) ➔ London (Kings Cross) / Manchester / Birmingham
          • Scores fit (94–98/100) and synchronizes with CSV, Excel, and outreach tracker
```

---

## 4. Mailbox Hierarchy & Priority Routing

When crawling target websites, the miner applies this strict hierarchy to select the optimal recipient:

| Priority | Inbox Pattern | Target Role | Email Type Assigned |
|---|---|---|---|
| **1** | `travel@`, `logistics@`, `fleet@` | Travel & Dispatch Coordinator | Direct Scratchpad Pitch |
| **2** | `operations@`, `delivery@` | Operations Director / Practice Lead | Direct Scratchpad Pitch |
| **3** | `projects@`, `contracts@` | Projects & Delivery Lead | Direct Scratchpad Pitch |
| **4** | `practice@`, `office@` | Practice Manager / Office Coordinator | Direct Scratchpad Pitch |
| **5** | Named (`firstname.lastname@`, `firstname@`) | Named Practice Lead (`Hi [First Name]`) | Direct Scratchpad Pitch |
| **6** | Regional (`leeds@`, `bristol@`, `birmingham@`) | Regional Office Dispatch | Direct Scratchpad Pitch |
| **7** | `enquiries@`, `hello@`, `contact@` | Client Enquiries / Studio Team | Triage Referral Rotation (A/B/C) |
| **8** | `info@` | Triage Front Desk | Triage Referral Rotation (A/B/C) |

---

## 5. Execution Commands & Project Management Playbook

### 1. Master Excel Command Center
The master spreadsheet at `C:\Users\isaac\Documents\endmile\endmile_master_pipeline.xlsx` serves as the founder's interactive command center:
* **Sheet 1: `App Prospects Pipeline`**: Contains all 2,763 consultancy leads with frozen panes and dropdown validation:
  * **Column B (`ManualApproval`)**: Select `Approved`, `Pending Review`, `Hold`, `Skip`, or `Sent`. By default, only leads marked `Approved` are dispatched.
  * **Column C (`AssignedTemplate`)**: Select `AUTO`, `DIRECT_SCRATCHPAD`, `DIRECT_RECHARGE`, `INFO_REF_A`, `INFO_REF_B`, `INFO_REF_C`, or `INFO_REF_D`.
  * **Column D (`FounderNotes`)**: Enter specific notes or instructions per account.
* **Sheet 2: `Venue Widget Pipeline`**: Contains all 4,992 cultural venues with 59 founder-confirmed contacts pre-approved, dropdown validations, and staging links.
* **Sheet 3: `Email Templates & Referrers`**: Full catalogue of direct pitches, info@ referral variations, follow-ups, and widget templates with exact word counts, subjects, and bodies.
* **Sheet 4: `A-B Testing & Funnel Dashboard`**: Live funnel scorecard and variant performance breakdown for both products.

### 2. Opening and Synchronizing the Workbook
```bash
# Instantly launch the master workbook in Microsoft Excel:
npm run pipeline:open

# Force manual re-synchronization of CSV and Excel:
npm run outreach:sync
```

### 3. Previewing Outbound Dispatches (Dry Run)
```bash
# Preview next 5 approved App emails:
npm run outreach:app:preview

# Preview next 5 approved Venue Widget emails:
npm run outreach:widget:preview

# Preview with a specific template override:
python scripts/outreach/send_app_outreach.py --dry-run --limit 5 --template INFO_REF_A

# Preview specific leads:
python scripts/outreach/send_app_outreach.py --dry-run --leads APP-002,APP-003
```

### 4. Live Sending During UK Business Hours (Paced 10–20 Mins Apart)
```bash
# Live send next 5 approved App emails:
npm run outreach:app:send

# Live send next 5 approved Venue Widget emails:
npm run outreach:widget:send
```

### 5. Tracking Replies & Pipeline Review
```bash
# View real-time unified multi-product scoreboard & A/B testing matrix:
npm run outreach:report

# Check incoming IMAP inbox for replies from prospects:
npm run outreach:check-inbox

# Log an App prospect reply manually:
python scripts/outreach/track_outreach_replies.py --lead-id APP-002 --outcome Referral --notes "Forwarded to Head of Ops" --referral-email ops@audacia.co.uk

# Log a Venue reply manually:
python scripts/outreach/track_outreach_replies.py --venue-id 345886715 --outcome Positive --notes "Wants staging test"
```

### 6. Pacing & Deliverability Guardrails
* **Daily Volume:** 5–15 emails/day (ramp to 20/day maximum).
* **Human Pacing:** 10–20 minutes randomized pause between dispatches (600–1200 seconds).
* **Business Hours Only:** 08:30–17:30 UK time, Monday through Friday.
* **Exclusions:** Dorset Software Services (`dorsetsoftware.com`) is hard-excluded across all scripts.
* **Bounce Rate Target:** Exactly 0.0% (guaranteed by live DNS MX validation prior to sending).

