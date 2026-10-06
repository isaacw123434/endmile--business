#!/usr/bin/env python3
"""
create_prospects_v3.py

Generates 'endmile widget v3.xlsx' and 'unserved_prospects_v3.csv' by:
1. Auditing and accurately classifying OwnershipType across all 4,993 venues:
   - Identifies Local Authority / Council owned venues (.gov.uk, municipal cultural trusts like Glasgow Life,
     Edinburgh Museums, Bristol Museums, TWAM, Hampshire Cultural Trust, Derby Museums, etc.)
   - Identifies Corporate Chains & Monopolies (Merlin Entertainments, English Heritage, National Trust,
     Historic Environment Scotland including Edinburgh Castle, Royal Collection Trust including Windsor Castle,
     ATG, LW Theatres, Delfont Mackintosh, Nimax, national museums, cinema chains, etc.)
   - Identifies University Campus & Academic venues (.ac.uk, Oxford/Cambridge/Edinburgh colleges, etc.)
   - Retains 'Independent Single/Dual-Site' strictly for genuine independent cultural venues and trusts.
2. Pre-populating newly discovered emails into 'Column 1' while preserving 100% of Isaac's manual notes & emails.
3. Preserving the exact column ordering and schema of 'endmile widget v2.xlsx'.
"""

import os
import re
import pandas as pd

SRC_EXCEL = r"C:\Users\isaac\Downloads\endmile widget v2.xlsx"
DEST_EXCEL = r"C:\Users\isaac\Downloads\endmile widget v3.xlsx"
DEST_CSV = r"c:\Users\isaac\Videos\files too big for onedrive\github\endmile-1\data\venues\unserved_prospects_v3.csv"

# Pre-discovered emails for specific target venues
NEW_DISCOVERED_EMAILS = {
    # M Shed (Bristol City Council)
    "M Shed": "philip.walker@bristol.gov.uk",
    # The Pump Room (Bath & North East Somerset Council)
    "The Pump Room": "robert_campbell@bathnes.gov.uk",
    # Museum of Oxford (Oxford City Council)
    "Museum of Oxford": "predway@oxford.gov.uk",
    # Northern Stage (Independent Theatre)
    "Northern Stage": "probson@northernstage.co.uk, hmcdonnell@northernstage.co.uk",
    # Bristol Old Vic (Independent Theatre)
    "Bristol Old Vic": "abigail.humphrey@bristololdvic.org.uk",
    # Theatre Royal Haymarket (Independent West End Theatre)
    "Theatre Royal Haymarket": "mark@trh.co.uk"
}

# Centralized council domains and arms-length cultural trusts (ALEOs)
COUNCIL_DOMAINS = [
    # Scotland ALEOs & Services
    "glasgowlife.org.uk", "glasgowconcerthalls.com", "edinburghmuseums.org.uk", "cultureedinburgh.com",
    "liveborders.org.uk", "onfife.com", "angusalive.com", "culturenl.co.uk", "eastayrshireleisure.com",
    "leisureandculturedundee.com", "culturepk.org.uk", "culturestirling.org", "dgculture.co.uk",
    "orkneymuseums.co.uk", "shetlandmuseumandarchives.org.uk", "aagm.co.uk", "mcmanus.co.uk",
    "usherhall.co.uk", "burrellcollection.com",
    # English Local Authority Trusts & Services
    "bristolmuseums.org.uk", "twmuseums.org.uk", "birminghammuseums.org.uk", "shropshiremuseums.org.uk",
    "derbymuseums.org", "leicestermuseums.org", "hullmuseums.co.uk", "hcandl.co.uk", "sheffieldmuseums.org.uk",
    "southendmuseums.co.uk", "bradfordmuseums.org", "bradford-theatres.co.uk", "wolverhamptonart.org.uk",
    "stokemuseums.org.uk", "stalbansmuseums.org.uk", "canterburymuseums.co.uk", "portsmouthmuseums.co.uk",
    "readingarts.com", "theboxplymouth.com", "scunthorpetheatres.co.uk", "hampshireculture.org.uk",
    "hampshireculturaltrust.org.uk", "swheritage.org.uk", "boltonlams.co.uk", "manchesterartgallery.org",
    "nottinghamcitymuseums.org.uk", "wollatonhall.org.uk", "yorkmuseumstrust.org.uk", "romanbaths.co.uk",
    "victoriagal.org.uk", "towerbridge.org.uk", "ltmuseum.co.uk", "boroughofpoole.com", "museumofoxford.org",
    "cimuseums.org.uk", "museumsnorfolk.org.uk", "culturewarrington.org", "eastridingculture.co.uk",
    "culturetrust.com", "harboroughmuseum.org.uk", "elsecar-heritage.com", "scarboroughmuseumsandgalleries.org.uk",
    "scarboroughspa.co.uk", "scarboroughopenairtheatre.com", "sheffieldcityhall.co.uk", "thecityofldn.com",
    "londonmuseum.org.uk", "discoverymuseum.org.uk",
    # Wales Local Authority Services
    "theatrausirgar.co.uk", "cofgar.wales", "monlife.co.uk", "swanseamuseum.co.uk"
]

