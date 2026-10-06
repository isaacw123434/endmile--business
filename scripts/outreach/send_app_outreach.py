#!/usr/bin/env python3
"""
EndMile Automated Outreach Dispatcher for Consultancy Pipeline
---------------------------------------------------------------
Sends targeted, low-friction, peer-to-peer cold emails directly from
data/consultancies/app_prospects_v1.csv and the master Excel workbook:
  C:\\Users\\isaac\\Downloads\\endmile app prospects v1.xlsx

Features:
- Full Project Management: Respects manual approvals ('Approved' status) and template choices from Excel.
- Bi-directional sync: Automatically detects if Excel was modified and syncs edits to CSV.
- Template Override: Supports row-level template choices or CLI flags (--template INFO_REF_A / --variant A).
- Drip throttles sending (5-15 per day) with randomized 10-20 min pauses during UK business hours.
- Dynamic plain-text rendering based on .agents/skills/cold-email/SKILL.md.
- Multi-Tab Preservation: In-place openpyxl updates preserving all tabs and data validation dropdowns.
- Zero manual tracking: updates CSV, Excel (Pipeline & A/B Review tabs), and traction/outreach-tracker.md.

Usage:
  # Preview next 5 approved emails in console without sending:
  python scripts/outreach/send_app_outreach.py --dry-run --limit 5

  # Live send 5 approved emails:
  python scripts/outreach/send_app_outreach.py --limit 5

  # Send specific leads:
  python scripts/outreach/send_app_outreach.py --leads APP-002,APP-003

  # Force a specific template/variant:
  python scripts/outreach/send_app_outreach.py --limit 5 --template INFO_REF_A
"""

import os
import sys
import re
import time
import random
import argparse
import getpass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
import pandas as pd
import openpyxl
from dotenv import load_dotenv

load_dotenv()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CSV_PATH = REPO_ROOT / "data" / "consultancies" / "app_prospects_v1.csv"
EXCEL_PATH = Path(r"C:\Users\isaac\Documents\endmile\endmile_master_pipeline.xlsx")
TRACKER_PATH = REPO_ROOT / "traction" / "outreach-tracker.md"

EXCLUDED_COMPANIES = ["DORSET SOFTWARE SERVICES", "DORSET SOFTWARE"]
EXCLUDED_DOMAINS = ["dorsetsoftware.com"]

def clean_company_name(name: str) -> str:
    """Turn 'DORSET SOFTWARE SERVICES LIMITED' into 'Dorset Software Services'."""
    if not isinstance(name, str):
        return ""
    cleaned = re.sub(r'\b(LIMITED|LTD|LLP|PLC|HOLDINGS|GROUP|UK)\b', '', name, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r'\s+', ' ', cleaned)
    if cleaned.isupper() or cleaned.islower():
        cleaned = cleaned.title()
    return cleaned.strip()

def clean_corridor(corridor: str) -> str:
    """Format corridor cleanly for natural email prose."""
    if not isinstance(corridor, str) or not corridor:
        return "regional client corridors"
    formatted = corridor.replace("➔", " to ").replace("->", " to ")
    formatted = re.sub(r'\([^\)]+\)', '', formatted)
    parts = re.split(r'\s+to\s+', formatted, maxsplit=1)
    if len(parts) >= 2:
        origin = parts[0].strip()
        dests = [d.strip() for d in parts[1].split("/") if d.strip()]
        if len(dests) > 1:
            dest_str = ", ".join(dests[:-1]) + f", or {dests[-1]}"
        elif dests:
            dest_str = dests[0]
        else:
            dest_str = "London"
        formatted = f"{origin} to {dest_str}"
    formatted = re.sub(r'\s+', ' ', formatted).strip()
    return formatted

def is_excluded(row: dict) -> bool:
    """Hard guard against sending to known users or excluded firms."""
    company = str(row.get("CompanyName", "")).upper()
    email = str(row.get("OperationalEmail", "")).lower()
    if any(ec in company for ec in EXCLUDED_COMPANIES):
        return True
    if any(ed in email for ed in EXCLUDED_DOMAINS):
        return True
    return False

