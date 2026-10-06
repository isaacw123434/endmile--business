#!/usr/bin/env python3
"""
EndMile Automated Outreach Dispatcher for Venue Travel Widget Pipeline
------------------------------------------------------------------------
Sends targeted, low-friction, peer-to-peer cold emails to UK cultural and visitor venues
directly from C:\\Users\\isaac\\Documents\\endmile\\endmile_master_pipeline.xlsx
(Sheet: 'Venue Widget Pipeline').

Features:
- Reads from the Master Multi-Product Pipeline in Documents\\endmile.
- Full Project Management: Respects 'ManualApproval' (defaults to 'Approved' only).
- Dispatches to founder-confirmed contacts (General Managers, Visitor Services, Box Office).
- Live interactive staging preview links generated per venue.
- Updates status in Excel workbook and traction/outreach-tracker.md.

Usage:
  # Preview next 5 approved venue emails in console without sending:
  python scripts/outreach/send_venue_outreach.py --dry-run --limit 5

  # Live send 5 approved venue emails:
  python scripts/outreach/send_venue_outreach.py --limit 5

  # Send specific venue IDs:
  python scripts/outreach/send_venue_outreach.py --venues 345886715,2789848831

  # Force a specific template:
  python scripts/outreach/send_venue_outreach.py --limit 5 --template VENUE_DWELL_TIME
"""

import os
import sys
import re
import time
import random
import argparse
import getpass
import smtplib
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
from pathlib import Path
import pandas as pd
import openpyxl
from dotenv import load_dotenv

try:
    from scripts.outreach.generate_venue_mock_screenshot import capture_venue_mock_screenshot
except ImportError:
    try:
        from generate_venue_mock_screenshot import capture_venue_mock_screenshot
    except ImportError:
        capture_venue_mock_screenshot = None

load_dotenv()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EXCEL_PATH = Path(r"C:\Users\isaac\Documents\endmile\endmile_master_pipeline.xlsx")
FALLBACK_EXCEL = Path(r"C:\Users\isaac\Downloads\endmile widget v4.xlsx")
TRACKER_PATH = REPO_ROOT / "traction" / "outreach-tracker.md"
SCREENSHOTS_DIR = REPO_ROOT / "screenshots" / "venues"

EXCLUDED_CHAINS = [
    "NATIONAL TRUST", "MERLIN", "AMBASSADOR THEATRE GROUP", "ATG TICKETS",
    "LIVE NATION", "ACADEMY MUSIC GROUP", "ROYAL COLLECTION TRUST"
]

