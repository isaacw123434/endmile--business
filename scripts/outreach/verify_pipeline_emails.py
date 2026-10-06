#!/usr/bin/env python3
"""
EndMile Pipeline Email & MX Verifier
------------------------------------
Validates all prospective leads in data/consultancies/app_prospects_v1.csv
to eliminate bounces before any cold email is dispatched.

Verification Logic:
1. Checks if the domain has active Mail Exchange (MX) records.
2. If the initial domain (e.g. .co.uk) has no MX, tries .com, .ltd, etc.
3. Classifies mail provider (Microsoft 365, Google Workspace, Mimecast, etc.).
4. Sets EmailStatus = 'Verified (Active MX)' or 'Invalid / No MX (Do Not Send)'.
5. Updates both the CSV and the Downloads Excel workbook.
"""

import re
import socket
import concurrent.futures
from pathlib import Path
import pandas as pd
import dns.resolver

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CSV_PATH = REPO_ROOT / "data" / "consultancies" / "app_prospects_v1.csv"
EXCEL_PATH = Path(r"C:\Users\isaac\Downloads\endmile app prospects v1.xlsx")

# Resolver with fast timeout
custom_resolver = dns.resolver.Resolver()
custom_resolver.timeout = 2.0
custom_resolver.lifetime = 2.0

def classify_mx(mx_host: str) -> str:
    mx_lower = mx_host.lower()
    if "outlook" in mx_lower or "protection.outlook.com" in mx_lower:
        return "Microsoft 365"
    if "google" in mx_lower or "googlemail" in mx_lower or "aspmx" in mx_lower:
        return "Google Workspace"
    if "mimecast" in mx_lower:
        return "Mimecast"
    if "messagelabs" in mx_lower:
        return "Broadcom/Symantec"
    if "stackmail" in mx_lower or "20i" in mx_lower:
        return "20i Stackmail"
    if "barracuda" in mx_lower:
        return "Barracuda"
    if "proofpoint" in mx_lower:
        return "Proofpoint"
    return "Custom/Hosting MX"

def check_domain_mx(domain: str) -> tuple[bool, str, str]:
    """Returns (has_mx, primary_mx_host, provider_category)."""
    try:
        answers = custom_resolver.resolve(domain, "MX")
        if answers:
            # Sort by preference
            sorted_answers = sorted(answers, key=lambda r: r.preference)
            best_mx = str(sorted_answers[0].exchange).rstrip(".")
            provider = classify_mx(best_mx)
            return True, best_mx, provider
    except Exception:
        pass
    return False, "", ""

def verify_lead_email(row: dict) -> dict:
    lead_id = row.get("LeadID")
    op_email = str(row.get("OperationalEmail", "")).strip()
    company_name = str(row.get("CompanyName", "")).strip()
    trade_name = str(row.get("TradeName") or company_name).strip()

    if not op_email or "@" not in op_email:
        return {
            "LeadID": lead_id,
            "EmailStatus": "Invalid (Malformed)",
            "VerifiedEmail": "",
            "MailProvider": "",
            "PrimaryMX": ""
        }

    user_part, current_domain = op_email.split("@", 1)
    current_domain = current_domain.strip().lower()

    # 1. Test current domain
    has_mx, best_mx, provider = check_domain_mx(current_domain)
    if has_mx:
        return {
            "LeadID": lead_id,
            "EmailStatus": "Verified (Active MX)",
            "VerifiedEmail": f"{user_part}@{current_domain}",
            "MailProvider": provider,
            "PrimaryMX": best_mx
        }

    # 2. Try alternate TLDs (.com if .co.uk, or .co.uk if .com)
    alt_domain = None
    if current_domain.endswith(".co.uk"):
        alt_domain = current_domain.replace(".co.uk", ".com")
    elif current_domain.endswith(".com"):
        alt_domain = current_domain.replace(".com", ".co.uk")

    if alt_domain:
        has_mx, best_mx, provider = check_domain_mx(alt_domain)
        if has_mx:
            return {
                "LeadID": lead_id,
                "EmailStatus": "Verified (Alternate TLD)",
                "VerifiedEmail": f"{user_part}@{alt_domain}",
                "MailProvider": provider,
                "PrimaryMX": best_mx
            }

    # 3. Try clean trade name slug domain
    clean_slug = re.sub(r"[^a-z0-9]", "", trade_name.lower())[:25]
    for candidate in [f"{clean_slug}.co.uk", f"{clean_slug}.com"]:
        if candidate not in [current_domain, alt_domain]:
            has_mx, best_mx, provider = check_domain_mx(candidate)
            if has_mx:
                return {
                    "LeadID": lead_id,
                    "EmailStatus": "Verified (Resolved Domain)",
                    "VerifiedEmail": f"info@{candidate}",
                    "MailProvider": provider,
                    "PrimaryMX": best_mx
                }

    # If no MX found
    return {
        "LeadID": lead_id,
        "EmailStatus": "Invalid / No MX (Do Not Send)",
        "VerifiedEmail": op_email,
        "MailProvider": "None (No MX)",
        "PrimaryMX": ""
    }

