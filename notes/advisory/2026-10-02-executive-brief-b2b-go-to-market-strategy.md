# Executive Brief – EndMile B2B Go-To-Market Strategy  

- **Date:** 2026-10-02
- **Source:** External Deep Research Intelligence & Founder Strategy
- **Category:** B2B SaaS Go-To-Market & Pricing Advisory (Wedge 2: Logistics Coordinator / Consultant Dispatch)
- **Status:** Strategic Reference Document

---

## Part 1: Monetising the Power User (Packaging & Billing)  

**Packaging & Paywall Architecture:** Offer a tiered freemium model that keeps core route-searching free but gates higher-value outputs and limits. For example:  
- **Free Tier:** Unlimited door-to-door route searches (train, car, taxi, etc.) with up to 3 saved journeys and basic risk/emissions info. No export/share features.  
- **Pro (Solo) Tier (£19/mo or £190/yr):** Unlimited saved routes and automated scheduling (e.g. save trips weeks ahead). Unlock **PDF route-evidence reports** for expense claims, custom HMRC mileage presets, and one-click export of cost/carbon breakdown. These gated “premium” features follow typical freemium practice (e.g. exports or analytics only in paid plans).  
- **Team Tier (£49/mo or £490/yr):** Includes all Solo features plus multi-user/seat access, team dashboards, branded itinerary templates (company logos on PDFs), and bulk CSV exports of travel costs for finance. This matches a *seat-based* model – free for an individual user, paid as soon as a team needs multiple seats.  

Key paywall trigger points: keep the **30-second route search** habit frictionless, but require upgrade for *dispatch tools* (PDF/email reports, multi-route scheduling, team billing exports). For instance, allow free users to run live comparisons, but prompt “Upgrade to export a PDF report” or “Upgrade to schedule unlimited routes” after a few uses. A clear “you’re missing X feature” message (e.g. “Unlock route exports for auditors”) can be shown once a user hits a limit. This follows best practices: map feature availability to usage stages and A/B test phrasing (e.g. “Upgrade to export” vs “Unlock unlimited exports”). 

**Pricing Points & Willingness-To-Pay:** Target the <£50/month departmental budget commonly used for shadow-IT purchases. A **Solo** plan at ~£19/mo (with a £190 annual option) sits under this threshold, so a coordinator can “just expense it” without CFO sign-off. The **Team** plan (~£49/mo or £490/yr) would be aimed at small travel/ops teams and justifiably higher due to multi-seat and extra features. (Annual billing should include ~2 months free to nudge commitment.) These price points align with typical SMB SaaS: small teams often pay £10–£20/user/mo for collaborative tools, and up to ~£50 for premium functionality. Emphasise the annual savings (e.g. “£190 billed yearly vs £228 monthly”). 

**Value-Proof Sales Angle:** Frame ROI in concrete terms. Early EndMile data shows an *average saving of £25.13 per trip* and 71% carbon reduction (see figure below). Even at £19/mo (≈£228/yr), avoiding *one disputed £110 mileage claim* covers six months of subscription. For example, a 200-mile trip (HMRC 55p/mile = £110) often gets challenged when a Trainline fare is only £60. EndMile reveals the hidden £15 parking and £25 taxi cost plus 2 extra hours driving. Preventing that single dispute “buys” half a year’s subscription.  

*Figure: EndMile’s app shows the Ripon→Jesmond example (drive vs rail+taxi). Driving was £31.13 (1h22) vs £28.11 for train (1h58, 61% less CO₂).*  

Leverage these points in copy and triggers. In-app notifications could congratulate the user on a “£25.13 saving this trip” and suggest upgrading to lock in more. When a user saves multiple routes, prompt them: *“Unlock automated scheduling and reporting – try EndMile Pro”*. Founder outreach emails (see Part 2) should lead with this ROI: e.g. “Capturing just one extra 200-mile trip saves the cost of 6 months of EndMile.”  

---

## Part 2: Acquiring More Coordinator Users (Bootstrapped Engine)  

