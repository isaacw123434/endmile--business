# Key Domain Terminology

This reference guide documents key domain terminology used across the EndMile monorepo. Developers and AI agents should refer to these definitions to maintain naming consistency.

| Term | Meaning |
|---|---|
| **Journey** | Complete trip from origin to destination, composed of segments (legs). |
| **Leg / Segment** | One leg using a single transport mode (e.g. "drive to station", "train to London Euston"). |
| **First Mile** | Origin to the first transport hub. |
| **Middle Leg** | Hub-to-hub trunk transport (train, coach). |
| **Last Mile** | Last transport hub to final destination. |
| **Hub** | Transport interchange — railway station, bus station, coach terminal, park & ride. |
| **Total Journey Cost** | Full door-to-door trip cost (formerly referenced as TCO) — fuel + parking + fares + congestion + ULEZ. |
| **Smart Choice** | Route with best time-cost-risk balance. Not necessarily fastest or cheapest. Default tab. |
| **Smart Swap** | Users swap a first-mile or last-mile segment mode (e.g. Uber → Bus). |
| **CRS code** | 3-letter station identifier (National Rail). e.g. PAD = London Paddington. |
| **NaPTAN** | National Public Transport Access Nodes — UK standard stop/station IDs. |
| **RLS** | Row-Level Security — PostgreSQL feature enforcing tenant data isolation. |
| **Scope 3** | Indirect GHG emissions from business travel (Category 6). What EndMile reports. |
| **DEFRA factors** | UK government greenhouse gas conversion factors for carbon calculations. Published annually. |
| **Policy compliance** | Whether a route meets employer's travel policy (max cost cap, preferred modes). |
| **ULEZ** | Ultra Low Emission Zone (London) — daily charge for non-compliant vehicles. |
| **Congestion Charge** | Daily charge for driving in central London. |
| **HMRC mileage rate** | UK tax-deductible mileage rate: 55p/mile (first 10,000 miles), 25p/mile thereafter. |
