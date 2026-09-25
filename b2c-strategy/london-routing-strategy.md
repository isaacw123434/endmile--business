# London Routing Architecture, Saba TfL "Park & Tube" Strategy & API Integration

## 1. Executive Summary & Problem Definition

London represents the largest destination market for UK travel, accounting for over **11,272 venues in our master OpenStreetMap dataset** and **6,101 qualifying commercial destinations** (major NHS hospitals, arenas, stadiums, universities, museums, theatres, and conference centres).

Historically, the entire Greater London area inside the M25 was hard-excluded from batch matrix generation via an `isInsideM25` bounding box (`lat 51.2..51.75, lon -0.55..0.35`). 

This document outlines:
1. **Available Data Assets**: Schema and structure of Saba TfL car parks and TfL Unified API.
2. **Current Routing Engine Mechanics**: How OSRM, MOTIS, and TfL live transit interact today.
3. **The "Park & Tube" Paradigm**: Replacing impractical central driving with outer-station parking + rapid rail transit.
4. **Codebase Logic Changes**: Server hub loading, hub discovery radii, routing profiles, and CLI batch filters.
5. **Main API vs B2C Matrix Scope**: Comparing benefits and risks of enabling this globally across B2B SaaS vs. B2C only.
6. **Pre/Post Snapshot Testing Protocol**: Deterministic before/after API comparison test harness.

---

## 2. Available Data Assets & Schema Specifications

