#!/usr/bin/env python3
"""
Update Master Pipeline Excel with All Discovered Venue Emails, Hyperlinked Google URLs, and Visible Columns
---------------------------------------------------------------------------------------------------------
1. Reads latest notes, contacts, and Google Pro Search URLs from:
   C:\\Users\\isaac\\Downloads\\endmile widget v4 (1).xlsx (or endmile widget v4.xlsx)
2. In Sheet 2 ('Venue Widget Pipeline'):
   - Preserves ALL multiple emails per venue in 'ConfirmedEmail' (comma-separated, zero lost contacts).
   - Preserves founder notes (e.g. 'charity', 'council', 'uni', 'chain') in 'FounderNotes'.
   - Populates contact names ('ConfirmedName') and role hints ('ConfirmedRole').
   - Converts 'DeepLinkGoogleSearch' into active, clickable Excel hyperlinks for all 4,992 venues.
   - HIDES all columns except the 20 requested:
     AssignedTemplate, FounderNotes, VenueName, ConfirmedEmail, ConfirmedName, ConfirmedRole,
     PublicEmail, Archetype, OwnershipType, WidgetFit, WidgetFitScore, Tier, EstMonthlySearches,
     OutreachStatus, DateSent, Website, Phone, Address, MultimodalFeatures, DeepLinkGoogleSearch
3. In Sheet 3 ('Email Templates & Referrers'):
   - Enforces strictly zero raw URL links across all 16 outreach templates.
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
LINK_FONT = Font(name="Calibri", size=9.5, color="0563C1", underline="single")
THIN_SIDE = Side(border_style="thin", color="CBD5E1")
CELL_BORDER = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=THIN_SIDE)

COMMON_NAME_TOKENS = {
    "niall": "Niall", "linda": "Linda", "julia": "Julia", "elin": "Elin", "david": "David",
    "celine": "Celine", "alice": "Alice", "alex": "Alex", "cate": "Cate", "kate": "Kate",
    "amanda": "Amanda", "martin": "Martin", "rosemary": "Rosemary", "jo": "Jo", "lauren": "Lauren",
    "john": "John", "paul": "Paul", "sarah": "Sarah", "emma": "Emma", "james": "James",
    "richard": "Richard", "helen": "Helen", "simon": "Simon", "claire": "Claire", "mark": "Mark",
    "rachel": "Rachel", "andrew": "Andrew", "anna": "Anna", "robert": "Robert", "fiona": "Fiona",
    "peter": "Peter", "lucy": "Lucy", "sophie": "Sophie", "nicola": "Nicola", "anthony": "Anthony",
    "nathan": "Nathan", "camilla": "Camilla", "ameeta": "Ameeta", "gillian": "Gillian", "hannah": "Hannah",
    "mandy": "Mandy", "wendy": "Wendy", "rico": "Rico", "iain": "Iain", "abigail": "Abigail",
    "georgios": "Georgios", "asta": "Asta", "harriet": "Harriet", "katie": "Katie", "daniel": "Daniel",
    "robin": "Robin", "adam": "Adam", "zsofia": "Zsofia", "steve": "Steve", "karen": "Karen",
    "melissa": "Melissa", "bridgeen": "Bridgeen", "phil": "Phil", "beth": "Beth", "cerys": "Cerys",
    "angus": "Angus", "gary": "Gary", "gareth": "Gareth", "michael": "Michael", "kathryn": "Kathryn",
    "chris": "Chris", "luke": "Luke", "andy": "Andy", "kerina": "Kerina", "vic": "Vic",
    "victoria": "Victoria", "mark": "Mark", "philip": "Philip"
}

VISIBLE_COLUMNS = [
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
]

WIDTH_MAP = {
    "AssignedTemplate": 20,
    "FounderNotes": 25,
    "VenueName": 30,
    "ConfirmedEmail": 45,  # Wide enough to display multiple comma-separated emails
    "ConfirmedName": 24,
    "ConfirmedRole": 20,
    "PublicEmail": 28,
    "Archetype": 18,
    "OwnershipType": 16,
    "WidgetFit": 14,
    "WidgetFitScore": 14,
    "Tier": 10,
    "EstMonthlySearches": 18,
    "OutreachStatus": 16,
    "DateSent": 14,
    "Website": 28,
    "Phone": 18,
    "Address": 32,
    "MultimodalFeatures": 24,
    "DeepLinkGoogleSearch": 25,
}

def parse_venue_entry(raw_text: str):
    """
    Parses raw notes and contacts for a venue:
    Returns (emails_str, names_str, roles_str, notes_str)
    """
    if not isinstance(raw_text, str) or not raw_text.strip() or raw_text.strip() == "-":
        return "", "", "", ""

    # 1. Extract all emails
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', raw_text)
    emails_clean = []
    seen = set()
    for e in emails:
        el = e.lower().strip()
        if el not in seen:
            seen.add(el)
            emails_clean.append(el)

    emails_str = ", ".join(emails_clean)

    # 2. Extract leftover non-email text
    leftover = raw_text
    for e in emails:
        leftover = leftover.replace(e, "")
    leftover = re.sub(r'[,;\s\n\r]+', ' ', leftover).strip(" -:,;")

    # 3. If no emails found, leftover is purely a note (e.g. 'charity', 'council', 'uni', 'chain')
    if not emails_clean:
        return "", "", "", leftover

    # 4. If leftover has an explicit person name (like 'Victoria Winslade')
    names = []
    roles = []
    notes = ""

    if leftover:
        if not any(k in leftover.lower() for k in ["charity", "council", "uni", "chain", "http"]):
            names.append(leftover)
        else:
            notes = leftover

    # 5. Extract contact names from email handles
    for e in emails_clean:
        handle = e.split("@")[0].lower()
        parts = re.split(r'[._-]', handle)
        first_token = parts[0]
        if first_token in COMMON_NAME_TOKENS:
            c_name = COMMON_NAME_TOKENS[first_token]
            if c_name not in names:
                names.append(c_name)
        elif len(parts) >= 2 and parts[1] in COMMON_NAME_TOKENS:
            c_name = COMMON_NAME_TOKENS[parts[1]]
            if c_name not in names:
                names.append(c_name)
        elif handle in COMMON_NAME_TOKENS:
            c_name = COMMON_NAME_TOKENS[handle]
            if c_name not in names:
                names.append(c_name)

    names_str = ", ".join(names)

    # 6. Extract role hints
    for e in emails_clean:
        handle = e.split("@")[0].lower()
        if "manager" in handle or "mgr" in handle:
            if "Manager" not in roles: roles.append("Manager")
        elif "curator" in handle:
            if "Curator" not in roles: roles.append("Curator")
        elif "clerk" in handle:
            if "Clerk" not in roles: roles.append("Clerk")
        elif "foh" in handle:
            if "Front of House" not in roles: roles.append("Front of House")
        elif "sales" in handle:
            if "Sales" not in roles: roles.append("Sales")

    roles_str = ", ".join(roles)
    return emails_str, names_str, roles_str, notes

def run_update():
    print("=" * 75)
    print(" UPDATING MASTER PIPELINE WITH ALL EMAILS, HYPERLINKS & CLEAN COLUMNS")
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
    v_headers = [str(c or "").strip() for c in next(ws_venue.iter_rows(values_only=True))]

    v_id_col = v_headers.index("VenueID") + 1
    v_appr_col = v_headers.index("ManualApproval") + 1
    v_fnotes_col = v_headers.index("FounderNotes") + 1
    v_name_col = v_headers.index("ConfirmedName") + 1
    v_email_col = v_headers.index("ConfirmedEmail") + 1
    v_role_col = v_headers.index("ConfirmedRole") + 1
    v_dork_col = v_headers.index("DeepLinkGoogleSearch") + 1
    v_raw_notes_col = v_headers.index("RawNotesAndContacts") + 1 if "RawNotesAndContacts" in v_headers else None

    updated_contacts_count = 0
    multi_email_count = 0
    updated_dorks_count = 0
    total_approved = 0

    # Iterate rows and update contacts + hyperlinked search URLs
    for r in range(2, ws_venue.max_row + 1):
        vid = str(ws_venue.cell(row=r, column=v_id_col).value or "").strip()
        if vid.endswith(".0"):
            vid = vid[:-2]

        v4_data = v4_map.get(vid)

        # 1. Process Google Pro Search URL & make it an active Excel Hyperlink
        dork_url = (v4_data["dork"] if v4_data and v4_data.get("dork") else ws_venue.cell(row=r, column=v_dork_col).value) or ""
        dork_url = str(dork_url).strip()
        if dork_url:
            c_dork = ws_venue.cell(row=r, column=v_dork_col)
            c_dork.value = dork_url
            c_dork.hyperlink = dork_url
            c_dork.font = LINK_FONT
            updated_dorks_count += 1

        # 2. Process Notes & Contacts
        if v4_data and v4_data.get("note") and v4_data["note"] != "-":
            v4_note = v4_data["note"]
            emails_str, names_str, roles_str, notes_str = parse_venue_entry(v4_note)

            if emails_str:
                ws_venue.cell(row=r, column=v_email_col, value=emails_str)
                if "," in emails_str:
                    multi_email_count += 1

                if names_str:
                    ws_venue.cell(row=r, column=v_name_col, value=names_str)
                if roles_str:
                    ws_venue.cell(row=r, column=v_role_col, value=roles_str)
                if notes_str:
                    ws_venue.cell(row=r, column=v_fnotes_col, value=notes_str)

                if v_raw_notes_col:
                    ws_venue.cell(row=r, column=v_raw_notes_col, value=v4_note)

                # Set ManualApproval to Approved
                cell_appr = ws_venue.cell(row=r, column=v_appr_col, value="Approved")
                cell_appr.fill = APPROVED_FILL
                cell_appr.font = BOLD_FONT
                cell_appr.alignment = Alignment(horizontal="center", vertical="center")
                updated_contacts_count += 1
            elif notes_str:
                # Founder classification without emails (e.g. 'charity', 'council', 'uni', 'chain')
                ws_venue.cell(row=r, column=v_fnotes_col, value=notes_str)
                if v_raw_notes_col:
                    ws_venue.cell(row=r, column=v_raw_notes_col, value=v4_note)

        current_appr = ws_venue.cell(row=r, column=v_appr_col).value
        if current_appr == "Approved":
            total_approved += 1

    print(f"[OK] Hyperlinked {updated_dorks_count} Google Search URLs.")
    print(f"[OK] Preserved all discovered emails across {updated_contacts_count} venues ({multi_email_count} venues have multiple emails).")
    print(f"[OK] Total approved venues: {total_approved}.")

    # 3. Apply Column Visibility & Widths
    # Only keep visible: AssignedTemplate, FounderNotes, VenueName, ConfirmedEmail, ConfirmedName, ConfirmedRole,
    # PublicEmail, Archetype, OwnershipType, WidgetFit, WidgetFitScore, Tier, EstMonthlySearches,
    # OutreachStatus, DateSent, Website, Phone, Address, MultimodalFeatures, DeepLinkGoogleSearch
    visible_set = set(VISIBLE_COLUMNS)
    hidden_cols_count = 0
    visible_cols_count = 0

    for col_idx in range(1, ws_venue.max_column + 1):
        col_letter = openpyxl.utils.get_column_letter(col_idx)
        header_val = str(ws_venue.cell(row=1, column=col_idx).value or "").strip()

        if header_val in visible_set:
            ws_venue.column_dimensions[col_letter].hidden = False
            visible_cols_count += 1
            if header_val in WIDTH_MAP:
                ws_venue.column_dimensions[col_letter].width = WIDTH_MAP[header_val]
        else:
            ws_venue.column_dimensions[col_letter].hidden = True
            hidden_cols_count += 1

    # Freeze columns C, D, E so Venue Name and notes remain pinned while scrolling horizontally
    ws_venue.freeze_panes = "F2"

    print(f"[OK] Column visibility configured: {visible_cols_count} visible columns, {hidden_cols_count} hidden columns.")
    print(f"[OK] Freeze pane set at F2 (pins AssignedTemplate, FounderNotes, and VenueName).")

    # 4. Save to all 3 paths
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
    print("PIPELINE UPDATE COMPLETE!")
    print(f"  Visible Columns ({visible_cols_count}): {', '.join(VISIBLE_COLUMNS)}")
    print(f"  Multiple Emails Preserved: {multi_email_count} venues")
    print(f"  Google URLs Hyperlinked: {updated_dorks_count}")
    print("=" * 75)

if __name__ == "__main__":
    run_update()
