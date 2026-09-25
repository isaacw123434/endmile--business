# Venue planner embed pilot

The pilot packages the existing EndMile Guide live planner in an isolated iframe. It does not expose destination coordinates in the venue's script tag and does not give the parent page API credentials.

## Pilot configuration

Pilot records live in `packages/b2c_site/src/utils/embed-config.js`. Each opaque, server-issued ID resolves at build time to one fixed venue data record, including its name and coordinates. A record also contains an explicit status, approved parent origins, and optional presentation settings. Disabled or unknown IDs do not produce an embed page.

The first controlled pilot is the Royal Armouries in Leeds (`venueId` `78431237`). Its approved parent origins are the EndMile venue-widget product page at `https://endmilerouting.co.uk` and `https://seleniumbase.io` for temporary testing through the [SeleniumBase iframe tester](https://seleniumbase.io/w3schools/iframes). Do not add a customer domain until its ownership and exact scheme/host have been verified.

## Installation

Add the loader to the approved page:

```html
<script
  src="https://guide.endmilerouting.co.uk/widget.js"
  data-embed-id="em_7Kx2pQ9mV4cN8rT6"
  data-title="Plan a journey to Royal Armouries in Leeds"
></script>
```

The loader derives the iframe host from its own URL, creates a full-width iframe, and accepts only integer resize messages from that iframe window and origin with the matching embed ID. The iframe sends resize messages only to configured parent origins. A `ResizeObserver` reports document-height changes after results, maps and mobile route details expand. The parent caps accepted heights at 2,400px to avoid unbounded messages while leaving enough room for responsive results without an internal iframe scrollbar.

## Security and abuse controls

- nginx and the public Caddy proxy deny framing for normal Guide pages. Both layers give the exact pilot path a `Content-Security-Policy: frame-ancestors` allow-list matching the pilot configuration, and Caddy must not attach `X-Frame-Options: DENY` to that response. Browsers enforce multiple CSP headers cumulatively, so an upstream `frame-ancestors 'none'` cannot be relaxed by nginx.
- The API CORS allow-list must contain the EndMile-hosted Guide origin, not venue origins. Autocomplete, place resolution, and streaming searches originate inside the iframe.
- Embedded requests identify `embedded_widget`, `live_widget`, the fixed venue ID, and the opaque embed ID. These are attribution and rate-limit inputs, not authentication. Never grant privileges based on them.
- Geocoding endpoints retain their per-IP limits. Streaming searches are limited to 30 requests per minute per IP and embed pair, backed by Redis in clustered production deployments. Cloudflare/WAF limits remain the outer per-IP layer.
- Trainline deep links use `buildTrainlineHref`; JustPark links use the shared Awin builders. Do not construct affiliate URLs in the embed page.

## Acceptance and rollout

1. Deploy the fixture from `/embed-fixture/` to the approved external origin rather than weakening `frame-ancestors` for local convenience.
2. Check 320 px, 375 px, tablet, and desktop widths. Confirm there is no horizontal scrolling and route/map expansion resizes the iframe.
3. Tab through autocomplete, suggestions, Compare Routes, sorting, route cards and CTAs. Confirm focus remains visible.
4. Confirm the fixture's hostile CSS and overwritten host `postMessage` do not affect the iframe.
5. Accept and refuse analytics consent where the controlled host supplies it. The pilot iframe itself does not load Guide analytics or advertising components.
6. Test invalid origins, an invalid/disabled embed ID, API 429, offline mode, autocomplete failure, place-resolution failure, journey timeout and an empty result.
7. Verify API logs show `embedded_widget` plus venue `78431237`, while Guide searches still show `guide`.
8. Verify Trainline and JustPark targets and affiliate attribution in a staging booking flow.
9. Use `seleniumbase.io` only for the temporary framing diagnostic. Before customer rollout, replace it with the verified venue origin, review traffic and abuse for at least one week, and explicitly approve any further venue-domain record and CSP addition.

Changing an approved origin requires updating the registry, the exact nginx location, and the exact Caddy matcher. This duplication is deliberate for the static deployment: a build must fail review if application configuration and both response-policy layers disagree.
