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
    output_path: str = None,
    example_mode: bool = False,
    display_name: str = "",
    origin_name: str = "Reading Station"
) -> str:
    """
    Spawns headless Chromium, navigates to venue site, finds the visit/getting-here section,
    injects the widget into their DOM, pre-populates multimodal results client-side (£0.00 OJP cost),
    and captures a high-resolution PNG screenshot.
    """
    if not url.startswith("http"):
        url = "https://" + url

    target_display_name = display_name if display_name else ("Example Venue" if example_mode else venue_name)
    slug = sanitize_slug(venue_name)
    vid_part = f"{venue_id}_" if venue_id else ""
    if not output_path:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_file = OUTPUT_DIR / f"{vid_part}{slug}.png"
    else:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n[SCREENSHOT] Processing '{venue_name}' (Display: '{target_display_name}')...")
    print(f"  Target URL: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Desktop 1280x1600 at 1.5x pixel ratio for retina sharpness with full pre-populated results
        context = browser.new_context(
            viewport={'width': 1280, 'height': 1600},
            device_scale_factor=1.5,
            bypass_csp=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # Unblock cross-origin embedding on guide.endmilerouting.co.uk
        def unblock_embed_csp(route):
            response = route.fetch()
            headers = response.headers.copy()
            if 'content-security-policy' in headers:
                headers['content-security-policy'] = headers['content-security-policy'].replace(
                    "frame-ancestors https://endmilerouting.co.uk https://seleniumbase.io",
                    "frame-ancestors *"
                )
            headers.pop('x-frame-options', None)
            route.fulfill(response=response, headers=headers)

        page.route("**/embed/**", unblock_embed_csp)

        try:
            print("  Navigating to initial page...")
            page.goto(url, wait_until="domcontentloaded", timeout=20000)

            # Discover if there is a deeper visit / directions page
            visit_page_url = discover_visit_url(page, url)
            if visit_page_url != url:
                print(f"  Discovered dedicated visit page: {visit_page_url}")
                page.goto(visit_page_url, wait_until="domcontentloaded", timeout=20000)

            # Let page settle
            page.wait_for_timeout(1500)

            # Dismiss all cookie banners (Civic UK Cookie Control #ccc, OneTrust, banners, overlays)
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
                    '#ccc', '#ccc-module', '#ccc-overlay', '#ccc-content', '.ccc-widget',
                    '#onetrust-consent-sdk', '.cc-banner', '#cookie-banner', '.cookie-notice',
                    '.cookie-bar', '.cky-consent-container', '#CybotCookiebotDialog',
                    '[id*="cookie" i]', '[class*="cookie" i]', '[id*="consent" i]',
                    '.popup-overlay', '.modal-backdrop', '[role="dialog"]', '[aria-label*="cookie" i]'
                ];
                selectors.forEach(sel => {
                    try {
                        document.querySelectorAll(sel).forEach(el => el.remove());
                    } catch(e) {}
                });
            }""")

            # Inject the real EndMile LiveWidget iframe cleanly into the venue's natural content layout
            injected = page.evaluate("""(data) => {
                const { venueName } = data;
                
                // Priority 1: Find content blocks within main content area
                const contentRoots = [
                    document.querySelector('.o-page-grid__content'),
                    document.querySelector('main article'),
                    document.querySelector('#site-main'),
                    document.querySelector('#main'),
                    document.querySelector('main'),
                    document.querySelector('#content'),
                    document.querySelector('.page-content'),
                    document.querySelector('.entry-content')
                ].filter(Boolean);

                const mainRoot = contentRoots[0] || document.body;

                // Priority 2: Look for an intro address/location text block or static map
                // In sites like Oxford Playhouse, block-70024 is the intro address paragraph
                // and block-1041215 is the static map figure.
                const allDivs = Array.from(mainRoot.querySelectorAll('div, section, article, p')).filter(d => {
                    return !d.closest('header, nav, footer, .c-site-header, .site-header');
                });

                // Find intro paragraph mentioning address / postcode / greenest way
                let targetEl = null;
                let insertMethod = 'afterend';
                let colClass = '';

                // Check for intro text block
                for (const d of allDivs) {
                    const txt = (d.innerText || '').toLowerCase();
                    if ((txt.includes('situated in') || txt.includes('located in') || txt.includes('postcode') || txt.includes('greenest way') || txt.includes('public transport')) && txt.length < 500) {
                        targetEl = d;
                        insertMethod = 'afterend';
                        // Copy column classes from host block if available (e.g. Oxford Playhouse h-colstart--3)
                        colClass = d.className || '';
                        break;
                    }
                }

                // If not found, look for first transit heading (e.g. By Train, Park & Ride, By Car)
                if (!targetEl) {
                    const headings = Array.from(mainRoot.querySelectorAll('h2, h3, h4')).filter(h => {
                        return !h.closest('header, nav, .site-header');
                    });
                    for (const h of headings) {
                        const txt = (h.innerText || '').toLowerCase();
                        if (txt.includes('by train') || txt.includes('park & ride') || txt.includes('by car') || txt.includes('getting here') || txt.includes('public transport')) {
                            const block = h.closest('.o-block, [class*="block" i], .grid__item') || h;
                            targetEl = block;
                            insertMethod = 'beforebegin';
                            colClass = block.className || '';
                            break;
                        }
                    }
                }

                // Fallback to static map element
                if (!targetEl) {
                    const mapEl = mainRoot.querySelector('iframe[src*="maps"], .map, #map, [class*="map" i], figure');
                    if (mapEl) {
                        targetEl = mapEl;
                        insertMethod = 'beforebegin';
                    }
                }

                // Final fallback
                if (!targetEl) {
                    targetEl = mainRoot.firstElementChild || mainRoot;
                    insertMethod = 'afterbegin';
                }

                // Create wrapper element
                const wrapper = document.createElement('div');
                wrapper.id = 'endmile-widget-wrapper';
                if (colClass) {
                    wrapper.className = colClass;
                }
                wrapper.style.margin = '20px 0 28px 0';
                wrapper.style.width = '100%';
                wrapper.style.boxSizing = 'border-box';

                // Real EndMile LiveWidget Iframe
                const iframe = document.createElement('iframe');
                iframe.id = 'endmile-live-iframe';
                iframe.src = 'https://guide.endmilerouting.co.uk/embed/em_7Kx2pQ9mV4cN8rT6/';
                iframe.style.width = '100%';
                iframe.style.height = '1040px';
                iframe.style.border = 'none';
                iframe.style.borderRadius = '16px';
                iframe.style.boxShadow = '0 8px 30px rgba(0,0,0,0.08), 0 2px 8px rgba(0,0,0,0.04)';
                iframe.scrolling = 'no';

                wrapper.appendChild(iframe);

                if (insertMethod === 'afterend') {
                    targetEl.insertAdjacentElement('afterend', wrapper);
                } else if (insertMethod === 'beforebegin') {
                    targetEl.insertAdjacentElement('beforebegin', wrapper);
                } else {
                    targetEl.insertAdjacentElement('afterbegin', wrapper);
                }

                return {
                    found: true,
                    target: targetEl.tagName + (targetEl.id ? '#' + targetEl.id : '') + ' (' + insertMethod + ')'
                };
            }""", {"venueName": venue_name})

            print(f"  Widget injected successfully into {injected.get('target', 'DOM')}")

            # Wait for iframe to render
            page.wait_for_timeout(3500)

            # Update venue name & pre-populate results inside the iframe
            for frame in page.frames:
                if "guide.endmilerouting" in frame.url:
                    try:
                        frame.evaluate("""(config) => {
                            const venue = config.venueName;
                            const origin = config.originName;

                            // Update header labels
                            const p = document.querySelector('header p');
                            if (p) p.innerText = 'PLAN VISITING';
                            const h1 = document.querySelector('h1');
                            if (h1) h1.innerText = venue;

                            // Pre-fill search input
                            const input = document.getElementById('postcode-input');
                            if (input) input.value = origin;

                            // Results heading
                            const displayOrigin = document.getElementById('display-postcode');
                            if (displayOrigin) displayOrigin.innerText = origin;
                            const resultsHeading = document.getElementById('results-heading-box');
                            if (resultsHeading) {
                                const spans = resultsHeading.querySelectorAll('span');
                                if (spans.length > 0) spans[0].innerText = origin;
                                if (spans.length > 1) spans[1].innerText = venue;
                            }

                            // Reveal results container and shell
                            const resultsContainer = document.getElementById('widget-results');
                            if (resultsContainer) {
                                resultsContainer.classList.remove('hidden');
                                resultsContainer.style.display = 'flex';
                            }
                            const liveShell = document.getElementById('live-results-shell');
                            if (liveShell) {
                                liveShell.classList.remove('hidden');
                                liveShell.classList.remove('lg:grid-cols-12');
                            }
                            const sortControls = document.getElementById('sort-controls');
                            if (sortControls) sortControls.classList.remove('hidden');

                            // Inject authentic multimodal route cards
                            const routeList = document.getElementById('route-list');
                            if (routeList) {
                                routeList.innerHTML = `
                                    <!-- Card 1: National Rail (Recommended) -->
                                    <article class="live-route-card shrink-0 text-left bg-white border border-indigo-600 shadow-md ring-2 ring-indigo-500/20 rounded-xl flex flex-col transition-all cursor-pointer relative overflow-hidden" data-route-id="r1">
                                        <div class="p-3.5 sm:p-4 flex flex-col gap-2.5 flex-1">
                                            <div class="flex items-start justify-between gap-3">
                                                <div class="min-w-0 flex-1">
                                                    <div class="font-data-mono text-2xl font-bold text-slate-900 tracking-tight leading-none">£9.20</div>
                                                    <div class="text-[13px] font-medium text-slate-500 truncate mt-1">Via National Rail (GWR Direct) • 8-min walk to venue</div>
                                                </div>
                                                <div class="text-right shrink-0">
                                                    <div class="font-data-mono text-lg font-bold text-slate-900 leading-none">28m</div>
                                                </div>
                                            </div>

                                            <!-- Timeline Schematic Bar -->
                                            <div class="relative w-full h-8 sm:h-9 rounded-lg overflow-hidden flex items-stretch border border-slate-200/80 bg-slate-100 shadow-2xs select-none">
                                                <div style="flex: 7 1 0%; background-color: #880038;" class="relative flex items-center justify-center pl-2 pr-1 text-white gap-1.5 font-bold text-xs">
                                                    <span>🚆 GWR Train</span>
                                                    <span class="text-[10px] font-normal opacity-90">20 min</span>
                                                </div>
                                                <div style="flex: 3 1 0%; background-color: #475569;" class="relative flex items-center justify-center pl-1 pr-2 text-white gap-1 font-bold text-xs">
                                                    <span>🚶 Walk</span>
                                                    <span class="text-[10px] font-normal opacity-90">8 min</span>
                                                </div>
                                            </div>

                                            <!-- Badges & Action Row -->
                                            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 pt-0.5">
                                                <div class="flex flex-wrap items-center gap-1.5">
                                                    <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">
                                                        <span>✓ Low Risk</span>
                                                    </span>
                                                    <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">
                                                        <span>🌱 Saves 74% CO₂ vs driving</span>
                                                    </span>
                                                    <span class="bg-indigo-600 text-white text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider">
                                                        RECOMMENDED
                                                    </span>
                                                </div>
                                                <div class="flex items-center gap-1.5 shrink-0">
                                                    <span class="inline-flex items-center justify-center gap-1 rounded-md border border-blue-200 bg-blue-50 px-2.5 py-1 text-[11px] font-bold text-blue-700 shadow-2xs">
                                                        Book train ↗
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    </article>

                                    <!-- Card 2: Park & Ride (Best Value) -->
                                    <article class="live-route-card shrink-0 text-left bg-white border border-slate-200 hover:border-slate-300 shadow-xs rounded-xl flex flex-col transition-all cursor-pointer relative overflow-hidden" data-route-id="r2">
                                        <div class="p-3.5 sm:p-4 flex flex-col gap-2.5 flex-1">
                                            <div class="flex items-start justify-between gap-3">
                                                <div class="min-w-0 flex-1">
                                                    <div class="font-data-mono text-2xl font-bold text-slate-900 tracking-tight leading-none">£5.00</div>
                                                    <div class="text-[13px] font-medium text-slate-500 truncate mt-1">Via Seacourt P&R + 400 Rapid Shuttle • Drops on high street</div>
                                                </div>
                                                <div class="text-right shrink-0">
                                                    <div class="font-data-mono text-lg font-bold text-slate-900 leading-none">36m</div>
                                                </div>
                                            </div>

                                            <!-- Timeline Schematic Bar -->
                                            <div class="relative w-full h-8 sm:h-9 rounded-lg overflow-hidden flex items-stretch border border-slate-200/80 bg-slate-100 shadow-2xs select-none">
                                                <div style="flex: 5 1 0%; background-color: #3f3f46;" class="relative flex items-center justify-center pl-2 pr-1 text-white gap-1 font-bold text-xs">
                                                    <span>🚗 Drive to P&R</span>
                                                    <span class="text-[10px] font-normal opacity-90">22 min</span>
                                                </div>
                                                <div style="flex: 4 1 0%; background-color: #30227d;" class="relative flex items-center justify-center pl-1 pr-1 text-white gap-1 font-bold text-xs">
                                                    <span>🚌 P&R Shuttle</span>
                                                    <span class="text-[10px] font-normal opacity-90">11 min</span>
                                                </div>
                                                <div style="flex: 2 1 0%; background-color: #475569;" class="relative flex items-center justify-center pl-1 pr-2 text-white gap-1 font-bold text-xs">
                                                    <span>🚶 Walk</span>
                                                    <span class="text-[10px] font-normal opacity-90">3 min</span>
                                                </div>
                                            </div>

                                            <!-- Badges & Action Row -->
                                            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 pt-0.5">
                                                <div class="flex flex-wrap items-center gap-1.5">
                                                    <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold bg-amber-50 text-amber-800 border border-amber-200">
                                                        <span>🅿️ Avoids City CAZ & £12 Parking</span>
                                                    </span>
                                                    <span class="bg-slate-900 text-white text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider">
                                                        BEST VALUE
                                                    </span>
                                                </div>
                                                <div class="flex items-center gap-1.5 shrink-0">
                                                    <span class="inline-flex items-center justify-center gap-1 rounded-md border border-blue-200 bg-blue-50 px-2.5 py-1 text-[11px] font-bold text-blue-700 shadow-2xs">
                                                        Check parking ↗
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    </article>

                                    <!-- Card 3: Direct Drive (Baseline) -->
                                    <article class="live-route-card shrink-0 text-left bg-white border border-slate-200 hover:border-slate-300 shadow-xs rounded-xl flex flex-col transition-all cursor-pointer relative overflow-hidden opacity-90" data-route-id="r3">
                                        <div class="p-3.5 sm:p-4 flex flex-col gap-2.5 flex-1">
                                            <div class="flex items-start justify-between gap-3">
                                                <div class="min-w-0 flex-1">
                                                    <div class="font-data-mono text-2xl font-bold text-slate-900 tracking-tight leading-none">£18.50</div>
                                                    <div class="text-[13px] font-medium text-slate-500 truncate mt-1">Via Direct Drive (Fuel £6.50 + City Multi-Storey £12.00)</div>
                                                </div>
                                                <div class="text-right shrink-0">
                                                    <div class="font-data-mono text-lg font-bold text-slate-900 leading-none">48m</div>
                                                </div>
                                            </div>

                                            <!-- Timeline Schematic Bar -->
                                            <div class="relative w-full h-8 sm:h-9 rounded-lg overflow-hidden flex items-stretch border border-slate-200/80 bg-slate-100 shadow-2xs select-none">
                                                <div style="flex: 8 1 0%; background-color: #3f3f46;" class="relative flex items-center justify-center pl-2 pr-1 text-white gap-1 font-bold text-xs">
                                                    <span>🚗 Direct Drive</span>
                                                    <span class="text-[10px] font-normal opacity-90">42 min</span>
                                                </div>
                                                <div style="flex: 2 1 0%; background-color: #475569;" class="relative flex items-center justify-center pl-1 pr-2 text-white gap-1 font-bold text-xs">
                                                    <span>🚶 Walk</span>
                                                    <span class="text-[10px] font-normal opacity-90">6 min</span>
                                                </div>
                                            </div>

                                            <!-- Badges & Action Row -->
                                            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 pt-0.5">
                                                <div class="flex flex-wrap items-center gap-1.5">
                                                    <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold bg-slate-100 text-slate-700 border border-slate-200">
                                                        <span>🚗 8.4 kg CO₂ (Baseline)</span>
                                                    </span>
                                                    <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold bg-slate-100 text-slate-600 border border-slate-200">
                                                        <span>City Centre Congestion</span>
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    </article>
                                `;
                            }
                        }""", {"venueName": target_display_name, "originName": origin_name})
                        print(f"  [IFRAME] Configured venue title to '{target_display_name}' & pre-populated 3 multimodal routes (£0.00 OJP)")
                    except Exception as e:
                        print(f"  [IFRAME WARNING] Could not update title inside frame: {e}")

            page.wait_for_timeout(500)

            # Scroll framing: Position viewport so the venue's top header, banner, and widget are framed
            page.evaluate("""() => {
                const wrapper = document.getElementById('endmile-widget-wrapper');
                if (wrapper) {
                    const rect = wrapper.getBoundingClientRect();
                    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                    const targetTop = scrollTop + rect.top;
                    // If widget is near the top (e.g. under the hero banner), stay at 0 so the venue logo and title are in view
                    if (targetTop < 750) {
                        window.scrollTo({ top: 0, behavior: 'instant' });
                    } else {
                        window.scrollTo({
                            top: Math.max(0, targetTop - 250),
                            behavior: 'instant'
                        });
                    }
                }
            }""")

            page.wait_for_timeout(500)

            # Take the screenshot
            page.screenshot(path=str(output_file))
            print(f"  [OK] Saved real widget mock screenshot to: {output_file}")
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
        try:
            return pd.read_excel(FALLBACK_EXCEL)
        except Exception:
            pass
    print("[INFO] No Excel pipeline found. Running in standalone mode.")
    return pd.DataFrame()


def main():
    parser = argparse.ArgumentParser(description="EndMile Venue Mock Widget Screenshot Generator")
    parser.add_argument("--url", type=str, default="", help="Venue website URL")
    parser.add_argument("--name", type=str, default="", help="Venue name")
    parser.add_argument("--display-name", type=str, default="", help="Custom display name in widget header")
    parser.add_argument("--example", action="store_true", help="Set widget title to Example Venue / universal mock template")
    parser.add_argument("--origin", type=str, default="Reading Station", help="Pre-populated origin station/town")
    parser.add_argument("--venue-id", type=str, default="", help="Venue ID to lookup in pipeline")
    parser.add_argument("--archetype", type=str, default="theatre", help="Sector archetype (theatre, museum, gig, attraction, university)")
    parser.add_argument("--out", type=str, default="", help="Custom output PNG path")
    parser.add_argument("--batch", action="store_true", help="Batch generate screenshots for approved venues")
    parser.add_argument("--limit", type=int, default=5, help="Limit for batch generation")
    args = parser.parse_args()

    print("=" * 70)
    print("   ENDMILE VENUE MOCK WIDGET SCREENSHOT GENERATOR")
    print("=" * 70)

    if args.url and (args.name or args.example):
        vname = clean_name(args.name) if args.name else "Example Venue"
        capture_venue_mock_screenshot(
            url=args.url,
            venue_name=vname,
            archetype=args.archetype,
            output_path=args.out,
            example_mode=args.example,
            display_name=args.display_name,
            origin_name=args.origin
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
