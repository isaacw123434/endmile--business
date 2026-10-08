#!/usr/bin/env python3
"""
EndMile Outreach Reply Tracker & Multi-Product Pipeline Review CLI
------------------------------------------------------------------
Tracks prospect responses, referral forwards, and conversion rates,
updating CSV, Master Excel workbook in Documents/endmile, and traction/outreach-tracker.md.
Also supports live IMAP inbox scanning for isaacw@endmilerouting.co.uk.

Usage:
  # View unified pipeline review and A/B testing scorecard:
  python scripts/outreach/track_outreach_replies.py --report

  # Log a response manually for an App consultancy:
  python scripts/outreach/track_outreach_replies.py --lead-id APP-002 --outcome Referral --notes "Forwarded to Head of Ops" --referral-email ops@audacia.co.uk

  # Log a response manually for a Venue:
  python scripts/outreach/track_outreach_replies.py --venue-id 345886715 --outcome Positive --notes "Wants staging embed test"

  # Check incoming email replies via IMAP:
  python scripts/outreach/track_outreach_replies.py --check-inbox
"""

import os
import sys
import argparse
import imaplib
import email
from email.header import decode_header
from datetime import datetime
from pathlib import Path
import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from dotenv import load_dotenv

load_dotenv()

def get_master_pipeline_path() -> Path:
    candidates = [
        Path(r"C:\Users\isaac\OneDrive\Documents\EndMile\endmile_master_pipeline.xlsx"),
        Path(r"C:\Users\isaac\OneDrive\Desktop\endmile_master_pipeline.xlsx"),
        Path(r"C:\Users\isaac\Documents\endmile\endmile_master_pipeline.xlsx"),
    ]
    for p in candidates:
        if p.exists():
            return p
    return candidates[0]

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CSV_PATH = REPO_ROOT / "data" / "consultancies" / "app_prospects_v1.csv"
EXCEL_PATH = get_master_pipeline_path()
TRACKER_PATH = REPO_ROOT / "traction" / "outreach-tracker.md"

def print_scoreboard():
    print("=" * 75)
    print(" ENDMILE EXECUTIVE COMMERCIAL PIPELINE & EXPERIMENTATION SCOREBOARD")
    print("=" * 75)

    df_app = None
    if CSV_PATH.exists():
        df_app = pd.read_csv(CSV_PATH)
    elif EXCEL_PATH.exists():
        try:
            df_app = pd.read_excel(EXCEL_PATH, sheet_name="App Prospects Pipeline")
        except Exception:
            pass

    df_venue = None
    if EXCEL_PATH.exists():
        try:
            df_venue = pd.read_excel(EXCEL_PATH, sheet_name="Venue Widget Pipeline")
        except Exception:
            pass

    # 1. Product 1: Consultancy App
    if df_app is not None:
        total_leads = len(df_app)
        verified = df_app["EmailStatus"].str.startswith("Verified", na=False).sum() if "EmailStatus" in df_app.columns else 0
        approved = (df_app["ManualApproval"] == "Approved").sum() if "ManualApproval" in df_app.columns else 0
        sent = (df_app["OutreachStatus"] == "Sent").sum() if "OutreachStatus" in df_app.columns else 0
        replies = df_app["OutreachStatus"].str.startswith("Replied", na=False).sum() if "OutreachStatus" in df_app.columns else 0
        reply_rate = (replies / sent * 100) if sent > 0 else 0.0

        print("PRODUCT 1: CONSULTANCY TRAVEL APP ('PAUL HARDY' ICP)")
        print(f"Total Registry Leads Sourced:     {total_leads:,}")
        print(f"Verified Active Zero-Bounce Leads: {verified:,} ({round(verified/total_leads*100, 1)}% of total)")
        print(f"Manually Approved in Excel:       {approved:,}")
        print(f"Total Emails Dispatched (Sent):   {sent:,}")
        print(f"Replies Received:                 {replies:,} (Reply Rate: {round(reply_rate, 1)}%)")
        print("-" * 75)

    # 2. Product 2: Venue Widget
    if df_venue is not None:
        v_total = len(df_venue)
        v_approved = (df_venue["ManualApproval"] == "Approved").sum() if "ManualApproval" in df_venue.columns else 0
        v_sent = (df_venue["OutreachStatus"] == "Sent").sum() if "OutreachStatus" in df_venue.columns else 0
        v_replies = df_venue["OutreachStatus"].str.startswith("Replied", na=False).sum() if "OutreachStatus" in df_venue.columns else 0
        v_reply_rate = (v_replies / v_sent * 100) if v_sent > 0 else 0.0

        print("PRODUCT 2: B2B VENUE TRAVEL WIDGET (THEATRES & CULTURAL VENUES)")
        print(f"Total Unserved Cultural Venues:   {v_total:,}")
        print(f"Manually Approved in Excel:       {v_approved:,}")
        print(f"Total Widget Emails Dispatched:   {v_sent:,}")
        print(f"Replies Received:                 {v_replies:,} (Reply Rate: {round(v_reply_rate, 1)}%)")
        print("-" * 75)

    # 3. A/B Testing Matrix
    print("A/B VARIANT EXPERIMENTATION MATRIX:")
    print(f"{'Product':<15} | {'Template Code':<24} | {'Sent':<5} | {'Replies':<7} | {'Reply %':<8} | {'Forwards'}")
    print("-" * 75)

    variants = [
        ("App", "INFO_REF_A"),
        ("App", "INFO_REF_B"),
        ("App", "INFO_REF_C"),
        ("App", "INFO_REF_D"),
        ("App", "DIRECT_SCRATCHPAD"),
        ("App", "DIRECT_RECHARGE"),
        ("Widget", "VENUE_VISIT_A"),
        ("Widget", "GIG_CURFEW_A"),
        ("Widget", "MUSEUM_PLANNER_A"),
        ("Widget", "HERITAGE_RURAL_B"),
        ("Widget", "ATTRACT_FAMILY_A"),
        ("Widget", "THEATRE_SCOPE3_A"),
        ("Widget", "VENUE_INFO_REFERRAL"),
        ("Widget", "VENUE_FOLLOWUP_PREVIEW")
    ]

    for prod, v in variants:
        df_target = df_app if prod == "App" else df_venue
        if df_target is not None:
            notes_col = "Notes" if "Notes" in df_target.columns else "AssignedTemplate"
            v_sent = df_target[df_target[notes_col].astype(str).str.contains(v, case=False, na=False) & (df_target["OutreachStatus"] == "Sent")].shape[0] if notes_col in df_target.columns else 0
            v_rep = df_target[df_target[notes_col].astype(str).str.contains(v, case=False, na=False) & df_target["OutreachStatus"].astype(str).str.startswith("Replied", na=False)].shape[0] if notes_col in df_target.columns else 0
            v_rate = f"{round(v_rep / v_sent * 100, 1)}%" if v_sent > 0 else "0.0%"
            v_fwd = df_target[df_target[notes_col].astype(str).str.contains(v, case=False, na=False) & (df_target["OutreachStatus"] == "Replied (Referral)")].shape[0] if notes_col in df_target.columns else 0
            print(f"{prod:<15} | {v:<24} | {v_sent:<5} | {v_rep:<7} | {v_rate:<8} | {v_fwd}")

    print("=" * 75)

