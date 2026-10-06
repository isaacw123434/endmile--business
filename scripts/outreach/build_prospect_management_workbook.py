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
        # APP TEMPLATES
        {
            "Product": "Consultancy App",
            "TemplateCode": "DIRECT_SCRATCHPAD",
            "TemplateName": "Direct Operations Scratchpad Pitch",
            "TargetInbox": "Direct Operations & Discovered Named Contacts (operations@, projects@, travel@, named lead)",
            "Subject": "{Company}'s travel planning",
            "Body": (
                "Hi {ContactName},\n\n"
                "When your consultants head out to client sites (like {TravelCorridor}), does someone on operations still spend 10 minutes juggling Google Maps, Trainline, and station parking to find the fastest and cheapest door-to-door route?\n\n"
                "I built EndMile (https://endmilerouting.co.uk) as a quick scratchpad for UK consultancies. It stacks up driving (at HMRC 55p/mile) against train fares, station parking, and destination taxis side-by-side in 10 seconds.\n\n"
                "Happy to send over a 30-second preview of how it works for {HQCity} corridors if helpful?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk | https://endmilerouting.co.uk\n\n"
                "PS: If you'd rather not hear about UK travel planning, reply 'unsubscribe' and I'll remove you immediately."
            ),
            "Angle": "Multi-Tab Friction (10-minute booking headache vs 10-second multimodal scratchpad)",
            "WordCount": 85,
            "WhenToUse": "Use when reaching named practice leads, travel coordinators, or specific operations/delivery inboxes."
        },
        {
            "Product": "Consultancy App",
            "TemplateCode": "DIRECT_RECHARGE",
            "TemplateName": "Direct Project Recharges & Margin Defense",
            "TargetInbox": "Finance, Commercial Leads, Project Directors (finance@, commercial@, projects@)",
            "Subject": "client travel recharges",
            "Body": (
                "Hi {ContactName},\n\n"
                "When {Company}'s consultants travel to client sites, do your finance or project leads ever run into pushback from client accounts payable over HMRC 55p mileage or taxi expenses?\n\n"
                "We've found many UK consultancies lose 1–5% of travel recharges simply because clients look up a superficial £50 train ticket and dispute a £110 car journey, ignoring station parking and taxi legs.\n\n"
                "We built EndMile (https://endmilerouting.co.uk) to calculate the true door-to-door comparison before consultants travel, generating a 1-page Pre-Trip Cost Justification PDF to attach directly to client invoices.\n\n"
                "Would it be helpful to see a sample justification report for {HQCity} routes?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk | https://endmilerouting.co.uk\n\n"
                "PS: If you'd rather not hear about UK travel planning, reply 'unsubscribe' and I'll remove you immediately."
            ),
            "Angle": "Client Invoice Dispute Defense (Defending 55p mileage claims against accounts payable pushback)",
            "WordCount": 95,
            "WhenToUse": "Use when targeting cost consultants, project managers, or finance contacts managing client recharges."
        },
        {
            "Product": "Consultancy App",
            "TemplateCode": "INFO_REF_A",
            "TemplateName": "Info Desk Referral A (Founder Discovery Ask)",
            "TargetInbox": "General Front-Desk / Triage Inboxes (info@, hello@, enquiries@, contact@)",
            "Subject": "quick question - travel coordination",
            "Body": (
                "Hi team,\n\n"
                "Could you point me to whoever looks after consultant travel or expenses at {Company}?\n\n"
                "I'm an independent UK software engineer building a tool to cut down the time consultancies spend planning client travel and comparing HMRC 55p mileage. Just wanted to ask them 2 quick questions about how they currently handle it.\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk | https://endmilerouting.co.uk\n\n"
                "PS: If you'd rather not hear about UK travel planning, reply 'unsubscribe' and I'll remove you immediately."
            ),
            "Angle": "Pre-Revenue Founder Discovery Ask (Authentic engineer persona asking 2 quick questions)",
            "WordCount": 38,
            "WhenToUse": "Default A/B test variant. Extremely disarming; gatekeepers forward directly to Ops."
        },
        {
            "Product": "Consultancy App",
            "TemplateCode": "INFO_REF_B",
            "TemplateName": "Info Desk Referral B (Multi-Tab Time Saver)",
            "TargetInbox": "General Front-Desk / Triage Inboxes (info@, hello@, enquiries@, contact@)",
            "Subject": "{Company}'s travel planning",
            "Body": (
                "Hi there,\n\n"
                "Quick question — who at {Company} coordinates travel when consultants head out to client sites (like {TravelCorridor})?\n\n"
                "I put together a simple tool (https://endmilerouting.co.uk) that works out driving mileage against train fares, parking, and taxis in 10 seconds, instead of jumping between 3 tabs.\n\n"
                "Worth passing this over to whoever handles travel for your team?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk | https://endmilerouting.co.uk\n\n"
                "PS: If you'd rather not hear about UK travel planning, reply 'unsubscribe' and I'll remove you immediately."
            ),
            "Angle": "Operational Time Saver (Helps receptionist pass a tangible utility to the travel planner)",
            "WordCount": 50,
            "WhenToUse": "Best for firms where regional office travel corridor is known."
        },
        {
            "Product": "Consultancy App",
            "TemplateCode": "INFO_REF_C",
            "TemplateName": "Info Desk Referral C (55p Mileage Dispute)",
            "TargetInbox": "General Front-Desk / Triage Inboxes (info@, hello@, enquiries@, contact@)",
            "Subject": "consultant travel expenses",
            "Body": (
                "Hi team,\n\n"
                "Could you point me to whoever manages travel expenses or project recharges at {Company}?\n\n"
                "I put together a simple tool for UK consultancies to help back up HMRC 55p mileage against rail costs when clients question travel invoices.\n\n"
                "Who would be best to speak with about that?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk | https://endmilerouting.co.uk\n\n"
                "PS: If you'd rather not hear about UK travel planning, reply 'unsubscribe' and I'll remove you immediately."
            ),
            "Angle": "Commercial Expense Routing (Routes to Accounts/Finance or Practice Lead)",
            "WordCount": 45,
            "WhenToUse": "Great for quantity surveyors, engineering practices, and advisory firms with heavy billing."
        },
        {
            "Product": "Consultancy App",
            "TemplateCode": "INFO_REF_D",
            "TemplateName": "Info Desk Referral D (Ultra-Short Gatekeeper Forward)",
            "TargetInbox": "General Front-Desk / Triage Inboxes (info@, hello@, enquiries@, contact@)",
            "Subject": "quick referral - operations / travel",
            "Body": (
                "Hi team,\n\n"
                "Could you point me in the right direction? Who at {Company} coordinates travel planning or expenses for consultants travelling to client sites?\n\n"
                "Thanks so much,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk | https://endmilerouting.co.uk\n\n"
                "PS: If you'd rather not hear about UK travel planning, reply 'unsubscribe' and I'll remove you immediately."
            ),
            "Angle": "Frictionless Forward Request (Zero pitch, pure routing request)",
            "WordCount": 28,
            "WhenToUse": "High-volume reception inboxes where lengthy messages get instantly archived."
        },
        {
            "Product": "Consultancy App",
            "TemplateCode": "FOLLOWUP_DIRECT_1",
            "TemplateName": "Direct Follow-Up (+3 to 4 Days)",
            "TargetInbox": "Direct Operations & Named Contacts",
            "Subject": "re: {Company}'s travel planning",
            "Body": (
                "Hi {ContactName},\n\n"
                "Just following up on this — know you're busy coordinating client dispatches.\n\n"
                "We set up a quick 1-click test link with {HQCity} corridors pre-configured: https://endmilerouting.co.uk\n\n"
                "No login or download needed — feel free to test your team's next client route and see if it cuts your planning time down from 15 minutes to 30 seconds.\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk | https://endmilerouting.co.uk"
            ),
            "Angle": "Zero-Friction Sandbox Link (No sign-up, instant gratification)",
            "WordCount": 55,
            "WhenToUse": "Send 3-4 days after DIRECT_SCRATCHPAD if no response."
        },
        {
            "Product": "Consultancy App",
            "TemplateCode": "FOLLOWUP_INFO_1",
            "TemplateName": "Info Desk Referral Follow-Up (+4 Days)",
            "TargetInbox": "General Front-Desk / Triage Inboxes (info@, hello@)",
            "Subject": "re: quick question - travel coordination",
            "Body": (
                "Hi team,\n\n"
                "Following up briefly on this — did you know who would be the best person to speak with regarding consultant travel or operations at {Company}?\n\n"
                "Much appreciated,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk | https://endmilerouting.co.uk"
            ),
            "Angle": "Polite Nudge (Ensures email didn't get buried in morning reception rush)",
            "WordCount": 32,
            "WhenToUse": "Send 4 business days after INFO_REF_A/B/C/D if no reply."
        },
        # VENUE WIDGET TEMPLATES
        {
            "Product": "Venue Travel Widget",
            "TemplateCode": "VENUE_DWELL_TIME",
            "TemplateName": "Venue Pre-Show Arrival & Dwell Time",
            "TargetInbox": "General Managers, Commercial Directors, Operations Leads",
            "Subject": "{VenueName}'s visitor arrivals",
            "Body": (
                "Hi {ContactName},\n\n"
                "When ticket holders head to {VenueName}, do you ever find that last-mile driving traffic and city centre parking searches leave audiences rushing through the doors right at the 2-minute bell?\n\n"
                "Beyond auditorium disruptions, when guests arrive flustered they skip the bar, programmes, and catering—which is where venues protect their operating margins.\n\n"
                "We built EndMile (https://endmilerouting.co.uk/venue-widget) as a 1-line travel planner that embeds directly on your visit page. It compares door-to-door rail against driving and verified parking tariffs in 10 seconds, encouraging visitors to plan ahead and arrive 30–45 minutes earlier.\n\n"
                "Would it be helpful to see a 30-second preview of how it looks on {VenueName}'s website?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk | https://endmilerouting.co.uk\n\n"
                "PS: If you'd rather not hear about UK venue travel, reply 'unsubscribe' and I'll remove you immediately."
            ),
            "Angle": "Protecting Bar & Concession Margins via Pre-Show Arrival Planning",
            "WordCount": 95,
            "WhenToUse": "Primary pitch for theatres, concert halls, and independent arts centres."
        },
        {
            "Product": "Venue Travel Widget",
            "TemplateCode": "VENUE_SCOPE3_GREENBOOK",
            "TemplateName": "Venue Carbon Reporting (Julie's Bicycle & Green Book)",
            "TargetInbox": "Executive Directors, Sustainability Leads, Civic Venue Ops",
            "Subject": "audience travel reporting",
            "Body": (
                "Hi {ContactName},\n\n"
                "For {VenueName}'s environmental reporting (such as Julie's Bicycle or the Theatre Green Book), how does your team currently measure audience travel emissions?\n\n"
                "Audience travel typically represents over 80% of a cultural venue's carbon footprint, but most venues have to rely on post-show email surveys with 3–4% response rates and rough estimations.\n\n"
                "We built EndMile (https://endmilerouting.co.uk/venue-widget) to automate this. It embeds as a 1-line journey planner on your visit page, giving visitors live rail, bus, and parking options while generating verified DEFRA Scope 3 carbon telemetry directly from actual journey searches.\n\n"
                "Would you be open to seeing a sample travel carbon export for {VenueName}?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk | https://endmilerouting.co.uk\n\n"
                "PS: If you'd rather not hear about UK venue travel, reply 'unsubscribe' and I'll remove you immediately."
            ),
            "Angle": "Automating Arts Council Julie's Bicycle Scope 3 Carbon Reporting",
            "WordCount": 105,
            "WhenToUse": "NPO theatres, civic museums, and heritage venues with grant reporting."
        },
        {
            "Product": "Venue Travel Widget",
            "TemplateCode": "VENUE_INFO_REFERRAL",
            "TemplateName": "Venue Front-Desk Referral Inquiry",
            "TargetInbox": "Box Office & Front Desk (info@, hello@, boxoffice@)",
            "Subject": "quick question - visitor travel",
            "Body": (
                "Hi team,\n\n"
                "Could you point me to whoever looks after visitor operations, guest experience, or sustainability at {VenueName}?\n\n"
                "I'm an independent UK software engineer building an embeddable journey planner to help UK venues improve pre-show arrival dwell times and automate audience travel carbon reporting. Just wanted to ask them 2 quick questions about how they currently handle arrival planning.\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk | https://endmilerouting.co.uk\n\n"
                "PS: If you'd rather not hear about UK venue travel, reply 'unsubscribe' and I'll remove you immediately."
            ),
            "Angle": "Disarming Engineer Referral Ask to Box Office / Gatekeeper",
            "WordCount": 48,
            "WhenToUse": "Default when targeting info@, hello@, or boxoffice@ inboxes."
        },
        {
            "Product": "Venue Travel Widget",
            "TemplateCode": "VENUE_FOLLOWUP_PREVIEW",
            "TemplateName": "Venue Interactive Preview Follow-Up (+3 Days)",
            "TargetInbox": "General Managers, Ops Directors, Box Office Leads",
            "Subject": "re: {VenueName}'s visitor arrivals",
            "Body": (
                "Hi {ContactName},\n\n"
                "Following up briefly on this — I went ahead and mocked up a quick interactive preview of how the planner would look embedded directly on your site:\n"
                "{PreviewUrl}\n\n"
                "Unlike traditional transit consultancy software (which usually carries £2,000+ setup fees), EndMile embeds via a single script tag with £0 setup and runs for £19/mo on a 14-day free pilot.\n\n"
                "Happy to send over the test snippet for your staging site if helpful?\n\n"
                "Best,\n"
                "Isaac\n"
                "Founder, EndMile\n"
                "isaacw@endmilerouting.co.uk | https://endmilerouting.co.uk"
            ),
            "Angle": "Zero Dev Friction (£0 setup, £19/mo, live interactive preview link)",
            "WordCount": 65,
            "WhenToUse": "Send 3 business days after initial venue touch."
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

        v_tpl_dv = DataValidation(type="list", formula1='"AUTO,VENUE_DWELL_TIME,VENUE_SCOPE3_GREENBOOK,VENUE_VISITOR_JOURNEY,VENUE_INFO_REFERRAL,VENUE_FOLLOWUP_PREVIEW"', allow_blank=True)
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

    # Save to C:\Users\isaac\Documents\endmile\endmile_master_pipeline.xlsx
    wb.save(EXCEL_PATH)
    print(f"\n[SUCCESS] Successfully saved Master Multi-Product Workbook to:\n  {EXCEL_PATH}")
    print(f"Total sheets: {wb.sheetnames}")

if __name__ == "__main__":
    build_workbook()