**Lookalike Segments & Company Archetypes:** Target UK mid-market firms (100–300 employees) with frequent regional travel. Beyond IT consultancies, focus on:  
- **Engineering Consultancies:** Civil, structural, mechanical design firms. These dispatch site engineers weekly and track travel budgets.  
- **Environmental/Survey Consultancies:** Field surveyors and ecologists who travel between offices and client sites.  
- **Professional Services:** Mid-tier management consultancies and audit/accountancy firms – e.g. regional BDO/Deloitte offices with “Travel Admin” roles. Travel-heavy groups in legal or architecture practices also fit.  
- **Clinical Trials & Life Sciences:** Pharma/medical research firms whose monitors often visit sites.  
- **Field Service Operations:** Telecom/IT service providers, equipment maintenance companies, utilities (gas, electrical) that send technicians to client sites.  
- **Any Growth Business with Field Staff:** Telecom installers, facilities companies, etc. Typically they’re too small for Concur but big enough to have an office manager or coordinator.  

These sectors often share the “dispatch” use-case – a non-travelling coordinator who must optimise routes and costs.  

**Job Titles & Decision-Makers:** Likely buyers are operational coordinators, not CFOs. Focus on: *Travel Coordinator*, *Logistics Coordinator*, *Office Manager/Administrator*, *Operations Executive/Officer*, *Practice Manager*, *Travel Administrator*, or *Fleet Coordinator*. In small consultancies these roles often handle expense and travel logistics. Our marketing should speak to the person organising trips, not the auditor – for example: “Hello [Operations Manager]” or “Travel Office”. For context, such coordinators **routinely review logistics to cut costs and save time**, so messaging should highlight time-saving and expense accuracy.  

**Zero-Cost Prospect Discovery (No Sales Navigator):** Use targeted Google searches and public data:  
- **Boolean X-Ray on LinkedIn:** For example:  
  ```text
  site:linkedin.com/in ("Travel Coordinator" OR "Logistics Coordinator" OR "Operations Executive" OR "Office Manager" OR "Travel Administrator") AND UK
  ```  
  This finds UK profiles with those titles. Add keywords or companies as needed, e.g. `AND (Engineering OR Consulting OR "Field Service")`. For more niche roles, try:  
  ```text
  site:linkedin.com/in ("Fleet Coordinator" OR "Practice Manager") AND UK
  ```  
  Focus on UK-based profiles and include role synonyms (e.g. “travel arranger”, “consultant travel”). Remove terms like “recruiter” or “jobs” to avoid postings.  
- **Companies House & SIC Codes:** Use the UK Companies House API or web to filter firms by Standard Industrial Classification (SIC). Relevant codes include **71121/71122** (engineering consultancies), **71201/71202** (technical/scientific testing & analysis, including environmental services), **70229** (management consultancy n.e.c.), and **69201/69202** (accountancy/auditing) for audit firms. Searching by these SICs yields lists of mid-sized consultancies and field service outfits where our user likely works.  
- **Directories & Lists:** Look at consultancy directories (e.g. *Clutch.co* lists UK consultants, *Consultancy.uk* publishes firm rankings) and sector associations (TechUK for tech firms, or IAgrE for environmental consultancies). Also check *Yellow Pages* or Google Maps for “consultancy” firms of the right size.  
- **Job Boards & Ads:** Monitor roles on sites like Indeed or Reed for companies **hiring** “travel coordinator” or “office administrator – travel”. The hiring company names from those ads are ideal targets. For example, search:  
  ```text
  site:indeed.co.uk "coordinate consultant travel" OR "manage staff travel"
  ```  
  or simply browse travel-related job postings to extract company names.  

**Sniper Outbound Outreach Playbook:** Craft a concise three-touch cold email sequence, British-tone, emphasising the shared pain. Below are illustrative templates (feel free to adapt to the persona):

1. **Email 1 – Introduction & Trojan Horse Offer:**  
   **Subject:** *Quick question about your travel costs*  
   **Body:**  
   ```text
   Hi [Name],

   I’m [Your Name], founder of EndMile. I noticed many consultancies juggle Google Maps, Trainline and local taxi sites just to compare travel options. The result: wasted time and surprise costs (parking, delays, VAT)… often leading to disputed expenses. 

   Would you be interested in a **free door-to-door cost audit** for one of your common routes? I’ll send a 1-page analysis (no charge) showing if your team is leaving money or time on the table.

   Best regards,
   [Your Name]
   [Position, EndMile]
   ```  
   *Hook:* Acknowledge their likely frustration with travel planning (“juggling…”, “surprise costs”).  
   *Value & Trojan Horse:* Offer a free one-off TCO analysis for a frequent route they make. This “audit” showcases EndMile’s value without commitment.  
   *CTA:* A simple reply: “reply with a trip and I’ll do the audit”. Keep it easy.  

