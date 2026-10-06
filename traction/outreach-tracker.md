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

## 2. Active Outbound Campaign Batches & Workflow

### Batch 2 (Consultancies — "Paul Profile"): ACTIVE PRIORITY
- **Master Workbook:** `C:\Users\isaac\Documents\endmile\endmile_master_pipeline.xlsx` (Sheet 1: `App Prospects Pipeline`).
- **Verified Pipeline:** **1,351 active verified leads** with live DNS MX servers (384 Microsoft 365, 216 Google Workspace, 701 Hosting MX, 50 Enterprise Gateways).
- **Founder Manual Project Management Gate:**
  - Isaac reviews leads in Excel tab `App Prospects Pipeline`.
  - Column B: `ManualApproval` (`Approved`, `Pending Review`, `Hold`, `Skip`, `Sent`).
  - Column C: `AssignedTemplate` (`AUTO`, `DIRECT_SCRATCHPAD`, `INFO_REF_A`, `INFO_REF_B`, `INFO_REF_C`, `INFO_REF_D`, `DIRECT_RECHARGE`).
  - Column D: `FounderNotes`.
  - `send_app_outreach.py` by default strictly dispatches **only leads marked `Approved`**.
- **A/B Testing Framework:**
  - `INFO_REF_A`: Founder Discovery Ask (38 words, authentic software engineer persona).
  - `INFO_REF_B`: Multi-Tab Time Saver (50 words, operational time-saving angle).
  - `INFO_REF_C`: 55p Mileage Dispute (45 words, client expense pushback angle).
  - `INFO_REF_D`: Gatekeeper Ultra-Short (28 words, frictionless forwarding request).
  - `DIRECT_SCRATCHPAD`: 10-Minute Travel Juggling (85 words, direct to ops / named staff).
  - `DIRECT_RECHARGE`: Pre-Trip PDF & Recharges (95 words, direct to finance / commercial).

### Batch 1 (B2B Venue Widget — Cultural Venues): CONFIRMED PIPELINE
- **Master Workbook:** `C:\Users\isaac\Documents\endmile\endmile_master_pipeline.xlsx` (Sheet 2: `Venue Widget Pipeline`).
- **Status:** **4,992 unserved UK cultural venues**. 59 founder-confirmed direct contacts pre-approved in Sheet 2.
- **Outreach Status:** Modular CLI `send_venue_outreach.py` ready for founder-approved dispatch.

---

## 3. Master Outreach Log

*Automatically updated whenever `npm run outreach:send` or `npm run outreach:widget:send` dispatches emails, or manually via chat.*

| Date Sent | Organization | Contact Name & Title | Segment | Channel | Angle / Template | Status | Next Follow-Up | Notes / Response |
|---|---|---|---|---|---|---|---|---|
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
