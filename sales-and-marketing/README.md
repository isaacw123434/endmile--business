# Sales & Marketing Command Center

Playbooks, outbound email sequences, buyer personas, onboarding processes, and discovery tools for driving revenue and customer acquisition.

## Documents

| Document | Focus & Target Audience |
|---|---|
| [`venue-widget-outbound-playbook.md`](venue-widget-outbound-playbook.md) | **B2B 'Plan Your Visit' Venue Widget Playbook:** Targeting 4,992 UK cultural destinations and independent visitor venues. Contains verified prospect discovery, footfall-to-search mathematical conversion models, 3-touch modular cold email copy, objection handling (e.g. "We already use Google Maps", "We have no budget"), and implementation snippets. |
| [`venue-widget-onboarding-and-approval.md`](venue-widget-onboarding-and-approval.md) | **Venue Widget Onboarding & Approval Process:** The step-by-step process when a venue agrees to install the widget. Covers CMS installation (WordPress, Squarespace, Wix, custom), pre-launch staging verification checklist, stakeholder sign-off, and ongoing Julie's Bicycle Scope 3 reporting. |
| [`b2b-pretrip-pdf-justification.md`](b2b-pretrip-pdf-justification.md) | **B2B Professional Services & Consultant Dispatch:** Focuses on the master product specification for the 2-page Pre-Trip Cost Justification PDF, consultant dispatch, HMRC 55p AMAP mileage defense, and PPN 06/21 Scope 3 carbon compliance. |
| [`consultant-and-field-travel-acquisition.md`](consultant-and-field-travel-acquisition.md) | **B2B Travel Acquisition & Commercial Monetization Strategy:** Comprehensive go-to-market and acquisition strategy across consultancies, engineering field services, and inspection teams. Includes ecosystem mapping, channel ranking filtered through strict monetization gates (rejecting expensive trade shows/PR), and the PLG freemium monetization funnel. |
| [`telemetry-and-discovery.md`](telemetry-and-discovery.md) | **Intent Telemetry & Forensic Discovery:** How to convert live journey searches, route completions, and search failures into actionable sales leads and product improvements. |

---

## Authoritative Prospect Pipelines & Data Files

| Pipeline | Target Audience | Authoritative CSV | Formatted Excel | Size & Quality |
|---|---|---|---|---|
| **Venue Widget SaaS (Master)** | Independent Cultural Venues & Theatres | [`../endmile-1/data/venues/unserved_prospects.csv`](file:///c:/Users/isaac/Videos/files%20too%20big%20for%20onedrive/github/endmile-1/data/venues/unserved_prospects.csv) | `C:\Users\isaac\Downloads\endmile_widget_prospects.xlsx` | **810 Exceptional Fit independent venues** (out of 4,414 total independents; 207 councils and 371 corporate chains segregated). Formatted as native Excel Table (`ProspectTable`) with 1-click filter dropdowns, deep-linked contact search, and live widget links. |
| **Venue Widget SaaS (Curated V3 Batch)** | High-Priority Independent Theatres & Trusts | [`../endmile-1/data/venues/unserved_prospects_v3.csv`](file:///c:/Users/isaac/Videos/files%20too%20big%20for%20onedrive/github/endmile-1/data/venues/unserved_prospects_v3.csv) | `C:\Users\isaac\Downloads\endmile widget v3.xlsx` | **~400 vetted independent venues** (tight sub-selection with pre-populated discovered emails in Column 1). |
| **Web App / Consultant SaaS** | UK Tech, Engineering & Management Consultancies ("Paul Profile") | [`data/consultancies/app_prospects_v1.csv`](data/consultancies/app_prospects_v1.csv) | `C:\Users\isaac\Downloads\endmile app prospects v1.xlsx` | **1,613 verified consultancies** (669 Exceptional, 886 Strong, 58 Moderate). Enriched via Companies House API across 80+ UK cities and outward postcodes with registered address, accounts type, operational inbox, telephone, and local travel corridors. |





---

## Key Buyer Personas

### 1. The Venue Commercial / Operations Director
- **Title:** Head of Visitor Experience, Commercial Director, Operations Manager.
- **Pain Points:** Visitors calling about parking congestion; outdated directions on website; failure to meet Arts Council England green travel mandates; losing mobile visitors due to bad Google Maps links.
- **Value Prop:** 1-line HTML embed, £0 setup, £19-£49/mo, automatic parking tariffs, carbon reporting.

### 2. The Logistics Coordinator / Travel Dispatcher / EA ("Paul Hardy" Persona)
- **Title:** Travel Coordinator, Office Operations Manager, Executive Assistant, Resource Dispatcher.
- **Company Profile:** IT consultancies, engineering firms, management consultancies, legal/accountancy practices, field service providers (50–500 employees).
- **Pain Points:** Disputed client travel recharges (rejection of £110 mileage expenses); consultant complaints about confusing train/taxi transfers; lack of defensible pre-trip audit documentation; manual time lost stitching together 3+ apps.
- **Value Prop:** 1-click Pre-Trip Justification PDF attached to invoices, zero-login mobile itinerary link sent to consultants, automated HMRC 55p AMAP vs rail TCO calculation (£19–£49/mo).