def log_reply_manually(lead_id: str = "", venue_id: str = "", outcome: str = "", notes: str = "", referral_email: str = ""):
    today_str = datetime.now().strftime("%Y-%m-%d")
    status_str = f"Replied ({outcome})" if outcome in ["Referral", "Positive", "Objection", "Unsubscribe"] else "Replied"

    # App Lead
    if lead_id:
        if not CSV_PATH.exists():
            print(f"Error: {CSV_PATH} not found.")
            return

        df = pd.read_csv(CSV_PATH)
        mask = df["LeadID"] == lead_id
        if not mask.any():
            print(f"Error: LeadID {lead_id} not found in database.")
            return

        existing_notes = str(df.loc[mask, "Notes"].values[0]) if pd.notna(df.loc[mask, "Notes"].values[0]) else ""
        updated_notes = f"{existing_notes} | Reply: {notes}"
        if referral_email:
            updated_notes += f" (Referral: {referral_email})"

        df.loc[mask, "OutreachStatus"] = status_str
        df.loc[mask, "ManualApproval"] = status_str
        df.loc[mask, "Notes"] = updated_notes
        df.to_csv(CSV_PATH, index=False, encoding="utf-8")
        print(f"[OK] Updated {lead_id} in {CSV_PATH.name} -> {status_str}")

        if EXCEL_PATH.exists():
            try:
                wb = openpyxl.load_workbook(EXCEL_PATH)
                if "App Prospects Pipeline" in wb.sheetnames:
                    ws = wb["App Prospects Pipeline"]
                    headers = [cell.value for cell in ws[1]]
                    lid_col = headers.index("LeadID") + 1
                    status_col = headers.index("OutreachStatus") + 1
                    appr_col = headers.index("ManualApproval") + 1
                    notes_col = headers.index("Notes") + 1

                    for row in range(2, ws.max_row + 1):
                        if str(ws.cell(row=row, column=lid_col).value) == lead_id:
                            ws.cell(row=row, column=status_col, value=status_str)
                            ws.cell(row=row, column=appr_col, value=status_str)
                            ws.cell(row=row, column=notes_col, value=updated_notes)
                            break
                    wb.save(EXCEL_PATH)
                    print(f"[OK] Synchronized {EXCEL_PATH.name}")
            except Exception as e:
                print(f"[WARNING] Could not update Excel file: {e}")

    # Venue Lead
    elif venue_id:
        if EXCEL_PATH.exists():
            try:
                wb = openpyxl.load_workbook(EXCEL_PATH)
                if "Venue Widget Pipeline" in wb.sheetnames:
                    ws = wb["Venue Widget Pipeline"]
                    headers = [cell.value for cell in ws[1]]
                    vid_col = headers.index("VenueID") + 1
                    status_col = headers.index("OutreachStatus") + 1
                    appr_col = headers.index("ManualApproval") + 1
                    notes_col = headers.index("FounderNotes") + 1

                    for row in range(2, ws.max_row + 1):
                        if str(ws.cell(row=row, column=vid_col).value) == str(venue_id):
                            ws.cell(row=row, column=status_col, value=status_str)
                            ws.cell(row=row, column=appr_col, value=status_str)
                            ws.cell(row=row, column=notes_col, value=notes)
                            break
                    wb.save(EXCEL_PATH)
                    print(f"[OK] Updated venue {venue_id} in {EXCEL_PATH.name} -> {status_str}")
            except Exception as e:
                print(f"[WARNING] Could not update Excel file for venue: {e}")

    # Update Markdown Tracker
    if TRACKER_PATH.exists():
        content = TRACKER_PATH.read_text(encoding="utf-8")
        target_name = lead_id or venue_id
        marker = "| Date | Contact & Company | Objection / Question Received | Brain Drafted Response | Outcome |"
        if marker in content:
            split_pos = content.find(marker)
            header_end = content.find("\n", split_pos)
            sep_end = content.find("\n", header_end + 1)
            new_row = f"| {today_str} | {target_name} | {notes} | Reviewed | {status_str} |\n"
            updated_content = content[:sep_end + 1] + new_row + content[sep_end + 1:]
            TRACKER_PATH.write_text(updated_content, encoding="utf-8")
            print(f"[OK] Logged in traction/outreach-tracker.md")

