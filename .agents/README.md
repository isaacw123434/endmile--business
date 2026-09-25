# Agent Working Memory

*Last updated: 2026-05-22*

This folder contains AI-readable working memory for EndMile. These files are intentionally shorter and more current than the durable engineering docs in `docs/`.

## How To Use This Folder

Read the smallest set of files needed for the task:

| Task type | Read first |
|---|---|
| Coding feature or bug | `AGENTS.md`, the package `AGENTS.md`, `.agents/operating-context.md`, and `.agents/roadmap.md` when product direction matters |
| Product, positioning, or roadmap | `.agents/operating-context.md`, `.agents/roadmap.md`, `.agents/product-marketing.md`, `.agents/customer-feedback.md`, `.agents/decisions.md`, `docs/product/b2b-pretrip-pdf-justification-and-dispatch.md` |
| B2B Team Logistics & PDF Itinerary Export | `docs/product/b2b-pretrip-pdf-justification-and-dispatch.md`, `.agents/roadmap.md`, `.agents/customer-feedback.md`, `docs/new-features/saved-route-pdf-reports.md` |
| Marketing copy, social posts, launch, outreach, SEO | `.agents/product-marketing.md`, `.agents/customer-feedback.md`, `.agents/brand-context.md`, `.agents/content-log.md`, `.agents/decisions.md` |
| Brand, visual design, landing page, UI copy | `.agents/brand-context.md`, `docs/brand/brand-and-design.md`, `.agents/product-marketing.md`, and the relevant package design guide |
| Customer research | `.agents/customer-feedback.md`, `.agents/product-marketing.md`, `.agents/roadmap.md` |

## File Roles

| File | Purpose |
|---|---|
| `.agents/operating-context.md` | Workflow rules for coding and non-coding AI work in this repo |
| `.agents/roadmap.md` | Current Now, Next, Later priorities and success signals |
| `.agents/product-marketing.md` | Positioning, audience, value proposition, objections, and claims boundaries |
| `.agents/customer-feedback.md` | Raw research, survey responses, voice-of-customer quotes, and evidence quality |
| `.agents/brand-context.md` | AI-friendly brand, visual, asset, and copy rules |
| `.agents/content-log.md` | Published posts, planned posts, draft posts, and content ideas |
| `.agents/decisions.md` | Lightweight product, marketing, and workflow decision log |
| `.agents/skills/` | Repo-local marketing skills installed for this checkout |

## Update Rules

- Update the source file closest to the new information.
- Keep raw customer words in `.agents/customer-feedback.md`, not only in summaries.
- Keep final or planned posts in `.agents/content-log.md`.
- Keep positioning changes in `.agents/product-marketing.md`.
- Keep priority changes in `.agents/roadmap.md`.
- Record meaningful direction changes in `.agents/decisions.md`.
- Add a `CHANGELOG.md` entry at the end of active AI sessions that modify repo files.

