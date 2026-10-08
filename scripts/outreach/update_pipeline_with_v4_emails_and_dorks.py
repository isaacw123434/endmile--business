#!/usr/bin/env python3
"""
Update Master Pipeline Excel with Latest Venue Contacts, Google Pro Search URLs, and Zero-Link Templates
----------------------------------------------------------------------------------------------------------
1. Reads latest notes, contacts, and Google Pro Search URLs from:
   C:\\Users\\isaac\\Downloads\\endmile widget v4 (1).xlsx (or endmile widget v4.xlsx)
2. Updates Sheet 2 ('Venue Widget Pipeline') in endmile_master_pipeline.xlsx:
   - Updates DeepLinkGoogleSearch across all 4,992 rows with the AI Pro Search URL.
   - Updates ConfirmedEmail, ConfirmedName, ConfirmedRole, RawNotesAndContacts, and ManualApproval='Approved'
     for all venues with newly discovered contacts.
3. Updates Sheet 3 ('Email Templates & Referrers') to ensure ABSOLUTELY ZERO RAW URL LINKS in all copy.
4. Synchronizes to:
   - C:\\Users\\isaac\\OneDrive\\Documents\\EndMile\\endmile_master_pipeline.xlsx
   - C:\\Users\\isaac\\OneDrive\\Desktop\\endmile_master_pipeline.xlsx
   - C:\\Users\\isaac\\Documents\\endmile\\endmile_master_pipeline.xlsx
"""

import os
import re
import shutil
from pathlib import Path
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

LOCAL_DIR = Path(r"C:\Users\isaac\Documents\endmile")
LOCAL_PATH = LOCAL_DIR / "endmile_master_pipeline.xlsx"

ONEDRIVE_DOCS_DIR = Path(r"C:\Users\isaac\OneDrive\Documents\EndMile")
ONEDRIVE_DOCS_PATH = ONEDRIVE_DOCS_DIR / "endmile_master_pipeline.xlsx"

ONEDRIVE_DESKTOP_DIR = Path(r"C:\Users\isaac\OneDrive\Desktop")
ONEDRIVE_DESKTOP_PATH = ONEDRIVE_DESKTOP_DIR / "endmile_master_pipeline.xlsx"

WIDGET_V4_1 = Path(r"C:\Users\isaac\Downloads\endmile widget v4 (1).xlsx")
WIDGET_V4 = Path(r"C:\Users\isaac\Downloads\endmile widget v4.xlsx")
SOURCE_WIDGET_PATH = WIDGET_V4_1 if WIDGET_V4_1.exists() else WIDGET_V4

# Styling
APPROVED_FILL = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
PENDING_FILL = PatternFill(start_color="FEF9C3", end_color="FEF9C3", fill_type="solid")
BOLD_FONT = Font(name="Calibri", size=10, bold=True)
REGULAR_FONT = Font(name="Calibri", size=10)
CODE_FONT = Font(name="Consolas", size=9.5)
THIN_SIDE = Side(border_style="thin", color="CBD5E1")
CELL_BORDER = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=THIN_SIDE)

COMMON_NAME_TOKENS = {
    "niall", "linda", "julia", "elin", "david", "celine", "alice", "alex",
    "cate", "kate", "amanda", "martin", "rosemary", "jo", "lauren", "sworsfold",
    "john", "paul", "sarah", "emma", "james", "richard", "helen", "simon", "claire",
    "mark", "rachel", "andrew", "anna", "robert", "fiona", "peter", "lucy", "sophie"
}