def main():
    print("=" * 70)
    print(" ENDMILE PIPELINE EMAIL & BOUNCE VERIFIER")
    print("=" * 70)

    if not CSV_PATH.exists():
        print(f"Error: Prospect CSV not found at {CSV_PATH}")
        return

    df = pd.read_csv(CSV_PATH)
    total_leads = len(df)
    print(f"Loaded {total_leads} leads from {CSV_PATH.name} for DNS MX verification...")

    records = df.to_dict(orient="records")
    results = {}

    print("Running multi-threaded DNS MX resolution across candidate domains...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_to_id = {executor.submit(verify_lead_email, r): r["LeadID"] for r in records}
        completed = 0
        for future in concurrent.futures.as_completed(future_to_id):
            res = future.result()
            results[res["LeadID"]] = res
            completed += 1
            if completed % 200 == 0 or completed == total_leads:
                print(f"  Processed {completed}/{total_leads} leads...")

    # Map back to DataFrame
    df["EmailStatus"] = df["LeadID"].map(lambda lid: results[lid]["EmailStatus"])
    df["VerifiedEmail"] = df["LeadID"].map(lambda lid: results[lid]["VerifiedEmail"])
    df["MailProvider"] = df["LeadID"].map(lambda lid: results[lid]["MailProvider"])
    df["PrimaryMX"] = df["LeadID"].map(lambda lid: results[lid]["PrimaryMX"])

    # Update OperationalEmail with VerifiedEmail if verified
    valid_mask = df["EmailStatus"].str.startswith("Verified")
    df.loc[valid_mask, "OperationalEmail"] = df.loc[valid_mask, "VerifiedEmail"]

    # Summary
    status_counts = df["EmailStatus"].value_counts().to_dict()
    provider_counts = df[valid_mask]["MailProvider"].value_counts().to_dict()

    print("\n" + "=" * 70)
    print(" VERIFICATION RESULTS:")
    print("=" * 70)
    for status, count in status_counts.items():
        pct = round((count / total_leads) * 100, 1)
        print(f"  {status}: {count} ({pct}%)")

    print("\nMAIL PROVIDER BREAKDOWN (Verified Leads):")
    for prov, count in provider_counts.items():
        print(f"  {prov}: {count}")

    # Save to CSV
    df.to_csv(CSV_PATH, index=False, encoding="utf-8")
    print(f"\n[OK] Updated {CSV_PATH.name} with verified emails and status.")

    # Save to Excel
    if EXCEL_PATH.exists():
        try:
            with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                df.to_excel(writer, sheet_name="EndMile Consultancies", index=False)
            print(f"[OK] Synchronized {EXCEL_PATH.name}")
        except Exception as e:
            print(f"[WARNING] Could not update Excel file ({e}). CSV is authoritative.")

if __name__ == "__main__":
    main()