def is_uk_business_hours() -> bool:
    """Check if current time is Monday-Friday between 08:30 and 17:30."""
    now = datetime.now()
    if now.weekday() >= 5:
        return False
    start_time = now.replace(hour=8, minute=30, second=0, microsecond=0)
    end_time = now.replace(hour=17, minute=30, second=0, microsecond=0)
    return start_time <= now <= end_time

def is_general_inbox(email: str) -> bool:
    """Detect if email is a front-desk/general triage inbox rather than a specific role."""
    if not isinstance(email, str) or "@" not in email:
        return True
    local = email.split("@")[0].lower()
    prefixes = ("info", "hello", "enquiries", "enquiry", "contact", "admin", "office", "reception", "mail", "helpdesk")
    return local in prefixes or any(local.startswith(p) for p in prefixes)

def build_email_content(
    row: dict,
    template_override: str = "",
    variant_override: str = "auto",
    variant_idx: int = 0,
    founder_name: str = "Isaac",
    sender_email: str = "isaacw@endmilerouting.co.uk"
) -> tuple[str, str, str]:
    """
    Renders punchy plain text cold email based on specified or assigned template.
    Returns (subject, body, template_code).
    """
    company_clean = clean_company_name(row.get("TradeName") or row.get("CompanyName", "your team"))
    hq_city = row.get("HQCity", "your area")
    if pd.isna(hq_city) or str(hq_city).strip().lower() in ["", "nan", "none"]:
        hq_city = "your area"
    corridor = clean_corridor(row.get("SampleTravelCorridor", ""))
    email_addr = str(row.get("OperationalEmail", ""))
    
    raw_contact = row.get("ContactName", "")
    if pd.isna(raw_contact) or str(raw_contact).strip().lower() in ["", "nan", "none"]:
        contact_name = ""
    else:
        contact_name = str(raw_contact).strip()

    is_general = is_general_inbox(email_addr) and not contact_name

    greeting = "Good morning," if datetime.now().hour < 12 else "Good afternoon,"
    if contact_name:
        greeting = f"{greeting[:-1]} {contact_name},"

    # Determine template to use
    assigned_tpl = str(row.get("AssignedTemplate", "")).strip().upper()
    if template_override:
        tpl_choice = template_override.upper()
    elif assigned_tpl and assigned_tpl not in ["", "AUTO", "NAN", "NONE"]:
        tpl_choice = assigned_tpl
    else:
        # Automatic assignment
        if not is_general:
            tpl_choice = "DIRECT_SCRATCHPAD"
        else:
            if variant_override and variant_override.upper() in ["A", "B", "C", "D"]:
                tpl_choice = f"INFO_REF_{variant_override.upper()}"
            else:
                rotation = ["INFO_REF_A", "INFO_REF_B", "INFO_REF_C", "INFO_REF_D"]
                tpl_choice = rotation[(variant_idx - 1) % len(rotation)]

    # 1. DIRECT_SCRATCHPAD
    if tpl_choice == "DIRECT_SCRATCHPAD":
        subject = f"{company_clean}'s travel planning"
        body = f"""{greeting}

When your consultants head out to client sites (like {corridor}), does someone on operations still spend 10 minutes juggling Google Maps, Trainline, and station parking to find the fastest and cheapest door-to-door route?

I built EndMile as a quick scratchpad for UK consultancies. It stacks up driving (at HMRC 55p/mile) against train fares, station parking, and destination taxis side-by-side in 10 seconds.

Happy to send over a 30-second preview of how it works for {hq_city} corridors if helpful?

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "DIRECT_SCRATCHPAD"

    # 2. DIRECT_RECHARGE
    elif tpl_choice == "DIRECT_RECHARGE":
        subject = "Client travel recharges"
        body = f"""{greeting}

When {company_clean}'s consultants travel to client sites, do your finance or project leads ever run into pushback from client accounts payable over HMRC 55p mileage or taxi expenses?

