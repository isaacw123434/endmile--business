# Agent Working Memory

*Last updated: 2026-09-25*

This directory contains AI-readable working memory for EndMile. These files represent current, active strategic state and decision history.

---

## 1. How To Use Working Memory & Notes

Read the smallest set of files needed for the task:

| Task Type | Read First |
|---|---|
| **Founder notes review & triage** | `notes/inbox/`, `.agents/customer-feedback.md`, `.agents/decisions.md`, `.agents/roadmap.md` |
| **Product, positioning, or roadmap** | `.agents/operating-context.md`, `.agents/roadmap.md`, `.agents/product-marketing.md`, `.agents/customer-feedback.md`, `.agents/decisions.md` |
| **B2B Pre-Trip PDF & Invoicing** | `sales-and-marketing/b2b-pretrip-pdf-justification.md`, `.agents/customer-feedback.md`, `.agents/roadmap.md` |
| **B2B Venue Travel Widget** | `sales-and-marketing/venue-widget-outbound-playbook.md`, `competitors/yst-detailed-landscape.md`, `.agents/product-marketing.md` |
| **Marketing copy, launch, outreach, SEO** | `.agents/product-marketing.md`, `.agents/customer-feedback.md`, `.agents/brand-context.md`, `.agents/content-log.md` |
| **Brand, visual design, landing page copy** | `.agents/brand-context.md`, `../endmile-1/docs/brand/brand-and-design.md`, `.agents/product-marketing.md` |
| **Customer feedback & objections** | `.agents/customer-feedback.md`, `notes/meetings/`, `.agents/product-marketing.md` |

---

## 2. Working Memory File Roles

| File | Purpose |
|---|---|
| [`.agents/operating-context.md`](operating-context.md) | Dual-repo architecture and Business Notes Advisor workflow rules |
| [`.agents/roadmap.md`](roadmap.md) | Current Now, Next, Later priorities, milestones, and success metrics |
| [`.agents/decisions.md`](decisions.md) | Authoritative architectural, commercial, and pricing decision log |
| [`.agents/product-marketing.md`](product-marketing.md) | Positioning, target ICPs, value props, and objection handling |
| [`.agents/customer-feedback.md`](customer-feedback.md) | Verbatim quotes, buyer personas (Paul Hardy, venue directors), evidence grades |
| [`.agents/brand-context.md`](brand-context.md) | Brand identity, typography, color palette, and copywriting voice |
| [`.agents/content-log.md`](content-log.md) | Published, planned, and draft marketing content |
| [`.agents/skills/`](skills/) | 30 specialized AI agent skills for growth, pricing, sales, and analytics |

---

## 3. Maintenance Rules for the Business Notes Advisor

- **Capture Verbatim Signal**: Record exact prospect words in `.agents/customer-feedback.md`.
- **Log Every Direction Change**: Any pricing, architectural, or commercial shift must be added to `.agents/decisions.md`.
- **Maintain Roadmap Currency**: Reflect completed or reprioritized initiatives in `.agents/roadmap.md`.
- **Preserve Lean Economics**: Ensure all strategic choices respect our ~£37–£50/month infrastructure ceiling.
