# VPS Access & Production Server Operations

Comprehensive guide to accessing, monitoring, and managing EndMile's production server infrastructure.

---

## 1. Server Specifications & Access Details

| Attribute | Value / Specification |
|---|---|
| **Hosting Provider** | Contabo Cloud VPS 30 |
| **Hardware Specs** | 8 vCPU Cores, 24 GB RAM, 400 GB SSD, 600 Mbit/s port |
| **Operating System** | Ubuntu 24.04 LTS |
| **Public IPv4** | `155.133.23.54` |
| **IPv6** | `2a02:c207:2315:1466::1/64` |
| **Primary Domain** | `endmilerouting.co.uk` (DNS hosted on 20i.com) |
| **API Domain** | `api.endmilerouting.co.uk` |
| **Guide Domain** | `guide.endmilerouting.co.uk` |
| **App Domain** | `app.endmilerouting.co.uk` |
| **SSH Command** | `ssh deploy@155.133.23.54` |
| **Application Root** | `/opt/endmile` |
| **Base Monthly Cost** | £16.00/mo |
| **Contabo Customer ID** | `14736229` |

### RAM Allocation Budget

| Service | Expected RAM | Role & Notes |
|---|---|---|
| **OSRM (Driving)** | ~3.1 GB | Full GB road network in memory (port 5000 loopback) |
| **OSRM (Cycling)** | ~1.5 GB | Full GB cycling network in memory (port 5001 loopback) |
| **MOTIS (Public Transit)**| ~2.5 GB | C++ multi-modal routing engine with TNDS GTFS data (port 8080 loopback) |
| **PostgreSQL + PostGIS** | ~1.0–2.0 GB | Relational DB: accounts, saved routes, telemetry, tenants |
| **Redis** | ~0.5 GB | In-memory cache (capped at 256 MB by config, LRU eviction) |
| **Node.js Fastify API** | ~0.5 GB | Application server & route scoring pipeline (port 3000) |
| **Web App (Nginx)** | ~50 MB | Static Flutter web build served by Nginx (port 80) |
| **Caddy v2** | ~50 MB | Reverse proxy terminating HTTPS/TLS with auto Let's Encrypt |
| **Linux OS Base** | ~1.0 GB | Ubuntu kernel & system daemons |
| **Total Used** | **~9.5–10.5 GB** | **~13.5–14.5 GB Headroom available** |

---

## 2. Docker Compose Stack

All core services run in Docker containers under `/opt/endmile/docker-compose.yml`.

### Service Details

| Service | Docker Image | Internal Port | External Exposure | Volume / Persistence |
|---|---|---|---|---|
| `caddy` | `caddy:2-alpine` | 80, 443 | **Public (80, 443)** | `caddy_data`, `caddy_config` |
| `server` | Built from `packages/server` | 3000 | None (proxied by Caddy) | None (stateless) |
| `postgres` | `postgis/postgis:15-3.4` | 5432 | None (Docker network) | `postgres_data` |
| `redis` | `redis:7-alpine` | 6379 | None (Docker network) | `redis_data` |
| `osrm-driving` | `osrm/osrm-backend:v5.26.0` | 5000 | 127.0.0.1:5000 (loopback) | `endmile_osrm_data` |
| `osrm-cycling` | `osrm/osrm-backend:v5.26.0` | 5001 | 127.0.0.1:5001 (loopback) | `endmile_osrm_cycling_data` |
| `motis` | `ghcr.io/motis-project/motis` | 8080 | 127.0.0.1:8080 (loopback) | `endmile_motis_data` |

---

## 3. Essential Server Management Commands

SSH into the server first:
```bash
ssh deploy@155.133.23.54
cd /opt/endmile
```

### Checking Status and Resource Consumption

```bash
# View all container states
docker compose ps

# Live per-container CPU & RAM consumption
docker stats --no-stream

# System-level RAM and disk space
free -h
df -h /
```

### Viewing Logs

```bash
# Follow logs for all services
docker compose logs -f

# Follow Fastify server logs only
docker compose logs -f server

# Follow MOTIS public transit engine logs
docker compose logs -f motis

# View last 100 lines of PostgreSQL logs
docker compose logs --tail 100 postgres
```

### Starting, Stopping, and Restarting Services

```bash
# Restart the Node API server after code update
docker compose restart server

# Restart MOTIS or OSRM
docker compose restart motis
docker compose restart osrm-driving

# Gracefully stop the entire stack
docker compose down

# Bring up all containers in the background
docker compose up -d
```

### Health Check Probes

```bash
# Node.js API health check
curl http://localhost:3000/health

# OSRM driving engine health
curl http://localhost:5000/health

# OSRM cycling engine health
curl http://localhost:5001/health

# MOTIS engine response probe
wget -qO- http://127.0.0.1:8080/
```

### PostgreSQL Backups

```bash
# Create timestamped SQL dump
docker compose exec postgres pg_dump -U endmile endmile > backup-$(date +%Y%m%d).sql

# Restore dump into database
docker compose exec -T postgres psql -U endmile endmile < backup-20260314.sql
```
