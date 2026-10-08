#!/usr/bin/env python3
"""
Build Master EndMile Lead Review, Templates & Project Management Workbook
-----------------------------------------------------------------------
Generates a structured, multi-tab Master Excel workbook at:
  C:\\Users\\isaac\\Documents\\endmile\\endmile_master_pipeline.xlsx
and synchronizes with:
  data/consultancies/app_prospects_v1.csv

Tabs created:
1. 'App Prospects Pipeline' - Master consultancy lead sheet (Paul profile) with dropdown approvals, template overrides, and frozen panes.
2. 'Venue Widget Pipeline' - Master cultural venue lead sheet (theatres, museums) with confirmed contacts and project management controls.
3. 'Email Templates & Referrers' - Comprehensive catalogue of direct pitches, info@ referral variations, follow-ups, and widget templates.
4. 'A-B Testing & Funnel Dashboard' - Real-time metrics, variant performance tracker, and conversion funnels for both products.
"""

import sys
import os
import re
from pathlib import Path
import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CSV_PATH = REPO_ROOT / "data" / "consultancies" / "app_prospects_v1.csv"
DOCS_DIR = Path(r"C:\Users\isaac\Documents\endmile")
EXCEL_PATH = DOCS_DIR / "endmile_master_pipeline.xlsx"
ONEDRIVE_DOCS_DIR = Path(r"C:\Users\isaac\OneDrive\Documents\EndMile")
ONEDRIVE_DOCS_PATH = ONEDRIVE_DOCS_DIR / "endmile_master_pipeline.xlsx"
ONEDRIVE_DESKTOP_DIR = Path(r"C:\Users\isaac\OneDrive\Desktop")
ONEDRIVE_DESKTOP_PATH = ONEDRIVE_DESKTOP_DIR / "endmile_master_pipeline.xlsx"
WIDGET_PATH = Path(r"C:\Users\isaac\Downloads\endmile widget v4.xlsx")

# Styling constants
NAVY_HEADER_FILL = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
TEAL_HEADER_FILL = PatternFill(start_color="0F766E", end_color="0F766E", fill_type="solid")
BLUE_HEADER_FILL = PatternFill(start_color="1D4ED8", end_color="1D4ED8", fill_type="solid")
PURPLE_HEADER_FILL = PatternFill(start_color="6D28D9", end_color="6D28D9", fill_type="solid")
GRAY_HEADER_FILL = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
WHITE_BOLD_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
REGULAR_FONT = Font(name="Calibri", size=10)
BOLD_FONT = Font(name="Calibri", size=10, bold=True)
CODE_FONT = Font(name="Consolas", size=9.5)

APPROVED_FILL = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")  # soft green
PENDING_FILL = PatternFill(start_color="FEF9C3", end_color="FEF9C3", fill_type="solid")   # soft yellow
EXCLUDED_FILL = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")  # soft gray
SENT_FILL = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid")      # soft blue

THIN_SIDE = Side(border_style="thin", color="CBD5E1")
CELL_BORDER = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=THIN_SIDE)

def extract_venue_contact_info(raw_text: str) -> tuple[str, str, str]:
    """Extracts (first_name, email, role) from Column 1 (Notes & Contacts)."""
    if not isinstance(raw_text, str) or not raw_text.strip() or raw_text.strip() == "-":
        return "", "", ""

    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', raw_text)
    if not email_match:
        return "", "", ""
    email = email_match.group(0).lower()

    name = ""
    role = ""
    clean_line = raw_text.split(",")[0].replace(email, "").strip(" -:,;")
    
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
    if name and not any(k in name.lower() for k in ["info", "hello", "team", "box office", "admin", "theatre", "museum", "office", "manager"]):
        name_tokens = name.split()
        if name_tokens:
            first_name = name_tokens[0].title()
    elif not name and "." in email.split("@")[0]:
        handle = email.split("@")[0]
        token = handle.split(".")[0]
        if token.isalpha() and len(token) >= 2 and token.lower() not in ["info", "admin", "office", "boxoffice", "contact", "marketing"]:
            first_name = token.title()
    elif not name:
        handle = email.split("@")[0]
        if handle.isalpha() and len(handle) >= 3 and handle.lower() not in ["info", "admin", "office", "boxoffice", "contact", "marketing", "manager"]:
            first_name = handle.title()

    return first_name, email, role