def clean_venue_name(name: str) -> str:
    """Clean and standardize venue name for natural email copy."""
    if not isinstance(name, str):
        return "your venue"
    cleaned = re.sub(r'\b(LIMITED|LTD|LLP|PLC|CIC|TRUST)\b', '', name, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def is_general_inbox(email: str) -> bool:
    """Check if email is a front-desk / triage inbox."""
    if not isinstance(email, str) or "@" not in email:
        return True
    local = email.split("@")[0].lower()
    prefixes = ("info", "hello", "enquiries", "enquiry", "contact", "boxoffice", "box-office", "reception", "admin", "office", "mail")
    return local in prefixes or any(local.startswith(p) for p in prefixes)

def generate_preview_url(domain: str, venue_name: str) -> str:
    """Generates the interactive staging preview URL on endmilerouting.co.uk."""
    clean_dom = str(domain).replace("https://", "").replace("http://", "").strip("/ ")
    encoded_venue = urllib.parse.quote_plus(venue_name)
    return f"https://endmilerouting.co.uk/venue-widget/?url={clean_dom}&venue={encoded_venue}"

def build_venue_email(
    row: dict,
    template_override: str = "",
    variant_override: str = "auto",
    screenshot_attached: bool = False,
    founder_name: str = "Isaac",
    sender_email: str = "isaacw@endmilerouting.co.uk"
) -> tuple[str, str, str, str]:
    """
    Renders punchy plain text cold email based on specified or assigned template.
    Returns (subject, body, template_code, preview_url).
    """
    venue_name = clean_venue_name(row.get("VenueName") or row.get("Name") or "your venue")
    domain = str(row.get("Website") or row.get("Domain") or "").strip()
    raw_name = row.get("ConfirmedName") or row.get("_extracted_name") or ""
    if pd.isna(raw_name) or str(raw_name).strip().lower() in ["nan", "none", ""]:
        first_name = ""
    else:
        first_name = str(raw_name).strip()

    contact_email = str(row.get("ConfirmedEmail") or row.get("_extracted_email") or row.get("PublicEmail") or row.get("RawEmail") or "").strip().lower()
    if contact_email in ["nan", "none"]:
        contact_email = ""

    raw_role = row.get("ConfirmedRole") or row.get("_extracted_role") or ""
    if pd.isna(raw_role) or str(raw_role).strip().lower() in ["nan", "none", ""]:
        role = "Visitor Services / Operations"
    else:
        role = str(raw_role).strip()

    preview_url = generate_preview_url(domain, venue_name)
    is_general = is_general_inbox(contact_email) and not first_name

    assigned_tpl = str(row.get("AssignedTemplate", "")).strip().upper()
    archetype = str(row.get("Archetype", "")).lower()
    venue_lower = venue_name.lower()

    if template_override:
        tpl_choice = template_override.upper()
    elif assigned_tpl and assigned_tpl not in ["", "AUTO", "NAN", "NONE"]:
        tpl_choice = assigned_tpl
    elif is_general:
        tpl_choice = "VENUE_INFO_REFERRAL"
    else:
        # Smart auto-selection based on archetype and variant (A or B)
        v_upper = variant_override.upper()
        if v_upper == "B":
            use_b = True
        elif v_upper == "A":
            use_b = False
        else:
            # Deterministic 50/50 split on VenueID hash
            vid_val = str(row.get("VenueID") or row.get("ID") or venue_name)
            use_b = (hash(vid_val) % 2 == 1)

        if "theatre" in archetype or "theatre" in venue_lower or "playhouse" in venue_lower:
            if any(k in venue_lower for k in ["opera", "ballet", "npo", "trust"]):
                tpl_choice = "THEATRE_GREENBOOK_B" if use_b else "THEATRE_SCOPE3_A"
            elif any(k in venue_lower for k in ["music", "gig", "hall", "academy", "o2"]):
                tpl_choice = "GIG_DISPERSAL_B" if use_b else "GIG_EGRESS_A"
            else:
                tpl_choice = "THEATRE_ACCESS_B" if use_b else "THEATRE_JOURNEY_A"
        elif "museum" in archetype or "gallery" in archetype or "museum" in venue_lower or "gallery" in venue_lower:
            if any(k in venue_lower for k in ["castle", "hall", "manor", "house", "gardens", "park", "estate"]):
                tpl_choice = "HERITAGE_LANES_B" if use_b else "HERITAGE_CATCHMENT_A"
            else:
                tpl_choice = "MUSEUM_ACCESS_B" if use_b else "MUSEUM_CAZ_A"
        elif "attraction" in archetype or "zoo" in archetype or "wildlife" in archetype or "zoo" in venue_lower or "safari" in venue_lower:
            if any(k in venue_lower for k in ["railway", "steam", "outdoor", "farm", "adventure"]):
                tpl_choice = "ATTRACT_GREEN_B" if use_b else "ATTRACT_HIGHWAY_A"
            else:
                tpl_choice = "ATTRACT_COST_B" if use_b else "ATTRACT_INGRESS_A"
        elif "university" in archetype or "campus" in archetype or "college" in venue_lower:
            tpl_choice = "UNI_CAMPUS_B" if use_b else "UNI_OPENDAY_A"
        else:
            tpl_choice = "THEATRE_ACCESS_B" if use_b else "THEATRE_JOURNEY_A"

    time_greeting = "Good morning," if datetime.now().hour < 12 else "Good afternoon,"
    salutation = f"{time_greeting[:-1]} {first_name}," if first_name else time_greeting

    # 1. THEATRES & PERFORMING ARTS
    if tpl_choice in ["THEATRE_VISIT_A", "THEATRE_JOURNEY_A"]:
        subject = f"Visitor directions for {venue_name}"
        cta = (
            f"I went ahead and mocked up how this looks on your actual visit page (see attached screenshot).\n\nWould you be open to trying a live preview?"
            if screenshot_attached else
            f"Worth seeing a 30-second staging preview configured for {venue_name}?"
        )
        body = f"""{salutation}

Looking at {venue_name}'s "Getting Here" page, visitors planning their trip currently have to read through static text and jump between map apps and train timetables to figure out their route.

We built EndMile as a lightweight, 1-line trip planner for UK venues. Ticket holders simply type their postcode and instantly get door-to-door transit times, station walks, and car parks directly on your page.

{cta}

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "THEATRE_VISIT_A", preview_url

    elif tpl_choice == "THEATRE_ACCESS_B":
        subject = f"Accessible travel to {venue_name}"
        cta = (
            f"I attached a quick mockup showing how this looks on your actual visit page. Would this be useful for {venue_name}?"
            if screenshot_attached else
            f"Would a 30-second preview for {venue_name} be helpful?"
        )
        body = f"""{salutation}

When patrons with access requirements plan a visit to {venue_name}, how easy is it for them to find step-free public transport and accessible parking guidance on your website?

Over 10% of cultural attendees require step-free transit, and uncertainty around station walking links or Blue Badge bays often creates booking hesitation.

We built EndMile to provide verified step-free rail routes, accessible station walking paths, and Blue Badge parking directly on your visit page in one line of code.

{cta}

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "THEATRE_ACCESS_B", preview_url

    elif tpl_choice in ["GIG_CURFEW_A", "GIG_EGRESS_A", "GIG_DISPERSAL_B"]:
        subject = f"Getting home from {venue_name}"
        cta = (
            f"I attached a mockup showing how it looks on your site. Happy to share a live preview if helpful?"
            if screenshot_attached else
            f"Happy to share a 30-second preview for {venue_name} if helpful?"
        )
        body = f"""{salutation}

For evening gigs finishing after 10:30 PM at {venue_name}, do attendees travelling in from surrounding towns often struggle to check return train and bus times in advance?

We built EndMile as a simple, 1-line trip planner for UK live venues. It lets ticket buyers check their exact route home—including last rail departures and station walking times—right on your event pages.

{cta}

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "GIG_CURFEW_A", preview_url

    elif tpl_choice in ["THEATRE_SCOPE3_A", "VENUE_SCOPE3_GREENBOOK"]:
        subject = "Audience travel reporting"
        cta = (
            f"I attached a mockup showing how the planner embeds on your visit page. Would you be open to seeing a sample carbon export for {venue_name}?"
            if screenshot_attached else
            f"Would you be open to seeing a sample carbon export for {venue_name}?"
        )
        body = f"""{salutation}

For {venue_name}'s annual Julie's Bicycle environmental reporting, how does your team currently measure audience travel carbon?

Audience travel typically represents over 80% of a cultural venue's footprint, yet most venues have to rely on post-show email surveys with 3–4% response rates and rough estimations.

We built EndMile to automate this. It embeds as a 1-line journey planner on your visit page, generating verified DEFRA Scope 3 carbon telemetry directly from real visitor journey queries.

{cta}

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "THEATRE_SCOPE3_A", preview_url

    elif tpl_choice == "THEATRE_GREENBOOK_B":
        subject = f"Theatre Green Book travel tracking"
        cta = (
            f"I attached a mockup showing how the low-carbon planner looks on your visit page. Happy to explore if helpful?"
            if screenshot_attached else
            f"Happy to send over a 30-second preview for {venue_name} if helpful?"
        )
        body = f"""{salutation}

As {venue_name} works toward Theatre Green Book standards, how are you demonstrating active audience travel decarbonisation?

Under the Green Book Operations volume, showing a measurable shift from private car use toward rail and public transit is essential, but hard to prove without travel data.

EndMile embeds a low-carbon journey planner on your visit page in one line of code, tracking audience modal shifts (active, rail, bus, EV) in real time.

{cta}

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "THEATRE_GREENBOOK_B", preview_url

    # 2. MUSEUMS & GALLERIES
    elif tpl_choice == "MUSEUM_CAZ_A":
        subject = f"Clean Air Zone & parking for {venue_name}"
        cta = (
            f"I mocked up how this looks on your actual visit page with Park & Ride tariffs (attached screenshot). Worth exploring for {venue_name}?"
            if screenshot_attached else
            f"Worth seeing a 30-second preview configured for {venue_name}?"
        )
        body = f"""{salutation}

With regional Clean Air Zones and city centre multi-storey parking tariffs climbing past £20, do visitors driving to {venue_name} often face surprise charges or fines?

Unclear parking guidance often leads to driver frustration before visitors even step through the doors.

We built EndMile as a 1-line embed that alerts visiting drivers to Clean Air Zones and points them directly to suburban Park & Ride hubs or direct rail connections, with live tariff comparisons.

{cta}

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "MUSEUM_CAZ_A", preview_url

    # 2. MUSEUMS & GALLERIES
    elif tpl_choice in ["MUSEUM_PLANNER_A", "MUSEUM_CAZ_A", "MUSEUM_ACCESS_B"]:
        subject = f"Travel directions for {venue_name}"
        cta = (
            f"I mocked up how this looks on {venue_name}'s visit page (attached). Worth sending over a quick preview link to test?"
            if screenshot_attached else
            f"Worth seeing a 30-second preview configured for {venue_name}?"
        )
        body = f"""{salutation}

Taking a look at the visitor guide on {venue_name}'s website, day visitors currently have to sort through multiple transport bullet points to compare driving vs public transit.

We built EndMile to give visitors an interactive door-to-door trip planner directly on your "Visit" page. Visitors enter their starting point and get live train times, walking routes, and official car parks side-by-side.

{cta}

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "MUSEUM_PLANNER_A", preview_url

    elif tpl_choice in ["HERITAGE_RURAL_B", "HERITAGE_CATCHMENT_A", "HERITAGE_LANES_B"]:
        subject = f"Car-free visitor routes to {venue_name}"
        cta = (
            f"Attached is a quick mockup of how it looks. Would a preview be of interest?"
            if screenshot_attached else
            f"Would it be helpful to see a 30-second preview for {venue_name}?"
        )
        body = f"""{salutation}

For tourists and visitors without a car, how easily can they work out how to reach {venue_name} via public transport from the nearest train station?

Many visitors assume historic sites are inaccessible without driving unless connecting bus routes or station taxis are clearly laid out.

EndMile embeds a 1-line route planner connecting mainline rail arrivals with local onward travel directly on your website.

{cta}

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "HERITAGE_RURAL_B", preview_url

    # 3. VISITOR ATTRACTIONS & ZOOS
    elif tpl_choice in ["ATTRACT_FAMILY_A", "ATTRACT_INGRESS_A", "ATTRACT_COST_B", "ATTRACT_HIGHWAY_A", "ATTRACT_GREEN_B"]:
        subject = f"Visitor trip planning for {venue_name}"
        cta = (
            f"I went ahead and mocked up how it looks on your visit page (attached). Worth seeing a 30-second live preview?"
            if screenshot_attached else
            f"Worth seeing a 30-second preview configured for {venue_name}?"
        )
        body = f"""{salutation}

Looking at the arrival advice on {venue_name}'s website, families planning a day out currently have to manually cross-reference driving routes, parking advice, and train connections across different tabs.

We built EndMile as an embeddable visit planner. Families simply enter their home town or postcode to see their exact driving time, car park locations, or public transit options in one place.

{cta}

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "ATTRACT_FAMILY_A", preview_url

    # 4. UNIVERSITIES & HIGHER EDUCATION
    elif tpl_choice == "UNI_OPENDAY_A":
        subject = f"Open day travel to {venue_name}"
        cta = (
            f"I attached a quick mockup of how this looks on your admissions page. Worth discussing a 14-day trial for {venue_name}?"
            if screenshot_attached else
            f"Worth seeing a 30-second staging preview for {venue_name}?"
        )
        body = f"""{salutation}

On undergraduate open days at {venue_name}, does campus parking regularly reach capacity by 9:30 AM, spilling thousands of visiting parents onto surrounding city roads?

First impressions matter for recruitment, but navigating campus barrier parking and city road closures is often a stressful start to the day.

EndMile embeds on your open day portal, guiding visiting families directly to designated satellite Park & Ride hubs, park-and-walk zones, or direct rail connections.

{cta}

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "UNI_OPENDAY_A", preview_url

    elif tpl_choice == "UNI_CAMPUS_B":
        subject = f"Campus transit wayfinding for {venue_name}"
        cta = (
            f"I attached a quick mockup of door-to-door campus navigation on your admissions page. Happy to share details if helpful?"
            if screenshot_attached else
            f"Happy to share a 30-second preview for {venue_name} if helpful?"
        )
        body = f"""{salutation}

When prospective students arrive at the railway station for open days or interviews at {venue_name}, how easily can they navigate to their specific faculty building or campus site?

Journey planning usually terminates at the city train station, leaving visitors confused by local bus shuttles and walking routes.

EndMile embeds on your admissions pages, routing visitors right to the entrance doors of specific university sites from anywhere in the UK.

{cta}

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "UNI_CAMPUS_B", preview_url

    elif tpl_choice == "UNI_TRAVELPLAN_A":
        subject = f"Section 106 travel plan for {venue_name}"
        cta = (
            f"I attached a mockup of how continuous travel telemetry looks on your campus portal. Would you be open to seeing a sample data export for {venue_name}?"
            if screenshot_attached else
            f"Would you be open to seeing a sample data export for {venue_name}?"
        )
        body = f"""{salutation}

Under {venue_name}'s local authority Section 106 planning agreements or Green Travel Plan, how does your estates team currently demonstrate modal split shifts away from single-occupancy cars?

Measuring actual student and visitor transport choices usually requires manual annual sample surveys.

EndMile embeds directly on campus visit and intranet pages, capturing continuous, verified travel search telemetry across active travel, rail, and bus to prove modal shift.

{cta}

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "UNI_TRAVELPLAN_A", preview_url

    # 5. UNIVERSAL GATEKEEPER & FOLLOW-UP
    elif tpl_choice == "VENUE_INFO_REFERRAL":
        subject = "Quick question - visitor travel"
        body = f"""{salutation}

Could you point me to whoever looks after visitor operations, guest experience, or transport planning at {venue_name}?

I'm an independent UK software engineer building an embeddable journey planner to help UK destinations manage visitor arrivals and transport clarity. Just wanted to ask them 2 quick questions about how they currently handle visit pages.

Best,
{founder_name}
Founder, EndMile
{sender_email}

No worries at all if this isn't relevant to your team."""
        return subject, body, "VENUE_INFO_REFERRAL", preview_url

    elif tpl_choice == "VENUE_FOLLOWUP_PREVIEW":
        subject = f"Re: {venue_name}'s travel planning"
        body = f"""{salutation}

Following up briefly on this — I went ahead and mocked up a quick preview of how the planner would look embedded directly on your site:
{preview_url}

Unlike traditional transit consultancy software (which usually carries £2,000+ setup fees), EndMile embeds via a single script tag with £0 setup and runs for £19/mo on a 14-day free pilot.

Happy to send over the test snippet for your staging site if helpful?

Best,
{founder_name}
Founder, EndMile
{sender_email}"""
        return subject, body, "VENUE_FOLLOWUP_PREVIEW", preview_url

    else:
        # Fallback default
        return build_venue_email(row, template_override="THEATRE_JOURNEY_A", variant_override=variant_override, screenshot_attached=screenshot_attached, founder_name=founder_name, sender_email=sender_email)

def is_uk_business_hours() -> bool:
    """Check if current time is Monday-Friday between 08:30 and 17:30 UK time."""
    now = datetime.now()
    if now.weekday() >= 5:
        return False
    start_time = now.replace(hour=8, minute=30, second=0, microsecond=0)
    end_time = now.replace(hour=17, minute=30, second=0, microsecond=0)
    return start_time <= now <= end_time

def load_venue_prospects() -> pd.DataFrame:
    """Loads prospects from Master Excel workbook in Documents/endmile."""
    if EXCEL_PATH.exists():
        try:
            print(f"[LOAD] Loading master workbook from {EXCEL_PATH} (Sheet: Venue Widget Pipeline)...")
            return pd.read_excel(EXCEL_PATH, sheet_name="Venue Widget Pipeline")
        except Exception as e:
            print(f"[LOAD WARNING] Could not read Venue Widget Pipeline from master workbook ({e}).")

    if FALLBACK_EXCEL.exists():
        print(f"[LOAD] Falling back to {FALLBACK_EXCEL.name}...")
        return pd.read_excel(FALLBACK_EXCEL)

    raise FileNotFoundError(f"Neither {EXCEL_PATH} nor {FALLBACK_EXCEL} was found.")

def update_tracker_markdown(sent_records: list[dict]):
    """Appends sent records to traction/outreach-tracker.md."""
    if not TRACKER_PATH.exists() or not sent_records:
        return

    content = TRACKER_PATH.read_text(encoding="utf-8")
    table_marker = "| Date Sent | Organization | Contact Name & Title | Segment | Channel | Angle / Template | Status | Next Follow-Up | Notes / Response |"

    if table_marker not in content:
        return

    today_str = datetime.now().strftime("%Y-%m-%d")
    new_rows = []
    for r in sent_records:
        venue = clean_venue_name(r.get("VenueName", ""))
        role = r.get("role", "Visitor Services / Ops")
        tpl = r.get("template_code", "VENUE_DWELL_TIME")
        recipient = r.get("recipient", "")
        row_str = f"| {today_str} | {venue} | {role} | Cultural Venue | Email ({recipient}) | {tpl} | Sent | +3 Days | Auto-dispatched via CLI |"
        new_rows.append(row_str)

    split_pos = content.find(table_marker)
    header_end = content.find("\n", split_pos)
    sep_end = content.find("\n", header_end + 1)

    updated_content = content[:sep_end + 1] + "\n".join(new_rows) + "\n" + content[sep_end + 1:]
    TRACKER_PATH.write_text(updated_content, encoding="utf-8")
    print(f"[OK] Appended {len(sent_records)} row(s) to traction/outreach-tracker.md")

def save_venue_pipeline_updates(sent_records: list[dict]):
    """In-place update of Excel Workbook for Venue Widget Pipeline tab."""
    if not EXCEL_PATH.exists() or not sent_records:
        return

    today_str = datetime.now().strftime("%Y-%m-%d")
    sent_dict = {str(r["VenueID"]): r for r in sent_records}

    try:
        wb = openpyxl.load_workbook(EXCEL_PATH)
        if "Venue Widget Pipeline" in wb.sheetnames:
            ws_venue = wb["Venue Widget Pipeline"]
            headers = [cell.value for cell in ws_venue[1]]
            vid_col = headers.index("VenueID") + 1
            appr_col = headers.index("ManualApproval") + 1
            tpl_col = headers.index("AssignedTemplate") + 1
            status_col = headers.index("OutreachStatus") + 1
            date_col = headers.index("DateSent") + 1

            for row_idx in range(2, ws_venue.max_row + 1):
                vid = str(ws_venue.cell(row=row_idx, column=vid_col).value)
                if vid in sent_dict:
                    r = sent_dict[vid]
                    ws_venue.cell(row=row_idx, column=appr_col, value="Sent")
                    ws_venue.cell(row=row_idx, column=tpl_col, value=r.get("template_code", "CLI"))
                    ws_venue.cell(row=row_idx, column=status_col, value="Sent")
                    ws_venue.cell(row=row_idx, column=date_col, value=today_str)

        dash_sheet_name = "A-B Testing & Dashboard" if "A-B Testing & Dashboard" in wb.sheetnames else "A-B Testing & Review"
        if dash_sheet_name in wb.sheetnames:
            ws_dash = wb[dash_sheet_name]
            # Update Total Widget Emails Dispatched
            for r_idx in range(14, 23):
                if ws_dash.cell(row=r_idx, column=1).value == "Total Widget Emails Dispatched":
                    cur_val = int(ws_dash.cell(row=r_idx, column=2).value or 0)
                    ws_dash.cell(row=r_idx, column=2, value=cur_val + len(sent_records))
                    break

            # Increment variant count
            for r_idx in range(24, 35):
                v_code = str(ws_dash.cell(row=r_idx, column=1).value).strip()
                matching = sum(1 for r in sent_records if r.get("template_code") == v_code)
                if matching > 0:
                    cur = int(ws_dash.cell(row=r_idx, column=4).value or 0)
                    ws_dash.cell(row=r_idx, column=4, value=cur + matching)

        wb.save(EXCEL_PATH)
        print(f"[OK] In-place synchronized Master Excel Workbook ({EXCEL_PATH.name})")
    except Exception as e:
        print(f"[WARNING] Could not update Excel workbook: {e}")

def send_smtp_email(
    to_email: str,
    subject: str,
    body: str,
    sender_email: str,
    screenshot_path: str = "",
    venue_name: str = "venue"
) -> bool:
    """Dispatches email via secure SMTP with optional screenshot attachment."""
    smtp_host = os.getenv("SMTP_HOST", "smtp.stackmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER", sender_email)
    smtp_pass = os.getenv("SMTP_PASSWORD")

    if not smtp_pass:
        print(f"SMTP password required for {smtp_user}. Aborting.")
        return False

    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = f"Isaac Willoughby <{sender_email}>"
    msg["To"] = to_email
    msg["Reply-To"] = sender_email

    body_part = MIMEText(body, "plain", "utf-8")
    msg.attach(body_part)

    if screenshot_path and os.path.exists(screenshot_path):
        try:
            with open(screenshot_path, "rb") as f:
                img_data = f.read()
            clean_slug = re.sub(r'[^a-zA-Z0-9]+', '_', venue_name.lower()).strip('_')
            filename = f"{clean_slug}_travel_planner_mock.png"
            img_part = MIMEImage(img_data, name=filename)
            img_part.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(img_part)
            print(f"  [ATTACHED] Mock screenshot attached: {filename}")
        except Exception as e:
            print(f"  [ATTACH ERROR] Could not attach screenshot {screenshot_path}: {e}")

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_user, smtp_pass)
            server.sendmail(sender_email, [to_email], msg.as_string())
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send email to {to_email}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="EndMile Automated Venue Outreach Dispatcher")
    parser.add_argument("--dry-run", action="store_true", help="Preview emails without sending")
    parser.add_argument("--limit", type=int, default=5, help="Maximum emails to send/preview (default 5)")
    parser.add_argument("--venues", type=str, default="", help="Comma-separated VenueIDs to dispatch")
    parser.add_argument("--template", type=str, default="", help="Force specific template code")
    parser.add_argument("--variant", choices=["A", "B", "auto"], default="auto", help="A/B test variant selection (A, B, or auto)")
    parser.add_argument("--screenshot", action="store_true", help="Generate/verify mock screenshot using Playwright DevTools injection")
    parser.add_argument("--attach-screenshot", action="store_true", help="Attach generated mock screenshot to outgoing email")
    parser.add_argument("--all", action="store_true", help="Ignore manual approval filter and send any uncontacted venue with contact email")
    parser.add_argument("--ignore-hours", action="store_true", help="Bypass UK business hours check")
    parser.add_argument("--delay-min", type=int, default=60, help="Minimum pause between sends in seconds")
    parser.add_argument("--delay-max", type=int, default=180, help="Maximum pause between sends in seconds")
    args = parser.parse_args()

    print("=" * 70)
    print("   ENDMILE VENUE TRAVEL WIDGET OUTBOUND DISPATCHER")
    print(f" Mode: {'DRY RUN (Preview Only)' if args.dry_run else 'LIVE SEND'}")
    print(f" Source: {EXCEL_PATH.name} (Sheet: Venue Widget Pipeline)")
    print(f" Variant: {args.variant.upper()}")
    print(f" Screenshots: {'ATTACH TO EMAIL' if args.attach_screenshot else ('GENERATE / PREVIEW' if args.screenshot else 'DISABLED')}")
    print(f" Approval Filter: {'ALL Venues' if args.all else 'Approved by Isaac in Excel only'}")
    print("=" * 70)

    if not args.dry_run and not args.ignore_hours and not is_uk_business_hours():
        print("[GUARD] Outside UK business hours (08:30-17:30 Mon-Fri). Use --ignore-hours or --dry-run.")
        sys.exit(0)

    df = load_venue_prospects()

    # Filter uncontacted
    if "OutreachStatus" in df.columns:
        uncontacted = df[df["OutreachStatus"] == "Uncontacted"].copy()
    else:
        uncontacted = df.copy()

    # Specific venues filter
    if args.venues:
        specific_venues = [v.strip() for v in args.venues.split(",") if v.strip()]
        batch = uncontacted[uncontacted["VenueID"].astype(str).isin(specific_venues)].copy()
        if batch.empty:
            print(f"None of specified venues {specific_venues} found in uncontacted queue.")
            return
    elif not args.all and "ManualApproval" in uncontacted.columns:
        # Default: Project Management Mode — only send leads Isaac approved
        batch = uncontacted[uncontacted["ManualApproval"] == "Approved"].copy()
        if batch.empty:
            print("[INFO] No venues currently marked 'Approved' in Venue Widget Pipeline.")
            print(f"Open '{EXCEL_PATH}', set ManualApproval to 'Approved' for your chosen venues, and re-run.")
            print("To send automatically to any venue with email, pass: --all")
            return
        batch = batch.head(args.limit)
    else:
        # Has an email
        has_email = uncontacted["ConfirmedEmail"].notna() | uncontacted["PublicEmail"].notna()
        batch = uncontacted[has_email].head(args.limit)

    print(f"Selected {len(batch)} venue(s) for dispatch.\n")

    sent_records = []

    for i, (_, lead) in enumerate(batch.iterrows(), 1):
        vid = str(lead.get("VenueID") or lead.get("ID") or "")
        vname = clean_venue_name(lead.get("VenueName") or lead.get("Name"))
        email = str(lead.get("ConfirmedEmail") or lead.get("PublicEmail") or lead.get("RawEmail") or "").strip().lower()
        role = str(lead.get("ConfirmedRole") or "Visitor Services / Operations")

        if not email or "@" not in email:
            print(f"[{i}/{len(batch)}] Skipping {vid} ({vname}) - No valid email address.")
            continue

        # Screenshot handling
        screenshot_path = ""
        if args.screenshot or args.attach_screenshot:
            clean_slug = re.sub(r'[^a-zA-Z0-9]+', '_', vname.lower()).strip('_')[:40]
            expected_shot = SCREENSHOTS_DIR / f"{vid}_{clean_slug}.png"
            fallback_shot = SCREENSHOTS_DIR / f"{clean_slug}.png"

            if expected_shot.exists():
                screenshot_path = str(expected_shot)
                print(f"  [SCREENSHOT CACHED] Found: {expected_shot.name}")
            elif fallback_shot.exists():
                screenshot_path = str(fallback_shot)
                print(f"  [SCREENSHOT CACHED] Found: {fallback_shot.name}")
            elif capture_venue_mock_screenshot:
                web_url = str(lead.get("Website") or lead.get("Domain") or "").strip()
                if web_url and web_url not in ["nan", "none"]:
                    print(f"  [SCREENSHOT] Generating mock screenshot for '{vname}'...")
                    shot = capture_venue_mock_screenshot(
                        url=web_url,
                        venue_name=vname,
                        venue_id=vid,
                        archetype=str(lead.get("Archetype", "theatre"))
                    )
                    if shot and os.path.exists(shot):
                        screenshot_path = shot

        subject, body, tpl_code, preview_url = build_venue_email(
            lead.to_dict(),
            template_override=args.template,
            variant_override=args.variant,
            screenshot_attached=bool(screenshot_path and args.attach_screenshot)
        )

        print("-" * 70)
        print(f"[{i}/{len(batch)}] Venue: {vname} (ID: {vid})")
        print(f"To:         {email}")
        print(f"Role:       {role}")
        print(f"Template:   {tpl_code}")
        print(f"Subject:    {subject}")
        print(f"Preview:    {preview_url}")
        if screenshot_path:
            print(f"Screenshot: {screenshot_path}")
        print("-" * 70)
        print(body)
        print("-" * 70 + "\n")

        if args.dry_run:
            continue

        # Live dispatch
        success = send_smtp_email(
            email,
            subject,
            body,
            "isaacw@endmilerouting.co.uk",
            screenshot_path=screenshot_path if args.attach_screenshot else "",
            venue_name=vname
        )
        if success:
            print(f"[SUCCESS] Dispatched to {email}")
            sent_records.append({
                "VenueID": vid,
                "VenueName": vname,
                "recipient": email,
                "role": role,
                "template_code": tpl_code,
                "preview_url": preview_url
            })
            if i < len(batch):
                pause_s = random.randint(args.delay_min, args.delay_max)
                print(f"[THROTTLE] Pausing {pause_s}s before next send...")
                time.sleep(pause_s)
        else:
            print(f"[FAILED] Could not send to {email}")

    if not args.dry_run and sent_records:
        save_venue_pipeline_updates(sent_records)
        update_tracker_markdown(sent_records)
        print(f"\n[COMPLETE] Successfully dispatched {len(sent_records)} venue email(s).")
    elif args.dry_run:
        print("\n[DRY RUN COMPLETE] No emails were actually transmitted.")

if __name__ == "__main__":
    main()