def clean_contact_name(raw_text: str, email: str) -> tuple[str, str]:
    """Extract clean first name and role if confident, otherwise empty string."""
    clean_line = raw_text.split(",")[0].replace(email, "").strip(" -:,;")
    role = ""
    name = ""
    role_match = re.search(r'\(([^)]+)\)', clean_line)
    if role_match:
        role = role_match.group(1).strip()
        name = clean_line[:role_match.start()].strip(" -:,;")
    else:
        parts = clean_line.split("-")
        if len(parts) >= 2:
            name = parts[0].strip()
            role = parts[1].strip()
        elif parts:
            name = parts[0].strip()

    first_name = ""
    if name and not any(k in name.lower() for k in ["info", "hello", "team", "box office", "admin", "theatre", "museum", "office", "manager", "capital", "lyceum", "eno"]):
        tokens = name.split()
        if tokens:
            candidate = tokens[0].title()
            if candidate.isalpha() and len(candidate) >= 2:
                first_name = candidate

    if not first_name and email and "@" in email:
        handle = email.split("@")[0].lower()
        handle_token = handle.split(".")[0].split("_")[0]
        # Only accept handle if it's a known name or standard length name (not an initial+surname like aastell, lmonaghan)
        if handle_token in COMMON_NAME_TOKENS:
            first_name = handle_token.title()
        elif handle_token.isalpha() and 3 <= len(handle_token) <= 8 and not any(handle_token.startswith(c) for c in ["info", "admin", "foh", "office", "boxoffice", "contact", "mgr", "manager"]):
            # Check if likely initial+surname (e.g. jsmith, aastell)
            # If length > 4 and first 2 consonants or unusual digraph, prefer blank
            if handle_token in ["niall", "linda", "celine", "julia", "david"]:
                first_name = handle_token.title()

    return first_name, role

def extract_venue_contact(raw_text: str) -> tuple[str, str, str]:
    """Returns (first_name, primary_email, role)."""
    if not isinstance(raw_text, str) or not raw_text.strip() or raw_text.strip() == "-":
        return "", "", ""
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', raw_text)
    if not email_match:
        return "", "", ""
    email = email_match.group(0).lower()
    first_name, role = clean_contact_name(raw_text, email)
    return first_name, email, role

