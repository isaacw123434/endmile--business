#!/usr/bin/env python3
"""
EndMile Staged Outbound Email Dispatcher
-----------------------------------------
Lightweight, human-in-the-loop email dispatcher for pre-reviewed batches.
Dispatches emails via SMTP with pristine multipart formatting (clean plain-text
+ HTML fallback) and optional verified mock screenshot attachments.

Features:
- Decoupled from monolithic Excel pipelines.
- Reads a clean JSON queue prepared and reviewed in Chat with Isaac.
- Enforces strict human-like formatting (zero weird line-breaks or 76-char wrapping bugs).
- Supports dry-run inspection, spaced pacing (10-20 mins) over UK business hours,
  or immediate single-item dispatch.
- Automatically logs sent emails to data/outreach/sent_log.csv and traction/outreach-tracker.md.
- Outputs structured table format ready for easy pasting into Google Sheets.
"""

import os
import sys
import re
import json
import time
import random
import html
import argparse
import smtplib
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SENT_LOG_CSV = REPO_ROOT / "data" / "outreach" / "sent_log.csv"
TRACKER_MD = REPO_ROOT / "traction" / "outreach-tracker.md"

def is_uk_business_hours() -> bool:
    """Check if current time is Monday-Friday between 08:30 and 17:30 UK time."""
    now = datetime.now()
    if now.weekday() >= 5:
        return False
    start_time = now.replace(hour=8, minute=30, second=0, microsecond=0)
    end_time = now.replace(hour=17, minute=30, second=0, microsecond=0)
    return start_time <= now <= end_time

