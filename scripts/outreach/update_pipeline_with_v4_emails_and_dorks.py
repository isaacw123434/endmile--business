#!/usr/bin/env python3
"""
Update Master Pipeline Excel - Aggregating Contacts & Notes Across All Versions (v1, v2, v3, v4)
------------------------------------------------------------------------------------------------
1. Scans and aggregates all contacts, emails, and founder notes from:
   - C:\\Users\\isaac\\Downloads\\endmile_widget_prospects.xlsx (v1)
   - C:\\Users\\isaac\\Downloads\\endmile widget v2.xlsx        (v2)
   - C:\\Users\\isaac\\Downloads\\endmile widget v3.xlsx        (v3)
   - C:\\Users\\isaac\\Downloads\\endmile widget v4.xlsx        (v4)
   - C:\\Users\\isaac\\Downloads\\endmile widget v4 (1).xlsx    (v4 latest)
2. In Sheet 2 ('Venue Widget Pipeline'):
   - Merges ALL emails per venue (comma-separated, zero lost contacts).
   - Merges founder notes (e.g. custom hook notes, 'charity', 'council', 'uni', 'chain').
   - Populates contact names ('ConfirmedName') and role hints ('ConfirmedRole').
   - Converts 'DeepLinkGoogleSearch' into active, clickable Excel hyperlinks for all 4,992 venues.
   - HIDES all columns except the 20 requested:
     AssignedTemplate, FounderNotes, VenueName, ConfirmedEmail, ConfirmedName, ConfirmedRole,
     PublicEmail, Archetype, OwnershipType, WidgetFit, WidgetFitScore, Tier, EstMonthlySearches,
     OutreachStatus, DateSent, Website, Phone, Address, MultimodalFeatures, DeepLinkGoogleSearch
3. Synchronizes to:
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

LOCAL_DIR = Path(r"C:\Users\isaac\Documents\endmile")
LOCAL_PATH = LOCAL_DIR / "endmile_master_pipeline.xlsx"

ONEDRIVE_DOCS_DIR = Path(r"C:\Users\isaac\OneDrive\Documents\EndMile")
ONEDRIVE_DOCS_PATH = ONEDRIVE_DOCS_DIR / "endmile_master_pipeline.xlsx"

ONEDRIVE_DESKTOP_DIR = Path(r"C:\Users\isaac\OneDrive\Desktop")
ONEDRIVE_DESKTOP_PATH = ONEDRIVE_DESKTOP_DIR / "endmile_master_pipeline.xlsx"

DOWNLOADS_DIR = Path(r"C:\Users\isaac\Downloads")
SOURCE_FILES = [
    DOWNLOADS_DIR / "endmile_widget_prospects.xlsx",
    DOWNLOADS_DIR / "endmile widget v2.xlsx",
    DOWNLOADS_DIR / "endmile widget v3.xlsx",
    DOWNLOADS_DIR / "endmile widget v4.xlsx",
    DOWNLOADS_DIR / "endmile widget v4 (1).xlsx",
]

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
    "victoria": "Victoria", "philip": "Philip"
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
    "FounderNotes": 28,
    "VenueName": 30,
    "ConfirmedEmail": 45,
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
    Returns (emails_list, names_list, roles_list, notes_list)
    """
    if not isinstance(raw_text, str) or not raw_text.strip() or raw_text.strip() == "-":
        return [], [], [], []

    # Check if raw_text is purely an automated search query
    is_query = '""' in raw_text or ('("' in raw_text and 'OR' in raw_text and 'endmile' in raw_text)

    # 1. Extract all emails
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', raw_text)
    emails_clean = []
    seen = set()
    for e in emails:
        el = e.lower().strip()
        if el not in seen:
            seen.add(el)
            emails_clean.append(el)

    # 2. Extract leftover non-email text
    leftover = raw_text
    for e in emails:
        leftover = leftover.replace(e, "")
    leftover = re.sub(r'[,;\s\n\r]+', ' ', leftover).strip(" -:,;")

    # If it was an automated query, do not treat leftover as a note
    if is_query:
        leftover = ""

    notes = []
    names = []
    roles = []

    # 3. Classify leftover
    if leftover:
        if any(k in leftover.lower() for k in ["charity", "council", "uni", "chain", "noticed", "curtain times"]):
            notes.append(leftover)
        else:
            names.append(leftover)

    # 4. Extract contact names from email handles
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

    # 5. Extract role hints
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

    return emails_clean, names, roles, notes