# Statutory national bodies and heritage trusts
HERITAGE_NATIONAL_DOMAINS = [
    "nationaltrust.org.uk", "nts.org.uk", "english-heritage.org.uk",
    "historicenvironment.scot", "historicengland.org.uk", "cadw.gov.wales", "cadw.wales",
    "hrp.org.uk", "historic-royal-palaces.org.uk", "rct.uk", "landmarktrust.org.uk",
    "wwt.org.uk", "rspb.org.uk", "woodlandtrust.org.uk", "canalrivertrust.org.uk",
    "forestryengland.uk", "forestryandland.gov.scot", "royalparks.org.uk",
    "kew.org", "rbge.org.uk", "zsl.org", "chesterzoo.org",
    "britishmuseum.org", "sciencemuseumgroup.org.uk", "sciencemuseum.org.uk",
    "railwaymuseum.org.uk", "scienceandindustrymuseum.org.uk", "locomotion.org.uk",
    "tate.org.uk", "nationalgallery.org.uk", "npg.org.uk", "vam.ac.uk", "vam.org.uk", "vanda.ac.uk",
    "nhm.ac.uk", "iwm.org.uk", "rmg.co.uk", "liverpoolmuseums.org.uk", "museum.wales",
    "nationalgalleries.org", "royalarmouries.org", "postalmuseum.org",
    "edinburghcastle.scot", "stirlingcastle.scot", "urquhartcastle.scot",
    "nmrn.org.uk", "shakespeare.org.uk", "southbankcentre.co.uk"
]

# Commercial chains, theatre operators, cinema chains, leisure groups
COMMERCIAL_CHAIN_DOMAINS = [
    # Merlin Entertainments
    "merlinentertainments.biz", "thedungeons.com", "madametussauds.com", "sealife.co.uk",
    "visitsealife.com", "londoneye.com", "warwick-castle.com", "shreksadventure.com",
    "altontowers.com", "thorpepark.com", "chessington.com", "legoland.co.uk",
    "beargryllsadventure.com", "cadburyworld.co.uk", "theblackpooltower.com",
    "peterrabbitexploreandplay.co.uk",
    # West End & Regional Theatre Groups
    "atgtickets.com", "ambassadortickets.com", "theambassadorstheatre.co.uk", "lwtheatres.co.uk",
    "delfontmackintosh.co.uk", "victoriapalacetheatre.co.uk", "nimaxtheatres.com",
    "trafalgartickets.com", "trafalgarentertainment.com", "reallyusefulgroup.com",
    "academymusicgroup.com", "livenation.co.uk", "ticketmaster.co.uk", "boomtownfair.co.uk",
    "nederlander.co.uk", "aldwychtheatre.com", "dominiontheatre.com", "dominiontheatrelondon.com",
    "thephoenixtheatre.co.uk",
    # Cinema Chains
    "odeon.co.uk", "cineworld.co.uk", "vue.co.uk", "myvue.com", "everymancinema.com",
    "showcasecinemas.co.uk", "picturehouses.com", "lightcinemas.co.uk", "curzon.com",
    "empirecinemas.co.uk", "wtwcinemas.co.uk", "merlincinemas.co.uk", "thereel.com", "omniplex.co.uk",
    # Attractions & Leisure Operators
    "continuumattractions.com", "realmarykingsclose.com", "yorkschocolatestory.com",
    "spinnakertower.co.uk", "oxfordcastleandprison.co.uk", "greenwoodfamilypark.co.uk",
    "coronationstreetexperience.co.uk", "parkwood-leisure.co.uk", "better.org.uk", "gll.org",
    "everyoneactive.com", "placesleisure.org", "goape.co.uk", "hollywoodbowl.co.uk",
    "tenpin.co.uk", "team-sport.co.uk", "escapehunt.com", "discovering-distilleries.com",
    "clarendonfineart.com"
]