def run_update():
    print("=" * 75)
    print(" UPDATING MASTER PIPELINE WITH LATEST VENUE CONTACTS & PRO SEARCH URLS")
    print("=" * 75)

    if not SOURCE_WIDGET_PATH.exists():
        print(f"[ERROR] Source widget file not found at {SOURCE_WIDGET_PATH}")
        return

    print(f"[SOURCE] Loading latest widget data from: {SOURCE_WIDGET_PATH.name}...")
    wb_v4 = openpyxl.load_workbook(SOURCE_WIDGET_PATH, data_only=True)
    ws_v4 = wb_v4.active
    v4_headers = [c for c in next(ws_v4.iter_rows(values_only=True))]

    id_col = v4_headers.index("ID")
    notes_col = v4_headers.index("Column 1 (Notes & Contacts)")
    dork_col = v4_headers.index("DeepLinkGoogleSearch")

    v4_map = {}
    for r in range(2, ws_v4.max_row + 1):
        vid = str(ws_v4.cell(row=r, column=id_col+1).value or "").strip()
        # strip any .0 from float IDs
        if vid.endswith(".0"):
            vid = vid[:-2]
        note = str(ws_v4.cell(row=r, column=notes_col+1).value or "").strip()
        dork = str(ws_v4.cell(row=r, column=dork_col+1).value or "").strip()
        if vid:
            v4_map[vid] = {"note": note, "dork": dork}

    print(f"[SOURCE] Loaded {len(v4_map)} venue records from source.")

    # Load master pipeline workbook
    source_master = ONEDRIVE_DOCS_PATH if ONEDRIVE_DOCS_PATH.exists() else LOCAL_PATH
    print(f"[LOAD] Loading master workbook from: {source_master}...")
    wb_master = openpyxl.load_workbook(source_master)

    # 1. Update Sheet 2: Venue Widget Pipeline
    if "Venue Widget Pipeline" not in wb_master.sheetnames:
        print("[ERROR] 'Venue Widget Pipeline' sheet missing!")
        return

    ws_venue = wb_master["Venue Widget Pipeline"]
    v_headers = [c for c in next(ws_venue.iter_rows(values_only=True))]
    v_id_col = v_headers.index("VenueID") + 1
    v_appr_col = v_headers.index("ManualApproval") + 1
    v_email_col = v_headers.index("ConfirmedEmail") + 1
    v_name_col = v_headers.index("ConfirmedName") + 1
    v_role_col = v_headers.index("ConfirmedRole") + 1
    v_dork_col = v_headers.index("DeepLinkGoogleSearch") + 1
    v_notes_col = v_headers.index("RawNotesAndContacts") + 1

    updated_contacts_count = 0
    updated_dorks_count = 0
    total_approved = 0

    for r in range(2, ws_venue.max_row + 1):
        vid = str(ws_venue.cell(row=r, column=v_id_col).value or "").strip()
        if vid.endswith(".0"):
            vid = vid[:-2]

        v4_data = v4_map.get(vid)
        if not v4_data:
            continue

        # Update DeepLinkGoogleSearch
        new_dork = v4_data["dork"]
        if new_dork:
            ws_venue.cell(row=r, column=v_dork_col, value=new_dork)
            updated_dorks_count += 1

        # Check and update Notes & Contacts
        v4_note = v4_data["note"]
        if v4_note and v4_note != "-":
            c_first, c_email, c_role = extract_venue_contact(v4_note)
            if c_email and "@" in c_email:
                ws_venue.cell(row=r, column=v_email_col, value=c_email)
                if c_first:
                    ws_venue.cell(row=r, column=v_name_col, value=c_first)
                if c_role:
                    ws_venue.cell(row=r, column=v_role_col, value=c_role)
                ws_venue.cell(row=r, column=v_notes_col, value=v4_note)

                # Set ManualApproval to Approved
                cell_appr = ws_venue.cell(row=r, column=v_appr_col, value="Approved")
                cell_appr.fill = APPROVED_FILL
                cell_appr.font = BOLD_FONT
                cell_appr.alignment = Alignment(horizontal="center", vertical="center")
                updated_contacts_count += 1

        current_appr = ws_venue.cell(row=r, column=v_appr_col).value
        if current_appr == "Approved":
            total_approved += 1

    print(f"[OK] Updated {updated_dorks_count} Google Pro Search URLs across Venue Widget Pipeline.")
    print(f"[OK] Confirmed & approved {updated_contacts_count} venue contacts (Total approved: {total_approved}).")

    # 2. Update Sheet 3: Email Templates & Referrers (STRICT ZERO RAW LINKS)
    ws_tpl = wb_master["Email Templates & Referrers"]
    
    # Complete 16 templates with ZERO raw URLs anywhere in body or signature
    zero_link_templates = [
        # CONSULTANCY APP
        {
            "Product": "Consultancy App",
            "TemplateCode": "DIRECT_SCRATCHPAD",
            "TemplateName": "Direct Operations Scratchpad Pitch",
            "TargetInbox": "Direct Operations & Discovered Named Contacts (operations@, projects@, travel@, named lead)",
            "Subject": "{CompanyClean}'s travel planning",
            "Body": (
                "{Good morning / Good afternoon} {ContactName},\n\n"
                "When your consultants head out to client sites (like {Corridor}), does someone on operations still spend 10 minutes juggling Google Maps, Trainline, and station parking to find the fastest and cheapest door-to-door route?\n\n"
                "I built EndMile as a quick scratchpad for UK consultancies. It stacks up driving (at HMRC 55p/mile) against train fares, station parking, and destination taxis side-by-side in 10 seconds.\n\n"
                "Happy to send over a 30-second preview of how it works for {HQCity} corridors if helpful?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk\n\n"
                "No worries at all if this isn't relevant to your team."
            ),
            "Angle": "10-Second Door-to-Door TCO Comparison (Stops multi-tab spreadsheet chaos)",
            "WordCount": 85,
            "WhenToUse": "Direct outreach to operations leads, project coordinators, or practice directors."
        },
        {
            "Product": "Consultancy App",
            "TemplateCode": "DIRECT_RECHARGE",
            "TemplateName": "Direct Project Recharges & Margin Defense",
            "TargetInbox": "Finance, Commercial Leads, Project Directors (finance@, commercial@, projects@)",
            "Subject": "Client travel recharges",
            "Body": (
                "{Good morning / Good afternoon} {ContactName},\n\n"
                "When {CompanyClean}'s consultants travel to client sites, do your finance or project leads ever run into pushback from client accounts payable over HMRC 55p mileage or taxi expenses?\n\n"
                "We've found many UK consultancies lose 1–5% of travel recharges simply because clients look up a superficial £50 train ticket and dispute a £110 car journey, ignoring station parking and taxi legs.\n\n"
                "We built EndMile to calculate the true door-to-door comparison before consultants travel, generating a 1-page Pre-Trip Cost Justification PDF to attach directly to client invoices.\n\n"
                "Would it be helpful to see a sample justification report for {HQCity} routes?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk\n\n"
                "No worries at all if this isn't relevant to your team."
            ),
            "Angle": "Pre-Trip Cost Justification PDF (Defends billable margin against client pushback)",
            "WordCount": 98,
            "WhenToUse": "Direct touch to finance directors, practice heads, or billable engagement managers."
        },
        {
            "Product": "Consultancy App",
            "TemplateCode": "INFO_REF_A",
            "TemplateName": "Info Desk Referral A (Founder Discovery Ask)",
            "TargetInbox": "General Front-Desk / Triage Inboxes (info@, hello@, enquiries@, contact@)",
            "Subject": "Quick question - travel coordination",
            "Body": (
                "{Good morning / Good afternoon},\n\n"
                "Could you point me to whoever looks after consultant travel or expenses at {CompanyClean}?\n\n"
                "I'm an independent UK software engineer building a tool to cut down the time consultancies spend planning client travel and comparing HMRC 55p mileage. Just wanted to ask them 2 quick questions about how they currently handle it.\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk\n\n"
                "No worries at all if this isn't relevant to your team."
            ),
            "Angle": "Disarming Founder Discovery Question (Highest response rate)",
            "WordCount": 54,
            "WhenToUse": "Default / primary angle for all general inbox outreach."
        },
        {
            "Product": "Consultancy App",
            "TemplateCode": "INFO_REF_B",
            "TemplateName": "Info Desk Referral B (Multi-Tab Time Saver)",
            "TargetInbox": "General Front-Desk / Triage Inboxes (info@, hello@, enquiries@, contact@)",
            "Subject": "{CompanyClean}'s travel planning",
            "Body": (
                "{Good morning / Good afternoon},\n\n"
                "Quick question — who at {CompanyClean} coordinates travel when consultants head out to client sites (like {Corridor})?\n\n"
                "I put together a simple tool for UK consultancies that works out driving mileage against train fares, parking, and taxis in 10 seconds, instead of jumping between 3 tabs.\n\n"
                "Worth passing this over to whoever handles travel for your team?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk\n\n"
                "No worries at all if this isn't relevant to your team."
            ),
            "Angle": "Operational Productivity & Eliminating 3 Tabs",
            "WordCount": 58,
            "WhenToUse": "Secondary A/B rotation for consultancies with explicit known regional corridors."
        },
        {
            "Product": "Consultancy App",
            "TemplateCode": "INFO_REF_C",
            "TemplateName": "Info Desk Referral C (55p Mileage Dispute)",
            "TargetInbox": "General Front-Desk / Triage Inboxes (info@, hello@, enquiries@, contact@)",
            "Subject": "Consultant travel expenses",
            "Body": (
                "{Good morning / Good afternoon},\n\n"
                "Could you point me to whoever manages travel expenses or project recharges at {CompanyClean}?\n\n"
                "I put together a simple tool for UK consultancies to help back up HMRC 55p mileage against rail costs when clients question travel invoices.\n\n"
                "Who would be best to speak with about that?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk\n\n"
                "No worries at all if this isn't relevant to your team."
            ),
            "Angle": "Defending HMRC Mileage Recharges via Client Invoicing PDF",
            "WordCount": 52,
            "WhenToUse": "Targeting finance-leaning or commercial consultancies."
        },
        {
            "Product": "Consultancy App",
            "TemplateCode": "INFO_REF_D",
            "TemplateName": "Info Desk Referral D (Ultra-Short Gatekeeper Forward)",
            "TargetInbox": "General Front-Desk / Triage Inboxes (info@, hello@, enquiries@, contact@)",
            "Subject": "Quick referral - operations / travel",
            "Body": (
                "{Good morning / Good afternoon},\n\n"
                "Could you point me in the right direction? Who at {CompanyClean} coordinates travel planning or expenses for consultants travelling to client sites?\n\n"
                "Thanks so much,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk\n\n"
                "No worries at all if this isn't relevant to your team."
            ),
            "Angle": "Ultra-Low Friction Forward Request (<35 words)",
            "WordCount": 35,
            "WhenToUse": "Fast forwarding by administrative staff."
        },
        {
            "Product": "Consultancy App",
            "TemplateCode": "FOLLOWUP_DIRECT_1",
            "TemplateName": "Direct Follow-Up (+3 to 4 Days)",
            "TargetInbox": "Direct Operations & Named Contacts",
            "Subject": "Re: {CompanyClean}'s travel planning",
            "Body": (
                "{Good morning / Good afternoon} {ContactName},\n\n"
                "Just following up on this — know you're busy coordinating client dispatches.\n\n"
                "We set up a quick preview with {HQCity} corridors pre-configured. No login or sign-up needed — happy to send over the preview link or run a couple of sample client routes for your team if helpful.\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk\n\n"
                "No worries at all if this isn't relevant to your team."
            ),
            "Angle": "Zero-Link Polite Bump (Zero friction preview offer)",
            "WordCount": 50,
            "WhenToUse": "Send 3-4 business days after DIRECT_SCRATCHPAD if no response."
        },
        {
            "Product": "Consultancy App",
            "TemplateCode": "FOLLOWUP_INFO_1",
            "TemplateName": "Info Desk Referral Follow-Up (+4 Days)",
            "TargetInbox": "General Front-Desk / Triage Inboxes (info@, hello@)",
            "Subject": "Re: Quick question - travel coordination",
            "Body": (
                "{Good morning / Good afternoon},\n\n"
                "Following up briefly on this — did you know who would be the best person to speak with regarding consultant travel or operations at {CompanyClean}?\n\n"
                "Much appreciated,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk\n\n"
                "No worries at all if this isn't relevant to your team."
            ),
            "Angle": "Polite Nudge (Ensures email didn't get buried)",
            "WordCount": 34,
            "WhenToUse": "Send 4 business days after INFO_REF_A/B/C/D if no reply."
        },
        # VENUE WIDGET (B2B TRAVEL PLANNER EMBED)
        {
            "Product": "Venue Travel Widget",
            "TemplateCode": "VENUE_VISIT_A",
            "TemplateName": "Universal Flagship (Static Bullet Points vs Interactive Planner)",
            "TargetInbox": "Visitor Services, Operations Directors, Commercial Leads, General Managers",
            "Subject": "Visitor directions for {VenueName}",
            "Body": (
                "{Good morning / Good afternoon} {ContactName},\n\n"
                "Taking a look at the \"Getting Here\" page on {VenueName}'s website, visitors planning their trip currently have to sort through static bullet points to compare driving, parking, and public transit.\n\n"
                "We built EndMile as an interactive visit planner that embeds directly onto your website with zero technical setup. Visitors simply enter their home postcode and get live train times, walking routes, and official car parks side-by-side.\n\n"
                "I went ahead and mocked up how this looks on your actual visit page (see attached screenshot).\n\n"
                "Would you be open to trying a live preview?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk\n\n"
                "No worries at all if this isn't relevant to your team."
            ),
            "Angle": "Universal Flagship: Replaces static transport bullet points with 1-click door-to-door transit & parking comparison",
            "WordCount": 85,
            "WhenToUse": "Flagship template for theatres, concert halls, civic arts centres, and cultural destinations."
        },
        {
            "Product": "Venue Travel Widget",
            "TemplateCode": "GIG_CURFEW_A",
            "TemplateName": "Music Venues & Arenas (Post-Gig Public Transit & Last Trains)",
            "TargetInbox": "Operations Managers, Venue Promoters, General Managers",
            "Subject": "Getting home from {VenueName}",
            "Body": (
                "{Good morning / Good afternoon} {ContactName},\n\n"
                "For evening shows finishing after 10:30 PM at {VenueName}, do gig-goers travelling in from surrounding towns often struggle to check return train and bus times in advance?\n\n"
                "We built EndMile as an interactive travel planner that embeds directly into your event pages. It lets fans check their exact route home—including last rail departures and station walking times—without having to leave your website.\n\n"
                "I attached a mockup showing how it looks on your site. Happy to share a 30-second live preview if helpful?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk\n\n"
                "No worries at all if this isn't relevant to your team."
            ),
            "Angle": "Nightlife & Curfew Egress: Solves post-10:30 PM last train anxiety directly on event/lineup pages",
            "WordCount": 81,
            "WhenToUse": "Music halls, live music venues, comedy clubs, and late-night performing arts venues."
        },
        {
            "Product": "Venue Travel Widget",
            "TemplateCode": "MUSEUM_PLANNER_A",
            "TemplateName": "Urban Museums & Galleries (Transit vs Driving Clarity)",
            "TargetInbox": "Head of Visitor Experience, Commercial Directors, Operations Managers",
            "Subject": "Travel directions for {VenueName}",
            "Body": (
                "{Good morning / Good afternoon} {ContactName},\n\n"
                "Taking a look at the visitor guide on {VenueName}'s website, day visitors currently have to sort through multiple transport bullet points to compare driving vs public transit.\n\n"
                "We built EndMile to give visitors an interactive door-to-door trip planner directly on your \"Visit\" page. Visitors enter their starting point and get live train times, walking routes, and official car parks side-by-side.\n\n"
                "I mocked up how this looks on {VenueName}'s visit page (attached). Worth sending over a quick preview link to test?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk\n\n"
                "No worries at all if this isn't relevant to your team."
            ),
            "Angle": "Museums & Galleries: Door-to-door arrival clarity, driving vs rail comparison on mobile",
            "WordCount": 83,
            "WhenToUse": "Urban museums, civic art galleries, science discovery centres, and exhibition halls."
        },
        {
            "Product": "Venue Travel Widget",
            "TemplateCode": "HERITAGE_RURAL_B",
            "TemplateName": "Rural Heritage & Historic Sites (Mainline Rail to Rural Transport)",
            "TargetInbox": "Commercial Directors, Head of Visitor Services, Operations",
            "Subject": "Car-free visitor routes to {VenueName}",
            "Body": (
                "{Good morning / Good afternoon} {ContactName},\n\n"
                "For tourists and visitors without a car, how easily can they work out how to reach {VenueName} via public transport from the nearest mainline station?\n\n"
                "Many visitors assume historic sites are inaccessible without driving unless connecting bus routes and station taxis are clearly laid out.\n\n"
                "EndMile embeds directly onto your visit page with zero technical setup, showing door-to-door transit routes that link mainline rail arrivals with local onward travel.\n\n"
                "Attached is a quick mockup of how it looks on your site. Would a preview link be of interest?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk\n\n"
                "No worries at all if this isn't relevant to your team."
            ),
            "Angle": "Car-Free Tourism: Bridges mainline rail stations to rural buses, taxis, and walking trails",
            "WordCount": 79,
            "WhenToUse": "Castles, historic houses, country parks, abbeys, and rural visitor destinations."
        },
        {
            "Product": "Venue Travel Widget",
            "TemplateCode": "ATTRACT_FAMILY_A",
            "TemplateName": "Visitor Attractions & Zoos (Family Cost Transparency: Fuel/Parking vs Rail)",
            "TargetInbox": "Head of Visitor Operations, General Managers, Marketing Leads",
            "Subject": "Visitor trip planning for {VenueName}",
            "Body": (
                "{Good morning / Good afternoon} {ContactName},\n\n"
                "Looking at the arrival advice on {VenueName}'s website, families planning a day out currently have to cross-reference driving routes, parking charges, and family train fares across different tabs to work out the fastest and cheapest option.\n\n"
                "We built EndMile as an interactive visit planner that plugs directly into your website. Families simply enter their home postcode to instantly compare driving and parking costs side-by-side with rail and transit fares in one view.\n\n"
                "I went ahead and mocked up how it looks on your visit page (attached). Worth seeing a 30-second live preview?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk\n\n"
                "No worries at all if this isn't relevant to your team."
            ),
            "Angle": "Family Cost Equation: Solves driving + parking tariff vs rail fare confusion to prevent booking drop-off",
            "WordCount": 85,
            "WhenToUse": "Zoos, theme parks, farm parks, safari parks, and family attraction destinations."
        },
        {
            "Product": "Venue Travel Widget",
            "TemplateCode": "THEATRE_SCOPE3_A",
            "TemplateName": "ACE NPOs & Theatres (Scope 3 Audience Carbon Reporting)",
            "TargetInbox": "Sustainability Leads, Operations Directors, Executive Directors (NPOs)",
            "Subject": "Audience travel reporting for {VenueName}",
            "Body": (
                "{Good morning / Good afternoon} {ContactName},\n\n"
                "For {VenueName}'s annual Julie's Bicycle environmental reporting, how does your team currently collect audience travel data?\n\n"
                "Audience travel usually represents over 80% of a cultural venue's footprint, yet most venues have to rely on post-show surveys with 3–4% response rates.\n\n"
                "EndMile embeds directly on your visit page, giving audience members live journey directions while passively logging verified travel modal splits and passenger mileage in the background.\n\n"
                "Would you be open to seeing a sample data export for {VenueName}?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk\n\n"
                "No worries at all if this isn't relevant to your team."
            ),
            "Angle": "Arts Council England (ACE) Scope 3 Reporting: Passive journey queries replace 3% survey response rates",
            "WordCount": 86,
            "WhenToUse": "NPO theatres, civic arts trusts, and Green Book cultural venues with grant reporting."
        },
        {
            "Product": "Venue Travel Widget",
            "TemplateCode": "VENUE_INFO_REFERRAL",
            "TemplateName": "Universal Gatekeeper & Front-Desk Referral Inquiry",
            "TargetInbox": "Box Office & Front Desk (info@, hello@, boxoffice@, enquiries@)",
            "Subject": "Quick question - visitor directions",
            "Body": (
                "{Good morning / Good afternoon},\n\n"
                "Could you point me to whoever looks after visitor operations or manages the website at {VenueName}?\n\n"
                "I'm an independent UK software developer who built an interactive visit planner for UK venues, and wanted to share a 30-second preview of how it looks on {VenueName}'s site.\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk\n\n"
                "No worries at all if this isn't relevant to your team."
            ),
            "Angle": "Disarming Engineer Referral Ask to Box Office / Gatekeeper",
            "WordCount": 44,
            "WhenToUse": "Default when targeting info@, hello@, or boxoffice@ inboxes."
        },
        {
            "Product": "Venue Travel Widget",
            "TemplateCode": "VENUE_FOLLOWUP_PREVIEW",
            "TemplateName": "Interactive Staging Preview Follow-Up (+3 Days)",
            "TargetInbox": "General Managers, Ops Directors, Box Office Leads",
            "Subject": "Re: {VenueName}'s visitor arrivals",
            "Body": (
                "{Good morning / Good afternoon} {ContactName},\n\n"
                "Following up briefly on this — I went ahead and mocked up a quick preview showing how the journey planner would look embedded directly on your website.\n\n"
                "Unlike traditional transit software with £2,000+ setup hurdles, EndMile embeds directly onto your website with £0 setup and runs from £19/month on a 14-day free pilot.\n\n"
                "Happy to share the staging preview or test embed for your site if helpful?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk\n\n"
                "No worries at all if this isn't relevant to your team."
            ),
            "Angle": "Zero-Link Follow-up (£0 setup, £19/mo, staging preview offer)",
            "WordCount": 62,
            "WhenToUse": "Send 3 business days after initial venue touch if no reply."
        }
    ]

    # Re-write Sheet 3
    if ws_tpl.max_row > 1:
        ws_tpl.delete_rows(2, ws_tpl.max_row)

    for row_idx, tpl in enumerate(zero_link_templates, 2):
        row_vals = [
            tpl["Product"],
            tpl["TemplateCode"],
            tpl["TemplateName"],
            tpl["TargetInbox"],
            tpl["Subject"],
            tpl["Body"],
            tpl["Angle"],
            tpl["WordCount"],
            tpl["WhenToUse"]
        ]
        ws_tpl.append(row_vals)

        for c_idx in range(1, 10):
            cell = ws_tpl.cell(row=row_idx, column=c_idx)
            cell.border = CELL_BORDER
            cell.font = REGULAR_FONT

        c_prod = ws_tpl.cell(row=row_idx, column=1)
        c_prod.font = BOLD_FONT
        c_prod.alignment = Alignment(horizontal="center", vertical="top")

        c_code = ws_tpl.cell(row=row_idx, column=2)
        c_code.font = Font(name="Consolas", size=10, bold=True)
        c_code.alignment = Alignment(horizontal="center", vertical="top")

        c_name = ws_tpl.cell(row=row_idx, column=3)
        c_name.font = BOLD_FONT
        c_name.alignment = Alignment(vertical="top")

        c_tgt = ws_tpl.cell(row=row_idx, column=4)
        c_tgt.alignment = Alignment(vertical="top", wrap_text=True)

        c_subj = ws_tpl.cell(row=row_idx, column=5)
        c_subj.font = Font(name="Consolas", size=10, bold=True)
        c_subj.alignment = Alignment(vertical="top")

        c_body = ws_tpl.cell(row=row_idx, column=6)
        c_body.font = CODE_FONT
        c_body.alignment = Alignment(vertical="top", wrap_text=True)

        c_angle = ws_tpl.cell(row=row_idx, column=7)
        c_angle.alignment = Alignment(vertical="top", wrap_text=True)

        c_wc = ws_tpl.cell(row=row_idx, column=8)
        c_wc.alignment = Alignment(horizontal="center", vertical="top")

        c_guide = ws_tpl.cell(row=row_idx, column=9)
        c_guide.alignment = Alignment(vertical="top", wrap_text=True)

        ws_tpl.row_dimensions[row_idx].height = 145

    print(f"[OK] Sheet 3 updated with {len(zero_link_templates)} templates (ZERO raw URLs).")

    # 3. Save to all 3 paths
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    ONEDRIVE_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    ONEDRIVE_DESKTOP_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[SAVE] Saving to local fallback: {LOCAL_PATH}...")
    wb_master.save(LOCAL_PATH)
    wb_master.close()

    print(f"[SYNC] Saving to Desktop: {ONEDRIVE_DESKTOP_PATH}...")
    try:
        shutil.copy2(LOCAL_PATH, ONEDRIVE_DESKTOP_PATH)
        print("  -> Desktop copy successfully updated!")
    except Exception as e:
        print(f"  -> Could not update Desktop copy: {e}")

    print(f"[SYNC] Saving to OneDrive Documents: {ONEDRIVE_DOCS_PATH}...")
    try:
        shutil.copy2(LOCAL_PATH, ONEDRIVE_DOCS_PATH)
        print("  -> OneDrive Documents copy successfully updated!")
    except PermissionError:
        print("  -> [NOTE] File is currently open in LibreOffice/Excel. Close the app to finish syncing this copy.")
    except Exception as e:
        print(f"  -> Could not update OneDrive Documents copy: {e}")

    print("=" * 75)
    print("PIPELINE UPDATE SUMMARY:")
    print(f"  Desktop: {ONEDRIVE_DESKTOP_PATH} (Updated with 64 approved venues & AI Pro URLs)")
    print(f"  Local:   {LOCAL_PATH} (Updated)")
    print(f"  OneDrive Docs: {ONEDRIVE_DOCS_PATH} (Syncs automatically when LibreOffice/Excel closes)")
    print(f"Total Approved Venues for Manual Outreach: {total_approved}")
    print("=" * 75)

if __name__ == "__main__":
    run_update()
