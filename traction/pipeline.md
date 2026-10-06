# Commercial Pipeline & Revenue Tracker

*Maintained by the Founder & EndMile Business Brain.*

---

## 1. Revenue Funnel Overview

| Stage | Venue Widget Pipeline (SaaS) | App / Consultant Pipeline (SaaS) | Potential MRR | Notes |
|---|---|---|---|---|
| **Audited Leads Sourced** | **4,992 Cultural Venues** (`endmile widget v4.xlsx` / Sheet 4 of Master Workbook) | **2,763 Consultancies** (1,351 Verified Active, `app_prospects_v1.csv` & Master Workbook) | £25,000–£120,000/mo | Sourced from Companies House API + ONS SIC registries; 0.0% hard bounce rate on verified |
| **Founder Manual Verification** | **In Progress (Isaac manually confirming emails)** | **20 Approved for Batch 1** (`ManualApproval == 'Approved'`) | — | Isaac project manages via Excel workbook dropdowns |
| **Outreach Sent** | 0 | 0 | — | Paced 10–20 mins apart during UK business hours (5–20/day) |
| **Conversation / Discovery** | 0 | 1 (Dorset Software / Paul Hardy) | £29–£49/mo | Organic usage analysis; converting to paid Pro workspace |
| **Trial / Active Pilot** | 0 | 0 | — | 14-day free sandbox trial |
| **Active Paying Customer** | 0 | 0 | £0/mo | Immediate Target: 10 paying customers (£290–£490 MRR) |

---

## 2. Active B2B Deals & Priority Leads in Flight

### A. Web App / Consultant Travel Dispatch ("Paul Profile")

*Full pipeline: [`data/consultancies/app_prospects_v1.csv`](../data/consultancies/app_prospects_v1.csv) / `C:\Users\isaac\Documents\endmile\endmile_master_pipeline.xlsx` (Sheet: `App Prospects Pipeline`)*  
*Total verified: 1,351 active consultancies (0.0% hard bounce rate, 100% verified UK MX infrastructure)*  
*Manual Control Columns:* `ManualApproval` (`Approved`, `Pending Review`, `Hold`, `Skip`, `Sent`), `AssignedTemplate` (`AUTO`, `DIRECT_SCRATCHPAD`, `INFO_REF_A`, `INFO_REF_B`, `INFO_REF_C`, `INFO_REF_D`, `DIRECT_RECHARGE`), `FounderNotes`.

| Lead ID | Company Name | Contact Role / Name | Approval Status | Assigned Template | Key Travel Corridor | Next Action |
|---|---|---|---|---|---|---|
| **APP-001** | **Dorset Software Services Ltd** | Paul Hardy (`logistics@dorsetsoftware.com`) | **Excluded / Existing** | Direct Pitch | Poole (BH15) ➔ London / Oxford | Organic Power User (Do not cold email) |
| **APP-002** | **Avecto Ltd** | Operations / Triage (`info@avecto.com`) | **Approved** | `AUTO` (INFO_REF_A) | Manchester / Cheshire ➔ London | Ready in Batch 1 (Preview verified) |
| **APP-003** | **Redrock Consulting Limited** | Operations / Triage (`info@redrockconsulting.co.uk`) | **Approved** | `AUTO` (INFO_REF_B) | Bristol ➔ London / Reading | Ready in Batch 1 (Preview verified) |
| **APP-006** | **Arbnco Ltd** | Practice / Operations (`info@arbnco.com`) | **Approved** | `AUTO` (INFO_REF_C) | Glasgow ➔ Edinburgh / Manchester | Ready in Batch 1 (Preview verified) |
| **APP-008** | **Chetwood Architects Limited** | Practice Manager (`info@chetwood.co.uk`) | **Approved** | `AUTO` (INFO_REF_D) | London (EC1) ➔ Birmingham / Leeds | Ready in Batch 1 |
| **APP-010** | **Quod Limited** | Planning Ops (`info@quod.com`) | **Approved** | `AUTO` | London (W1) ➔ Leeds / Bristol | Ready in Batch 1 |
| **APP-012** | **Hydrock Consultants Limited** | Engineering Ops (`bristol@hydrock.com`) | **Approved** | `DIRECT_SCRATCHPAD` | Bristol ➔ London / Cardiff | Ready in Batch 1 |
| **APP-015** | **Buro Happold Limited** | Project Travel Team (`info@burohappold.com`) | **Approved** | `AUTO` | Bath / London ➔ Leeds / Manchester | Ready in Batch 1 |

---

### B. Venue Travel Widget SaaS (Cultural Venues & Theatres)

*Full pipeline: `C:\Users\isaac\Documents\endmile\endmile_master_pipeline.xlsx` (Sheet: `Venue Widget Pipeline`)*  
*Status: 4,992 unserved UK cultural venues identified; 59 founder-confirmed contacts pre-approved in Sheet 2.*

| Venue Name | Archetype | Fit Tier | Public Email | Isaac Confirmed Contact | Key Multimodal Feature | Next Step |
|---|---|---|---|---|---|---|
| **Charing Cross Theatre** | Regional Independent Theatre | Exceptional Fit (95) | `info@charingcrosstheatre.co.uk` | `manager@charingcrosstheatre.co.uk` | Walkable Rail (2m); High Footfall | Awaiting manual confirmation before batch send |
| **Sharmanka Kinetic Theatre** | Civic Museum / Gallery | Exceptional Fit (95) | `info@sharmanka.com` | `office@sharmanka.com` | Walkable Rail (4m); Park & Ride | Awaiting manual confirmation before batch send |
| **Harrogate Theatre** | Civic Theatre & Arts Centre | Exceptional Fit (93) | `info@harrogatetheatre.co.uk` | Box Office & Ops Lead | Train (5m); Council Car Parks | Awaiting manual confirmation |
| **The Lowry** | Large Arts & Performance Complex | Growth Fit (90) | `info@thelowry.com` | Visitor Services Manager | Tram / Metrolink, Multi-storey | Awaiting manual confirmation |

---

## 3. Product Lines & Unit Economics Guardrails

| Product Line | Pricing | Target Gross Margin | Direct Marginal Cost |
|---|---|---|---|
| **Venue Travel Widget SaaS** | £19–£49/mo | >95% | ~£0.50/mo OJP rail searches |
| **Consultant Pre-Trip SaaS** | £29–£49/mo | >94% | ~£1.00/mo OJP rail searches |
| **B2C Programmatic Affiliates** | Performance-based | 100% | £0 marginal cost (precomputed) |

*Contabo Cloud VPS 30: £16.00/mo | OJP Rail API: £0.00042/call (~2.19p/search blended) | Total monthly burn: ~£37–£50/mo.*