def classify_venue_ownership(row):
    domain = str(row.get("Domain", "")).lower().strip()
    website = str(row.get("Website", "")).lower().strip()
    name = str(row.get("Name", "")).strip()
    name_lower = name.lower()
    col1 = str(row.get("Column 1", "")).strip().lower()

    # Preserve Isaac's explicit manual classifications if entered in Column 1
    if col1 == "chain":
        return "Corporate Chain / Centralized Trust"
    if col1 == "council":
        return "Local Authority / Council"
    if col1 == "uni":
        return "University Campus / Academic"

    # 1. Academic & University
    if ".ac.uk" in domain or ".ac.uk" in website or "etoncollege.com" in domain:
        return "University Campus / Academic"
    if re.search(r"\b(university|campus)\b", name_lower) and not any(k in name_lower for k in ["theatre", "playhouse", "museum", "gallery"]):
        return "University Campus / Academic"

    # 2. Local Authority / Council
    if ".gov.uk" in domain or ".gov.uk" in website or ".gov.wales" in domain or ".gov.scot" in domain:
        if any(h in domain for h in ["cadw", "historic-scotland"]):
            return "Corporate Chain / Centralized Trust"
        return "Local Authority / Council"

    if any(cd in domain or cd in website for cd in COUNCIL_DOMAINS):
        return "Local Authority / Council"

    if any(term in name_lower for term in [
        "city council", "borough council", "district council", "county council", "town council", "parish council"
    ]):
        return "Local Authority / Council"

    if name in [
        "M Shed", "The Pump Room", "Museum of Oxford", "Roman Baths", "Nelson Monument",
        "Shrewsbury Castle", "Maumbury Rings", "Usher Hall", "City Halls & Old Fruitmarket",
        "Victoria Art Gallery", "The Burrell Collection"
    ]:
        return "Local Authority / Council"

    # 3. Corporate Chain / Centralized Trust
    if any(hd in domain or hd in website for hd in HERITAGE_NATIONAL_DOMAINS):
        return "Corporate Chain / Centralized Trust"

    if any(cd in domain or cd in website for cd in COMMERCIAL_CHAIN_DOMAINS):
        return "Corporate Chain / Centralized Trust"

    chain_names = [
        "dungeon", "madame tussauds", "sea life", "legoland", "alton towers", "thorpe park",
        "chessington", "london eye", "windsor castle", "buckingham palace", "holyroodhouse",
        "tower of london", "hampton court palace", "edinburgh castle", "stirling castle",
        "warwick castle", "mary king's close", "gladstone's land", "coronation street experience",
        "palace of holyroodhouse", "kew palace"
    ]
    if any(cn in name_lower for cn in chain_names):
        return "Corporate Chain / Centralized Trust"

    # Retain previous Corporate Chain or Council if already marked in v2
    curr = str(row.get("OwnershipType", ""))
    if curr in ["Corporate Chain / Centralized Trust", "Local Authority / Council"]:
        return curr

    return "Independent Single/Dual-Site"