def load_aggregated_downloads():
    """Aggregates all contacts, emails, and notes across all available versions in Downloads."""
    aggregated_by_id = {}
    aggregated_by_name = {}

    for p in SOURCE_FILES:
        if not p.exists():
            continue
        print(f"[SOURCE] Scanning {p.name}...")
        wb = openpyxl.load_workbook(p, read_only=True)
        ws = wb.active
        headers = [str(c or '').strip() for c in next(ws.iter_rows(max_row=1, values_only=True))]

        id_idx = headers.index("ID")
        name_idx = headers.index("Name")
        dork_idx = headers.index("DeepLinkGoogleSearch") if "DeepLinkGoogleSearch" in headers else None

        col1_idx = None
        for idx, h in enumerate(headers):
            if "column 1" in h.lower() or "notes" in h.lower():
                col1_idx = idx
                break

        for r in ws.iter_rows(min_row=2, values_only=True):
            vid = str(r[id_idx] or '').strip().replace('.0', '')
            vname = str(r[name_idx] or '').strip()
            val = str(r[col1_idx] or '').strip() if col1_idx is not None and col1_idx < len(r) else ''
            dork = str(r[dork_idx] or '').strip() if dork_idx is not None and dork_idx < len(r) else ''

            if vid not in aggregated_by_id:
                aggregated_by_id[vid] = {
                    'name': vname,
                    'emails': [],
                    'names': [],
                    'roles': [],
                    'notes': [],
                    'dork': dork
                }
            if vname not in aggregated_by_name:
                aggregated_by_name[vname] = aggregated_by_id[vid]

            # If this file has an updated dork with the new suffix, record it
            if dork and ('give me some emails' in dork or not aggregated_by_id[vid]['dork']):
                aggregated_by_id[vid]['dork'] = dork

            if val and val != '-' and val != 'None':
                emails, names, roles, notes = parse_venue_entry(val)
                for e in emails:
                    if e not in aggregated_by_id[vid]['emails']:
                        aggregated_by_id[vid]['emails'].append(e)
                for n in names:
                    if n not in aggregated_by_id[vid]['names']:
                        aggregated_by_id[vid]['names'].append(n)
                for ro in roles:
                    if ro not in aggregated_by_id[vid]['roles']:
                        aggregated_by_id[vid]['roles'].append(ro)
                for no in notes:
                    if no not in aggregated_by_id[vid]['notes']:
                        aggregated_by_id[vid]['notes'].append(no)

    print(f"[SOURCE] Finished aggregating. {len(aggregated_by_id)} unique venue IDs loaded.")
    return aggregated_by_id, aggregated_by_name