def get_templates_data():
    """Returns the structured list of all email templates, info desk referral variations, and follow-ups."""
    return [
        # APP TEMPLATES (Consultancy Travel Scratchpad & Cost Justification)
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
                "Following up briefly on my earlier note — did you want to take a quick look at the 10-second multimodal scratchpad for {CompanyClean}?\n\n"
                "Happy to run a couple of sample routes for your team if helpful.\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk\n\n"
                "No worries at all if this isn't relevant to your team."
            ),
            "Angle": "Polite Bump (Zero friction preview offer)",
            "WordCount": 55,
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
        # VENUE WIDGET TEMPLATES (B2B Travel Planner Embed)
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
                "Following up briefly on this — I went ahead and mocked up a quick preview of how the planner would look embedded directly on your site:\n"
                "{PreviewUrl}\n\n"
                "Unlike traditional transit software with £2,000+ setup hurdles, EndMile embeds directly onto your website with £0 setup and runs from £19/month on a 14-day free pilot.\n\n"
                "Happy to share the staging preview or test embed for your site if helpful?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk"
            ),
            "Angle": "Zero Dev Friction (£0 setup, £19/mo, live interactive preview link)",
            "WordCount": 65,
            "WhenToUse": "Send 3 business days after initial venue touch if no reply."
        }
    ]