2. **Email 2 – Social Proof/Reminder:**  
   **Subject:** *Did you see the £25+ saving on one route?*  
   **Body:**  
   ```text
   Hi [Name],

   Just following up – last week’s travel audit offer is still open. Our early users (mostly UK consultancies) report **£25 saved per trip on average** and 1–2 extra hours gained by rail vs car. Even on 200-mile trips, figuring the *full* door-to-door cost prevents £100+ mileage disputes.

   If you have 5 minutes, I can send that audit – one route, one page, all no-obligation. 

   Cheers,
   [Your Name]
   ```  
   *Hook:* Cite EndMile’s data-backed impact (“£25 saved per trip, 71% carbon cut”).  
   *Value:* Emphasize saving real money and time, directly hinting “one dispute = big savings”.  
   *CTA:* “Reply or let me know” for the free route audit. Keep tone friendly and peer-level.  

3. **Email 3 – Final Nudge / Closing the Loop:**  
   **Subject:** *Travel costs still eating into your margins?*  
   **Body:**  
   ```text
   Hi [Name],

   Sorry for the persistence – I won’t fill your inbox. I just hate seeing talented teams write off travel costs. By the way, I confirmed with [competitor firm name or previous contact] that just **preventing a single £110 charge write-off** covers 6 months of EndMile.

   No pressure, but if you ever want that route analysis or a quick demo in action, just let me know. 

   All the best,
   [Your Name]
   ```  
   *Hook:* Remind them of the pain (client audits rejecting invoices).  
   *Value:* Use a concrete example: “one £110 disputed claim = 6-month subscription” to underline ROI.  
   *CTA:* Keep it passive (“if you ever want… just let me know”), leaving an open door.  

Each email is ~100 words, peer-to-peer and problem-focused. These sequence steps a friendly offer → data-backed proof → closure, with a “no-strings” audit as a Trojan horse to start dialogue.

**Paid Ads Feasibility:** With a lean budget (£100–£300/mo), broad Google or LinkedIn ads are low ROI here. There’s limited search volume for niche queries like “door-to-door travel cost UK” or “mileage vs train fare calculator UK,” making CPC high and conversion uncertain. LinkedIn Ads could target titles (Operations, Travel Manager) but cost per lead would likely exceed our budget without premium targeting. Instead, focus on ultra-specific keywords if at all: e.g. *“UK consultant travel cost comparison,” “HMRC mileage vs train fare calculator”*. Test only a tiny Google Ads campaign to see clicks on these long-tail terms; if it’s too expensive, pivot entirely to organic: high-intent SEO content (see next section) and direct outreach yield better ROI. In practice, targeted LinkedIn InMail (though premium) or niche forum ads (e.g. industry newsletters) might also work better than generic ads.

**Product-Led Growth & Organic Flywheels:** Leverage viral loops and free tools to spread awareness organically:  
- **Shareable Itineraries:** Allow coordinators to share saved routes via link or PDF. Every shared itinerary (e.g. forwarded to a travelling consultant or client) includes a small “Powered by EndMile” footer. This network effect means when consultants click the shared link, they see EndMile’s calculation firsthand (without needing their own account). Inside organizations, this invites colleagues to sign up. Academic data suggests within-company sharing can boost freemium conversions.  
- **Expense Reports as Marketing:** Encourage coordinators to dispatch the EndMile-generated cost report to finance/AP. If an auditor or client sees a branded PDF justifying mileage vs fare, it doubles as a referral. Make the PDF clear and visually professional so recipients ask, “What’s EndMile?”  
- **Free Calculators/Lead Magnets:** Create a downloadable or web calculator (no login) like “Calculate Travel TCO: Car vs Train” where a user enters an origin/destination and gets a cost/time/CO₂ breakdown. Users who try it (or a free Excel template comparing 55p mileage to train fares) provide email addresses to receive the report, generating leads. Promote this via LinkedIn posts or SEO. Another idea: an infographic comparing HMRC 55p/mile to average train/parking costs on common corridors. These tools demonstrate EndMile’s value and capture contacts.  
- **Content Marketing:** Blog posts targeting questions like “55p vs rail: which is cheaper?”, or case studies (e.g. “How Company X saved £30k in travel last year”) can attract organic traffic. Writing in British English (referencing *HMRC AMAP rates*, *National Rail fares*, *London Congestion Charge*, *VAT* etc.) builds credibility. Every content piece should subtly plug EndMile (“by the way, EndMile does this automatically”).  
- **Community & Referrals:** Ask happy coordinators to introduce EndMile to colleagues at other firms (referral rewards or just goodwill). Engage on LinkedIn groups for UK consultants or transport/planning forums by sharing tips (without heavy sales pitch) to drive curiosity.  

