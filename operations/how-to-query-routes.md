# How to Query Routes on the VPS & Production API

Actionable recipes and `curl` commands for querying EndMile's routing pipeline and inspecting routing engines.

---

## 1. Querying the Production Journey Search API

The public API is hosted on the `api.` subdomain: `https://api.endmilerouting.co.uk`.

### The Live Streaming SSE Endpoint

`GET https://api.endmilerouting.co.uk/journeys/search/stream`

This endpoint streams Server-Sent Events (`data: {...}\n\n`), returning progressive multimodal results as they are resolved (direct driving first, then public transit, then Smart Swap combinations).

#### Example 1: Full Multimodal Journey (Ripon to Darlington)
```bash
curl -N "https://api.endmilerouting.co.uk/journeys/search/stream?\
originLat=54.1374&\
originLon=-1.5241&\
destLat=54.5245&\
destLon=-1.5534&\
departAt=2026-10-06T09%3A00%3A00.000Z"
```

#### Example 2: Train + Taxi Only (Excluding Other Modes)
To exclude specific modes, pass a URL-encoded JSON object in `constraints`:
`{"excludedModes":["driving","bus","coach","tram","underground","dlr","overground","elizabeth-line","cycling"]}`:

```bash
curl -N "https://api.endmilerouting.co.uk/journeys/search/stream?\
originLat=54.1374&\
originLon=-1.5241&\
destLat=54.5245&\
destLon=-1.5534&\
departAt=2026-10-06T09%3A00%3A00.000Z&\
constraints=%7B%22excludedModes%22%3A%5B%22driving%22%2C%22bus%22%2C%22coach%22%2C%22tram%22%2C%22underground%22%2C%22dlr%22%2C%22overground%22%2C%22elizabeth-line%22%2C%22cycling%22%5D%7D"
```

#### Adding Telemetry Attribution Headers
To test telemetry tracking without interfering with routing:
```bash
curl -N -H "X-EndMile-Client-Surface: app" \
        -H "X-EndMile-Client-Feature: journey_search" \
        "https://api.endmilerouting.co.uk/journeys/search/stream?originLat=54.1374&originLon=-1.5241&destLat=54.5245&destLon=-1.5534"
```

---

## 2. Direct Queries to Routing Engines on the VPS

To test the routing engines directly without the Node.js API layer, SSH into the VPS:

```bash
ssh deploy@155.133.23.54
```

### A. Querying MOTIS Directly (Port 8080)
MOTIS handles buses, trams, light rail, metro, and ferry timetables across Great Britain.

```bash
# Query MOTIS intermodal routing between two coordinates
curl -s -X POST http://127.0.0.1:8080/ \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "/intermodal",
    "content_type": "IntermodalRoutingRequest",
    "content": {
      "start_type": "PreTripPPR",
      "start": {
        "position": {"lat": 53.7949, "lng": -1.5471}
      },
      "destination_type": "PostTripPPR",
      "destination": {
        "position": {"lat": 53.7997, "lng": -1.5492}
      },
      "search_type": "Default",
      "search_dir": "Forward",
      "interval": {
        "begin": 1791277200,
        "end": 1791284400
      }
    }
  }' | jq .
```

### B. Querying OSRM Driving Engine Directly (Port 5000)
OSRM provides sub-millisecond driving distances, durations, and polylines across the GB road network.

```bash
# Leeds Station (-1.5471, 53.7949) to Bradford Interchange (-1.7505, 53.7925)
# Coordinates format: {longitude},{latitude}
curl -s "http://127.0.0.1:5000/route/v1/driving/-1.5471,53.7949;-1.7505,53.7925?overview=false" | jq .
```

Expected response format:
```json
{
  "code": "Ok",
  "routes": [
    {
      "geometry": "...",
      "legs": [
        {
          "distance": 15820.4,
          "duration": 1420.2,
          "weight": 1420.2
        }
      ],
      "distance": 15820.4,
      "duration": 1420.2
    }
  ],
  "waypoints": [...]
}
```

### C. Querying OSRM Cycling Engine Directly (Port 5001)

```bash
# Leeds Station to Bradford Interchange via cycle network
curl -s "http://127.0.0.1:5001/route/v1/cycling/-1.5471,53.7949;-1.7505,53.7925?overview=false" | jq .
```

---

## 3. Saving Live Responses to File for Debugging

From inside the VPS:
```bash
ssh deploy@155.133.23.54
curl -N "https://api.endmilerouting.co.uk/journeys/search/stream?originLat=54.1374&originLon=-1.5241&destLat=54.5245&destLon=-1.5534" > /tmp/search-result.txt 2>&1
head -n 20 /tmp/search-result.txt
```
