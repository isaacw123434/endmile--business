import requests
import re

url = "https://www.crowncommercial.gov.uk/agreements/RM6187"
r = requests.get(url, timeout=10)
print("RM6187 status:", r.status_code)
csv_links = [l for l in re.findall(r'href=["\']([^"\']+)["\']', r.text) if '.csv' in l.lower() or 'supplier' in l.lower()]
print("Supplier links:", csv_links[:10])

# Also check G-Cloud 13
url_gc = "https://www.crowncommercial.gov.uk/agreements/RM1557.13"
r_gc = requests.get(url_gc, timeout=10)
print("G-Cloud status:", r_gc.status_code)
csv_gc = [l for l in re.findall(r'href=["\']([^"\']+)["\']', r_gc.text) if '.csv' in l.lower() or 'supplier' in l.lower()]
print("G-Cloud supplier links:", csv_gc[:10])