These PLG strategies rely on easing inside-the-team sharing. As one freemium case study found, **“within-organization network effects”** significantly amplify conversion. In short, make it effortless for a coordinator to evangelise EndMile when they see it working.

---

## Part 3: Immediate 30-Day Execution Roadmap  

**Week 1:** Finalise pricing/tiers and implement the paywall. In the app and website, build the tier structure: mark exports, scheduling and branding as “Pro features”. Draft the copy for upgrade prompts (test “Upgrade to export” message). Set pricing pages and checkout flows (£19/£49). Update the home page to mention ROI (e.g. “£25 saved per trip”). Prepare tracking: define metrics (daily active coordinators, saved routes, free→trial sign-ups). Set up analytics for email opens and sign-ups.  

**Week 2:** Create outreach assets. Compile lists via the boolean searches above and Companies House filtering. Draft email sequences (as above) and set up a mail merge (or a CRM) to send them. Post an LinkedIn outreach: e.g. “UK firms: Are you paying drivers 55p/mile or rail fares? EndMile can compare them in seconds” with a link to the audit offer. Launch one or two Google Search Ads targeting “consultant travel planning” and “door to door travel cost” just to test response (monitor cost).  

**Week 3:** Begin outbound campaign. Send Email #1 to 50–100 coordinators. Follow up Email #2 one week later to non-responders, then Email #3. Simultaneously, publish a “Travel Cost Calculator” landing page/blog as a lead magnet. Promote it via social channels and relevant LinkedIn groups. Offer immediate audit results to anyone who signs up. Schedule quick demos or Skype calls if someone shows interest.  

**Week 4:** Analyze results & iterate. Check key metrics:  
- **Traffic/Signups:** Target is ~50 new active users (coordinator accounts) this month.  
- **Engagement:** Are users running >3 searches? Are they saving routes?  
- **Outreach:** Aim for >20% email open rate and 5–10% reply rate on the cold outreach.  
- **Conversion:** With freemium, expect ~2–5% of engaged users to trial/upgrade. Ideally close 1–2 paying customers by month-end, or at least trials in pipeline.  
- **Paid Ads:** Review any leads/clicks from ads; kill them if ROI is poor.  
- Adjust messaging based on feedback (e.g. if many ask “How do I get the audit?”, make CTA clearer).  

By day 30, we should have at least a few free users actively scheduling trips and a pipeline of interested coordinators. Even if no paying customer yet, success is defined by building usage (habits) and capturing leads. For example, winning *5 mid-sized users* saving an average £25/trip would total ~£125/month worth of value – proof of demand. Continue iterating in the next months: refine the paywall prompts, expand outreach to new sectors identified, and solidify at least 1 case study from a pilot customer.

**Metrics & Benchmarks:** Track and review weekly: number of new free accounts, saved routes, email responses, trials, and paid signups. Set targets reflecting typical freemium patterns (e.g. 3% paid conversion). If we reach, say, 100 active free users, ~3 should convert in steady state. If we fall short, double down on outreach or adjust pricing/features. Also monitor qualitative feedback: common objections or feature requests may inform Part 1 decisions.  

---

**Sources & References:** EndMile telemetry and product specs; UK SaaS pricing literature; HMRC AMAP / DEFRA emissions guidelines; UK Companies House SIC directories.
