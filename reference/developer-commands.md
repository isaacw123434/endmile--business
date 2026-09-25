# Developer Commands Reference

This document catalogs common development commands used across the EndMile monorepo. Use these commands to manage dependencies, execute test suites, run static analysis tools, and deploy applications.

---

## 1. Monorepo & Server commands (pnpm)

Run these commands from the root directory of the monorepo:

```bash
# Install all package and project dependencies
pnpm install

# Run TypeScript type checking on the server package
pnpm --filter @endmile/server typecheck

# Run all server tests (unit and integration tests)
pnpm --filter @endmile/server test

# Run server tests in watch mode for active development
pnpm --filter @endmile/server test:watch

# Run ESLint to analyze static code quality in the server package
pnpm --filter @endmile/server lint

# Start the Fastify backend development server (with hot reload enabled)
pnpm --filter @endmile/server dev

# Compile TypeScript code to production JavaScript
pnpm --filter @endmile/server build
```

---

## 2. Flutter Client App (`packages/app`)

Run these commands from the `packages/app` directory:

```bash
# Run the client app on an active emulator or connected mobile device
flutter run

# Run the client app in web mode using Google Chrome
flutter run -d chrome

# Run all widget and unit tests
flutter test

# Run static analysis (fails on any warnings; must pass before committing)
flutter analyze --fatal-infos

# Check code formatting in the app package
dart format --set-exit-if-changed .

# Build a release-ready Android APK
flutter build apk --release
```

---

## 3. Flutter B2B Admin Portal (`packages/admin_portal`)

Run these commands from the `packages/admin_portal` directory:

```bash
# Run the admin portal in Chrome (web-only platform)
flutter run -d chrome

# Run all widget and unit tests for the admin portal
flutter test

# Run static analysis (must pass with zero warnings before committing)
flutter analyze --fatal-infos

# Check code formatting in the admin portal package
dart format --set-exit-if-changed .
```

---

## 4. Docker Compose & Local Infrastructure

Run these commands from the root directory to manage local services (Postgres, Redis, OSRM, MOTIS):

```bash
# Start all local infrastructure containers in detached mode
docker compose up -d

# View live, streaming logs for the Fastify server container
docker compose logs -f server

# Stop all active containers without losing volume data
docker compose down

# Stop all active containers and completely delete databases and volumes
docker compose down -v
```

---

## 5. Landing Site (`packages/landing`)

Run these commands from the root directory of the monorepo:

```bash
# Start the Astro landing site in development mode
pnpm --filter @endmile/landing dev

# Build the static marketing site
pnpm --filter @endmile/landing build

# Preview the built landing site
pnpm --filter @endmile/landing preview
```
