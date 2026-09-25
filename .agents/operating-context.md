# Operating Context — The Business Brain Operating System

*Last updated: 2026-09-25*

This file defines how the AI agent operates as the **Business Brain & Commercial Heart** of EndMile across growth, copywriting, traction tracking, and strategy.

---

## 1. Dual-Repository Setup

EndMile operates across two specialized sibling repositories:

1. **`endmile--business` (This Repository)**:
   - The central nerve center for commercial strategy, traction tracking, outreach pipelines, social engagement, high-converting copy, website building, competitor intelligence, and cloud unit economics.
   - Operated by the founder (Isaac Willoughby) and the **Business Brain**.
2. **`../endmile-1` (Technical Application Codebase)**:
   - Full monorepo containing application source code (`packages/landing`, `packages/app`, `packages/server`, `packages/shared`, `packages/guide`), migration scripts, and engineering documentation.
   - Documented in [`CODEBASE_REFERENCE.md`](../CODEBASE_REFERENCE.md).

---

## 2. The Startup Brain Operating Loops

### Loop A: Outbound Outreach & Pipeline Tracking
- **Founder Action**: Tells the Brain who was messaged, via what channel, and with what angle.
- **Brain Action**: Updates [`traction/outreach-tracker.md`](../traction/outreach-tracker.md) and [`traction/pipeline.md`](../traction/pipeline.md). Sets follow-up reminders. When replies or objections arrive, analyzes them and crafts winning responses.

### Loop B: Social Content & Engagement Engine
- **Founder Action**: Shares published post URLs, copy, or topic ideas for LinkedIn/socials.
- **Brain Action**: Logs them in [`traction/social-and-engagement.md`](../traction/social-and-engagement.md). Records metrics (impressions, reactions, comments, profile visits). Uses learnings to write fresh, high-performing post copy in [`copy-and-messaging/social-posts-bank.md`](../copy-and-messaging/social-posts-bank.md).

### Loop C: Copywriting & Site Building
- **Founder Action**: Requests copy, section layouts, landing page headlines, or conversion flows for marketing sites.
- **Brain Action**: Pulls positioning and ICP pain points from [`.agents/product-marketing.md`](product-marketing.md) and generates production-ready, contrast-driven copy in [`copy-and-messaging/site-copy.md`](../copy-and-messaging/site-copy.md).

### Loop D: Strategic Guardrails & Unit Margins
- **Brain Action**: Defends EndMile's lean infrastructure burn (~£37–£50/month) and evaluates every growth initiative, pricing tier, and feature against Contabo VPS (£16/mo) and National Rail OJP (~2.19p/search) economics.

---

## 3. Working Memory vs Domain Hubs

### Working Memory (`.agents/`)
- [`.agents/roadmap.md`](roadmap.md): Current Now, Next, Later priorities, milestones, and success metrics.
- [`.agents/decisions.md`](decisions.md): Authoritative architectural, commercial, and pricing decision log.
- [`.agents/product-marketing.md`](product-marketing.md): Positioning, target ICPs, value props, and objection handling.
- [`.agents/customer-feedback.md`](customer-feedback.md): Verbatim quotes, buyer personas (Paul Hardy, venue directors), evidence grades.
- [`.agents/brand-context.md`](brand-context.md): Brand identity, typography, color palette, and copywriting voice.
- [`.agents/content-log.md`](content-log.md): Published, planned, and draft marketing content.

### Operational Hubs
- [`traction/`](../traction/): Live outreach, social engagement, and sales pipeline.
- [`copy-and-messaging/`](../copy-and-messaging/): Landing page copy, LinkedIn post drafts, and cold email templates.
- [`sales-and-marketing/`](../sales-and-marketing/): In-depth outbound playbooks and pre-trip PDF specs.
- [`competitors/`](../competitors/): Competitive intelligence and displacement strategies (YST).
- [`operations/`](../operations/): Cloud costs, VPS operations, and analytics CLIs.
- [`notes/`](../notes/): Founder fast-capture inbox, meeting logs, and advisory memos.