def format_clean_email(
    to_email: str,
    subject: str,
    body_text: str,
    sender_email: str = "isaacw@endmilerouting.co.uk",
    screenshot_path: str = "",
    venue_name: str = "venue",
    inline_image: bool = True
) -> MIMEMultipart:
    """
    Constructs an email message with dual plain text and HTML parts,
    guaranteeing natural human line spacing and embedding images inline
    directly inside the body text (preventing attachment spam penalties).
    """
    msg = MIMEMultipart("related" if inline_image else "mixed")
    msg["Subject"] = subject.strip()
    msg["From"] = f"Isaac Willoughby <{sender_email}>"
    msg["To"] = to_email.strip()
    msg["Reply-To"] = sender_email

    alt_part = MIMEMultipart("alternative")

    # Clean plain text: split paragraphs, trim trailing spaces, join with \n\n
    paragraphs = [p.strip() for p in body_text.strip().split("\n\n") if p.strip()]
    normalized_plain_text = "\n\n".join(paragraphs)

    text_part = MIMEText(normalized_plain_text, "plain", "utf-8")
    alt_part.attach(text_part)

    # Clean HTML: semantic <p> blocks with clean system font styling
    cid_key = "venue_preview_img"
    html_paragraphs = []
    image_inserted = False

    for p in paragraphs:
        # Convert single newlines inside paragraph to <br> if any
        escaped_p = html.escape(p).replace("\n", "<br>")
        html_paragraphs.append(
            f'<p style="margin: 0 0 16px 0; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.5; color: #1e293b;">{escaped_p}</p>'
        )

        # If inline image is requested and this paragraph introduces the placement, insert image right below it
        if inline_image and screenshot_path and os.path.exists(screenshot_path) and not image_inserted:
            if any(k in p.lower() for k in ["example placement", "mocked up", "attached is", "here is an example", "attached an example", "mockup"]):
                html_paragraphs.append(
                    f'<div style="margin: 18px 0; text-align: left;"><img src="cid:{cid_key}" alt="Example Placement - EndMile LiveWidget" style="max-width: 100%; height: auto; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.06); display: block;" /></div>'
                )
                image_inserted = True

    # If image wasn't inserted after a matching keyword, append it before the sign-off
    if inline_image and screenshot_path and os.path.exists(screenshot_path) and not image_inserted:
        # Insert before the last 2 paragraphs (Best, Isaac)
        insert_idx = max(0, len(html_paragraphs) - 2)
        html_paragraphs.insert(
            insert_idx,
            f'<div style="margin: 18px 0; text-align: left;"><img src="cid:{cid_key}" alt="Example Placement - EndMile LiveWidget" style="max-width: 100%; height: auto; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.06); display: block;" /></div>'
        )

    html_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin: 0; padding: 0; background: #ffffff;">
{"".join(html_paragraphs)}
</body>
</html>"""

    html_part = MIMEText(html_content, "html", "utf-8")
    alt_part.attach(html_part)

    msg.attach(alt_part)

    # Attach/Embed screenshot
    if screenshot_path and os.path.exists(screenshot_path):
        try:
            with open(screenshot_path, "rb") as f:
                img_data = f.read()
            clean_slug = re.sub(r'[^a-zA-Z0-9]+', '_', venue_name.lower()).strip('_')[:35]
            filename = f"{clean_slug}_example_placement.png"
            img_part = MIMEImage(img_data, name=filename)
            if inline_image:
                img_part.add_header("Content-ID", f"<{cid_key}>")
                img_part.add_header("Content-Disposition", "inline", filename=filename)
            else:
                img_part.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(img_part)
        except Exception as e:
            print(f"  [EMBED WARNING] Could not embed {screenshot_path}: {e}")

    return msg

def send_via_smtp(
    msg: MIMEMultipart,
    to_email: str,
    sender_email: str = "isaacw@endmilerouting.co.uk"
) -> bool:
    """Dispatches email via configured SMTP server."""
    smtp_host = os.getenv("SMTP_HOST", "smtp.stackmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER", sender_email)
    smtp_pass = os.getenv("SMTP_PASSWORD")

    if not smtp_pass:
        print(f"[ERROR] SMTP password missing in .env. Cannot dispatch to {to_email}.")
        return False

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_user, smtp_pass)
            server.sendmail(sender_email, [to_email], msg.as_string())
        return True
    except Exception as e:
        print(f"[ERROR] SMTP dispatch failed for {to_email}: {e}")
        return False

def append_to_sent_log(record: dict):
    """Appends record to data/outreach/sent_log.csv."""
    SENT_LOG_CSV.parent.mkdir(parents=True, exist_ok=True)
    file_exists = SENT_LOG_CSV.exists()

    headers = ["Date", "Time", "Organization", "ContactName", "Recipient", "Subject", "Template", "ScreenshotAttached", "Status", "Notes"]
    with open(SENT_LOG_CSV, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write(",".join(headers) + "\n")
        row = [
            record.get("date", ""),
            record.get("time", ""),
            f'"{record.get("org", "").replace(chr(34), chr(39))}"',
            f'"{record.get("contact", "").replace(chr(34), chr(39))}"',
            record.get("recipient", ""),
            f'"{record.get("subject", "").replace(chr(34), chr(39))}"',
            record.get("template", ""),
            str(record.get("screenshot_attached", False)),
            record.get("status", "Sent"),
            f'"{record.get("notes", "").replace(chr(34), chr(39))}"'
        ]
        f.write(",".join(row) + "\n")

def append_to_markdown_tracker(records: list[dict]):
    """Appends sent records to traction/outreach-tracker.md."""
    if not TRACKER_MD.exists() or not records:
        return

    content = TRACKER_MD.read_text(encoding="utf-8")
    table_marker = "| Date Sent | Organization | Contact Name & Title | Segment | Channel | Angle / Template | Status | Next Follow-Up | Notes / Response |"

    if table_marker not in content:
        return

    today_str = datetime.now().strftime("%Y-%m-%d")
    new_rows = []
    for r in records:
        org = r.get("org", "Unknown Org")
        contact = r.get("contact", "Front Desk")
        recipient = r.get("recipient", "")
        tpl = r.get("template", "AI_STAGED")
        notes = r.get("notes", "Staged via chat, reviewed by founder")
        row_str = f"| {today_str} | {org} | {contact} | Lead | Email ({recipient}) | {tpl} | Sent | +3 Days | {notes} |"
        new_rows.append(row_str)

    split_pos = content.find(table_marker)
    header_end = content.find("\n", split_pos)
    sep_end = content.find("\n", header_end + 1)

    updated_content = content[:sep_end + 1] + "\n".join(new_rows) + "\n" + content[sep_end + 1:]
    TRACKER_MD.write_text(updated_content, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="EndMile Staged Outbound Email Dispatcher")
    parser.add_argument("--queue", type=str, required=True, help="Path to JSON file containing approved email queue")
    parser.add_argument("--dry-run", action="store_true", help="Preview emails in console without sending")
    parser.add_argument("--ignore-hours", action="store_true", help="Bypass UK business hours check")
    parser.add_argument("--delay-min", type=int, default=10, help="Minimum pause between sends in minutes (default 10)")
    parser.add_argument("--delay-max", type=int, default=20, help="Maximum pause between sends in minutes (default 20)")
    parser.add_argument("--immediate", action="store_true", help="Send all immediately without interval spacing")
    args = parser.parse_args()

    queue_path = Path(args.queue)
    if not queue_path.exists():
        print(f"[ERROR] Queue file not found: {queue_path}")
        sys.exit(1)

    with open(queue_path, "r", encoding="utf-8") as f:
        queue = json.load(f)

    if not isinstance(queue, list) or not queue:
        print("[ERROR] Queue must be a non-empty list of email objects.")
        sys.exit(1)

    print("=" * 70)
    print("   ENDMILE STAGED OUTBOUND EMAIL DISPATCHER")
    print(f" Mode: {'DRY RUN (Preview Only)' if args.dry_run else 'LIVE DISPATCH'}")
    print(f" Total leads in queue: {len(queue)}")
    print(f" Spacing: {'Immediate' if args.immediate else f'{args.delay_min}-{args.delay_max} mins'}")
    print("=" * 70)

    if not args.dry_run and not args.ignore_hours and not is_uk_business_hours():
        print("[GUARD] Outside UK business hours (08:30-17:30 Mon-Fri). Use --ignore-hours or --dry-run.")
        sys.exit(0)

    sent_records = []

    for i, item in enumerate(queue, 1):
        to_email = item.get("to", "").strip()
        subject = item.get("subject", "").strip()
        body = item.get("body", "").strip()
        org_name = item.get("name", item.get("venue", "Lead"))
        contact_name = item.get("contact_name", "")
        tpl_code = item.get("template_code", "CUSTOM")
        shot_path = item.get("screenshot_path", "")
        sender = item.get("sender", "isaacw@endmilerouting.co.uk")
        notes = item.get("notes", "")

        print(f"\n[{i}/{len(queue)}] Preparing: {org_name} -> {to_email}")
        print(f"  Subject:    {subject}")
        print(f"  Template:   {tpl_code}")
        print(f"  Screenshot: {shot_path if shot_path and os.path.exists(shot_path) else 'None'}")

        msg = format_clean_email(
            to_email=to_email,
            subject=subject,
            body_text=body,
            sender_email=sender,
            screenshot_path=shot_path,
            venue_name=org_name
        )

        if args.dry_run:
            print("  [DRY RUN] Email constructed successfully. Preview of plain body:")
            print("  " + "-" * 50)
            for line in body.split("\n"):
                print(f"  | {line}")
            print("  " + "-" * 50)
            continue

        success = send_via_smtp(msg, to_email, sender_email=sender)
        now = datetime.now()
        if success:
            print(f"  [SUCCESS] Dispatched to {to_email}")
            record = {
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M:%S"),
                "org": org_name,
                "contact": contact_name,
                "recipient": to_email,
                "subject": subject,
                "template": tpl_code,
                "screenshot_attached": bool(shot_path and os.path.exists(shot_path)),
                "status": "Sent",
                "notes": notes
            }
            sent_records.append(record)
            append_to_sent_log(record)

            if i < len(queue) and not args.immediate:
                delay_sec = random.randint(args.delay_min * 60, args.delay_max * 60)
                print(f"  [PACING] Pausing {delay_sec // 60}m {delay_sec % 60}s before next send...")
                time.sleep(delay_sec)
        else:
            print(f"  [FAILED] Could not send to {to_email}")

    if not args.dry_run and sent_records:
        append_to_markdown_tracker(sent_records)
        print("\n" + "=" * 70)
        print(f"[COMPLETE] Dispatched {len(sent_records)}/{len(queue)} email(s).")
        print(f"Log appended to: {SENT_LOG_CSV}")
        print("=" * 70)

        # Output a tab-separated table for easy pasting into Google Sheets
        print("\n--- GOOGLE SHEETS COPY-PASTE BLOCK ---")
        print("Date\tTime\tOrganization\tEmail\tTemplate\tStatus\tNotes")
        for r in sent_records:
            print(f"{r['date']}\t{r['time']}\t{r['org']}\t{r['recipient']}\t{r['template']}\t{r['status']}\t{r['notes']}")
        print("--------------------------------------\n")

if __name__ == "__main__":
    main()