def check_inbox_imap():
    imap_host = os.getenv("IMAP_HOST", "imap.stackmail.com")
    imap_port = int(os.getenv("IMAP_PORT", 993))
    imap_user = os.getenv("SMTP_USER", "isaacw@endmilerouting.co.uk")
    imap_pass = os.getenv("SMTP_PASSWORD")

    if not imap_pass:
        print("IMAP password not set in environment (SMTP_PASSWORD). Skipping auto-scan.")
        return

    print(f"Connecting to IMAP {imap_host}:{imap_port} for {imap_user}...")
    try:
        mail = imaplib.IMAP4_SSL(imap_host, imap_port)
        mail.login(imap_user, imap_pass)
        mail.select("INBOX")
        
        status, messages = mail.search(None, "UNSEEN")
        if status != "OK":
            print("No new unread messages.")
            mail.logout()
            return

        msg_ids = messages[0].split()
        print(f"Found {len(msg_ids)} unread email(s). Scanning for prospect replies...")
        
        df_app = pd.read_csv(CSV_PATH) if CSV_PATH.exists() else None
        
        for mid in msg_ids:
            res, msg_data = mail.fetch(mid, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    sender = msg.get("From")
                    subject, encoding = decode_header(msg.get("Subject"))[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8", errors="replace")
                    print(f" - Unread email from: {sender} | Subject: {subject}")
                    
                    if df_app is not None and "@" in str(sender):
                        sender_email = sender.split("<")[-1].replace(">", "").strip().lower()
                        sender_domain = sender_email.split("@")[-1]
                        match = df_app[df_app["OperationalEmail"].str.contains(sender_domain, case=False, na=False)]
                        if not match.empty:
                            matched_lid = match.iloc[0]["LeadID"]
                            co = match.iloc[0]["CompanyName"]
                            print(f"   >>> MATCHED APP PROSPECT: {matched_lid} ({co})!")

        mail.logout()
    except Exception as e:
        print(f"IMAP connection note: {e}")

def main():
    parser = argparse.ArgumentParser(description="EndMile Outreach Reply Tracker & Review")
    parser.add_argument("--report", action="store_true", help="Print multi-product scoreboard")
    parser.add_argument("--lead-id", type=str, help="App LeadID (e.g. APP-002)")
    parser.add_argument("--venue-id", type=str, help="Venue ID (e.g. 345886715)")
    parser.add_argument("--outcome", type=str, choices=["Referral", "Positive", "Objection", "Unsubscribe", "Other"], help="Outcome category")
    parser.add_argument("--notes", type=str, default="", help="Notes or summary of reply")
    parser.add_argument("--referral-email", type=str, default="", help="Referred email address if forwarded")
    parser.add_argument("--check-inbox", action="store_true", help="Scan IMAP inbox for incoming prospect replies")
    args = parser.parse_args()

    if args.check_inbox:
        check_inbox_imap()

    if (args.lead_id or args.venue_id) and args.outcome:
        log_reply_manually(lead_id=args.lead_id, venue_id=args.venue_id, outcome=args.outcome, notes=args.notes, referral_email=args.referral_email)

    if args.report or not ((args.lead_id or args.venue_id) and args.outcome):
        print_scoreboard()

if __name__ == "__main__":
    main()