We've found many UK consultancies lose 1–5% of travel recharges simply because clients look up a superficial £50 train ticket and dispute a £110 car journey, ignoring station parking and taxi legs.

We built EndMile to calculate the true door-to-door comparison before consultants travel, generating a 1-page Pre-Trip Cost Justification PDF to attach directly to client invoices.

Would it be helpful to see a sample justification report for {hq_city} routes?

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "DIRECT_RECHARGE"

    # 3. INFO_REF_A (Founder Discovery Ask)
    elif tpl_choice in ["INFO_REF_A", "A"]:
        subject = "Quick question - travel coordination"
        body = f"""{greeting}

Could you point me to whoever looks after consultant travel or expenses at {company_clean}?

I'm an independent UK software engineer building a tool to cut down the time consultancies spend planning client travel and comparing HMRC 55p mileage. Just wanted to ask them 2 quick questions about how they currently handle it.

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "INFO_REF_A"

    # 4. INFO_REF_B (Multi-Tab Time Saver)
    elif tpl_choice in ["INFO_REF_B", "B"]:
        subject = f"{company_clean}'s travel planning"
        body = f"""{greeting}

Quick question — who at {company_clean} coordinates travel when consultants head out to client sites (like {corridor})?

I put together a simple tool for UK consultancies that works out driving mileage against train fares, parking, and taxis in 10 seconds, instead of jumping between 3 tabs.

Worth passing this over to whoever handles travel for your team?

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "INFO_REF_B"

    # 5. INFO_REF_C (55p Mileage Dispute)
    elif tpl_choice in ["INFO_REF_C", "C"]:
        subject = "Consultant travel expenses"
        body = f"""{greeting}

Could you point me to whoever manages travel expenses or project recharges at {company_clean}?

I put together a simple tool for UK consultancies to help back up HMRC 55p mileage against rail costs when clients question travel invoices.

Who would be best to speak with about that?

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "INFO_REF_C"

    # 6. INFO_REF_D (Ultra-Short Gatekeeper Forward)
    elif tpl_choice in ["INFO_REF_D", "D"]:
        subject = "Quick referral - operations / travel"
        body = f"""{greeting}

Could you point me in the right direction? Who at {company_clean} coordinates travel planning or expenses for consultants travelling to client sites?