def main():
    print(f"Reading source Excel: {SRC_EXCEL}")
    df = pd.read_excel(SRC_EXCEL, sheet_name=0)
    total_venues = len(df)
    print(f"Loaded {total_venues} venues.")
    print("Original OwnershipType breakdown:")
    print(df["OwnershipType"].value_counts())

    # Step 1: Reclassify OwnershipType
    print("\nApplying granular OwnershipType classification...")
    new_ownership = df.apply(classify_venue_ownership, axis=1)
    df["OwnershipType"] = new_ownership
    print("\nUpdated OwnershipType breakdown:")
    print(df["OwnershipType"].value_counts())

    # Step 2: Inject newly discovered emails into Column 1 without touching existing values
    print("\nInjecting newly discovered contact emails into 'Column 1'...")
    injected_count = 0
    preserved_count = 0

    for idx, row in df.iterrows():
        existing_col1 = row["Column 1"]
        has_existing = pd.notna(existing_col1) and str(existing_col1).strip() != ""
        venue_name = str(row["Name"]).strip()

        if has_existing:
            preserved_count += 1
        elif venue_name in NEW_DISCOVERED_EMAILS:
            email_val = NEW_DISCOVERED_EMAILS[venue_name]
            df.at[idx, "Column 1"] = email_val
            injected_count += 1
            print(f"  [+] Injected email for '{venue_name}' (idx {idx}): {email_val}")

    total_col1 = df["Column 1"].dropna().count()
    print(f"\nColumn 1 Summary:")
    print(f"  Existing values preserved: {preserved_count}")
    print(f"  New emails injected:       {injected_count}")
    print(f"  Total populated in Col 1:  {total_col1}")

    # Step 3: Validate column schema matches v2 exactly
    orig_cols = [
        "ID", "Name", "Archetype", "OwnershipType", "WidgetFit", "WidgetFitScore",
        "MultimodalFeatures", "Domain", "Website", "Phone", "RawEmail", "Tier",
        "EstMonthlySearches", "Capacity", "Score", "Address", "Column 1",
        "Contact Search Query", "EmailHook"
    ]
    df = df[orig_cols]

    # Step 4: Write v3 Excel file
    print(f"\nWriting v3 Excel: {DEST_EXCEL}")
    with pd.ExcelWriter(DEST_EXCEL, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="unserved_prospects", index=False)
    print(f"Successfully saved {DEST_EXCEL}")

    # Step 5: Write v3 CSV file
    print(f"Writing v3 CSV: {DEST_CSV}")
    os.makedirs(os.path.dirname(DEST_CSV), exist_ok=True)
    df.to_csv(DEST_CSV, index=False, encoding="utf-8-sig")
    print(f"Successfully saved {DEST_CSV}")

    # Step 6: Outreach Summary for Isaac
    indies = df[df["OwnershipType"] == "Independent Single/Dual-Site"]
    exceptional_indies = indies[indies["WidgetFit"] == "Exceptional Fit"]
    strong_indies = indies[indies["WidgetFit"] == "Strong Fit"]

    print("\n" + "=" * 60)
    print("ENDMILE VENUE OUTREACH POOL (V3 AUDITED)")
    print("=" * 60)
    print(f"Total Database:                     {len(df):,}")
    print(f"Independent Single/Dual-Site:       {len(indies):,} (High-ROI Decision Maker Pool)")
    print(f"  - Exceptional Fit (Top Priority): {len(exceptional_indies):,}")
    print(f"  - Strong Fit:                     {len(strong_indies):,}")
    print(f"Corporate Chains / Trusts Excluded: {len(df[df['OwnershipType'] == 'Corporate Chain / Centralized Trust']):,}")
    print(f"Local Authorities / Councils Excl:  {len(df[df['OwnershipType'] == 'Local Authority / Council']):,}")
    print(f"University Campuses Excluded:       {len(df[df['OwnershipType'] == 'University Campus / Academic']):,}")
    print("=" * 60)

if __name__ == "__main__":
    main()