def build_workbook():
    print("=" * 75)
    print(" BUILDING MASTER ENDMILE MULTI-PRODUCT PIPELINE WORKBOOK")
    print("=" * 75)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    if not CSV_PATH.exists():
        print(f"Error: {CSV_PATH} not found.")
        sys.exit(1)

    df_csv = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df_csv)} consultancy records from {CSV_PATH.name}")

    # Ensure required project management columns exist
    if "ManualApproval" not in df_csv.columns:
        df_csv["ManualApproval"] = "Pending Review"
    if "AssignedTemplate" not in df_csv.columns:
        df_csv["AssignedTemplate"] = "AUTO"
    if "FounderNotes" not in df_csv.columns:
        df_csv["FounderNotes"] = ""

    verified_mask = df_csv["EmailStatus"].str.startswith("Verified", na=False)
    uncontacted_mask = df_csv["OutreachStatus"] == "Uncontacted"
    exc_mask = df_csv["LeadFitTier"] == "Exceptional Fit"
    
    excluded_mask = df_csv["CompanyName"].str.contains("DORSET SOFTWARE", case=False, na=False) | \
                    df_csv["OperationalEmail"].str.contains("dorsetsoftware.com", case=False, na=False) | \
                    df_csv["EmailStatus"].str.startswith("Quarantined", na=False)
    
    df_csv.loc[excluded_mask, "ManualApproval"] = "Excluded / No MX"
    
    # Pre-approve top 20 verified exceptional fit leads
    top_20_mask = verified_mask & uncontacted_mask & exc_mask & ~excluded_mask
    top_20_indices = df_csv[top_20_mask].head(20).index
    df_csv.loc[top_20_indices, "ManualApproval"] = "Approved"

    core_front_cols = [
        "LeadID",
        "ManualApproval",
        "AssignedTemplate",
        "FounderNotes",
        "CompanyName",
        "TradeName",
        "ContactName",
        "TargetRole",
        "OperationalEmail",
        "HQCity",
        "SampleTravelCorridor",
        "LeadFitTier",
        "FitScore",
        "OutreachStatus",
        "DateSent",
        "EmailStatus",
        "MailProvider"
    ]
    
    remaining_cols = [c for c in df_csv.columns if c not in core_front_cols]
    final_cols = core_front_cols + remaining_cols
    df_app_prospects = df_csv[final_cols].copy()

    # Save synchronized CSV
    df_app_prospects.to_csv(CSV_PATH, index=False, encoding="utf-8")
    print(f"[OK] Synchronized project management columns in {CSV_PATH.name}")

    # Create OpenPyXL Workbook
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    # -------------------------------------------------------------
    # TAB 1: App Prospects Pipeline (Consultancies)
    # -------------------------------------------------------------
    print("Creating Sheet 1: App Prospects Pipeline...")
    ws_app = wb.create_sheet(title="App Prospects Pipeline")
    ws_app.views.sheetView[0].showGridLines = True

    app_headers = list(df_app_prospects.columns)
    ws_app.append(app_headers)
    for col_num, header in enumerate(app_headers, 1):
        cell = ws_app.cell(row=1, column=col_num)
        cell.font = WHITE_BOLD_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        if header in ["ManualApproval", "AssignedTemplate", "FounderNotes"]:
            cell.fill = TEAL_HEADER_FILL
        elif header in ["LeadID", "CompanyName", "ContactName", "OperationalEmail"]:
            cell.fill = BLUE_HEADER_FILL
        else:
            cell.fill = NAVY_HEADER_FILL
        cell.border = CELL_BORDER

    ws_app.row_dimensions[1].height = 28

    for row_idx, row_data in enumerate(df_app_prospects.itertuples(index=False), 2):
        row_values = ["" if pd.isna(val) else str(val) for val in row_data]
        ws_app.append(row_values)
        
        approval_val = str(row_data.ManualApproval)
        approval_cell = ws_app.cell(row=row_idx, column=app_headers.index("ManualApproval") + 1)
        approval_cell.alignment = Alignment(horizontal="center", vertical="center")
        approval_cell.font = BOLD_FONT
        
        if approval_val == "Approved":
            approval_cell.fill = APPROVED_FILL
        elif approval_val == "Pending Review":
            approval_cell.fill = PENDING_FILL
        elif "Excluded" in approval_val or "No MX" in approval_val:
            approval_cell.fill = EXCLUDED_FILL
        elif approval_val == "Sent":
            approval_cell.fill = SENT_FILL

        template_cell = ws_app.cell(row=row_idx, column=app_headers.index("AssignedTemplate") + 1)
        template_cell.alignment = Alignment(horizontal="center", vertical="center")
        template_cell.font = CODE_FONT

    # Dropdown validation
    app_approval_dv = DataValidation(type="list", formula1='"Approved,Pending Review,Hold,Skip,Sent,Excluded / No MX"', allow_blank=True)
    ws_app.add_data_validation(app_approval_dv)
    app_appr_col = get_column_letter(app_headers.index("ManualApproval") + 1)
    app_approval_dv.add(f"{app_appr_col}2:{app_appr_col}{len(df_app_prospects)+1}")

    app_template_dv = DataValidation(type="list", formula1='"AUTO,DIRECT_SCRATCHPAD,DIRECT_RECHARGE,INFO_REF_A,INFO_REF_B,INFO_REF_C,INFO_REF_D"', allow_blank=True)
    ws_app.add_data_validation(app_template_dv)
    app_tpl_col = get_column_letter(app_headers.index("AssignedTemplate") + 1)
    app_template_dv.add(f"{app_tpl_col}2:{app_tpl_col}{len(df_app_prospects)+1}")

    ws_app.freeze_panes = "E2"
    ws_app.auto_filter.ref = ws_app.dimensions

    app_col_widths = {
        "LeadID": 12, "ManualApproval": 18, "AssignedTemplate": 20, "FounderNotes": 25,
        "CompanyName": 32, "TradeName": 26, "ContactName": 18, "TargetRole": 28,
        "OperationalEmail": 30, "HQCity": 16, "SampleTravelCorridor": 32,
        "LeadFitTier": 16, "FitScore": 10, "OutreachStatus": 15, "DateSent": 13,
        "EmailStatus": 24, "MailProvider": 22, "Sector": 22, "EstimatedHeadcount": 18, "Website": 28
    }
    for col_idx, col_name in enumerate(app_headers, 1):
        letter = get_column_letter(col_idx)
        ws_app.column_dimensions[letter].width = app_col_widths.get(col_name, 18)

    # -------------------------------------------------------------
    # TAB 2: Venue Widget Pipeline (Cultural Venues & Theatres)
    # -------------------------------------------------------------
    print("Creating Sheet 2: Venue Widget Pipeline...")
    ws_venue = wb.create_sheet(title="Venue Widget Pipeline")
    ws_venue.views.sheetView[0].showGridLines = True

    venue_headers = [
        "VenueID",
        "ManualApproval",
        "AssignedTemplate",
        "FounderNotes",
        "VenueName",
        "ConfirmedEmail",
        "ConfirmedName",
        "ConfirmedRole",
        "PublicEmail",
        "Archetype",
        "OwnershipType",
        "WidgetFit",
        "WidgetFitScore",
        "Tier",
        "EstMonthlySearches",
        "OutreachStatus",
        "DateSent",
        "Website",
        "Phone",
        "Address",
        "MultimodalFeatures",
        "DeepLinkGoogleSearch",
        "EndMileGuideUrl",
        "EmailHook",
        "RawNotesAndContacts"
    ]
    ws_venue.append(venue_headers)
    for col_num, h in enumerate(venue_headers, 1):
        cell = ws_venue.cell(row=1, column=col_num)
        cell.font = WHITE_BOLD_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        if h in ["ManualApproval", "AssignedTemplate", "FounderNotes"]:
            cell.fill = TEAL_HEADER_FILL
        elif h in ["VenueID", "VenueName", "ConfirmedEmail", "ConfirmedName"]:
            cell.fill = PURPLE_HEADER_FILL
        else:
            cell.fill = NAVY_HEADER_FILL
        cell.border = CELL_BORDER

    ws_venue.row_dimensions[1].height = 28

    if WIDGET_PATH.exists():
        wb_w = openpyxl.load_workbook(WIDGET_PATH, read_only=True)
        sheet_w = wb_w.active
        w_data = list(sheet_w.iter_rows(values_only=True))
        w_raw_headers = list(w_data[0])

        w_id_idx = w_raw_headers.index("ID")
        w_name_idx = w_raw_headers.index("Name")
        w_arch_idx = w_raw_headers.index("Archetype")
        w_own_idx = w_raw_headers.index("OwnershipType")
        w_fit_idx = w_raw_headers.index("WidgetFit")
        w_score_idx = w_raw_headers.index("WidgetFitScore")
        w_tier_idx = w_raw_headers.index("Tier")
        w_search_idx = w_raw_headers.index("EstMonthlySearches")
        w_web_idx = w_raw_headers.index("Website")
        w_phone_idx = w_raw_headers.index("Phone")
        w_email_idx = w_raw_headers.index("RawEmail")
        w_addr_idx = w_raw_headers.index("Address")
        w_feat_idx = w_raw_headers.index("MultimodalFeatures")
        w_notes_idx = w_raw_headers.index("Column 1 (Notes & Contacts)")
        w_dork_idx = w_raw_headers.index("DeepLinkGoogleSearch")
        w_guide_idx = w_raw_headers.index("EndMileGuideUrl")
        w_hook_idx = w_raw_headers.index("EmailHook")

        venue_rows_count = 0
        approved_venue_count = 0

        for r_idx, r in enumerate(w_data[1:], 2):
            vid = str(r[w_id_idx] or "")
            vname = str(r[w_name_idx] or "")
            raw_notes = str(r[w_notes_idx] or "")
            c_name, c_email, c_role = extract_venue_contact_info(raw_notes)
            public_email = str(r[w_email_idx] or "").strip()
            
            # If founder has confirmed an email in Column 1, pre-approve
            has_confirmed_email = bool(c_email and "@" in c_email)
            approval_val = "Approved" if has_confirmed_email else "Pending Review"
            if has_confirmed_email:
                approved_venue_count += 1

            tpl_val = "AUTO"
            row_vals = [
                vid,
                approval_val,
                tpl_val,
                "",  # FounderNotes
                vname,
                c_email,
                c_name,
                c_role,
                public_email,
                str(r[w_arch_idx] or ""),
                str(r[w_own_idx] or ""),
                str(r[w_fit_idx] or ""),
                str(r[w_score_idx] or ""),
                str(r[w_tier_idx] or ""),
                str(r[w_search_idx] or ""),
                "Uncontacted",
                "",  # DateSent
                str(r[w_web_idx] or ""),
                str(r[w_phone_idx] or ""),
                str(r[w_addr_idx] or ""),
                str(r[w_feat_idx] or ""),
                str(r[w_dork_idx] or ""),
                str(r[w_guide_idx] or ""),
                str(r[w_hook_idx] or ""),
                raw_notes
            ]
            ws_venue.append(row_vals)
            venue_rows_count += 1

            # Style approval cell
            c_appr = ws_venue.cell(row=r_idx, column=2)
            c_appr.alignment = Alignment(horizontal="center", vertical="center")
            c_appr.font = BOLD_FONT
            if approval_val == "Approved":
                c_appr.fill = APPROVED_FILL
            else:
                c_appr.fill = PENDING_FILL

            c_tpl = ws_venue.cell(row=r_idx, column=3)
            c_tpl.alignment = Alignment(horizontal="center", vertical="center")
            c_tpl.font = CODE_FONT

        # Add validations
        v_appr_dv = DataValidation(type="list", formula1='"Approved,Pending Review,Hold,Skip,Sent"', allow_blank=True)
        ws_venue.add_data_validation(v_appr_dv)
        v_appr_dv.add(f"B2:B{venue_rows_count+1}")

        v_tpl_dv = DataValidation(type="list", formula1='"AUTO,VENUE_VISIT_A,GIG_CURFEW_A,MUSEUM_PLANNER_A,HERITAGE_RURAL_B,ATTRACT_FAMILY_A,THEATRE_SCOPE3_A,VENUE_INFO_REFERRAL,VENUE_FOLLOWUP_PREVIEW"', allow_blank=True)
        ws_venue.add_data_validation(v_tpl_dv)
        v_tpl_dv.add(f"C2:C{venue_rows_count+1}")

        ws_venue.freeze_panes = "E2"
        ws_venue.auto_filter.ref = ws_venue.dimensions

        venue_col_widths = {
            "VenueID": 14, "ManualApproval": 18, "AssignedTemplate": 26, "FounderNotes": 25,
            "VenueName": 32, "ConfirmedEmail": 30, "ConfirmedName": 18, "ConfirmedRole": 24,
            "PublicEmail": 28, "Archetype": 28, "OwnershipType": 24, "WidgetFit": 16,
            "WidgetFitScore": 14, "Tier": 18, "EstMonthlySearches": 18, "OutreachStatus": 15,
            "DateSent": 13, "Website": 28, "Phone": 18
        }
        for col_idx, col_name in enumerate(venue_headers, 1):
            letter = get_column_letter(col_idx)
            ws_venue.column_dimensions[letter].width = venue_col_widths.get(col_name, 20)

        print(f"[OK] Added {venue_rows_count} venues ({approved_venue_count} pre-approved from founder notes).")

    # -------------------------------------------------------------
    # TAB 3: Email Templates & Referrers (Both Products)
    # -------------------------------------------------------------
    print("Creating Sheet 3: Email Templates & Referrers...")
    ws_templates = wb.create_sheet(title="Email Templates & Referrers")
    ws_templates.views.sheetView[0].showGridLines = True

    tpl_headers = [
        "Product",
        "Template Code",
        "Template Name",
        "Target Recipient / Inbox",
        "Subject Line",
        "Email Body (Plain Text with Variables)",
        "Hook / Value Prop Angle",
        "Word Count",
        "When to Use / Guidance"
    ]
    ws_templates.append(tpl_headers)
    for col_num, h in enumerate(tpl_headers, 1):
        c = ws_templates.cell(row=1, column=col_num)
        c.fill = BLUE_HEADER_FILL
        c.font = WHITE_BOLD_FONT
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = CELL_BORDER

    ws_templates.row_dimensions[1].height = 28

    templates_list = get_templates_data()
    for row_idx, t in enumerate(templates_list, 2):
        ws_templates.append([
            t["Product"],
            t["TemplateCode"],
            t["TemplateName"],
            t["TargetInbox"],
            t["Subject"],
            t["Body"],
            t["Angle"],
            t["WordCount"],
            t["WhenToUse"]
        ])
        
        # Product tag
        c_prod = ws_templates.cell(row=row_idx, column=1)
        c_prod.font = BOLD_FONT
        c_prod.alignment = Alignment(horizontal="center", vertical="top")

        c_code = ws_templates.cell(row=row_idx, column=2)
        c_code.font = Font(name="Consolas", size=10, bold=True, color="1E3A8A")
        c_code.alignment = Alignment(horizontal="center", vertical="top")
        
        c_name = ws_templates.cell(row=row_idx, column=3)
        c_name.font = BOLD_FONT
        c_name.alignment = Alignment(vertical="top")

        c_tgt = ws_templates.cell(row=row_idx, column=4)
        c_tgt.alignment = Alignment(vertical="top", wrap_text=True)

        c_subj = ws_templates.cell(row=row_idx, column=5)
        c_subj.font = Font(name="Consolas", size=10, bold=True)
        c_subj.alignment = Alignment(vertical="top")

        c_body = ws_templates.cell(row=row_idx, column=6)
        c_body.font = CODE_FONT
        c_body.alignment = Alignment(vertical="top", wrap_text=True)

        c_angle = ws_templates.cell(row=row_idx, column=7)
        c_angle.alignment = Alignment(vertical="top", wrap_text=True)

        c_wc = ws_templates.cell(row=row_idx, column=8)
        c_wc.alignment = Alignment(horizontal="center", vertical="top")

        c_guide = ws_templates.cell(row=row_idx, column=9)
        c_guide.alignment = Alignment(vertical="top", wrap_text=True)

        ws_templates.row_dimensions[row_idx].height = 145

    ws_templates.column_dimensions["A"].width = 22
    ws_templates.column_dimensions["B"].width = 24
    ws_templates.column_dimensions["C"].width = 28
    ws_templates.column_dimensions["D"].width = 30
    ws_templates.column_dimensions["E"].width = 28
    ws_templates.column_dimensions["F"].width = 65
    ws_templates.column_dimensions["G"].width = 32
    ws_templates.column_dimensions["H"].width = 12
    ws_templates.column_dimensions["I"].width = 36
    ws_templates.freeze_panes = "A2"

    # -------------------------------------------------------------
    # TAB 4: A-B Testing & Funnel Dashboard (Unified Executive View)
    # -------------------------------------------------------------
    print("Creating Sheet 4: A-B Testing & Funnel Dashboard...")
    ws_dash = wb.create_sheet(title="A-B Testing & Dashboard")
    ws_dash.views.sheetView[0].showGridLines = True

    # Title Banner
    ws_dash.merge_cells("A1:G1")
    title_cell = ws_dash["A1"]
    title_cell.value = "ENDMILE EXECUTIVE COMMERCIAL PIPELINE & A/B EXPERIMENTATION DASHBOARD"
    title_cell.font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    title_cell.fill = NAVY_HEADER_FILL
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws_dash.row_dimensions[1].height = 35

    # Section 1: App Funnel
    ws_dash.cell(row=3, column=1, value="PRODUCT 1: CONSULTANCY TRAVEL APP ('PAUL HARDY' ICP)").font = Font(size=11, bold=True, color="1E3A8A")
    for c in range(1, 5):
        cell = ws_dash.cell(row=4, column=c)
        cell.fill = BLUE_HEADER_FILL
        cell.font = WHITE_BOLD_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = CELL_BORDER

    ws_dash.cell(row=4, column=1, value="Funnel Stage")
    ws_dash.cell(row=4, column=2, value="Current Value")
    ws_dash.cell(row=4, column=3, value="Target / Benchmark")
    ws_dash.cell(row=4, column=4, value="Conversion Strategy & Architecture")

    app_verified_count = int(verified_mask.sum())
    app_approved_count = int((df_csv["ManualApproval"] == "Approved").sum())
    app_sent_count = int((df_csv["OutreachStatus"] == "Sent").sum())

    app_funnel = [
        ("Total Leads in Sourcing Registry", len(df_csv), "1,500–3,000", "Companies House API + 32 High-Travel Consulting Niches"),
        ("Verified Active Zero-Bounce Leads (Live MX)", app_verified_count, "1,500+", "100% verified mail exchange (Microsoft 365, Google Workspace, Mimecast)"),
        ("Manually Approved for Outbound", app_approved_count, "5–20 / day", "Founder checked in tab 'App Prospects Pipeline'"),
        ("Total Emails Dispatched (Sent)", app_sent_count, "250 / month", "Sent via send_app_outreach.py (10–20 min intervals, Mon-Fri 08:30-17:30 UK)"),
        ("Direct & Referral Replies Received", 0, "25 / month (10%)", "Captured from isaacw@endmilerouting.co.uk inbox"),
        ("Discovery / Sandbox Walkthroughs", 0, "8 / month (30% of replies)", "Demonstrating 10-second multimodal pre-trip scratchpad"),
        ("Closed Paying SaaS Accounts (£29–£49/mo)", 0, "2–4 / month", "Target: First 10 paying customers (£290–£490 MRR)")
    ]

    for r_idx, (m_label, m_val, m_tgt, m_notes) in enumerate(app_funnel, 5):
        c1 = ws_dash.cell(row=r_idx, column=1, value=m_label)
        c2 = ws_dash.cell(row=r_idx, column=2, value=m_val)
        c3 = ws_dash.cell(row=r_idx, column=3, value=m_tgt)
        c4 = ws_dash.cell(row=r_idx, column=4, value=m_notes)
        c1.font = BOLD_FONT
        c2.alignment = Alignment(horizontal="center")
        c3.alignment = Alignment(horizontal="center")
        for cell in [c1, c2, c3, c4]:
            cell.border = CELL_BORDER

    # Section 2: Venue Widget Funnel
    start_venue_funnel = 14
    ws_dash.cell(row=start_venue_funnel - 1, column=1, value="PRODUCT 2: B2B VENUE TRAVEL WIDGET (THEATRES & CULTURAL VENUES)").font = Font(size=11, bold=True, color="6D28D9")
    for c in range(1, 5):
        cell = ws_dash.cell(row=start_venue_funnel, column=c)
        cell.fill = PURPLE_HEADER_FILL
        cell.font = WHITE_BOLD_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = CELL_BORDER

    ws_dash.cell(row=start_venue_funnel, column=1, value="Funnel Stage")
    ws_dash.cell(row=start_venue_funnel, column=2, value="Current Value")
    ws_dash.cell(row=start_venue_funnel, column=3, value="Target / Benchmark")
    ws_dash.cell(row=start_venue_funnel, column=4, value="Conversion Strategy & Architecture")

    venue_funnel = [
        ("Total Unserved UK Cultural Venues", 4992, "4,992", "Independent Regional Theatres, Arts Centres & Civic Museums"),
        ("Founder Confirmed Direct Contacts", 59, "100+", "Manually confirmed in Column 1 (General Managers, Box Office, Ops)"),
        ("Manually Approved for Outbound", 59, "5–10 / day", "Founder checked in tab 'Venue Widget Pipeline'"),
        ("Total Widget Emails Dispatched", 0, "150 / month", "Sent via send_venue_outreach.py with live interactive preview link"),
        ("Venue Replies Received", 0, "15 / month (10%)", "Captured from isaacw@endmilerouting.co.uk"),
        ("Staging Test Embeds / Sandboxes", 0, "5 / month", "1-line embed script on staging/visit page"),
        ("Live Paying Embed Subscriptions (£19–£49/mo)", 0, "2–4 / month", "Target: £19–£49/mo SaaS gross margin >95%")
    ]

    for r_idx, (m_label, m_val, m_tgt, m_notes) in enumerate(venue_funnel, start_venue_funnel + 1):
        c1 = ws_dash.cell(row=r_idx, column=1, value=m_label)
        c2 = ws_dash.cell(row=r_idx, column=2, value=m_val)
        c3 = ws_dash.cell(row=r_idx, column=3, value=m_tgt)
        c4 = ws_dash.cell(row=r_idx, column=4, value=m_notes)
        c1.font = BOLD_FONT
        c2.alignment = Alignment(horizontal="center")
        c3.alignment = Alignment(horizontal="center")
        for cell in [c1, c2, c3, c4]:
            cell.border = CELL_BORDER

    # Section 3: A/B Testing Matrix (App Variants)
    start_ab = 24
    ws_dash.cell(row=start_ab - 1, column=1, value="A/B EXPERIMENTATION MATRIX (APP HOOKS & TEMPLATES)").font = Font(size=11, bold=True, color="0F766E")
    ws_dash.cell(row=start_ab, column=1, value="Variant Code").font = WHITE_BOLD_FONT
    ws_dash.cell(row=start_ab, column=2, value="Angle / Psychology").font = WHITE_BOLD_FONT
    ws_dash.cell(row=start_ab, column=3, value="Target Inbox").font = WHITE_BOLD_FONT
    ws_dash.cell(row=start_ab, column=4, value="Sent").font = WHITE_BOLD_FONT
    ws_dash.cell(row=start_ab, column=5, value="Replies").font = WHITE_BOLD_FONT
    ws_dash.cell(row=start_ab, column=6, value="Reply %").font = WHITE_BOLD_FONT
    ws_dash.cell(row=start_ab, column=7, value="Forwards / Referrals").font = WHITE_BOLD_FONT

    for c in range(1, 8):
        cell = ws_dash.cell(row=start_ab, column=c)
        cell.fill = TEAL_HEADER_FILL
        cell.font = WHITE_BOLD_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = CELL_BORDER

    ab_variants = [
        ("INFO_REF_A", "Founder Discovery Ask (38 words)", "info@, hello@ triage", 0, 0, "0.0%", 0),
        ("INFO_REF_B", "Multi-Tab Time Saver (50 words)", "info@, hello@ triage", 0, 0, "0.0%", 0),
        ("INFO_REF_C", "55p Mileage Dispute (45 words)", "info@, hello@ triage", 0, 0, "0.0%", 0),
        ("INFO_REF_D", "Gatekeeper Referral (28 words)", "info@, hello@ triage", 0, 0, "0.0%", 0),
        ("DIRECT_SCRATCHPAD", "10-Min Travel Juggling (85 words)", "Direct Ops / Named Staff", 0, 0, "0.0%", 0),
        ("DIRECT_RECHARGE", "Invoice Dispute & Recharges (95 words)", "Finance / Commercial Leads", 0, 0, "0.0%", 0),
        ("VENUE_DWELL_TIME", "Pre-Show Arrival & Bar Spend (95w)", "Venue General Managers / Ops", 0, 0, "0.0%", 0),
        ("VENUE_SCOPE3_GREENBOOK", "Julie's Bicycle Scope 3 CO2 (105w)", "Venue Sustainability Leads", 0, 0, "0.0%", 0),
    ]

    for r_idx, (v_code, v_desc, v_inbox, v_sent, v_rep, v_rate, v_fwd) in enumerate(ab_variants, start_ab + 1):
        c1 = ws_dash.cell(row=r_idx, column=1, value=v_code)
        c2 = ws_dash.cell(row=r_idx, column=2, value=v_desc)
        c3 = ws_dash.cell(row=r_idx, column=3, value=v_inbox)
        c4 = ws_dash.cell(row=r_idx, column=4, value=v_sent)
        c5 = ws_dash.cell(row=r_idx, column=5, value=v_rep)
        c6 = ws_dash.cell(row=r_idx, column=6, value=v_rate)
        c7 = ws_dash.cell(row=r_idx, column=7, value=v_fwd)
        
        c1.font = CODE_FONT
        c4.alignment = Alignment(horizontal="center")
        c5.alignment = Alignment(horizontal="center")
        c6.alignment = Alignment(horizontal="center")
        c7.alignment = Alignment(horizontal="center")
        for cell in [c1, c2, c3, c4, c5, c6, c7]:
            cell.border = CELL_BORDER

    ws_dash.column_dimensions["A"].width = 34
    ws_dash.column_dimensions["B"].width = 36
    ws_dash.column_dimensions["C"].width = 28
    ws_dash.column_dimensions["D"].width = 12
    ws_dash.column_dimensions["E"].width = 12
    ws_dash.column_dimensions["F"].width = 12
    ws_dash.column_dimensions["G"].width = 24

    # Save to C:\Users\isaac\Documents\endmile\endmile_master_pipeline.xlsx and sync
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    ONEDRIVE_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    ONEDRIVE_DESKTOP_DIR.mkdir(parents=True, exist_ok=True)

    wb.save(EXCEL_PATH)
    print(f"\n[SUCCESS] Successfully saved Master Multi-Product Workbook to:\n  {EXCEL_PATH}")

    import shutil
    shutil.copy2(EXCEL_PATH, ONEDRIVE_DOCS_PATH)
    print(f"[SYNC] Copied to OneDrive Documents: {ONEDRIVE_DOCS_PATH}")
    shutil.copy2(EXCEL_PATH, ONEDRIVE_DESKTOP_PATH)
    print(f"[SYNC] Copied to Desktop: {ONEDRIVE_DESKTOP_PATH}")
    print(f"Total sheets: {wb.sheetnames}")

if __name__ == "__main__":
    build_workbook()