Thanks so much,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "INFO_REF_D"

    # Fallback to INFO_REF_A
    else:
        subject = "Quick question - travel coordination"
        body = f"""{greeting}

Could you point me to whoever looks after consultant travel or expenses at {company_clean}?

I'm an independent UK software engineer building a tool to cut down the time consultancies spend planning client travel and comparing HMRC 55p mileage. Just wanted to ask them 2 quick questions about how they currently handle it.

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "INFO_REF_A"

def sync_dataframes():
    """Bi-directional sync between CSV and Excel, giving precedence to whichever was modified most recently."""
    if not CSV_PATH.exists():
        print(f"Error: {CSV_PATH} not found.")
        sys.exit(1)

    if not EXCEL_PATH.exists():
        return pd.read_csv(CSV_PATH)

    excel_mtime = EXCEL_PATH.stat().st_mtime
    csv_mtime = CSV_PATH.stat().st_mtime

    if excel_mtime > csv_mtime + 2:
        try:
            print("[SYNC] Detected manual changes in Excel workbook. Synchronizing to CSV...")
            df_excel = pd.read_excel(EXCEL_PATH, sheet_name="App Prospects Pipeline")
            df_excel.to_csv(CSV_PATH, index=False, encoding="utf-8")
            return df_excel
        except Exception as e:
            print(f"[SYNC WARNING] Failed to read Excel directly ({e}); falling back to CSV.")
            return pd.read_csv(CSV_PATH)
    else:
        return pd.read_csv(CSV_PATH)

def update_tracker_markdown(sent_records: list[dict]):
    """Appends sent records to traction/outreach-tracker.md Master Outreach Log."""
    if not TRACKER_PATH.exists() or not sent_records:
        return

    content = TRACKER_PATH.read_text(encoding="utf-8")
    table_marker = "| Date Sent | Organization | Contact Name & Title | Segment | Channel | Angle / Template | Status | Next Follow-Up | Notes / Response |"

    if table_marker not in content:
        return

    today_str = datetime.now().strftime("%Y-%m-%d")
    new_rows = []
    for r in sent_records:
        company = clean_company_name(r.get("TradeName") or r.get("CompanyName", ""))
        role = r.get("TargetRole", "Operations / Practice Lead")
        tpl = r.get("template_code", "App Outreach")
        row_str = f"| {today_str} | {company} | {role} | Consultancy | Email ({r['recipient']}) | {tpl} | Sent | +3 Days | Auto-dispatched via CLI |"
        new_rows.append(row_str)

    split_pos = content.find(table_marker)
    header_end = content.find("\n", split_pos)
    sep_end = content.find("\n", header_end + 1)

    updated_content = content[:sep_end + 1] + "\n".join(new_rows) + "\n" + content[sep_end + 1:]
    TRACKER_PATH.write_text(updated_content, encoding="utf-8")
    print(f"[OK] Appended {len(sent_records)} row(s) to traction/outreach-tracker.md")

def save_pipeline_updates(df: pd.DataFrame, sent_records: list[dict]):
    """Updates CSV and preserves Excel multi-tab workbook with in-place updates."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    sent_dict = {r["LeadID"]: r for r in sent_records}

    for lid, r in sent_dict.items():
        mask = df["LeadID"] == lid
        df.loc[mask, "OutreachStatus"] = "Sent"
        df.loc[mask, "ManualApproval"] = "Sent"
        df.loc[mask, "DateSent"] = today_str
        df.loc[mask, "AssignedTemplate"] = r.get("template_code", "CLI")
        df.loc[mask, "Notes"] = f"Sent: {r.get('template_code', 'CLI')}"

    # 1. Update CSV
    df.to_csv(CSV_PATH, index=False, encoding="utf-8")
    print(f"[OK] Updated {len(sent_records)} lead(s) in {CSV_PATH.name}")

    # 2. In-place update of Excel Workbook
    if EXCEL_PATH.exists():
        try:
            wb = openpyxl.load_workbook(EXCEL_PATH)
            if "App Prospects Pipeline" in wb.sheetnames:
                ws_leads = wb["App Prospects Pipeline"]
                headers = [cell.value for cell in ws_leads[1]]
                lid_col = headers.index("LeadID") + 1
                appr_col = headers.index("ManualApproval") + 1
                tpl_col = headers.index("AssignedTemplate") + 1
                status_col = headers.index("OutreachStatus") + 1
                date_col = headers.index("DateSent") + 1
                notes_col = headers.index("Notes") + 1

                for row_idx in range(2, ws_leads.max_row + 1):
                    lid = ws_leads.cell(row=row_idx, column=lid_col).value
                    if lid in sent_dict:
                        r = sent_dict[lid]
                        ws_leads.cell(row=row_idx, column=appr_col, value="Sent")
                        ws_leads.cell(row=row_idx, column=tpl_col, value=r.get("template_code", "CLI"))
                        ws_leads.cell(row=row_idx, column=status_col, value="Sent")
                        ws_leads.cell(row=row_idx, column=date_col, value=today_str)
                        ws_leads.cell(row=row_idx, column=notes_col, value=f"Sent: {r.get('template_code', 'CLI')}")

            # Update A/B Testing & Dashboard Tab counters
            dash_sheet_name = "A-B Testing & Dashboard" if "A-B Testing & Dashboard" in wb.sheetnames else "A-B Testing & Review"
            if dash_sheet_name in wb.sheetnames:
                ws_review = wb[dash_sheet_name]
                # Find the Sent count in App Funnel
                for r_idx in range(4, 13):
                    if ws_review.cell(row=r_idx, column=1).value == "Total Emails Dispatched (Sent)":
                        current_sent = int(ws_review.cell(row=r_idx, column=2).value or 0)
                        ws_review.cell(row=r_idx, column=2, value=current_sent + len(sent_records))
                        break

                # Increment variant breakdown
                for r_idx in range(24, 34):
                    v_code = str(ws_review.cell(row=r_idx, column=1).value).strip()
                    matching_sent = sum(1 for r in sent_records if r.get("template_code") == v_code)
                    if matching_sent > 0:
                        cur_v_sent = int(ws_review.cell(row=r_idx, column=4).value or 0)
                        ws_review.cell(row=r_idx, column=4, value=cur_v_sent + matching_sent)

            wb.save(EXCEL_PATH)
            print(f"[OK] In-place synchronized multi-tab workbook at {EXCEL_PATH.name}")
        except Exception as e:
            print(f"[WARNING] Could not update Excel workbook: {e}")

