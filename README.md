# EndMile — The Business Brain & Commercial Command Center

[![Analytics Tests](https://img.shields.io/badge/analytics%20tests-passing-brightgreen)](scripts/analytics/)
[![Production Host](https://img.shields.io/badge/host-Contabo%20VPS%2030-blue)](operations/vps-access-and-operations.md)
[![Monthly Burn](https://img.shields.io/badge/infrastructure%20burn-~£37%2Fmo-green)](operations/infrastructure-costs-and-economics.md)

This repository is the **Business Brain & Commercial Heart** of **EndMile** (`endmilerouting.co.uk`), partnering directly with founder Isaac Willoughby to drive traction, craft high-converting copy, track outbound sales, analyze social engagement, and scale SaaS revenue.

The technical application codebase lives in the sibling repository: [`../endmile-1`](file:///c:/Users/isaac/Videos/files%20too%20big%20for%20onedrive/github/endmile-1). See [`CODEBASE_REFERENCE.md`](CODEBASE_REFERENCE.md) for full architecture and code mapping.

---

## Repository Structure

```text
.
├── AGENTS.md                                # Root instructions & operating system for the Business Brain
├── GEMINI.md                                # Gemini & Antigravity workspace guide
├── CLAUDE.md                                # Claude Code compatibility guide
├── CODEBASE_REFERENCE.md                    # Link to code repo (../endmile-1), tech stack, mapping
├── package.json                             # Analytics CLI test and execution scripts
├── traction/                                # Real-Time Commercial Traction & Pipeline Hub
│   ├── README.md                            # Traction operating guide
│   ├── outreach-tracker.md                  # Outbound sales touches, channels, follow-ups, and responses
│   ├── social-and-engagement.md             # Social posts (LinkedIn, X), metrics, impressions, comments
│   └── pipeline.md                          # Active B2B deals, trials, and MRR pipeline
├── copy-and-messaging/                      # High-Converting Copywriting & Site Building Lab
│   ├── README.md                            # Copywriting principles & voice guidelines
│   ├── site-copy.md                         # Full conversion copy & section layout for marketing sites
│   ├── social-posts-bank.md                 # Ready-to-publish LinkedIn post copy for the founder
│   └── outbound-email-templates.md          # High-converting cold email sequences for each ICP
├── sales-and-marketing/                     # Commercial Playbooks & Outbound Engines
│   ├── venue-widget-outbound-playbook.md   # Outbound sales playbook, modular cold email copy
│   ├── b2b-pretrip-pdf-justification.md    # Pre-trip travel cost justification & Paul Hardy persona
│   └── telemetry-and-discovery.md           # Search telemetry and intent discovery playbook
├── competitors/                             # Competitor Dossiers & Pricing Intelligence
│   ├── landscape-summary.md                 # MaaS, T&E, and routing platforms (Whim, SkedGo, Navan...)
│   ├── yst-detailed-landscape.md            # You. Smart. Thing. rate cards, enterprise vs free links
│   └── competitor-dossiers.md               # Feature comparison matrix & EndMile displacement wedges
├── operations/                              # VPS, Cost Economics, Analytics & Routing Queries
│   ├── vps-access-and-operations.md         # SSH access, server specs, Docker stack, health checks
│   ├── infrastructure-costs-and-economics.md# Contabo VPS, OJP API cost, Supabase, monthly burn
│   ├── how-to-query-routes.md               # Curl examples for streaming API, MOTIS & OSRM
│   ├── analytics-and-telemetry-cli.md       # How to run CLIs to query VPS DB, GA4, GSC & Bing
│   └── maintenance-and-rebuilds.md          # Weekly TNDS GTFS refresh & deployment workflow
├── b2c-strategy/                            # B2C Programmatic SEO & Venue Matrix
│   ├── b2c-strategy-overview.md             # B2C strategy & commercial monetization
│   ├── execution-progress.md                # Phase roadmap & milestone tracker
│   ├── publishing-guide.md                  # Venue publishing & allowlist operational guide
│   ├── embed-pilot.md                       # Controlled venue embed pilot
│   └── london-routing-strategy.md           # London routing & Park & Tube strategy
├── notes/                                   # Founder Drop Zone & Scratchpad
│   ├── README.md                            # Brainstorming & scratchpad guide
│   ├── inbox/                               # Fast capture drop-zone for raw notes, transcripts, ideas
│   ├── meetings/                            # Structured customer, prospect, partner, and advisor notes
│   ├── advisory/                            # Strategic memos and risk assessments from the Brain
│   └── templates/                           # Markdown templates (meetings, hypotheses, objections, memos)
├── .agents/                                 # Active Strategic Memory & 30 Business Skills
│   ├── roadmap.md                           # Commercial and product roadmap
│   ├── decisions.md                         # Architectural, product & commercial decision log
│   ├── product-marketing.md                 # Positioning, ICPs, and core value propositions
│   ├── customer-feedback.md                 # Buyer personas (Paul Hardy, venue directors) & interviews
│   ├── brand-context.md                     # Brand identity, tone of voice, visual rules
│   ├── operating-context.md                 # Dual-repo architecture & operational workflows
│   ├── content-log.md                       # Publishing & content status authority
│   └── skills/                              # 30 specialized AI agent skills (cold email, pricing, CRO...)
├── scripts/                                 # Production CLIs & Analytics Engines
│   └── analytics/
│       ├── guide-performance.mjs            # Guide & B2C analytics CLI (GA4, GSC, Bing, VPS DB)
│       ├── guide-performance.test.mjs       # CLI tests
│       ├── app-performance.mjs              # App & journey planner analytics CLI
│       ├── app-performance.test.mjs         # CLI tests
│       └── submit-indexnow.mjs              # IndexNow submission CLI
└── reference/                               # Domain Terminology & System Architecture
    ├── terminology.md                       # Comprehensive domain terminology dictionary
    ├── architecture-overview.md             # Clean Architecture, data flows & routing pipeline
    └── developer-commands.md                # Package & deployment commands
```

---

## Quick Start for Founder (Isaac)

### 1. Track Outbound & Social Engagement
- Tell the Brain what you posted or who you emailed:
  - *"I reached out to 12 theatres in the Midlands"* $\rightarrow$ Logged in [`traction/outreach-tracker.md`](traction/outreach-tracker.md).
  - *"I just posted about the Trainline illusion on LinkedIn"* $\rightarrow$ Logged in [`traction/social-and-engagement.md`](traction/social-and-engagement.md).
  - *"Got a reply from a theatre asking about pricing"* $\rightarrow$ Tracked in [`traction/pipeline.md`](traction/pipeline.md) with response drafted.

### 2. Grab Ready-to-Use Copy & Templates
- Need a LinkedIn post to publish today? Check [`copy-and-messaging/social-posts-bank.md`](copy-and-messaging/social-posts-bank.md).
- Need high-converting landing page sections? Check [`copy-and-messaging/site-copy.md`](copy-and-messaging/site-copy.md).
- Need cold outreach emails? Check [`copy-and-messaging/outbound-email-templates.md`](copy-and-messaging/outbound-email-templates.md).

### 3. Review Roadmap & Strategic Memory
- Current priorities & milestones: [`.agents/roadmap.md`](.agents/roadmap.md)
- Commercial decision history: [`.agents/decisions.md`](.agents/decisions.md)
- Competitor teardowns & pricing: [`competitors/README.md`](competitors/README.md)

### 4. Run Analytics & Telemetry
```bash
# Test analytics CLIs
npm run test:analytics

# B2C Guide pageviews, widget searches, and OJP costs (last 28 days)
npm run analytics:guide -- --days 28 --markdown

# App traffic channels, corridors, and cost savings
npm run analytics:app -- --days 28 --markdown
```
