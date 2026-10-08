#!/usr/bin/env python3
"""
Update Master Pipeline Excel Workbook with Refined Email Templates and Validations
----------------------------------------------------------------------------------
1. Updates Sheet 3 ('Email Templates & Referrers') with refined, approved B2B copy.
2. Updates DataValidation on Sheet 2 ('Venue Widget Pipeline') column C.
3. Synchronizes the workbook across:
   - C:\\Users\\isaac\\OneDrive\\Documents\\EndMile\\endmile_master_pipeline.xlsx (Windows File Explorer default)
   - C:\\Users\\isaac\\OneDrive\\Desktop\\endmile_master_pipeline.xlsx (Desktop direct access)
   - C:\\Users\\isaac\\Documents\\endmile\\endmile_master_pipeline.xlsx (Local fallback)
"""

import os
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

# Formatting constants
NAVY_HEADER_FILL = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
TEAL_HEADER_FILL = PatternFill(start_color="0F766E", end_color="0F766E", fill_type="solid")
BLUE_HEADER_FILL = PatternFill(start_color="1D4ED8", end_color="1D4ED8", fill_type="solid")
WHITE_BOLD_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
REGULAR_FONT = Font(name="Calibri", size=10)
BOLD_FONT = Font(name="Calibri", size=10, bold=True)
CODE_FONT = Font(name="Consolas", size=9.5)

THIN_SIDE = Side(border_style="thin", color="CBD5E1")
CELL_BORDER = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=THIN_SIDE)

def update_workbook():
    source_path = LOCAL_PATH if LOCAL_PATH.exists() else ONEDRIVE_DOCS_PATH
    if not source_path.exists():
        print(f"[ERROR] Source workbook not found at {source_path}")
        return

    print(f"[LOAD] Loading master workbook from {source_path}...")
    wb = openpyxl.load_workbook(source_path)

    # 1. Update Sheet 3: Email Templates & Referrers
    if "Email Templates & Referrers" in wb.sheetnames:
        ws_templates = wb["Email Templates & Referrers"]
    else:
        ws_templates = wb.create_sheet(title="Email Templates & Referrers")

    # Consultancy Templates (Standardized, time-aware, zero raw links in Touch 1, natural sign-off)
    consultancy_templates = [
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
            "WhenToUse": "Direct outreach to operations leads, project coordinators, or directors."
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
        }
    ]

    # Venue Widget Templates (Approved refined copy)
    venue_templates = [
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

    all_templates = consultancy_templates + venue_templates

    # Clear existing rows in Sheet 3 below row 1
    max_r = ws_templates.max_row
    if max_r > 1:
        ws_templates.delete_rows(2, max_r)

    # Re-populate Sheet 3
    for row_idx, tpl in enumerate(all_templates, 2):
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
        ws_templates.append(row_vals)

        # Style cells
        for c_idx in range(1, 10):
            cell = ws_templates.cell(row=row_idx, column=c_idx)
            cell.border = CELL_BORDER
            cell.font = REGULAR_FONT

        c_prod = ws_templates.cell(row=row_idx, column=1)
        c_prod.font = BOLD_FONT
        c_prod.alignment = Alignment(horizontal="center", vertical="top")

        c_code = ws_templates.cell(row=row_idx, column=2)
        c_code.font = Font(name="Consolas", size=10, bold=True)
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

    print(f"[OK] Sheet 3 updated with {len(all_templates)} templates.")

    # 2. Update DataValidation on Sheet 2: Venue Widget Pipeline
    if "Venue Widget Pipeline" in wb.sheetnames:
        ws_venue = wb["Venue Widget Pipeline"]
        v_rows = ws_venue.max_row
        venue_tpl_list = "AUTO,VENUE_VISIT_A,GIG_CURFEW_A,MUSEUM_PLANNER_A,HERITAGE_RURAL_B,ATTRACT_FAMILY_A,THEATRE_SCOPE3_A,VENUE_INFO_REFERRAL,VENUE_FOLLOWUP_PREVIEW"
        
        # Replace or add template validation
        new_v_tpl_dv = DataValidation(type="list", formula1=f'"{venue_tpl_list}"', allow_blank=True)
        
        # Remove old C column validation if present
        dvs_to_keep = []
        for dv in ws_venue.data_validations.dataValidation:
            # Check if this validation covers column C
            sqref_str = str(dv.sqref)
            if "C2:" in sqref_str or "C" in sqref_str:
                pass # discard old C validation
            else:
                dvs_to_keep.append(dv)
        ws_venue.data_validations.dataValidation = dvs_to_keep
        ws_venue.add_data_validation(new_v_tpl_dv)
        new_v_tpl_dv.add(f"C2:C{v_rows}")
        print(f"[OK] Sheet 2 DataValidation updated for {v_rows} venue rows.")

    # 3. Save to primary locations
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    ONEDRIVE_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    ONEDRIVE_DESKTOP_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[SAVE] Saving to {LOCAL_PATH}...")
    wb.save(LOCAL_PATH)

    print(f"[SYNC] Copying to OneDrive Documents: {ONEDRIVE_DOCS_PATH}...")
    shutil.copy2(LOCAL_PATH, ONEDRIVE_DOCS_PATH)

    print(f"[SYNC] Copying to Desktop: {ONEDRIVE_DESKTOP_PATH}...")
    shutil.copy2(LOCAL_PATH, ONEDRIVE_DESKTOP_PATH)

    print("=" * 70)
    print("ALL SYNCS COMPLETED SUCCESSFULLY:")
    print(f"  1. OneDrive Documents (File Explorer default): {ONEDRIVE_DOCS_PATH}")
    print(f"  2. Desktop: {ONEDRIVE_DESKTOP_PATH}")
    print(f"  3. Local Documents fallback: {LOCAL_PATH}")
    print("=" * 70)

if __name__ == "__main__":
    update_workbook()
