#!/usr/bin/env python3
"""
EndMile Venue Mock Widget Screenshot Generator
------------------------------------------------
Navigates to a venue's official website (auto-discovering their 'Visit' or 'Getting Here' page),
injects the EndMile Journey Planner widget directly into their DOM via DevTools evaluation,
and captures a crisp, high-resolution screenshot of their site showing EndMile seamlessly integrated.

Usage:
  # Single venue by URL and Name:
  python scripts/outreach/generate_venue_mock_screenshot.py --url https://www.oxfordplayhouse.com --name "Oxford Playhouse" --archetype theatre

  # Single venue by VenueID from master pipeline:
  python scripts/outreach/generate_venue_mock_screenshot.py --venue-id 345886715

  # Batch generate for top 5 approved venues:
  python scripts/outreach/generate_venue_mock_screenshot.py --batch --limit 5
"""

import os
import sys
import re
import argparse
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright

def get_master_pipeline_path() -> Path:
    candidates = [
        Path(r"C:\Users\isaac\OneDrive\Documents\EndMile\endmile_master_pipeline.xlsx"),
        Path(r"C:\Users\isaac\OneDrive\Desktop\endmile_master_pipeline.xlsx"),
        Path(r"C:\Users\isaac\Documents\endmile\endmile_master_pipeline.xlsx"),
    ]
    for p in candidates:
        if p.exists():
            return p
    return candidates[0]

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EXCEL_PATH = get_master_pipeline_path()
FALLBACK_EXCEL = Path(r"C:\Users\isaac\Downloads\endmile widget v4.xlsx")
OUTPUT_DIR = REPO_ROOT / "screenshots" / "venues"

VISIT_KEYWORDS = [
    "getting-here", "getting here", "getting_here",
    "your-visit", "your visit", "visiting-us", "visiting us", "visit-us", "visit us", "visiting", "visit",
    "how-to-find-us", "how to find us", "find-us", "find us",
    "plan-your-visit", "plan your visit",
    "directions", "location", "travel"
]

