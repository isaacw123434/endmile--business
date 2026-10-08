# Outbound Outreach & Sales Tracker

*Maintained by the Founder & EndMile Business Brain.*

---

## 1. High-Level Outbound Metrics

| Metric | Current Value | Target (Monthly) | Notes |
|---|---|---|---|
| **Total Contacts Sourced** | **2,763 Consultancies** / **4,992 Venues** | 250 / mo | 100% verified UK MX records (0.0% hard bounce rate) |
| **Manually Approved for Outbound** | **20 Consultancies / 59 Venues** | 5–20 / day | Reviewed by Isaac in Excel tabs `App Prospects Pipeline` & `Venue Widget Pipeline` |
| **Total Emails Dispatched** | 0 | 250 / mo | Human-spaced (10–20 mins apart) during UK business hours |
| **Direct & Referral Replies Received** | 0 | 25 (10% reply rate) | Tracked via CLI `npm run outreach:report` |
| **Positive Discovery / Walkthroughs** | 0 | 8 / mo (30% of replies) | 10-second multimodal pre-trip demo |
| **Active Pilots / Free Trials** | 0 | 4 / mo | 14-day Pro workspace sandbox |
| **Closed Paying Customers** | 0 | 2–4 / mo | Target: First 10 paying customers (£290–£490 MRR) |

---

## 2. Operating Model: AI-Assisted Google Sheets & Chat Staging

> [!TIP]
> **Workflow Evolution (2026-10-08):**
> Monolithic automated Python dispatch scripts have been archived because they were too rigid and did not allow human visual inspection of email drafts and mock widget screenshots.
> The active operating model is **Human-in-the-Loop AI Collaboration**:
> 1. **Lead Sourcing & Curation**: Founder manages and edits master leads in **Google Sheets online**, using Google Gemini in Google Sheets for quick web lookups, categorization, and filtering.
> 2. **Batch Drop in Chat**: Founder pastes ~5 target leads into the Antigravity chat window with URLs, emails, and desired template codes (or asks for recommendations).
> 3. **AI Staging & Screenshot Generation**: Antigravity generates pixel-perfect mock screenshots using standalone Playwright (`generate_venue_mock_screenshot.py`), drafts the exact email text with formatting verified (clean paragraph breaks, no 76-character wrapping glitches, zero links), and presents a full preview in chat.
> 4. **Founder Review Gate**: Founder reviews each draft and screenshot, approves, tweaks, or skips.
> 5. **Paced Scheduling**: Antigravity dispatches approved emails spaced 10–20 minutes apart during UK business hours using `scripts/outreach/send_staged_emails.py`.
> 6. **Feedback Loop**: Sent details are logged to `data/outreach/sent_log.csv` and `traction/outreach-tracker.md`, providing a clean copy-paste block for the founder to sync back into Google Sheets.

### Batch 2 (Consultancies — "Paul Profile"): ACTIVE PRIORITY
- **Master Sheet**: Online Google Sheet (Consultancy Prospects).
- **Verified Pipeline**: **1,351 active verified leads** with live DNS MX servers.
- **Outreach Angles**: `INFO_REF_A` (Founder Discovery Ask), `INFO_REF_B` (Multi-Tab Time Saver), `DIRECT_SCRATCHPAD` (Pre-Trip Comparison), `DIRECT_RECHARGE` (Pre-Trip PDF & AP Recharges).

### Batch 1 (B2B Venue Widget — Cultural Venues): ACTIVE PRIORITY
- **Master Sheet**: Online Google Sheet (Venue Widget Pipeline — 4,992 unserved UK cultural venues).
- **Outreach Angles**: `VENUE_VISIT_A` (Interactive Visit Planner), `GIG_CURFEW_A` (Late-Night Curfew), `MUSEUM_PLANNER_A` (City Transit vs Car), `THEATRE_SCOPE3_A` (Julie's Bicycle Scope 3 Carbon), `VENUE_INFO_REFERRAL` (Disarming Reception Ask).


---

## 3. Master Outreach Log

*Automatically updated whenever `npm run outreach:send` or `npm run outreach:widget:send` dispatches emails, or manually via chat.*

| Date Sent | Organization | Contact Name & Title | Segment | Channel | Angle / Template | Status | Next Follow-Up | Notes / Response |
|---|---|---|---|---|---|---|---|---|
| 2026-10-08 | Oxford Playhouse | Emma | Lead | Email (emma.jones@26pmx.com) | VENUE_VISIT_A (Example Placement Mock) | Sent | +3 Days | Partner work email test - inbox/spam verification with inline CID image |
| *YYYY-MM-DD* | *Sample Practice* | *Operations Lead* | *Consultancy* | *Email* | *DIRECT_SCRATCHPAD* | *Sent* | *+3 Days* | *Initial outreach sent* |

---

## 4. Response & Objection Quick-Log

*Logged automatically via `python scripts/outreach/track_outreach_replies.py` or manually.*

| Date | Contact & Company | Objection / Question Received | Brain Drafted Response | Outcome |
|---|---|---|---|---|
| | | | | |

---

## 5. Daily Project Management CLI Commands

```bash
# 0. Open the Master Multi-Product Pipeline in Microsoft Excel:
npm run pipeline:open

# 1. Preview next 5 approved App emails in console (Zero risk dry-run):
npm run outreach:app:preview

# 2. Live send 5 approved App emails (10-20 min intervals, Mon-Fri 08:30-17:30 UK):
npm run outreach:app:send

# 3. Preview next 5 approved Venue Widget emails in console:
npm run outreach:widget:preview

# 4. Live send 5 approved Venue Widget emails:
npm run outreach:widget:send

# 5. View unified multi-product scoreboard & A/B testing matrix:
npm run outreach:report

# 6. Check incoming IMAP inbox for replies from prospects:
npm run outreach:check-inbox

# 7. Log an incoming reply manually:
python scripts/outreach/track_outreach_replies.py --lead-id APP-002 --outcome Referral --notes "Forwarded to Head of Ops" --referral-email ops@audacia.co.uk
```
