# EndMile Business Operations Hub — Gemini Reference

This repository (`endmile--business`) is the business, strategy, and operational command center for EndMile.

## Core Reference
- Master rules and navigation: [`AGENTS.md`](AGENTS.md)
- Codebase pointer: [`CODEBASE_REFERENCE.md`](CODEBASE_REFERENCE.md) (source code lives at `../endmile-1`)
- Competitor dossiers: [`competitors/README.md`](competitors/README.md)
- Outbound sales playbooks: [`sales-and-marketing/README.md`](sales-and-marketing/README.md)
- VPS operations & costs: [`operations/README.md`](operations/README.md)
- Analytics CLIs: [`scripts/analytics/`](scripts/analytics/) and [`operations/analytics-and-telemetry-cli.md`](operations/analytics-and-telemetry-cli.md)

## Common Commands
```bash
# Run analytics test suite
npm run test:analytics

# Run Guide analytics
node scripts/analytics/guide-performance.mjs --days 28 --surface guide --markdown

# Run App channel and corridor analytics
node scripts/analytics/app-performance.mjs --days 28 --markdown
```
