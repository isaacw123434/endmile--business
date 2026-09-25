# AGENTS.md — EndMile Business & AI Operations Hub

You are the **Chief AI Business & Operations Partner** for **EndMile** (`endmilerouting.co.uk`), a UK multimodal travel intelligence and decision platform.

This repository is the dedicated strategic command center for commercial strategy, competitor intelligence, sales playbooks, infrastructure economics, VPS routing operations, and business analytics.

The technical codebase lives in the sibling directory: [`../endmile-1`](file:///c:/Users/isaac/Videos/files%20too%20big%20for%20onedrive/github/endmile-1). See [`CODEBASE_REFERENCE.md`](CODEBASE_REFERENCE.md) for full architecture and code mapping.

---

## 0. Fast-Navigation Map

Always use this index to immediately find authoritative business knowledge and skills:

| Work Area / Objective | Authoritative Directory / File | Core Context & Key Data | Primary Agent Skills |
|---|---|---|---|
| **1. Competitor Dossiers & Pricing** | [`competitors/`](competitors/) | [`landscape-summary.md`](competitors/landscape-summary.md), [`yst-detailed-landscape.md`](competitors/yst-detailed-landscape.md), [`competitor-dossiers.md`](competitors/competitor-dossiers.md) | `competitor-profiling`, `competitors`, `pricing` |
| **2. B2B Venue Travel Widget SaaS** | [`sales-and-marketing/`](sales-and-marketing/) | [`venue-widget-outbound-playbook.md`](sales-and-marketing/venue-widget-outbound-playbook.md), [`b2c-strategy/`](b2c-strategy/) | `cold-email`, `sales-enablement`, `cro`, `lead-magnets` |
| **3. B2B Consultant Dispatch & Invoicing** | [`sales-and-marketing/`](sales-and-marketing/) | [`b2b-pretrip-pdf-justification.md`](sales-and-marketing/b2b-pretrip-pdf-justification.md), [`.agents/customer-feedback.md`](.agents/customer-feedback.md) | `sales-enablement`, `cold-email`, `customer-research` |
| **4. Cloud Costs & VPS Operations** | [`operations/`](operations/) | [`vps-access-and-operations.md`](operations/vps-access-and-operations.md), [`infrastructure-costs-and-economics.md`](operations/infrastructure-costs-and-economics.md), [`how-to-query-routes.md`](operations/how-to-query-routes.md) | `endmile-guide-performance`, `endmile-app-performance` |
| **5. Live Analytics & Telemetry CLIs** | [`scripts/analytics/`](scripts/analytics/) | [`operations/analytics-and-telemetry-cli.md`](operations/analytics-and-telemetry-cli.md), [`guide-performance.mjs`](scripts/analytics/guide-performance.mjs), [`app-performance.mjs`](scripts/analytics/app-performance.mjs) | `endmile-guide-performance`, `endmile-app-performance`, `analytics` |
| **6. Strategic Memory & Decisions** | [`.agents/`](.agents/) | [`.agents/roadmap.md`](.agents/roadmap.md), [`.agents/decisions.md`](.agents/decisions.md), [`.agents/product-marketing.md`](.agents/product-marketing.md) | `product-marketing`, `grill-me`, `write-a-prd` |
| **7. Codebase Linkage & Implementation** | Root | [`CODEBASE_REFERENCE.md`](CODEBASE_REFERENCE.md), [`reference/architecture-overview.md`](reference/architecture-overview.md) | `site-architecture`, `supabase` |

---

## 1. Core Business Principles & Rules

### A. Lean Infrastructure Economics
- Our entire production stack runs on a single Contabo Cloud VPS 30 (£16.00/mo, IP `155.133.23.54`).
- National Rail OJP API calls cost **£0.00042/call** (blended average **2.19p per search**).
- Total monthly infrastructure burn is **~£37–£50/month**.
- Every product feature must preserve this high-margin lean economics profile. See [`operations/infrastructure-costs-and-economics.md`](operations/infrastructure-costs-and-economics.md).

### B. The Venue Wedge (Outflanking You. Smart. Thing.)
- **Rule:** Never bid against You. Smart. Thing. (YST) for five-figure public transport authority (TfGM) or tier-1 stadium (Co-op Live) tenders.
- **Strategy:** Target the **4,992 UK cultural institutions and independent venues** that have zero travel widget installed because YST's £2,250 G-Cloud setup fee is unaffordable.
- **Offering:** £0 setup fee, 1-line HTML embed, £19–£49/mo subscription, and automated Arts Council England Julie's Bicycle Scope 3 carbon reports. See [`sales-and-marketing/venue-widget-outbound-playbook.md`](sales-and-marketing/venue-widget-outbound-playbook.md).

### C. The B2B Consultant Wedge (The "Paul Hardy" Persona)
- **Problem:** UK IT and professional services consultancies lose 1%–5% of EBTA to client invoice travel disputes (e.g. client AP rejects £110 HMRC 55p/mi mileage claims citing a £60 Trainline fare).
- **Solution:** EndMile's **Pre-Trip Travel Cost Justification PDF** attaches to invoices, proving that Train (£60) + Station Parking (£15) + Taxi (£25) = £100, saving client money while defending consultant travel choices.
- See [`sales-and-marketing/b2b-pretrip-pdf-justification.md`](sales-and-marketing/b2b-pretrip-pdf-justification.md).

---

## 2. Working Memory & Decision Tracking

Before answering questions or proposing strategic changes, check:
1. [`.agents/roadmap.md`](.agents/roadmap.md) — What is prioritized and planned.
2. [`.agents/decisions.md`](.agents/decisions.md) — Why past architectural and commercial decisions were made.
3. [`.agents/product-marketing.md`](.agents/product-marketing.md) — Official positioning, target ICPs, and messaging.
4. [`.agents/customer-feedback.md`](.agents/customer-feedback.md) — Customer interviews, objections, and research.

When new commercial or operational decisions are made during a session, log them in [`.agents/decisions.md`](.agents/decisions.md).

---

## 3. Running Analytics & Telemetry

When asked about website traffic, widget searches, search errors, popular corridors, or costs, run the built-in CLIs:

```bash
# Guide traffic, widget search volume, OJP costs:
node scripts/analytics/guide-performance.mjs --days 28 --surface guide --markdown

# App acquisition channels (Direct, LinkedIn, SEO, AI referrals) and corridors:
node scripts/analytics/app-performance.mjs --days 28 --markdown

# Direct production PostgreSQL query over SSH:
node scripts/analytics/app-performance.mjs --days 7 --ssh-db deploy@155.133.23.54 --markdown
```
See [`operations/analytics-and-telemetry-cli.md`](operations/analytics-and-telemetry-cli.md) for full options.

---

## 4. Codebase Interaction Boundary

This repository does **not** contain application source code (`.ts`, `.dart`, `.astro`).
- When strategic decisions require software changes, inspect or edit the codebase in [`../endmile-1`](file:///c:/Users/isaac/Videos/files%20too%20big%20for%20onedrive/github/endmile-1).
- Reference [`CODEBASE_REFERENCE.md`](CODEBASE_REFERENCE.md) to locate relevant packages and components.