def clean_name(name: str) -> str:
    if not isinstance(name, str):
        return "Your Venue"
    cleaned = re.sub(r'\b(LIMITED|LTD|LLP|PLC|CIC|TRUST)\b', '', name, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def sanitize_slug(name: str) -> str:
    cleaned = re.sub(r'[^a-zA-Z0-9]+', '_', name.lower()).strip('_')
    return cleaned[:40]

def discover_visit_url(page, base_url: str) -> str:
    """Attempts to find the venue's dedicated 'getting here' or 'visit' page."""
    try:
        current_url = page.url
        # If current URL already looks like a visit page, stay here
        if any(k.replace(" ", "-") in current_url.lower() or k.replace(" ", "") in current_url.lower() for k in VISIT_KEYWORDS):
            return current_url

        # Search visible links on the page
        links = page.eval_on_selector_all("a[href]", """elements => {
            return elements.map(e => ({
                href: e.getAttribute('href'),
                text: (e.innerText || '').trim().toLowerCase()
            }));
        }""")

        # Priority 1: Exact Getting Here / Directions
        for item in links:
            href = item.get("href") or ""
            text = item.get("text") or ""
            if any(k in text for k in ["getting here", "how to find us", "directions", "travel"]):
                resolved = urllib.parse.urljoin(base_url, href)
                if resolved.startswith("http") and resolved != base_url:
                    return resolved

        # Priority 2: Visit / Visiting Us
        for item in links:
            href = item.get("href") or ""
            text = item.get("text") or ""
            if any(k in text for k in ["your visit", "visit us", "visiting", "plan your visit"]):
                resolved = urllib.parse.urljoin(base_url, href)
                if resolved.startswith("http") and resolved != base_url:
                    return resolved

        # Priority 3: Check href paths
        for item in links:
            href = item.get("href") or ""
            href_lower = href.lower()
            if any(k.replace(" ", "-") in href_lower for k in ["getting-here", "find-us", "visit", "directions"]):
                resolved = urllib.parse.urljoin(base_url, href)
                if resolved.startswith("http") and resolved != base_url:
                    return resolved

    except Exception as e:
        print(f"  [DISCOVER WARNING] Could not parse links: {e}")

    return base_url

def generate_widget_html(venue_name: str, archetype: str = "theatre") -> str:
    """Builds a pixel-perfect, realistic, high-converting EndMile mock widget card."""
    arch = archetype.lower()

    # Dynamic route examples based on sector
    if "gig" in arch or "music" in arch:
        mode1_title = "🚆 National Rail + Last Train"
        mode1_badge = "Late Curfew"
        mode1_time = "38 mins"
        mode1_cost = "£8.50"
        mode1_desc = "Last return departs 23:24 • 6 min walk from station to entrance doors."

        mode2_title = "🚗 Arterial Drop-Off & P&R"
        mode2_badge = "Easy Dispersal"
        mode2_time = "45 mins"
        mode2_cost = "£6.00"
        mode2_desc = "Designated taxi pickup & rapid dispersal corridor away from curfew congestion."

        mode3_title = "🚌 Night Transit Shuttle"
        mode3_badge = "Post-Show"
        mode3_time = "52 mins"
        mode3_cost = "£2.50"
        mode3_desc = "Direct night bus connections running until 00:30."

    elif "museum" in arch or "gallery" in arch:
        mode1_title = "🚆 Direct Rail + Step-Free Walk"
        mode1_badge = "Lowest CO₂"
        mode1_time = "42 mins"
        mode1_cost = "£11.20"
        mode1_desc = "Mainline station • Level step-free walking route directly to main atrium."

        mode2_title = "🚗 Park & Ride Hub"
        mode2_badge = "Avoids CAZ £8"
        mode2_time = "50 mins"
        mode2_cost = "£7.50"
        mode2_desc = "Fuel £4.50 + P&R Shuttle £3.00 • Avoids city Clean Air Zone & £22 multi-storey."

        mode3_title = "🚌 Metro / Bus Rapid"
        mode3_badge = "Frequent"
        mode3_time = "58 mins"
        mode3_cost = "£3.00"
        mode3_desc = "Stops outside entrance gates every 10 mins."

    elif "attraction" in arch or "zoo" in arch or "heritage" in arch:
        mode1_title = "🚗 Direct Bypass Highway"
        mode1_badge = "Avoids Queues"
        mode1_time = "48 mins"
        mode1_cost = "£8.20"
        mode1_desc = "Steers via arterial bypass directly to Overflow Gate B before 10am peak rush."

        mode2_title = "🚆 Mainline Rail + Shuttle Bus"
        mode2_badge = "Good Journey"
        mode2_time = "1h 05m"
        mode2_cost = "£13.50"
        mode2_desc = "Off-peak train + connecting heritage bus • 20% green admission discount."

        mode3_title = "🚌 Regional Coach Link"
        mode3_badge = "Family Saver"
        mode3_time = "1h 20m"
        mode3_cost = "£6.00"
        mode3_desc = "Direct service drops at visitor welcome centre."

    else: # Default Theatres / Arts
        mode1_title = "🚆 National Rail (GWR / Avanti)"
        mode1_badge = "Lowest CO₂"
        mode1_time = "52 mins"
        mode1_cost = "£14.20"
        mode1_desc = "Direct rail • 7 min step-free walk straight to foyer and pre-show bar."

        mode2_title = "🚗 Park & Ride Shuttle"
        mode2_badge = "Save £16 vs City"
        mode2_time = "1h 10m"
        mode2_cost = "£8.50"
        mode2_desc = "Fuel £5.00 + Bus £3.50 • Guaranteed parking, avoids evening multi-storey queue."

        mode3_title = "🚌 Express Coach Service"
        mode3_badge = "Every 15m"
        mode3_time = "1h 25m"
        mode3_cost = "£9.00"
        mode3_desc = "Departs central station • 3 min walk to auditorium entrance."

    return f"""
<div id="endmile-mock-widget" style="
    margin: 30px 0 45px 0 !important;
    padding: 24px 28px !important;
    background: #ffffff !important;
    border: 2px solid #4f46e5 !important;
    border-radius: 18px !important;
    box-shadow: 0 12px 36px -4px rgba(79, 70, 229, 0.18), 0 4px 12px -2px rgba(0,0,0,0.08) !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    color: #0f172a !important;
    max-width: 920px !important;
    width: 100% !important;
    box-sizing: border-box !important;
    position: relative !important;
    z-index: 9999 !important;
    display: block !important;
    text-align: left !important;
">
    <!-- Header Bar -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid #e2e8f0; padding-bottom: 14px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="background: linear-gradient(135deg, #4f46e5, #3730a3); color: white; font-weight: 800; font-size: 14px; width: 28px; height: 28px; border-radius: 8px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(79,70,229,0.3);">E</div>
            <div>
                <span style="font-size: 15px; font-weight: 700; color: #1e1b4b; display: block; line-height: 1.2;">EndMile Journey Intelligence</span>
                <span style="font-size: 11px; color: #64748b;">Interactive Visit Planner Preview</span>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="background: #e0e7ff; color: #3730a3; font-size: 11px; font-weight: 700; text-transform: uppercase; padding: 4px 10px; border-radius: 999px;">1-Line Embed</span>
            <span style="font-size: 12px; color: #475569; font-weight: 600;">Destination: <strong>{venue_name}</strong></span>
        </div>
    </div>

    <!-- Search input simulation -->
    <div style="margin-bottom: 20px;">
        <label style="display: block; font-size: 13px; font-weight: 600; color: #1e293b; margin-bottom: 6px;">Where are you travelling from?</label>
        <div style="display: flex; gap: 10px; align-items: center;">
            <div style="position: relative; flex: 1;">
                <input type="text" value="London / Regional Station (Example)" readonly style="
                    width: 100%; height: 46px; padding: 0 16px; font-size: 14px; border: 1.5px solid #cbd5e1; border-radius: 10px; background: #f8fafc; color: #1e293b; font-weight: 500; box-sizing: border-box; outline: none;
                " />
            </div>
            <button style="
                background: #4f46e5; color: white; font-weight: 700; font-size: 14px; height: 46px; padding: 0 22px; border-radius: 10px; border: none; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 4px rgba(79,70,229,0.25);
            ">Compare Routes →</button>
        </div>
    </div>

    <!-- Door-to-Door Journey Comparison Cards -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 14px; margin-bottom: 18px;">
        <!-- Card 1 -->
        <div style="border: 2px solid #6366f1; background: #f5f3ff; border-radius: 12px; padding: 14px; box-shadow: 0 2px 6px rgba(99,102,241,0.08);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-weight: 700; font-size: 13px; color: #4338ca;">{mode1_title}</span>
                <span style="background: #dcfce7; color: #15803d; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px;">{mode1_badge}</span>
            </div>
            <div style="display: flex; align-items: baseline; gap: 8px; margin-bottom: 6px;">
                <span style="font-size: 20px; font-weight: 800; color: #0f172a;">{mode1_time}</span>
                <span style="font-size: 15px; font-weight: 700; color: #059669;">{mode1_cost}</span>
            </div>
            <div style="font-size: 11px; color: #475569; line-height: 1.45;">
                {mode1_desc}
            </div>
        </div>

        <!-- Card 2 -->
        <div style="border: 1px solid #cbd5e1; background: #ffffff; border-radius: 12px; padding: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-weight: 700; font-size: 13px; color: #0f172a;">{mode2_title}</span>
                <span style="background: #e0f2fe; color: #0369a1; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px;">{mode2_badge}</span>
            </div>
            <div style="display: flex; align-items: baseline; gap: 8px; margin-bottom: 6px;">
                <span style="font-size: 20px; font-weight: 800; color: #0f172a;">{mode2_time}</span>
                <span style="font-size: 15px; font-weight: 700; color: #0f172a;">{mode2_cost}</span>
            </div>
            <div style="font-size: 11px; color: #475569; line-height: 1.45;">
                {mode2_desc}
            </div>
        </div>

        <!-- Card 3 -->
        <div style="border: 1px solid #cbd5e1; background: #ffffff; border-radius: 12px; padding: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-weight: 700; font-size: 13px; color: #0f172a;">{mode3_title}</span>
                <span style="background: #f1f5f9; color: #475569; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px;">{mode3_badge}</span>
            </div>
            <div style="display: flex; align-items: baseline; gap: 8px; margin-bottom: 6px;">
                <span style="font-size: 20px; font-weight: 800; color: #0f172a;">{mode3_time}</span>
                <span style="font-size: 15px; font-weight: 700; color: #0f172a;">{mode3_cost}</span>
            </div>
            <div style="font-size: 11px; color: #475569; line-height: 1.45;">
                {mode3_desc}
            </div>
        </div>
    </div>

    <!-- Trust and Features Footer -->
    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; font-size: 11px; color: #64748b; border-top: 1px solid #f1f5f9; padding-top: 10px;">
        <div style="display: flex; gap: 14px; flex-wrap: wrap;">
            <span>✓ Verified step-free public transport</span>
            <span>✓ Real parking tariffs & Park & Ride</span>
            <span>✓ Scope 3 carbon telemetry automated</span>
        </div>
        <div style="font-weight: 700; color: #4f46e5;">
            Powered by EndMile • £0 Setup • 1-Line Embed
        </div>
    </div>
</div>
"""

def capture_venue_mock_screenshot(
    url: str,
    venue_name: str,
    venue_id: str = "",
    archetype: str = "theatre",
    output_path: str = None
) -> str:
    """
    Spawns headless Chromium, navigates to venue site, finds the visit/getting-here section,
    injects the widget into their DOM, and captures a high-resolution PNG screenshot.
    """
    if not url.startswith("http"):
        url = "https://" + url

    slug = sanitize_slug(venue_name)
    vid_part = f"{venue_id}_" if venue_id else ""
    if not output_path:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_file = OUTPUT_DIR / f"{vid_part}{slug}.png"
    else:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n[SCREENSHOT] Processing '{venue_name}'...")
    print(f"  Target URL: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Desktop 1280x850 at 1.5x pixel ratio for sharp retina text
        context = browser.new_context(
            viewport={'width': 1280, 'height': 850},
            device_scale_factor=1.5,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            print("  Navigating to initial page...")
            page.goto(url, wait_until="domcontentloaded", timeout=15000)

            # Discover if there is a deeper visit / directions page
            visit_page_url = discover_visit_url(page, url)
            if visit_page_url != url:
                print(f"  Discovered dedicated visit page: {visit_page_url}")
                page.goto(visit_page_url, wait_until="domcontentloaded", timeout=15000)

            # Let page settle briefly
            page.wait_for_timeout(1000)

            # Dismiss cookie banners via button click and DOM removal
            try:
                for btn_text in ["I Accept Cookies", "Accept All", "Accept Cookies", "Accept all", "Agree", "I Accept", "Allow All", "Got it", "OK"]:
                    btn = page.locator(f"button:has-text('{btn_text}'), a:has-text('{btn_text}')")
                    if btn.count() > 0:
                        btn.first.click(timeout=1000)
                        page.wait_for_timeout(300)
                        break
            except Exception:
                pass

            page.evaluate("""() => {
                const selectors = [
                    '#onetrust-consent-sdk', '.cc-banner', '#cookie-banner', '.cookie-notice',
                    '.cookie-bar', '.cky-consent-container', '#CybotCookiebotDialog',
                    '[id*="cookie" i]', '[class*="cookie" i]', '[id*="consent" i]',
                    '.popup-overlay', '.modal-backdrop', '[role="dialog"]'
                ];
                selectors.forEach(sel => {
                    try {
                        document.querySelectorAll(sel).forEach(el => {
                            if ((el.innerText || '').toLowerCase().includes('cookie') || el.classList.contains('modal-backdrop')) {
                                el.remove();
                            }
                        });
                    } catch(e) {}
                });
            }""")

            widget_html = generate_widget_html(venue_name, archetype)

            # Inject widget into the page DOM (strictly inside main content area, avoiding nav/header)
            injected = page.evaluate("""(html) => {
                // Priority 1: Main page H1 containing directions/visit keywords (e.g. 'Getting Here', 'Your Visit')
                const allH1s = Array.from(document.querySelectorAll('h1')).filter(h => {
                    const inNav = h.closest('nav, .site-header, .c-site-header, .menu, .o-nav');
                    return !inNav;
                });
                for (const h of allH1s) {
                    const txt = (h.innerText || '').toLowerCase().trim();
                    if (txt.includes('getting here') || txt.includes('visit') || txt.includes('find us') || txt.includes('directions')) {
                        // Match BEM headers like c-page-header, page-header, hero, banner
                        const target = h.closest('[class*="page-header" i], [class*="hero" i], [class*="banner" i]') || h;
                        target.insertAdjacentHTML('afterend', html);
                        return { found: true, target: 'Main H1 Header (' + txt.substring(0, 30) + ')', isTopBanner: true };
                    }
                }

                // Priority 2: Find main content root
                const mainRoot = document.querySelector('main, article, #site-main, #main, #content, .o-page-grid__content, .page-content, .entry-content') || document.body;

                // Priority 3: Static map element (replace or prepend to map)
                const mapEl = mainRoot.querySelector('iframe[src*="google.com/maps"], .map, #map, [class*="map__" i]');
                if (mapEl && mapEl.parentElement) {
                    mapEl.insertAdjacentHTML('beforebegin', html);
                    return { found: true, target: 'Above static map (' + mapEl.tagName + ')', isTopBanner: false };
                }

                // Priority 4: In-content Heading containing directions/travel/visit keywords
                const headings = Array.from(mainRoot.querySelectorAll('h1, h2, h3, h4')).filter(h => {
                    return !h.closest('header, nav, .site-header, .c-site-header, .menu, .sidebar, .o-nav');
                });

                for (const h of headings) {
                    const txt = (h.innerText || '').toLowerCase().trim();
                    if (txt.includes('getting here') || txt.includes('find us') || txt.includes('directions') || txt.includes('how to find') || txt.includes('by train') || txt.includes('by car') || txt.includes('your visit')) {
                        h.insertAdjacentHTML('afterend', html);
                        return { found: true, target: h.tagName + ' (' + txt.substring(0, 30) + ')', isTopBanner: false };
                    }
                }

                // Priority 5: First child of main container
                if (mainRoot !== document.body) {
                    mainRoot.insertAdjacentHTML('afterbegin', html);
                    return { found: true, target: mainRoot.tagName + ' (main content root)', isTopBanner: false };
                }

                // Fallback: Body
                document.body.insertAdjacentHTML('afterbegin', html);
                return { found: true, target: 'body', isTopBanner: false };
            }""", widget_html)

            print(f"  Widget injected successfully into {injected.get('target', 'DOM')}")

            # Scroll so the widget is nicely framed with the venue's header/nav bar visible
            is_top = injected.get('isTopBanner', False)
            page.evaluate(f"""() => {{
                const widget = document.getElementById('endmile-mock-widget');
                if (widget) {{
                    if ({str(is_top).lower()}) {{
                        // Scroll to top or just slight scroll so venue header nav + banner + widget are all in frame
                        window.scrollTo({{ top: 0, behavior: 'instant' }});
                    }} else {{
                        const rect = widget.getBoundingClientRect();
                        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                        window.scrollTo({{
                            top: Math.max(0, scrollTop + rect.top - 140),
                            behavior: 'instant'
                        }});
                    }}
                }}
            }}""")

            page.wait_for_timeout(500)

            # Take the screenshot
            page.screenshot(path=str(output_file))
            print(f"  [OK] Saved mock screenshot to: {output_file}")
            browser.close()
            return str(output_file)

        except Exception as e:
            print(f"  [ERROR] Failed to capture screenshot: {e}")
            browser.close()
            return ""

def load_venues_df() -> pd.DataFrame:
    if EXCEL_PATH.exists():
        try:
            return pd.read_excel(EXCEL_PATH, sheet_name="Venue Widget Pipeline")
        except Exception:
            pass
    if FALLBACK_EXCEL.exists():
        return pd.read_excel(FALLBACK_EXCEL)
    raise FileNotFoundError("Master pipeline spreadsheet not found.")

def main():
    parser = argparse.ArgumentParser(description="EndMile Venue Mock Widget Screenshot Generator")
    parser.add_argument("--url", type=str, default="", help="Venue website URL")
    parser.add_argument("--name", type=str, default="", help="Venue name")
    parser.add_argument("--venue-id", type=str, default="", help="Venue ID to lookup in pipeline")
    parser.add_argument("--archetype", type=str, default="theatre", help="Sector archetype (theatre, museum, gig, attraction, university)")
    parser.add_argument("--out", type=str, default="", help="Custom output PNG path")
    parser.add_argument("--batch", action="store_true", help="Batch generate screenshots for approved venues")
    parser.add_argument("--limit", type=int, default=5, help="Limit for batch generation")
    args = parser.parse_args()

    print("=" * 70)
    print("   ENDMILE VENUE MOCK WIDGET SCREENSHOT GENERATOR")
    print("=" * 70)

    if args.url and args.name:
        capture_venue_mock_screenshot(
            url=args.url,
            venue_name=clean_name(args.name),
            archetype=args.archetype,
            output_path=args.out
        )
        return

    df = load_venues_df()

    if args.venue_id:
        match = df[df["VenueID"].astype(str) == str(args.venue_id)]
        if match.empty:
            print(f"Venue ID {args.venue_id} not found in pipeline.")
            return
        row = match.iloc[0]
        url = str(row.get("Website") or row.get("Domain") or "")
        name = clean_name(row.get("VenueName") or row.get("Name"))
        archetype = str(row.get("Archetype", "theatre"))
        capture_venue_mock_screenshot(url, name, venue_id=str(args.venue_id), archetype=archetype, output_path=args.out)
        return

    if args.batch:
        if "ManualApproval" in df.columns:
            targets = df[df["ManualApproval"] == "Approved"].copy()
        else:
            targets = df.copy()

        has_web = targets["Website"].notna() | targets.get("Domain", pd.Series()).notna()
        targets = targets[has_web].head(args.limit)

        print(f"Batch generating screenshots for {len(targets)} venue(s)...\n")
        generated = []
        for i, (_, row) in enumerate(targets.iterrows(), 1):
            vid = str(row.get("VenueID") or "")
            name = clean_name(row.get("VenueName") or row.get("Name"))
            url = str(row.get("Website") or row.get("Domain") or "")
            archetype = str(row.get("Archetype", "theatre"))

            out = capture_venue_mock_screenshot(url, name, venue_id=vid, archetype=archetype)
            if out:
                generated.append(out)

        print(f"\n[COMPLETE] Successfully generated {len(generated)} screenshot(s) in {OUTPUT_DIR}")
        return

    print("Please specify either --url and --name, --venue-id, or --batch.")

if __name__ == "__main__":
    main()