### 2.1 Saba TfL Station Car Park Network
Transport for London’s official car parks are operated by **Saba Parking** ([https://www.sabaparking.co.uk/en/tfl](https://www.sabaparking.co.uk/en/tfl)).

#### Key Characteristics:
* **Coverage**: 60+ dedicated station car parks situated at strategic outer London Underground, Overground, and Elizabeth Line termini/stations.
* **Capacity**: Typically 150 to 550+ dedicated parking bays per station.
* **Tariffs**: Daily tariffs range from **£5.00 to £8.50/day** on weekdays, and **£3.00 to £4.50/day** on weekends/off-peak (compared to £35.00–£50.00/day in Central London).
* **Payment**: Saba App / RingGo / Autopay.

#### Target Data Schema for Ingestion (`data/park-and-ride/sites.json` & `data/city_parking/parking.json`):
```json
{
  "placeId": "tfl:carpark:stanmore",
  "name": "Stanmore Underground Station Car Park (TfL)",
  "formattedAddress": "London Underground Ltd, Stanmore Station, London HA7 4PD",
  "coordinates": {
    "lat": 51.6194,
    "lon": -0.3025,
    "source": "tfl_saba_verified"
  },
  "mode": "metro",
  "transitMode": "underground",
  "connectedStation": {
    "name": "Stanmore",
    "crs": null,
    "naptan": "940GZZLUSTM",
    "lines": ["Jubilee Line"],
    "tflZone": 5
  },
  "corridor": "M1_NORTH",
  "parkingSpaces": 450,
  "accessibleSpaces": 14,
  "evChargingBays": 8,
  "fee": "6.50",
  "parkingCost": "6.50",
  "weekendParkingCost": "3.50",
  "operator": "Saba Parking / TfL",
  "returnBusFare": null,
  "transitReturnFarePence": 700
}
```

### 2.2 Inbound Motorway Corridors & Priority Stations

| Motorway / Highway Corridor | Origin Regions Served | Recommended Outer Hubs | Lines & Frequencies |
|---|---|---|---|
| **M1 & A1(M) North** | Leeds, Sheffield, Nottingham, Leicester, Luton, Milton Keynes | **Stanmore**, **Canons Park**, **High Barnet**, **Cockfosters**, **Oakwood** | Jubilee (every 2–3 min), Northern, Piccadilly |
| **M40 & A40 West/NW** | Birmingham, Oxford, Coventry, High Wycombe | **Hillingdon** (A40 junction), **Ickenham**, **Ruislip**, **West Ruislip**, **Uxbridge** | Metropolitan & Piccadilly, Central, Chiltern |
| **M4 & A4 West** | Bristol, Swindon, Reading, Slough, Heathrow | **Osterley** (M4 J2/A4), **Hatton Cross**, **Hayes & Harlington**, **West Drayton**, **Burnham** | Piccadilly, Elizabeth Line |
| **M11 & A12/A13 East** | Cambridge, Norwich, Chelmsford, Colchester, Stansted | **Epping** (M11 J7), **Debden**, **Loughton**, **Newbury Park**, **Redbridge**, **Shenfield** | Central Line, Elizabeth Line |
| **M23 / M3 / A3 South** | Brighton, Crawley, Southampton, Portsmouth, Guildford | **Morden** (Northern terminus), **North Greenwich** (A102 / Blackwall), **Richmond** | Northern, Jubilee, District |

---

## 3. Current Server Routing Mechanics (What Already Works)

The EndMile backend at `packages/server/src/` already includes complete infrastructure for multimodal London routing:

```
                  ┌──────────────────────────────────────────────────────────┐
                  │                 Server: PlanJourney Use Case             │
                  └─────────────────────────────┬────────────────────────────┘
                                                │
                 ┌──────────────────────────────┼────────────────────────────┐
                 ▼                              ▼                            ▼
   ┌───────────────────────────┐  ┌───────────────────────────┐  ┌───────────────────────────┐
   │    Road Routing (OSRM)    │  │   National Rail (MOTIS)   │  │   London Transit (TfL)    │
   │ packages/server/.../osrm/ │  │ packages/server/.../motis │  │ packages/server/.../tfl/  │
   ├───────────────────────────┤  ├───────────────────────────┤  ├───────────────────────────┤
   │ Direct Drive distances,   │  │ Intercity rail to London  │  │ Live TfL Unified API:     │
   │ durations, fuel costs,    │  │ termini (Euston, KGX,     │  │ Underground, Elizabeth    │
   │ Congestion Charge (£15),  │  │ Victoria, Paddington,     │  │ Line, DLR, Overground,    │
   │ and ULEZ applicability.   │  │ Waterloo, London Bridge). │  │ and London Buses.         │
   └───────────────────────────┘  └───────────────────────────┘  └───────────────────────────┘
```

### Verified Live End-to-End Test Results:
* **Birmingham New Street $\to$ Buckingham Palace**:
  * *Direct Drive*: 147 min, £35.84 (Fuel + Congestion Charge + Central Parking).
  * *Train & Walk*: Birmingham New Street $\to$ London Euston (train) $\to$ Victoria (tube) $\to$ 10 min walk (£28.50, 130 min).
* **Reading $\to$ Wembley Stadium**:
  * *Direct Drive*: **57 min, £5.76 fuel** (OSRM routing around the A404/M40/A406).
  * *Train & Tube*: Elizabeth Line $\to$ Overground (120 min, £17.10).
* **Birmingham $\to$ The O2 Arena**:
  * *Train & Transit*: Train to Euston $\to$ Northern line to London Bridge $\to$ Jubilee line to North Greenwich $\to$ 3 min walk.

---

## 4. Codebase Logic Changes Required

### 4.1 Server Hub Loader (`packages/server/src/infrastructure/hubs/hub-data-loader.ts`)
* **Current Behavior**: `buildParkAndRideHubs` reads `data/park-and-ride/sites.json` and filters out sites missing space/cost data.
* **Modification**:
  1. Add the ~60 Saba TfL car parks to `data/park-and-ride/sites.json` with `transitMode: 'underground'` or `'elizabeth_line'`.
  2. In `hub-data-loader.ts`, ensure `PR_MODE_MAP` properly maps `'metro'` and `'underground'` to `underground` transport mode.

### 4.2 Journey Planner Hub Discovery Radii (`packages/server/src/application/use-cases/plan-journey.ts`)
* **Current Behavior (lines 207–213)**:
  ```typescript
  const prHubs = (await this.hubFinder.findNearby(destination, { radiusMetres: 20_000, types: ['parkAndRide'] })).slice(0, 6);
  ```
* **Modification for Greater London**:
  * Central London venues (Zone 1) are typically **18km to 28km** away from the outer M25 Park & Tube stations (e.g. Stanmore is 21km from Trafalgar Square; Epping is 26km).
  * For destinations where `isInsideM25(destination)` is true:
    * Expand `radiusMetres` for `parkAndRide` hub lookup from `20_000` to **`35_000`** (35 km) so that outer-corridor stations (Stanmore, Hillingdon, Cockfosters, Epping, Morden) are discovered as valid arrival hubs.
    * Rank outer hubs by alignment with origin vector (e.g. northbound drivers get Stanmore/Cockfosters; westbound drivers get Hillingdon/Osterley).

### 4.3 Matrix Batch Generator CLI (`scripts/batch-router/generate-venue-matrix.mjs`)
* **Current Behavior (lines 111–164)**:
  `isInsideM25(lat, lon)` causes `isQualifyingVenue` to return `false` for all 11,272 London venues.
* **Modification**:
  1. Remove `!isInsideM25(lat, lon)` from `isQualifyingVenue(venue)`.
  2. Keep London venues eligible for batch routing.
  3. Support `TFL_APP_KEY` in environment variables during batch execution to prevent rate limiting against `api.tfl.gov.uk` (TfL free tier allows 500 requests/min with key).

---

## 5. Scope Evaluation: B2C Flag Only vs. Main Server API

| Evaluation Factor | B2C Batch Flag Only (`b2c_matrix`) | Apply to Main API (B2B SaaS + App) |
|---|---|---|
| **Primary Use Case** | SEO venue guides & visitor planning (`guide.endmilerouting.co.uk`). | Corporate travel planning, emissions reduction, travel policy compliance (`app.endmilerouting.co.uk`). |
| **User Value** | High: Tourists and day-trippers visiting arenas/museums avoid £50 parking scams and £15 Congestion Charge. | Very High: Corporate employers avoid paying £15 CC + £15 ULEZ + £45 Central London car park expense claims for traveling staff. |
| **Performance Impact** | Zero runtime server impact (pre-computed into static JSON). | Low: TfL API calls take 150–300ms, executed in parallel during Stage 0 with circuit breaker protection. |
| **Recommendation** | **Enable Immediately** in B2C dataset. | **Enable in Core Hub Layer**: By adding Saba TfL stations as `parkAndRide` hubs with a 35km radius, both B2C and B2B benefit automatically without branching logic. |

---

## 6. Pre/Post Snapshot Testing Protocol

To verify London routing improvements without regression, implement a snapshot comparison harness before and after ingesting Saba TfL hubs.

### 6.1 Representative Test Venue Suite

```javascript
export const LONDON_TEST_BENCHMARK_VENUES = [
  // 1. Zone 1 Central (Congestion Charge Zone)
  { id: '10000001', name: 'Buckingham Palace', lat: 51.5014, lon: -0.1419, zone: 'Zone 1' },
  { id: '10000002', name: 'British Museum', lat: 51.5194, lon: -0.1270, zone: 'Zone 1' },
  { id: '10000003', name: 'St Thomas Hospital', lat: 51.4988, lon: -0.1186, zone: 'Zone 1' },
  
  // 2. Zone 2/3 Inner London (ULEZ / High Density)
  { id: '10000004', name: 'The O2 Arena', lat: 51.5030, lon: 0.0031, zone: 'Zone 2/3' },
  { id: '10000005', name: 'Emirates Stadium', lat: 51.5549, lon: -0.1084, zone: 'Zone 2' },
  { id: '10000006', name: 'ExCeL London', lat: 51.5076, lon: 0.0298, zone: 'Zone 3' },

  // 3. Zone 4/5/6 Outer London (Event / Suburban)
  { id: '10000007', name: 'Wembley Stadium', lat: 51.5560, lon: -0.2796, zone: 'Zone 4' },
  { id: '10000008', name: 'Twickenham Stadium', lat: 51.4559, lon: -0.3415, zone: 'Zone 5' },
  { id: '10000009', name: 'Richmond Golf Club', lat: 51.4428, lon: -0.2989, zone: 'Zone 4' }
];
```

### 6.2 Snapshot Test Execution Script (`scripts/test-london-snapshot.mjs`)

```javascript
// Test harness to record before vs after route metrics
import fs from 'node:fs';

async function runSnapshot(outputFilename) {
  const origins = [
    { name: 'Birmingham', lat: 52.4862, lon: -1.8904 },
    { name: 'Leeds', lat: 53.8008, lon: -1.5491 },
    { name: 'Bristol', lat: 51.4545, lon: -2.5879 },
    { name: 'Cambridge', lat: 52.2053, lon: 0.1218 },
    { name: 'Brighton', lat: 50.8225, lon: -0.1372 }
  ];

  const results = [];

  for (const venue of LONDON_TEST_BENCHMARK_VENUES) {
    for (const origin of origins) {
      const response = await fetch('https://api.endmilerouting.co.uk/journeys/search/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-EndMile-Client-Surface': 'test_snapshot'
        },
        body: JSON.stringify({
          origin: { lat: origin.lat, lon: origin.lon },
          destination: { lat: venue.lat, lon: venue.lon },
          departAt: '2026-08-24T08:00:00.000Z',
          constraints: { routingProfile: 'b2c_matrix', includeCityParking: true }
        })
      });
      // Parse SSE stream and record categories, durations, and costs
      // Save structured snapshot to outputFilename
    }
  }
  fs.writeFileSync(outputFilename, JSON.stringify(results, null, 2));
}
```

## 7. `SmartChoice` Scoring Verification & Best-Route Selection

A critical requirement is ensuring that the server's **`smartChoice`** ranking algorithm selects the genuinely best, most practical route for London destinations, and that the batch matrix generator preserves this choice without regression.

### 7.1 How `SmartChoice` Functions for London Scenarios

The EndMile server calculates a multi-criteria weighted score for every candidate route:
$$\text{Score} = w_t \cdot \text{Duration} + w_c \cdot \text{CostPence} + w_i \cdot \text{Interchanges} + w_e \cdot \text{Emissions} + w_w \cdot \text{WalkFatigue}$$

In London, extreme cost and time differentials occur between travel modes:
1. **Central London (Zone 1)**: Direct driving incurs fuel + £15.00 Congestion Charge + £35–£50 central NCP parking. Total cost is £45–£65 for a 2.5 hour crawl in traffic.
2. **Park & Tube**: Driving down M1/M40 to Stanmore/Hillingdon + Tube into Zone 1 costs **£14–£18 total** and avoids central traffic.
3. **National Rail + Tube**: Fast train from Birmingham/Leeds into Euston/Kings Cross + 10 min Tube leg costs **£25–£35** and takes ~2 hours.

### 7.2 Validation Scenarios for `SmartChoice` Selection

| Test Scenario | Origin $\to$ Destination | Expected `SmartChoice` #1 Rank | Why This Route Must Win |
|---|---|---|---|
| **Central London Congestion** | Birmingham $\to$ British Museum (Zone 1) | **National Rail + Tube** or **Park & Tube (Hillingdon)** | Direct Drive is penalized heavily by £15 Congestion Charge + £35 Bloomsbury parking + central traffic delay. |
| **Outer London / Orbital Route** | Reading $\to$ Wembley Stadium (Zone 4) | **Direct Drive** (via M4/M40/A406) | Direct driving is **57 min, £5.76 fuel** vs 120 min £17.10 on train/tube. `smartChoice` must correctly favor driving here. |
| **Corridor Alignment** | Leeds (M1) $\to$ The O2 Arena (East London) | **Park & Tube (Cockfosters/Stanmore)** or **Train (Kings Cross $\to$ Northern $\to$ Jubilee)** | Router must select Northern/Northwestern P&R hub aligned with driver's inbound motorway, avoiding routing across south/west London. |
| **Local Station Walk Preference** | Manchester $\to$ Buckingham Palace | **Walk to Manchester Piccadilly $\to$ Train $\to$ Euston** | First-mile logic must select walking to Piccadilly rather than an out-of-town taxi to Stockport/Macclesfield. |

### 7.3 Verifying `SmartChoice` in CLI Matrix Summarisation

In `scripts/batch-router/generate-venue-matrix.mjs`, `summariseJourneys` processes `apiResult.smartChoice` as its primary candidate pool:
```javascript
// Step 1: Iterate smartChoice first so best[cat] gets the server's top-ranked recommendation
const allJourneys = [
  ...(apiResult.smartChoice || []),
  ...(apiResult.cheapest || []),
  ...(apiResult.fastest || [])
];
```
#### Automated Verification Checklist:
1. **Category Assignment**: For each category (`trainWalk`, `trainTaxi`, `driveToCityPark`, `parkAndRide`), the journey in `summary[cat]` must match the journey with lowest `rankIndex` from the server's `smartChoice` tab.
2. **No False Durations Overwriting Value**: If `fastest` has a route arriving 2 minutes earlier by taking a £40 out-of-town taxi, `isBetterCategoryJourney` must **reject** it and retain the `smartChoice` local walking departure.
3. **Multiple P&Rs Retained**: `categories.parkAndRides` retains all unique P&R hubs (sorted by total journey duration) so visitors can choose alternative corridors.

---

## 8. Pre/Post Snapshot Testing Protocol

To verify London routing improvements without regression, implement a snapshot comparison harness before and after ingesting Saba TfL hubs.

### 8.1 Representative Test Venue Suite

```javascript
export const LONDON_TEST_BENCHMARK_VENUES = [
  // 1. Zone 1 Central (Congestion Charge Zone)
  { id: '10000001', name: 'Buckingham Palace', lat: 51.5014, lon: -0.1419, zone: 'Zone 1' },
  { id: '10000002', name: 'British Museum', lat: 51.5194, lon: -0.1270, zone: 'Zone 1' },
  { id: '10000003', name: 'St Thomas Hospital', lat: 51.4988, lon: -0.1186, zone: 'Zone 1' },
  
  // 2. Zone 2/3 Inner London (ULEZ / High Density)
  { id: '10000004', name: 'The O2 Arena', lat: 51.5030, lon: 0.0031, zone: 'Zone 2/3' },
  { id: '10000005', name: 'Emirates Stadium', lat: 51.5549, lon: -0.1084, zone: 'Zone 2' },
  { id: '10000006', name: 'ExCeL London', lat: 51.5076, lon: 0.0298, zone: 'Zone 3' },

  // 3. Zone 4/5/6 Outer London (Event / Suburban)
  { id: '10000007', name: 'Wembley Stadium', lat: 51.5560, lon: -0.2796, zone: 'Zone 4' },
  { id: '10000008', name: 'Twickenham Stadium', lat: 51.4559, lon: -0.3415, zone: 'Zone 5' },
  { id: '10000009', name: 'Richmond Golf Club', lat: 51.4428, lon: -0.2989, zone: 'Zone 4' }
];
```

### 8.2 Snapshot Test Execution Script (`scripts/test-london-snapshot.mjs`)

```javascript
// Test harness to record before vs after route metrics
import fs from 'node:fs';

async function runSnapshot(outputFilename) {
  const origins = [
    { name: 'Birmingham', lat: 52.4862, lon: -1.8904 },
    { name: 'Leeds', lat: 53.8008, lon: -1.5491 },
    { name: 'Bristol', lat: 51.4545, lon: -2.5879 },
    { name: 'Cambridge', lat: 52.2053, lon: 0.1218 },
    { name: 'Brighton', lat: 50.8225, lon: -0.1372 }
  ];

  const results = [];

  for (const venue of LONDON_TEST_BENCHMARK_VENUES) {
    for (const origin of origins) {
      const response = await fetch('https://api.endmilerouting.co.uk/journeys/search/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-EndMile-Client-Surface': 'test_snapshot'
        },
        body: JSON.stringify({
          origin: { lat: origin.lat, lon: origin.lon },
          destination: { lat: venue.lat, lon: venue.lon },
          departAt: '2026-08-24T08:00:00.000Z',
          constraints: { routingProfile: 'b2c_matrix', includeCityParking: true }
        })
      });
      // Parse SSE stream and record categories, durations, costs, and smartChoice rank
      // Save structured snapshot to outputFilename
    }
  }
  fs.writeFileSync(outputFilename, JSON.stringify(results, null, 2));
}
```

### 8.3 Expected Assertion Criteria for Snapshot Diffs

1. **Park & Tube Presence**:
   * *Before*: `parkAndRide` is `undefined` or empty for Central London venues from Birmingham/Leeds.
   * *After*: `parkAndRide` is present, routing to Stanmore (from North) or Hillingdon (from West) + Jubilee/Metropolitan Line into Central London.
2. **Cost Optimization & SmartChoice Selection**:
   * *Direct Drive Cost*: £35–£55 (includes £15 CC + £25–£40 central parking).
   * *Park & Tube Cost*: **£12–£18** (Fuel to outer station + £6.50 Saba parking + £3.40 Tube fare).
   * **Assertion**: `smartChoice[0]` must rank **Park & Tube** or **National Rail** above Direct Drive for Zone 1 destinations.
3. **Transit Continuity**:
   * All onward transit legs from railway stations (e.g. Euston $\to$ British Museum or Waterloo $\to$ St Thomas') must use live TfL Underground/bus legs without error.

---

## 9. Phased Implementation Roadmap

1. **Step 1: Dataset Compilation**: Extract, clean, and validate all 60+ Saba TfL station car parks with coordinates, spaces, tariffs, and line affiliations into `data/park-and-ride/sites.json`.
2. **Step 2: Server Hub Discovery Update**: Update `plan-journey.ts` to expand P&R discovery radius to 35km for London destination queries.
3. **Step 3: Baseline Snapshot**: Run snapshot test harness capturing baseline routing before deploying hub updates.
4. **Step 4: Verification & Comparison**: Re-run snapshot harness and verify that Park & Tube routes correctly populate with valid Saba parking, TfL fares, and appropriate `smartChoice` rankings.
5. **Step 5: Staged Rollout**: Process top 100 London venues first, verify on `guide.endmilerouting.co.uk`, and monitor TfL API rate limits.

