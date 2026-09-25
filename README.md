# EndMile — Business Operations, Strategy & AI Command Center

[![Analytics Tests](https://img.shields.io/badge/analytics%20tests-passing-brightgreen)](scripts/analytics/)
[![Production Host](https://img.shields.io/badge/host-Contabo%20VPS%2030-blue)](operations/vps-access-and-operations.md)
[![Monthly Burn](https://img.shields.io/badge/infrastructure%20burn-~£37%2Fmo-green)](operations/infrastructure-costs-and-economics.md)

This repository serves as the central operations, commercial strategy, sales engine, and telemetry hub for **EndMile** (`endmilerouting.co.uk`). It is organized specifically for autonomous AI agents and executive operators to manage the business, outflank competitors, execute outbound sales, and monitor system performance.

The technical application codebase is maintained separately at [`../endmile-1`](file:///c:/Users/isaac/Videos/files%20too%20big%20for%20onedrive/github/endmile-1). See [`CODEBASE_REFERENCE.md`](CODEBASE_REFERENCE.md) for full architecture and code mapping.

---

## Repository Structure

```text
.
├── AGENTS.md                                # Root instructions & system prompt for AI business agents
├── GEMINI.md                                # Gemini CLI & Antigravity workspace guide
├── CLAUDE.md                                # Claude Code compatibility guide
├── CODEBASE_REFERENCE.md                    # Link to code repo (../endmile-1), tech stack, mapping
├── package.json                             # Analytics CLI test and execution scripts
├── .agents/                                 # AI working memory & 30 specialized business skills
│   ├── roadmap.md                           # Commercial and product roadmap
│   ├── decisions.md                         # Architectural, product & commercial decision log
│   ├── product-marketing.md                 # Positioning, ICPs, and core value propositions
│   ├── customer-feedback.md                 # Buyer personas (Paul Hardy, venue directors) & interviews
│   ├── brand-context.md                     # Brand identity, tone of voice, visual rules
│   ├── operating-context.md                 # Operating environment, cost constraints, team setup
│   ├── content-log.md                       # Publishing & content status authority
│   └── skills/                              # 30 specialized AI agent skills (cold email, pricing, CRO...)
├── competitors/                             # Competitor dossiers & intelligence
│   ├── landscape-summary.md                 # MaaS, T&E, and routing platforms (Whim, SkedGo, Navan...)
│   ├── yst-detailed-landscape.md            # You. Smart. Thing. rate cards, enterprise vs free links
│   └── competitor-dossiers.md               # Feature comparison matrix & EndMile wedges
├── sales-and-marketing/                     # Commercial playbooks & outbound engines
│   ├── venue-widget-outbound-playbook.md   # Outbound sales playbook, modular cold email copy
│   ├── b2b-pretrip-pdf-justification.md    # Pre-trip travel cost justification & Paul Hardy persona
│   └── telemetry-and-discovery.md           # Search telemetry and intent discovery playbook
├── operations/                              # VPS, cost economics, analytics & routing queries
│   ├── vps-access-and-operations.md         # SSH access, server specs, Docker stack, health checks
│   ├── infrastructure-costs-and-economics.md# Contabo VPS, OJP API cost, Supabase, monthly burn
│   ├── how-to-query-routes.md               # Curl examples for streaming API, MOTIS & OSRM
│   ├── analytics-and-telemetry-cli.md       # How to run CLIs to query VPS DB, GA4, GSC & Bing
│   └── maintenance-and-rebuilds.md          # Weekly TNDS GTFS refresh & deployment workflow
├── scripts/                                 # Production CLIs & analytics engines
│   └── analytics/
│       ├── guide-performance.mjs            # Guide & B2C analytics CLI (GA4, GSC, Bing, VPS DB)
│       ├── guide-performance.test.mjs       # CLI tests
│       ├── app-performance.mjs              # App & journey planner analytics CLI
│       ├── app-performance.test.mjs         # CLI tests
│       └── submit-indexnow.mjs              # IndexNow submission CLI
├── b2c-strategy/                            # B2C Programmatic SEO & Venue Matrix
│   ├── b2c-strategy-overview.md             # B2C strategy & commercial monetization
│   ├── execution-progress.md                # Phase roadmap & milestone tracker
│   ├── publishing-guide.md                  # Venue publishing & allowlist operational guide
│   ├── embed-pilot.md                       # Controlled venue embed pilot
│   └── london-routing-strategy.md           # London routing & Park & Tube strategy
└── reference/                               # High-level technical reference & domain context
    ├── terminology.md                       # Comprehensive domain terminology dictionary
    ├── architecture-overview.md             # Clean Architecture, data flows & routing pipeline
    └── developer-commands.md                # Package & deployment commands
```

---

## Quick Start for AI Agents & Operators

### 1. View Strategic Roadmap & Decision Log
- Current priorities: [`.agents/roadmap.md`](.agents/roadmap.md)
- Architectural & commercial decisions: [`.agents/decisions.md`](.agents/decisions.md)

### 2. Run Analytics CLIs
```bash
# Test analytics CLIs
npm run test:analytics

# B2C Guide pageviews, widget searches, and OJP costs (last 28 days)
npm run analytics:guide -- --days 28 --markdown

# App traffic channels, corridors, and TCO savings
npm run analytics:app -- --days 28 --markdown

# Query live production database via SSH
npm run analytics:app -- --days 7 --ssh-db deploy@155.133.23.54 --markdown
```

### 3. Competitor Intelligence & Outbound Sales
- Review competitive pricing and displacement wedges in [`competitors/README.md`](competitors/README.md).
- Access cold email copy and objection handling in [`sales-and-marketing/README.md`](sales-and-marketing/README.md).

### 4. VPS Access & Operations
- Server specs, SSH, and Docker management in [`operations/vps-access-and-operations.md`](operations/vps-access-and-operations.md).
- Routing query recipes in [`operations/how-to-query-routes.md`](operations/how-to-query-routes.md).