def send_via_resend(api_key: str, sender_email: str, recipient: str, subject: str, body: str) -> dict:
    """Sends a plain-text email using Resend API with 2048-bit DKIM signature."""
    import requests
    payload = {
        "from": f"Isaac Willoughby <{sender_email}>",
        "to": [recipient],
        "reply_to": sender_email,
        "subject": subject,
        "text": body
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    r = requests.post("https://api.resend.com/emails", headers=headers, json=payload, timeout=15)
    r.raise_for_status()
    return r.json()

def send_via_smtp(smtp_server, sender_email, recipient, subject, body):
    """Sends a plain-text email using an active SMTP connection with RFC headers."""
    import email.utils
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Isaac Willoughby <{sender_email}>"
    msg["To"] = recipient
    msg["Reply-To"] = sender_email
    msg["Date"] = email.utils.formatdate(localtime=True)
    msg["Message-ID"] = email.utils.make_msgid(domain="endmilerouting.co.uk")

    part = MIMEText(body, "plain", "utf-8")
    msg.attach(part)

    smtp_server.sendmail(sender_email, recipient, msg.as_string())
    return msg

def main():
    parser = argparse.ArgumentParser(description="EndMile Automated Outreach Dispatcher")
    parser.add_argument("--dry-run", action="store_true", help="Preview emails in console without sending")
    parser.add_argument("--limit", type=int, default=5, help="Number of emails to send (default: 5, max recommended: 20)")
    parser.add_argument("--tier", type=str, default="Exceptional Fit", help="LeadFitTier filter (default: 'Exceptional Fit')")
    parser.add_argument("--template", type=str, default="", help="Override template code (e.g. INFO_REF_A, INFO_REF_B, DIRECT_SCRATCHPAD)")
    parser.add_argument("--variant", type=str, default="auto", choices=["auto", "A", "B", "C", "D"], help="Referral variation for info@ desks")
    parser.add_argument("--leads", type=str, default="", help="Comma-separated LeadIDs to send (e.g. APP-002,APP-003)")
    parser.add_argument("--all", action="store_true", help="Ignore manual approval filter and send any uncontacted verified leads")
    parser.add_argument("--delay-min", type=int, default=600, help="Minimum pause between sends in seconds (default: 600s = 10 mins)")
    parser.add_argument("--delay-max", type=int, default=1200, help="Maximum pause between sends in seconds (default: 1200s = 20 mins)")
    parser.add_argument("--ignore-business-hours", action="store_true", help="Send outside 08:30-17:30 UK Mon-Fri")
    parser.add_argument("--test-to", type=str, default="", help="Send a single test email to specified address without modifying pipeline state")
    parser.add_argument("--from-email", type=str, default=os.getenv("SMTP_USER", "isaacw@endmilerouting.co.uk"))
    args = parser.parse_args()

    print("=" * 70)
    print(" ENDMILE AUTOMATED OUTREACH DISPATCHER & PROJECT MANAGER")
    print(f" Mode: {'DRY RUN (Console Preview Only)' if args.dry_run else 'LIVE SEND'}")
    print(f" Approval Filter: {'ALL Uncontacted' if args.all else 'Approved by Isaac in Excel only'}")
    print(f" Batch Limit: {args.limit} | Template Override: {args.template or 'Row-Level / Auto'}")
    print(f" Human Pacing: {round(args.delay_min/60, 1)}–{round(args.delay_max/60, 1)} mins between sends")
    print("=" * 70)

    if not args.dry_run and not args.ignore_business_hours:
        if not is_uk_business_hours():
            now_str = datetime.now().strftime("%A %H:%M")
            print(f"[PAUSED] Current time is {now_str} (outside UK business hours: 08:30–17:30 Mon–Fri).")
            print("Sending during active UK office hours maximizes open and forward rates.")
            print("To send right now anyway, add the flag: --ignore-business-hours")
            return

    df = sync_dataframes()

    # Lead filtering
    is_verified = df["EmailStatus"].str.startswith("Verified", na=False)
    uncontacted = df[(df["OutreachStatus"] == "Uncontacted") & is_verified].copy()
    uncontacted = uncontacted[~uncontacted.apply(is_excluded, axis=1)]

    # Check for specific lead IDs
    if args.leads:
        target_ids = [lid.strip() for lid in args.leads.split(",") if lid.strip()]
        batch = uncontacted[uncontacted["LeadID"].isin(target_ids)].copy()
        if batch.empty:
            print(f"None of the specified leads {target_ids} were found uncontacted in verified pipeline.")
            return
    elif not args.all:
        # Default: Project Management Mode — only send leads Isaac approved in Excel
        batch = uncontacted[uncontacted["ManualApproval"] == "Approved"].copy()
        if batch.empty:
            print("[INFO] No leads currently marked 'Approved' in Excel.")
            print(f"Open '{EXCEL_PATH}', set ManualApproval to 'Approved' for your chosen leads, and re-run.")
            print("To send automatically without waiting for manual approval, pass: --all")
            return
        batch = batch.head(args.limit)
    else:
        # Send top uncontacted in tier
        tier_leads = uncontacted[uncontacted["LeadFitTier"] == args.tier]
        if tier_leads.empty:
            tier_leads = uncontacted
        batch = tier_leads.head(args.limit)

    print(f"Selected {len(batch)} lead(s) for dispatch.\n")

    if args.dry_run:
        print("-" * 70)
        print("PREVIEWING GENERATED EMAILS:")
        print("-" * 70)
        for idx, (_, row) in enumerate(batch.iterrows(), 1):
            subject, body, template_code = build_email_content(
                row.to_dict(),
                template_override=args.template,
                variant_override=args.variant,
                variant_idx=idx,
                sender_email=args.from_email
            )
            recipient = row.get("OperationalEmail", "info@example.co.uk")
            approval = row.get("ManualApproval", "Approved")
            print(f"[{idx}/{len(batch)}] TO: {recipient} ({row.get('CompanyName')})")
            print(f"LEAD ID: {row.get('LeadID')} | APPROVAL STATUS: {approval}")
            print(f"TEMPLATE USED: {template_code}")
            print(f"SUBJECT: {subject}")
            print("BODY:")
            print(body)
            print("-" * 70)
        print("\nDry run complete. No emails were sent. Run without --dry-run when ready to send live.")
        return

    # Live sending setup: Prefer Resend API (DKIM verified), fallback to SMTP
    resend_api_key = os.getenv("RESEND_API_KEY")
    sender_email = args.from_email
    server = None

    if resend_api_key:
        print("[OK] Using Resend API (2048-bit DKIM signed via endmilerouting.co.uk).\n")
    else:
        smtp_host = os.getenv("SMTP_HOST", "smtp.stackmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        smtp_pass = os.getenv("SMTP_PASSWORD")
        if not smtp_pass:
            print(f"SMTP Configuration for {sender_email} via {smtp_host}:{smtp_port}")
            smtp_pass = getpass.getpass(f"Enter password for {sender_email} (or set SMTP_PASSWORD env var): ")
            if not smtp_pass:
                print("Password required for live sending. Aborting.")
                sys.exit(1)

        print(f"Connecting to SMTP server {smtp_host}:{smtp_port}...")
        try:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=15)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, smtp_pass)
            print("[OK] SMTP authentication successful.\n")
        except Exception as e:
            print(f"[ERROR] Failed to connect/authenticate with SMTP server: {e}")
            sys.exit(1)

    def dispatch_email(recipient: str, subject: str, body: str):
        if resend_api_key:
            return send_via_resend(resend_api_key, sender_email, recipient, subject, body)
        else:
            return send_via_smtp(server, sender_email, recipient, subject, body)

    if args.test_to:
        test_row = batch.iloc[0].to_dict() if not batch.empty else {
            "LeadID": "TEST-001",
            "CompanyName": "Chorus IT Limited",
            "TradeName": "Chorus IT",
            "OperationalEmail": "hello@chorus.co.uk",
            "SampleTravelCorridor": "Bristol / Portishead (BS20) -> Birmingham / London",
            "HQCity": "Bristol",
            "AssignedTemplate": "INFO_REF_A"
        }
        subject, body, template_code = build_email_content(
            test_row,
            template_override=args.template,
            sender_email=sender_email
        )
        print("=" * 70)
        print(f"DISPATCHING TEST EMAIL TO: {args.test_to}")
        print(f"SAMPLE COMPANY: {test_row.get('TradeName') or test_row.get('CompanyName')}")
        print(f"TEMPLATE: {template_code}")
        print(f"SUBJECT: {subject}")
        print("-" * 70)
        print(body)
        print("=" * 70)
        try:
            dispatch_email(args.test_to, subject, body)
            print(f"\n[OK] Test email successfully sent to {args.test_to}!")
            print("No pipeline rows or counters were modified. Review your inbox/spam folder.")
        except Exception as e:
            print(f"\n[ERROR] Failed to send test email: {e}")
        finally:
            if server:
                try:
                    server.quit()
                except Exception:
                    pass
        return

    sent_records = []

    try:
        for idx, (_, row) in enumerate(batch.iterrows(), 1):
            lead_id = row["LeadID"]
            recipient = row.get("OperationalEmail")
            if not recipient or "@" not in str(recipient):
                print(f"[{idx}/{len(batch)}] Skipping {lead_id} - Invalid recipient email: {recipient}")
                continue

            subject, body, template_code = build_email_content(
                row.to_dict(),
                template_override=args.template,
                variant_override=args.variant,
                variant_idx=idx,
                sender_email=sender_email
            )
            print(f"[{idx}/{len(batch)}] Sending [{template_code}] to {recipient} ({clean_company_name(row.get('CompanyName'))})...", end="", flush=True)

            try:
                dispatch_email(recipient, subject, body)
                print(" [SENT]")
                sent_records.append({
                    "LeadID": lead_id,
                    "CompanyName": row.get("CompanyName"),
                    "TradeName": row.get("TradeName"),
                    "TargetRole": row.get("TargetRole"),
                    "recipient": recipient,
                    "template_code": template_code
                })
            except Exception as send_err:
                print(f" [FAILED: {send_err}]")

            # Pause between sends
            if idx < len(batch):
                delay = random.randint(args.delay_min, args.delay_max)
                minutes = round(delay / 60, 1)
                print(f"     Human pacing pause: waiting {minutes} mins ({delay}s) before next dispatch...")
                time.sleep(delay)

    finally:
        try:
            server.quit()
        except Exception:
            pass

    # Save updates
    if sent_records:
        print("\nUpdating tracking databases and Excel sheets...")
        save_pipeline_updates(df, sent_records)
        update_tracker_markdown(sent_records)
        print(f"\n[SUCCESS] Successfully sent {len(sent_records)} email(s) and logged in all trackers.")
    else:
        print("\nNo emails were successfully sent.")

if __name__ == "__main__":
    main()
