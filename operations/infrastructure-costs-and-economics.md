# Infrastructure Costs, Unit Economics & Scaling Budget

Detailed financial accounting of EndMile's operating expenses, cost-per-search economics, and scaling milestones.

---

## 1. Current Monthly Infrastructure Burn

EndMile operates on an ultra-efficient lean infrastructure model utilizing self-hosted routing engines rather than expensive third-party mapping APIs.

| Service / Provider | Purpose | Monthly Cost (GBP) | Annual Cost (GBP) |
|---|---|---|---|
| **Contabo Cloud VPS 30** | Dedicated host for OSRM, MOTIS, Node.js, Postgres, Redis, Caddy | £16.00 | £192.00 |
| **National Rail OJP API** | Live GB train itineraries, fares, and calling points | ~£20.00–£25.00 | ~£250.00 |
| **20i.com Domain & DNS** | `endmilerouting.co.uk` domain registration & DNS management | ~£0.85 | ~£10.20 |
| **Google Maps API** | Address autocomplete & geocoding (Places API) | Free tier ($200 monthly credit) | £0.00 |
| **Supabase** | Cloud Auth & identity store (free tier) | £0.00 | £0.00 |
| **Resend** | Transactional email relay for authentication | Free tier (up to 3,000 emails/mo) | £0.00 |
| **GitHub Actions** | CI/CD automated test runs and VPS deploys | Free tier (2,000 min/mo) | £0.00 |
| **Total Monthly Burn** | | **~£37.00 – £45.00** | **~£452.00** |

---

## 2. Unit Economics of a Journey Search

### National Rail OJP Cost Breakdown
- **Rate Card:** **£0.00042 per individual API call** (less than half of 1/10th of a penny).
- **Standard Search Pipeline:**
  - Main OJP calls: 29.8 calls / search
  - Calling points calls: 3.9 calls / search
  - Total calls: 33.7 calls / search
  - **Standard Cost:** **1.42p per search**
- **Streaming Multi-Hub Search Pipeline:**
  - Multi-hub pairs (up to 9 origin × 9 destination hubs): 52.3 calls / search
  - Real-time calling points enrichment (top 20 routes): 6.8 calls / search
  - Total calls: 59.1 calls / search
  - **Streaming Cost:** **2.48p per search**
- **Blended Weighted Average:** **2.19p per search** across production searches.

### Caching ROI
- Searches are bucketed to 5-minute departure windows (`ARRIVAL_BUCKET_MS = 300,000`).
- The `CachedTrainPlanner` caches identical hub pairs in Redis with a 5-minute TTL.
- For high-volume corridors (e.g. Manchester $\to$ Leeds, London $\to$ Birmingham), cache hits eliminate **100% of repeated OJP charges**.

---

## 3. Commercial Margin Analysis

### B2B Pro Subscription (£19.00 / month)
- **Revenue per Subscriber:** £19.00
- **Typical Usage:** A travel coordinator plans ~40 business journeys per month.
- **Direct API Cost:** $40 \times 2.19\text{p} = \mathbf{£0.88}$
- **Gross Profit Margin:** **£18.12 (95.4% Gross Margin)**
- **Disputed Invoice Protection Value:** Preventing a single rejected £110 consultant travel expense pays for **5.8 months** of the subscription.

### B2B Venue Travel Widget (£19.00 – £49.00 / month)
- **Revenue per Venue:** £19.00 (Standard) or £49.00 (Pro with Scope 3 carbon reporting)
- **Typical Footfall Usage:** An independent museum with 50,000 annual visitors generates ~250–350 widget route searches per month.
- **Direct Cost:** $300 \times 2.19\text{p} = \mathbf{£6.57}$ (or £0 if driving/bus routes dominate).
- **Gross Profit Margin:** **65.4% to 86.6% Gross Margin**.

---

## 4. Scaling Horizon & Projected Infrastructure Costs

| Phase | Concurrent Users | Monthly Searches | Infrastructure Setup | Projected Monthly Cost |
|---|---|---|---|---|
| **Current (Baseline)** | 1–5 concurrent | 1,000 – 3,000 | Single Contabo VPS (single Node process, 14 GB free RAM) | **~£37 / mo** |
| **Phase 1 (Growth)** | 10–50 concurrent | 10,000 – 30,000 | Same Contabo VPS; Node.js 4-worker clustering, Caddy response compression | **~£50 – £80 / mo** (primarily OJP API calls) |
| **Phase 2 (Scale)** | 50–200 concurrent | 50,000 – 150,000 | Second VPS for routing engines; dedicated Postgres instance; Redis queue workers | **~£120 – £180 / mo** |
| **Phase 3 (Enterprise)**| 200+ concurrent | 250,000+ | Load-balanced cluster; dedicated OJP connection pool; read replicas | **~£250 – £450 / mo** |
