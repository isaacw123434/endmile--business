import requests
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.outreach.mine_verified_leads import find_verified_domain

ch_key = "2f9f5eed-3be4-43aa-9761-353d9067fdc1"
url = "https://api.company-information.service.gov.uk/advanced-search/companies"
params = {
    "company_name_includes": "cost consultants",
    "company_status": "active",
    "size": 50
}
r = requests.get(url, params=params, auth=(ch_key, ""))
items = r.json().get("items", [])
print(f"Testing {len(items)} 'cost consultants':")
found = 0
for it in items:
    name = it.get("company_name")
    dom, mx, prov = find_verified_domain(name)
    if dom:
        found += 1
        print(f"  [+] {name} -> {dom} ({prov})")
    else:
        # print first 5 failed to inspect
        if found < 3:
            print(f"  [-] {name} -> NO MATCH")
print(f"Total matched: {found}/{len(items)}")