def run_update():
    print("=" * 75)
    print(" UPDATING MASTER PIPELINE: AGGREGATING v1, v2, v3, v4 & HYPERLINKING")
    print("=" * 75)

    agg_id, agg_name = load_aggregated_downloads()

    # Load master pipeline workbook
    source_master = ONEDRIVE_DOCS_PATH if ONEDRIVE_DOCS_PATH.exists() else LOCAL_PATH
    print(f"[LOAD] Loading master workbook from: {source_master}...")
    wb_master = openpyxl.load_workbook(source_master)

    if "Venue Widget Pipeline" not in wb_master.sheetnames:
        print("[ERROR] 'Venue Widget Pipeline' sheet missing!")
        return

    ws_venue = wb_master["Venue Widget Pipeline"]
    v_headers = [str(c or "").strip() for c in next(ws_venue.iter_rows(values_only=True))]

    v_id_col = v_headers.index("VenueID") + 1
    v_appr_col = v_headers.index("ManualApproval") + 1
    v_fnotes_col = v_headers.index("FounderNotes") + 1
    v_vname_col = v_headers.index("VenueName") + 1
    v_name_col = v_headers.index("ConfirmedName") + 1
    v_email_col = v_headers.index("ConfirmedEmail") + 1
    v_role_col = v_headers.index("ConfirmedRole") + 1
    v_dork_col = v_headers.index("DeepLinkGoogleSearch") + 1

    updated_contacts_count = 0
    multi_email_count = 0
    notes_count = 0
    hyperlinked_dorks_count = 0
    total_approved = 0

    for r in range(2, ws_venue.max_row + 1):
        vid = str(ws_venue.cell(row=r, column=v_id_col).value or "").strip().replace(".0", "")
        vname = str(ws_venue.cell(row=r, column=v_vname_col).value or "").strip()

        # Match by ID first, then fallback to VenueName if available
        venue_rec = agg_id.get(vid)
        if not venue_rec and vname in agg_name:
            venue_rec = agg_name[vname]

        # 1. Hyperlink Google Search URL
        existing_dork = ws_venue.cell(row=r, column=v_dork_col).value or ""
        target_dork = (venue_rec['dork'] if venue_rec and venue_rec.get('dork') else existing_dork) or ""
        target_dork = str(target_dork).strip()

        if target_dork:
            c_dork = ws_venue.cell(row=r, column=v_dork_col)
            c_dork.value = target_dork
            c_dork.hyperlink = target_dork
            c_dork.font = LINK_FONT
            hyperlinked_dorks_count += 1

        # 2. Populate Aggregated Emails & Contacts
        if venue_rec:
            emails = venue_rec['emails']
            names = venue_rec['names']
            roles = venue_rec['roles']
            notes = venue_rec['notes']

            if emails:
                emails_str = ", ".join(emails)
                ws_venue.cell(row=r, column=v_email_col, value=emails_str)
                if len(emails) > 1:
                    multi_email_count += 1

                if names:
                    ws_venue.cell(row=r, column=v_name_col, value=", ".join(names))
                if roles:
                    ws_venue.cell(row=r, column=v_role_col, value=", ".join(roles))

                # Approve venue
                cell_appr = ws_venue.cell(row=r, column=v_appr_col, value="Approved")
                cell_appr.fill = APPROVED_FILL
                cell_appr.font = BOLD_FONT
                cell_appr.alignment = Alignment(horizontal="center", vertical="center")
                updated_contacts_count += 1

            if notes:
                notes_str = "; ".join(notes)
                ws_venue.cell(row=r, column=v_fnotes_col, value=notes_str)
                notes_count += 1

        current_appr = ws_venue.cell(row=r, column=v_appr_col).value
        if current_appr == "Approved":
            total_approved += 1

    print(f"[OK] Hyperlinked {hyperlinked_dorks_count} Google Search URLs.")
    print(f"[OK] Populated confirmed emails across {updated_contacts_count} venues ({multi_email_count} venues with multiple emails).")
    print(f"[OK] Populated founder notes across {notes_count} venues.")
    print(f"[OK] Total approved venues: {total_approved}.")

    # 3. Apply Column Visibility & Widths
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

    print(f"[OK] Column visibility: {visible_cols_count} visible columns, {hidden_cols_count} hidden columns.")
    print(f"[OK] Freeze pane pinned at F2 (AssignedTemplate, FounderNotes, VenueName).")

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
    print("ALL VERSIONS AGGREGATION COMPLETE!")
    print(f"  Total Approved Venues: {total_approved}")
    print(f"  Multi-Email Venues: {multi_email_count}")
    print(f"  Founder Notes Populated: {notes_count}")
    print(f"  Hyperlinked URLs: {hyperlinked_dorks_count}")
    print(f"  Visible Columns ({visible_cols_count}): {', '.join(VISIBLE_COLUMNS)}")
    print("=" * 75)

if __name__ == "__main__":
    run_update()
