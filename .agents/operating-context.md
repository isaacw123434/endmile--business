# Operating Context

*Last updated: 2026-05-22*

This file defines how AI agents should work on EndMile across coding and non-coding tasks.

## Repository Strategy

Keep coding, product, brand, and early marketing context in this monorepo for now.

Reason: EndMile is still validating product direction. Code, roadmap, positioning, landing page copy, product UX, and customer feedback are tightly coupled. Splitting marketing into a separate repo would make most useful AI tasks slower because agents would need cross-repo context.

Create a separate brand or marketing repo only when external collaborators need access to campaigns, decks, interviews, or brand assets without touching code.

## Working Memory vs Durable Docs

Use `.agents/` for current AI working memory:

- short
- direct
- decision-oriented
- updated when direction changes
- read before AI tasks

Use `docs/` for durable project documentation:

- architecture references
- feature plans
- audits
- brand design guide
- technical inventories
- formal product planning

## Coding Workflow

For coding tasks:

1. Read root `AGENTS.md`.
2. Read the relevant package `AGENTS.md`.
3. Read `.agents/roadmap.md` if product direction affects the implementation.
4. Read `.agents/brand-context.md` and `docs/brand/brand-and-design.md` for UI, copy, landing page, or visual work.
5. Make the smallest coherent code change.
6. Run relevant checks.
7. Update `CHANGELOG.md`.
8. Update `.agents/decisions.md` if the change makes or reflects a product decision.

Follow the root architecture rules: Clean Architecture boundaries, dependency injection, integer pence for money, UTC timestamps, RLS for tenant data, no speculative abstractions, and no placeholder code.

## Non-Coding Workflow

For product, marketing, social, launch, research, or roadmap tasks:

1. Read `.agents/product-marketing.md`.
2. Read `.agents/customer-feedback.md` before making claims about pain, personas, demand, buyer urgency, or proof.
3. Read `.agents/brand-context.md` for tone, naming, style, and assets.
4. Read `.agents/content-log.md` for published, planned, and draft social content.
5. Read `.agents/roadmap.md` and `.agents/decisions.md` for current direction.
6. Produce or update the requested artifact.
7. Save new evidence, direction, or content in the right `.agents` file.
8. Update `CHANGELOG.md` when repo files change.

## Brand And Design Workflow

Brand and design tasks usually touch both product strategy and code.

Read:

- `.agents/brand-context.md`
- `docs/brand/brand-and-design.md`
- `.agents/product-marketing.md`
- `.agents/customer-feedback.md` when copy depends on customer pain
- package design docs if implementation touches Flutter or web UI

Keep brand work grounded in visible product behaviour. Avoid generic marketing language that is not supported by current product capabilities.

## Research Discipline

Treat current customer evidence as directional, not validated.

Current evidence is based on five pre-launch survey responses. It supports the existence of planning friction, cost pressure, timing anxiety, and expense uncertainty. It does not prove a firm buyer persona, pricing model, ROI claim, or enterprise procurement path.

When new research appears:

- put the raw quote or transcript in `.agents/customer-feedback.md`
- update synthesis only after patterns repeat
- update `.agents/roadmap.md` if priorities change
- update `.agents/product-marketing.md` only if positioning changes

## Content Discipline

Use `.agents/content-log.md` as the source of truth for posts and campaign history.

Mark each item as:

- published
- planned
- draft
- source data only

Do not treat planned drafts as published content. Do not turn source data into final post copy without a fresh prompt.

## Open Questions To Ask The User

Ask these when the answer matters to the task and is not already in the docs:

- Which segment is the current priority: consultants, universities, event organisers, business parks, sustainability leads, or corporate travel teams?
- Is EndMile currently positioning as early tester access, demo, beta, or live product?
- Is the main conversion action "Compare a route", "Try the Demo", "Install the app", or "Contact us"?
- Has the LinkedIn page URL changed or been recorded?
- Has the planned 2026-05-27 LinkedIn post been published?
- Are there new customer conversations that should be logged before copy or roadmap decisions are made?

