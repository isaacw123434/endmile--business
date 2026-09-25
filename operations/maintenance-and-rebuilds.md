# Maintenance, Timetable Rebuilds & Deployment Pipeline

Procedures for scheduled data updates, timetable refreshes, and CI/CD automated deployments.

---

## 1. Weekly Maintenance: TNDS GTFS Timetable Rebuild

MOTIS routes buses, coaches, trams, and ferries using UK Traveline National Dataset (TNDS) GTFS data. Because transit operators adjust schedules frequently, this dataset must be refreshed weekly.

> [!WARNING]
> Transit routing is unavailable during the 5–10 minute rebuild. Run during off-peak hours (e.g. Sunday late night). Driving, cycling, and train routing remain operational.

### Weekly Rebuild Procedure

```bash
# 1. SSH into the VPS
ssh deploy@155.133.23.54
cd /opt/endmile

# 2. Stop MOTIS
docker compose stop motis

# 3. Clean existing timetable cache
docker run --rm -v endmile_motis_data:/data alpine rm -rf /data/*

# 4. Run the automated setup script (fetches fresh TNDS GTFS and processes graph)
bash scripts/setup-motis.sh

# 5. Start MOTIS with fresh timetable data
docker compose up -d motis

# 6. Verify health
wget -qO- http://127.0.0.1:8080/
docker compose logs --tail 50 motis
```

---

## 2. Yearly Maintenance

### A. OSRM Road & Cycling Network Rebuild (Annual)
Rebuild once per year to incorporate new roads, bypasses, roundabouts, and speed limit adjustments from OpenStreetMap GB:

```bash
ssh deploy@155.133.23.54
cd /opt/endmile

# Rebuild Driving
docker compose stop osrm-driving
docker volume rm endmile_osrm_data
bash scripts/setup-osrm.sh
docker compose up -d osrm-driving

# Rebuild Cycling
docker compose stop osrm-cycling
docker volume rm endmile_osrm_cycling_data
bash scripts/setup-osrm.sh
docker compose up -d osrm-cycling
```
*Driving rebuild takes ~30–60 minutes.*

### B. DEFRA Greenhouse Gas Emission Factors (Annual)
The UK Department for Energy Security and Net Zero (DESNZ / DEFRA) updates carbon conversion factors every June/July.
Update the factors file in the codebase (`data/defra-emission-factors-2026.json`) to keep Scope 3 carbon accounting compliant.

---

## 3. Automated CI/CD Deployment Flow

When code is committed and pushed to `main` in the codebase (`endmile-1`), GitHub Actions automatically builds and deploys to the VPS.

### Deployment Pipeline (`.github/workflows/deploy.yml`):
1. **Trigger:** Push to `main` touching `packages/server`, `docker-compose.yml`, or root dependencies.
2. **Action:**
   - Connects to VPS via SSH (`VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY`).
   - Runs `git pull origin main`.
   - Runs `pnpm install` and compiles TypeScript (`pnpm build`).
   - Restarts the Node.js Fastify server container (`docker compose restart server`).
3. **Zero Downtime for Routing Engines:** The deploy does **not** touch or restart OSRM, MOTIS, or PostgreSQL.
