#!/usr/bin/env node

import { execFile } from 'node:child_process';
import { access, readFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);
const DEFAULT_SITE_URL = 'sc-domain:endmilerouting.co.uk';
const DEFAULT_BING_SITE_URL = 'https://guide.endmilerouting.co.uk/';
const DEFAULT_BING_API_KEY = 'f9541b772ec346ea816b0395881232e0';
const DEFAULT_GA4_PROPERTY = 'properties/531529105';
const DEFAULT_VENUE_DATA = 'data/venues/master_venues.json';
const OJP_COST_MILLI_PENCE = 42;
const trackedPaths = [
  '/journeys/search',
  '/journeys/search/stream',
  '/api/public/v1/routes/compare',
];

export function parseArgs(argv) {
  const flags = new Map();
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (!arg.startsWith('--')) continue;
    const key = arg.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) flags.set(key, true);
    else {
      flags.set(key, next);
      i++;
    }
  }
  return {
    days: numberFlag(flags, 'days', 28),
    from: stringFlag(flags, 'from'),
    to: stringFlag(flags, 'to'),
    surface: stringFlag(flags, 'surface'),
    venueId: stringFlag(flags, 'venue-id'),
    page: stringFlag(flags, 'page'),
    sshDb: stringFlag(flags, 'ssh-db'),
    sshDbDir: stringFlag(flags, 'ssh-db-dir') ?? '/opt/endmile',
    sshDbUser: stringFlag(flags, 'ssh-db-user') ?? 'endmile',
    sshDbName: stringFlag(flags, 'ssh-db-name') ?? 'endmile',
    siteUrl: stringFlag(flags, 'site-url') ?? DEFAULT_SITE_URL,
    bingApiKey: stringFlag(flags, 'bing-api-key') ?? process.env.BING_API_KEY ?? DEFAULT_BING_API_KEY,
    bingSiteUrl: stringFlag(flags, 'bing-site-url') ?? (flags.get('surface') === 'app' ? 'https://endmilerouting.co.uk/' : DEFAULT_BING_SITE_URL),
    noBing: Boolean(flags.get('no-bing')),
    query: stringFlag(flags, 'query'),
    limit: numberFlag(flags, 'limit', 15),
    ga4Property: stringFlag(flags, 'ga4-property') ?? DEFAULT_GA4_PROPERTY,
    googleCloudConfig: stringFlag(flags, 'google-cloud-config'),
    gscGoogleCloudConfig: stringFlag(flags, 'gsc-google-cloud-config'),
    ga4GoogleCloudConfig: stringFlag(flags, 'ga4-google-cloud-config'),
    venueData: stringFlag(flags, 'venue-data') ?? DEFAULT_VENUE_DATA,
    json: Boolean(flags.get('json')),
    markdown: Boolean(flags.get('markdown')),
    fixtureDir: stringFlag(flags, 'fixture-dir'),
  };
}

export function dateRange(options, now = new Date()) {
  const to = options.to ? parseIsoDate(options.to) : isoDate(now);
  if (options.from) return { from: parseIsoDate(options.from), to };
  const start = new Date(`${to}T00:00:00.000Z`);
  start.setUTCDate(start.getUTCDate() - Math.max(options.days - 1, 0));
  return { from: isoDate(start), to };
}

export async function buildReport(options, loaders) {
  const range = dateRange(options);
  const [gscRows, ga4Rows, endpointRows, apiRows, venueLookup, bingData] = await Promise.all([
    loaders.gsc(options, range),
    loaders.ga4(options, range),
    loaders.endpoint(options, range),
    loaders.api(options, range),
    loaders.venues(options),
    loaders.bing ? loaders.bing(options, range) : null,
  ]);

  const seo = summarizeGsc(gscRows, venueLookup, options);
  const bing = summarizeBing(bingData, range, venueLookup, options);
  const engagement = summarizeGa4(ga4Rows, venueLookup);
  const api = summarizeApi(endpointRows, apiRows, venueLookup);
  return {
    generatedAt: new Date().toISOString(),
    dateRange: range,
    filters: publicFilters(options),
    seo,
    bing,
    engagement,
    api,
    opportunities: findOpportunities(seo, engagement, api, bing),
  };
}

export function summarizeGsc(rows, venueLookup = new Map(), options = {}) {
  const filteredRows = options.query
    ? rows.filter((row) => (row.query ?? '').toLowerCase().includes(options.query.toLowerCase()))
    : rows;

  const totals = filteredRows.reduce((acc, row) => ({
    clicks: acc.clicks + number(row.clicks),
    impressions: acc.impressions + number(row.impressions),
    weightedPosition: acc.weightedPosition + number(row.position) * number(row.impressions),
  }), { clicks: 0, impressions: 0, weightedPosition: 0 });

  return {
    totals: {
      clicks: totals.clicks,
      impressions: totals.impressions,
      ctr: rate(totals.clicks, totals.impressions),
      position: totals.impressions ? round(totals.weightedPosition / totals.impressions, 1) : 0,
    },
    rows: filteredRows.map((row) => {
      const venueId = venueIdFromPage(row.page ?? '');
      return {
        query: row.query ?? '',
        page: row.page ?? '',
        venueId,
        venueName: venueName(venueLookup, venueId),
        clicks: number(row.clicks),
        impressions: number(row.impressions),
        ctr: number(row.ctr),
        position: number(row.position),
      };
    }),
  };
}

export function summarizeGa4(rows, venueLookup = new Map()) {
  const byPage = new Map();
  const byEvent = new Map();
  for (const row of rows) {
    const eventName = row.eventName ?? '';
    const page = row.pageLocation ?? row.pagePath ?? '';
    const count = number(row.eventCount);
    byEvent.set(eventName, (byEvent.get(eventName) ?? 0) + count);
    if (!page) continue;
    const venueId = venueIdFromPage(page);
    const entry = byPage.get(page) ?? {
      page,
      venueId,
      venueName: venueName(venueLookup, venueId),
      isVenuePage: Boolean(venueId || page.includes('/venues/')),
      events: {},
      totalEvents: 0,
    };
    entry.events[eventName] = (entry.events[eventName] ?? 0) + count;
    entry.totalEvents += count;
    byPage.set(page, entry);
  }
  const allPages = [...byPage.values()].sort((a, b) => b.totalEvents - a.totalEvents);
  return {
    byEvent: Object.fromEntries([...byEvent.entries()].sort()),
    byPage: allPages,
    venuePages: allPages.filter((p) => p.isVenuePage),
    directoryPages: allPages.filter((p) => !p.isVenuePage),
  };
}

export function summarizeApi(endpointRows, apiRows, venueLookup = new Map()) {
  const endpointTotals = endpointRows.reduce((acc, row) => ({
    searches: acc.searches + number(row.searches),
    cacheHits: acc.cacheHits + number(row.cache_hits),
  }), { searches: 0, cacheHits: 0 });
  const ojpCalls = apiRows
    .filter((row) => row.service === 'ojp')
    .reduce((sum, row) => sum + number(row.calls), 0);

  return {
    searches: endpointTotals.searches,
    cacheHits: endpointTotals.cacheHits,
    cacheHitRate: rate(endpointTotals.cacheHits, endpointTotals.searches),
    ojpCalls,
    ojpCostPounds: round((ojpCalls * OJP_COST_MILLI_PENCE) / 100_000, 4),
    bySurface: endpointRows.map((row) => normalizeEndpointRow(row, venueLookup)),
  };
}

export function summarizeBing(raw, range, venueLookup = new Map(), options = {}) {
  if (!raw) {
    return {
      totals: { clicks: 0, impressions: 0, ctr: 0, position: 0 },
      queries: [],
      pages: [],
      crawl: null,
    };
  }

  const inRangeTraffic = (raw.traffic || []).filter((row) => {
    const d = parseWcfDate(row.Date);
    return d && d >= range.from && d <= range.to;
  });

  const totals = inRangeTraffic.reduce(
    (acc, row) => ({
      clicks: acc.clicks + number(row.Clicks),
      impressions: acc.impressions + number(row.Impressions),
    }),
    { clicks: 0, impressions: 0 },
  );

  const queryRows = (raw.queries || [])
    .map((row) => {
      const clicks = number(row.Clicks);
      const impressions = number(row.Impressions);
      const pos = number(row.AvgImpressionPosition);
      return {
        query: row.Query ?? '',
        clicks,
        impressions,
        ctr: rate(clicks, impressions),
        position: pos > 0 ? pos : 0,
        date: parseWcfDate(row.Date),
      };
    })
    .filter((row) => {
      if (options.query && !row.query.toLowerCase().includes(options.query.toLowerCase())) return false;
      if (options.venueId) {
        const vName = venueLookup.get(String(options.venueId));
        if (vName && !row.query.toLowerCase().includes(vName.toLowerCase())) return false;
      }
      return true;
    })
    .sort((a, b) => b.clicks - a.clicks || b.impressions - a.impressions);

  const pageFilter = externalPageFilter(options);
  const pageRows = (raw.pages || [])
    .map((row) => {
      const page = row.Query ?? '';
      const clicks = number(row.Clicks);
      const impressions = number(row.Impressions);
      const pos = number(row.AvgImpressionPosition);
      const venueId = venueIdFromPage(page);
      return {
        page,
        venueId,
        venueName: venueName(venueLookup, venueId),
        clicks,
        impressions,
        ctr: rate(clicks, impressions),
        position: pos > 0 ? pos : 0,
        date: parseWcfDate(row.Date),
      };
    })
    .filter((row) => {
      if (pageFilter && !row.page.includes(pageFilter)) return false;
      if (options.venueId && row.venueId !== options.venueId) return false;
      return true;
    })
    .sort((a, b) => b.clicks - a.clicks || b.impressions - a.impressions);

  const totalImps = queryRows.reduce((sum, q) => sum + q.impressions, 0);
  const weightedPos = queryRows.reduce((sum, q) => sum + q.position * q.impressions, 0);
  const avgPos = totalImps > 0 ? round(weightedPos / totalImps, 1) : 0;

  const latestCrawl = raw.crawl && raw.crawl.length > 0 ? raw.crawl[raw.crawl.length - 1] : null;

  return {
    totals: {
      clicks: totals.clicks,
      impressions: totals.impressions,
      ctr: rate(totals.clicks, totals.impressions),
      position: avgPos,
    },
    queries: queryRows,
    pages: pageRows,
    crawl: latestCrawl
      ? {
          inIndex: number(latestCrawl.InIndex),
          crawledPages: number(latestCrawl.CrawledPages),
          crawlErrors: number(latestCrawl.CrawlErrors),
          code2xx: number(latestCrawl.Code2xx),
          code4xx: number(latestCrawl.Code4xx),
          code5xx: number(latestCrawl.Code5xx),
          blockedByRobotsTxt: number(latestCrawl.BlockedByRobotsTxt),
        }
      : null,
    quota: raw.quota
      ? {
          daily: number(raw.quota.DailyQuota),
          monthly: number(raw.quota.MonthlyQuota),
        }
      : null,
  };
}

export function findOpportunities(seo, engagement, api, bing) {
  const weakCtr = seo.rows
    .filter((row) => row.impressions >= 10 && row.ctr < 0.05)
    .slice(0, 10);
  const bingOpportunities = bing?.queries
    ? bing.queries
        .filter((q) => q.impressions >= 2 && q.position <= 5 && q.clicks === 0)
        .slice(0, 10)
    : [];
  const pagesWithoutStarts = engagement.byPage
    .filter((row) => (row.events.page_view ?? 0) > 0 && !(row.events.live_widget_start > 0))
    .slice(0, 10);
  const widgetErrors = engagement.byPage
    .filter((row) => row.events.live_search_error > 0)
    .slice(0, 10);
  const slowApi = api.bySurface
    .filter((row) => row.p95DurationMs >= 20_000)
    .slice(0, 10);
  return { weakCtr, bingOpportunities, pagesWithoutStarts, widgetErrors, slowApi };
}

export function renderMarkdown(report) {
  const lines = [
    '# EndMile Guide Performance',
    '',
    `Range: ${report.dateRange.from} to ${report.dateRange.to}`,
    '',
    '## Google Search Console (SEO)',
    `Clicks: ${report.seo.totals.clicks}`,
    `Impressions: ${report.seo.totals.impressions}`,
    `CTR: ${percent(report.seo.totals.ctr)}`,
    `Average position: ${report.seo.totals.position}`,
    '',
  ];

  const displayLimit = report.filters?.limit ?? 15;

  if (report.bing && (report.bing.totals.impressions > 0 || report.bing.queries.length > 0 || report.bing.crawl)) {
    lines.push(
      '## Bing Search Performance',
      `Clicks: ${report.bing.totals.clicks}`,
      `Impressions: ${report.bing.totals.impressions}`,
      `CTR: ${percent(report.bing.totals.ctr)}`,
      `Average position: ${report.bing.totals.position}`,
    );
    if (report.bing.crawl?.inIndex) {
      lines.push(`Pages in Bing index: ${report.bing.crawl.inIndex} (${report.bing.crawl.code2xx} HTTP 200, ${report.bing.crawl.crawlErrors} errors)`);
    }
    if (report.bing.quota?.daily) {
      lines.push(`URL submission quota: ${report.bing.quota.daily}/day (${report.bing.quota.monthly}/month)`);
    }
    lines.push('');

    if (report.bing.queries.length > 0) {
      lines.push(
        '### Top Bing Queries',
        table(
          ['Query', 'Clicks', 'Impressions', 'CTR', 'Position'],
          report.bing.queries.slice(0, displayLimit).map((row) => [
            row.query,
            row.clicks,
            row.impressions,
            percent(row.ctr),
            row.position,
          ]),
        ),
        '',
      );
    }

    if (report.bing.pages.length > 0) {
      lines.push(
        '### Top Bing Pages',
        table(
          ['Venue / Page', 'Clicks', 'Impressions', 'CTR', 'Position'],
          report.bing.pages.slice(0, displayLimit).map((row) => [
            row.venueName ? `${row.venueName} (${row.venueId})` : row.page,
            row.clicks,
            row.impressions,
            percent(row.ctr),
            row.position,
          ]),
        ),
        '',
      );
    }
  }

  lines.push('## Engagement & Conversion Breakdown');

  if (report.engagement.venuePages && report.engagement.venuePages.length > 0) {
    lines.push(
      '### Venue Page Actions & Monetisation',
      table(
        ['Venue / Guide Page', 'Views', 'Live Widget Views', 'Affiliate Clicks', 'App CTAs', 'Other Clicks'],
        report.engagement.venuePages.slice(0, displayLimit).map((p) => [
          p.venueName ? `${p.venueName} (${p.venueId})` : p.page,
          p.events.page_view ?? 0,
          p.events.live_widget_view ?? 0,
          p.events.affiliate_click ?? 0,
          p.events.app_cta_click ?? 0,
          (p.events.cta_click ?? 0) + (p.events.click ?? 0),
        ]),
      ),
      '',
    );
  }

  if (report.engagement.directoryPages && report.engagement.directoryPages.length > 0) {
    lines.push(
      '### Directory & Homepage Navigation',
      table(
        ['Directory Page', 'Page Views', 'App CTAs', 'Nav Clicks'],
        report.engagement.directoryPages.slice(0, displayLimit).map((p) => [
          p.page,
          p.events.page_view ?? 0,
          (p.events.app_cta_click ?? 0) + (p.events.cta_click ?? 0),
          (p.events.click ?? 0) + (p.events.venue_link_click ?? 0),
        ]),
      ),
      '',
    );
  }

  lines.push(
    '### Domain-wide Event Totals',
    table(['Event', 'Count'], Object.entries(report.engagement.byEvent)),
    '',
    '## API',
    `Searches: ${report.api.searches}`,
    `Cache hit rate: ${percent(report.api.cacheHitRate)}`,
    `OJP calls: ${report.api.ojpCalls}`,
    `Estimated OJP cost: GBP ${report.api.ojpCostPounds.toFixed(4)}`,
    '',
    table(
      ['Surface', 'Feature', 'Source', 'Searches', 'Cache hit rate', 'p95 ms'],
      report.api.bySurface.map((row) => [
        row.clientSurface,
        row.clientFeature,
        row.sourceLabel,
        row.searches,
        percent(row.cacheHitRate),
        row.p95DurationMs,
      ]),
    ),
    '',
    '## Opportunities',
    ...opportunityLines(report.opportunities),
  );
  return `${lines.join('\n')}\n`;
}

export async function fixtureLoaders(fixtureDir) {
  return {
    gsc: () => readJson(path.join(fixtureDir, 'gsc.json')),
    ga4: () => readJson(path.join(fixtureDir, 'ga4.json')),
    endpoint: () => readJson(path.join(fixtureDir, 'endpoint-calls.json')),
    api: () => readJson(path.join(fixtureDir, 'api-calls.json')),
    venues: (options) => loadVenueLookup(options),
    bing: async () => {
      try {
        return await readJson(path.join(fixtureDir, 'bing.json'));
      } catch {
        return null;
      }
    },
  };
}

export async function liveLoaders() {
  return {
    gsc: loadGscRows,
    ga4: loadGa4Rows,
    endpoint: loadEndpointRows,
    api: loadApiRows,
    venues: loadVenueLookup,
    bing: loadBingRows,
  };
}

async function loadVenueLookup(options) {
  if (!options.venueData) return new Map();
  const venuePath = path.resolve(options.venueData);
  try {
    await access(venuePath);
  } catch {
    return new Map();
  }
  const rows = await readJson(venuePath);
  if (!Array.isArray(rows)) return new Map();
  return new Map(rows
    .filter((row) => row.id !== undefined && row.name)
    .map((row) => [String(row.id), String(row.name)]));
}

async function loadGscRows(options, range) {
  const token = await googleAccessToken(options, options.gscGoogleCloudConfig);
  const body = {
    startDate: range.from,
    endDate: range.to,
    dimensions: ['query', 'page'],
    rowLimit: 25000,
    dimensionFilterGroups: pageFilterGroups(externalPageFilter(options)),
  };
  const url = `https://searchconsole.googleapis.com/webmasters/v3/sites/${encodeURIComponent(options.siteUrl)}/searchAnalytics/query`;
  const json = await googlePost(url, token, body);
  return (json.rows ?? []).map((row) => ({
    query: row.keys?.[0] ?? '',
    page: row.keys?.[1] ?? '',
    clicks: row.clicks,
    impressions: row.impressions,
    ctr: row.ctr,
    position: row.position,
  }));
}

async function loadGa4Rows(options, range) {
  const token = await googleAccessToken(options, options.ga4GoogleCloudConfig);
  const body = {
    dateRanges: [{ startDate: range.from, endDate: range.to }],
    dimensions: [{ name: 'eventName' }, { name: 'pageLocation' }],
    metrics: [{ name: 'eventCount' }],
    limit: '10000',
    dimensionFilter: ga4PageFilter(externalPageFilter(options)),
  };
  const json = await googlePost(`https://analyticsdata.googleapis.com/v1beta/${options.ga4Property}:runReport`, token, body);
  return (json.rows ?? []).map((row) => ({
    eventName: row.dimensionValues?.[0]?.value ?? '',
    pageLocation: row.dimensionValues?.[1]?.value ?? '',
    eventCount: row.metricValues?.[0]?.value ?? 0,
  }));
}

async function loadBingRows(options, _range) {
  if (options.noBing || !options.bingApiKey) return null;
  const siteUrl = options.bingSiteUrl || DEFAULT_BING_SITE_URL;
  const apiKey = options.bingApiKey;
  try {
    const [trafficRes, queryRes, pageRes, crawlRes, quotaRes] = await Promise.all([
      fetch(`https://ssl.bing.com/webmaster/api.svc/json/GetRankAndTrafficStats?siteUrl=${encodeURIComponent(siteUrl)}&apikey=${apiKey}`),
      fetch(`https://ssl.bing.com/webmaster/api.svc/json/GetQueryStats?siteUrl=${encodeURIComponent(siteUrl)}&apikey=${apiKey}`),
      fetch(`https://ssl.bing.com/webmaster/api.svc/json/GetPageStats?siteUrl=${encodeURIComponent(siteUrl)}&apikey=${apiKey}`),
      fetch(`https://ssl.bing.com/webmaster/api.svc/json/GetCrawlStats?siteUrl=${encodeURIComponent(siteUrl)}&apikey=${apiKey}`),
      fetch(`https://ssl.bing.com/webmaster/api.svc/json/GetUrlSubmissionQuota?siteUrl=${encodeURIComponent(siteUrl)}&apikey=${apiKey}`),
    ]);

    const trafficJson = trafficRes.ok ? await trafficRes.json() : { d: [] };
    const queryJson = queryRes.ok ? await queryRes.json() : { d: [] };
    const pageJson = pageRes.ok ? await pageRes.json() : { d: [] };
    const crawlJson = crawlRes.ok ? await crawlRes.json() : { d: [] };
    const quotaJson = quotaRes.ok ? await quotaRes.json() : { d: null };

    return {
      traffic: trafficJson.d || [],
      queries: queryJson.d || [],
      pages: pageJson.d || [],
      crawl: crawlJson.d || [],
      quota: quotaJson.d || null,
    };
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : String(error),
      traffic: [],
      queries: [],
      pages: [],
      crawl: [],
    };
  }
}

function parseWcfDate(wcfDate) {
  if (!wcfDate) return null;
  const match = String(wcfDate).match(/\d+/);
  if (!match) return null;
  return new Date(parseInt(match[0], 10)).toISOString().slice(0, 10);
}

async function loadEndpointRows(options, range) {
  if (options.sshDb) return loadRemoteRows(options, endpointRemoteSql(options, range));
  const pool = await createPool();
  try {
    const query = endpointSql(options, range);
    const result = await pool.query(query.text, query.values);
    return result.rows;
  } finally {
    await pool.end();
  }
}

async function loadApiRows(_options, range) {
  if (_options.sshDb) return loadRemoteRows(_options, apiRemoteSql(range));
  const pool = await createPool();
  try {
    const result = await pool.query(
      `SELECT service, COUNT(*)::int AS calls
       FROM api_calls
       WHERE created_at >= $1::timestamptz AND created_at < ($2::date + INTERVAL '1 day')
       GROUP BY service
       ORDER BY calls DESC`,
      [range.from, range.to],
    );
    return result.rows;
  } finally {
    await pool.end();
  }
}

async function loadRemoteRows(options, sql) {
  const { stdout } = await execFileAsync('ssh', [
    '-o',
    'BatchMode=yes',
    options.sshDb,
    remotePsqlCommand(options, sql),
  ], { maxBuffer: 50 * 1024 * 1024 });
  return JSON.parse(stdout.trim() || '[]');
}

function remotePsqlCommand(options, sql) {
  return [
    `cd ${shellSingleQuote(options.sshDbDir)}`,
    '&&',
    'docker compose exec -T postgres',
    `psql -U ${shellSingleQuote(options.sshDbUser)}`,
    `-d ${shellSingleQuote(options.sshDbName)}`,
    '-At -v ON_ERROR_STOP=1',
    `-c ${shellSingleQuote(sql)}`,
  ].join(' ');
}

function endpointRemoteSql(options, range) {
  const clauses = [
    `created_at >= ${sqlLiteral(range.from)}::timestamptz`,
    `created_at < (${sqlLiteral(range.to)}::date + INTERVAL '1 day')`,
    `path = ANY(ARRAY[${trackedPaths.map(sqlLiteral).join(', ')}]::text[])`,
  ];
  addOptionalRemoteClause(clauses, 'client_surface', options.surface);
  addOptionalRemoteClause(clauses, 'source_id', options.venueId);
  return jsonAggSql(`SELECT
      client_surface,
      client_feature,
      source_kind,
      source_id,
      COUNT(*)::int AS searches,
      SUM(CASE WHEN cache_hit THEN 1 ELSE 0 END)::int AS cache_hits,
      ROUND(AVG(duration_ms))::int AS avg_duration_ms,
      ROUND(percentile_cont(0.5) WITHIN GROUP (ORDER BY duration_ms))::int AS p50_duration_ms,
      ROUND(percentile_cont(0.95) WITHIN GROUP (ORDER BY duration_ms))::int AS p95_duration_ms
    FROM endpoint_calls
    WHERE ${clauses.join(' AND ')}
    GROUP BY client_surface, client_feature, source_kind, source_id
    ORDER BY searches DESC`);
}

function apiRemoteSql(range) {
  return jsonAggSql(`SELECT service, COUNT(*)::int AS calls
    FROM api_calls
    WHERE created_at >= ${sqlLiteral(range.from)}::timestamptz
      AND created_at < (${sqlLiteral(range.to)}::date + INTERVAL '1 day')
    GROUP BY service
    ORDER BY calls DESC`);
}

function jsonAggSql(selectSql) {
  return `SELECT COALESCE(json_agg(row_to_json(rows)), '[]'::json)::text FROM (${selectSql}) rows`;
}

function endpointSql(options, range) {
  const values = [range.from, range.to, trackedPaths];
  const clauses = [
    'created_at >= $1::timestamptz',
    "created_at < ($2::date + INTERVAL '1 day')",
    'path = ANY($3::text[])',
  ];
  addOptionalClause(clauses, values, 'client_surface', options.surface);
  addOptionalClause(clauses, values, 'source_id', options.venueId);
  return {
    text: `SELECT
        client_surface,
        client_feature,
        source_kind,
        source_id,
        COUNT(*)::int AS searches,
        SUM(CASE WHEN cache_hit THEN 1 ELSE 0 END)::int AS cache_hits,
        ROUND(AVG(duration_ms))::int AS avg_duration_ms,
        ROUND(percentile_cont(0.5) WITHIN GROUP (ORDER BY duration_ms))::int AS p50_duration_ms,
        ROUND(percentile_cont(0.95) WITHIN GROUP (ORDER BY duration_ms))::int AS p95_duration_ms
      FROM endpoint_calls
      WHERE ${clauses.join(' AND ')}
      GROUP BY client_surface, client_feature, source_kind, source_id
      ORDER BY searches DESC`,
    values,
  };
}

function addOptionalClause(clauses, values, column, value) {
  if (!value) return;
  values.push(value);
  clauses.push(`${column} = $${values.length}`);
}

function addOptionalRemoteClause(clauses, column, value) {
  if (!value) return;
  clauses.push(`${column} = ${sqlLiteral(value)}`);
}

function externalPageFilter(options) {
  if (options.page) return options.page;
  return options.surface === 'guide' ? 'guide.endmilerouting.co.uk' : undefined;
}

async function createPool() {
  const databaseUrl = process.env.ANALYTICS_DATABASE_URL ?? process.env.DATABASE_URL;
  if (!databaseUrl) throw new Error('ANALYTICS_DATABASE_URL or DATABASE_URL is required');
  const require = createRequire(import.meta.url);
  const pgPath = require.resolve('pg', { paths: [path.resolve('packages/server')] });
  const pgModule = await import(pathToFileURL(pgPath).href);
  const Pool = pgModule.Pool ?? pgModule.default?.Pool;
  return new Pool({ connectionString: databaseUrl });
}

async function googleAccessToken(options = {}, configOverride) {
  if (process.env.GOOGLE_ACCESS_TOKEN) return process.env.GOOGLE_ACCESS_TOKEN;
  const args = ['auth', 'application-default', 'print-access-token'];
  const command = process.platform === 'win32' ? 'cmd.exe' : 'gcloud';
  const commandArgs = process.platform === 'win32' ? ['/d', '/s', '/c', `gcloud ${args.join(' ')}`] : args;
  const googleCloudConfig = configOverride ?? options.googleCloudConfig;
  const env = googleCloudConfig
    ? { ...process.env, CLOUDSDK_CONFIG: path.resolve(googleCloudConfig) }
    : process.env;
  const { stdout } = await execFileAsync(command, commandArgs, { env });
  return stdout.trim();
}

async function googlePost(url, token, body) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  if (!response.ok) throw new Error(`Google API ${response.status}: ${await response.text()}`);
  return response.json();
}

function pageFilterGroups(page) {
  if (!page) return undefined;
  return [{
    filters: [{ dimension: 'page', operator: 'contains', expression: page }],
  }];
}

function ga4PageFilter(page) {
  if (!page) return undefined;
  return {
    filter: {
      fieldName: 'pageLocation',
      stringFilter: { matchType: 'CONTAINS', value: page },
    },
  };
}

function publicFilters(options) {
  return {
    surface: options.surface ?? null,
    venueId: options.venueId ?? null,
    query: options.query ?? null,
    limit: options.limit ?? 15,
    page: externalPageFilter(options) ?? null,
    siteUrl: options.siteUrl,
    bingSiteUrl: options.noBing ? null : options.bingSiteUrl,
    ga4Property: options.ga4Property,
    gscGoogleCloudConfig: options.gscGoogleCloudConfig ?? null,
    ga4GoogleCloudConfig: options.ga4GoogleCloudConfig ?? null,
    venueData: options.venueData,
  };
}

function shellSingleQuote(value) {
  return `'${String(value).replaceAll("'", "'\\''")}'`;
}

function sqlLiteral(value) {
  return `'${String(value).replaceAll("'", "''")}'`;
}

function normalizeEndpointRow(row, venueLookup = new Map()) {
  const sourceId = row.source_id ?? null;
  const sourceName = row.source_kind === 'venue' ? venueName(venueLookup, sourceId) : null;
  return {
    clientSurface: row.client_surface,
    clientFeature: row.client_feature,
    sourceKind: row.source_kind,
    sourceId,
    sourceName,
    sourceLabel: sourceLabel(row.source_kind, sourceId, sourceName),
    searches: number(row.searches),
    cacheHits: number(row.cache_hits),
    cacheHitRate: rate(number(row.cache_hits), number(row.searches)),
    avgDurationMs: number(row.avg_duration_ms),
    p50DurationMs: number(row.p50_duration_ms),
    p95DurationMs: number(row.p95_duration_ms),
  };
}

function venueIdFromPage(page) {
  return page.match(/-(\d+)\/?$/)?.[1] ?? null;
}

function venueName(venueLookup, venueId) {
  if (!venueId) return null;
  return venueLookup.get(String(venueId)) ?? null;
}

function sourceLabel(sourceKind, sourceId, sourceName) {
  if (sourceKind === 'venue' && sourceName && sourceId) return `${sourceName} (${sourceId})`;
  if (sourceKind === 'venue' && sourceId) return `Unknown venue (${sourceId})`;
  return sourceKind ?? 'none';
}

function number(value) {
  return Number(value ?? 0);
}

function rate(part, total) {
  return total > 0 ? round(part / total, 4) : 0;
}

function round(value, places = 2) {
  const factor = 10 ** places;
  return Math.round(value * factor) / factor;
}

function percent(value) {
  return `${round(value * 100, 2)}%`;
}

function parseIsoDate(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) throw new Error(`Invalid date: ${value}`);
  return value;
}

function isoDate(date) {
  return date.toISOString().slice(0, 10);
}

function numberFlag(flags, key, fallback) {
  const value = flags.get(key);
  if (value === undefined || value === true) return fallback;
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed < 1) throw new Error(`--${key} must be a positive integer`);
  return parsed;
}

function stringFlag(flags, key) {
  const value = flags.get(key);
  return typeof value === 'string' ? value : undefined;
}

async function readJson(filePath) {
  return JSON.parse(await readFile(filePath, 'utf8'));
}

function table(headers, rows) {
  if (rows.length === 0) return '_No rows._';
  const output = [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
  ];
  for (const row of rows) output.push(`| ${row.join(' | ')} |`);
  return output.join('\n');
}

function opportunityLines(opportunities) {
  const lines = [];
  lines.push(`Weak CTR pages (Google): ${opportunities.weakCtr.length}`);
  for (const row of opportunities.weakCtr.slice(0, 5)) {
    lines.push(`- ${row.page} (${row.impressions} impressions, ${percent(row.ctr)} CTR)`);
  }
  if (opportunities.bingOpportunities && opportunities.bingOpportunities.length > 0) {
    lines.push(`High-ranking Bing queries with 0 clicks: ${opportunities.bingOpportunities.length}`);
    for (const row of opportunities.bingOpportunities.slice(0, 5)) {
      lines.push(`- "${row.query}" (pos ${row.position}, ${row.impressions} impressions)`);
    }
  }
  lines.push(`Pages with views but no widget starts: ${opportunities.pagesWithoutStarts.length}`);
  lines.push(`Pages with widget errors: ${opportunities.widgetErrors.length}`);
  lines.push(`Slow API groups: ${opportunities.slowApi.length}`);
  return lines;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const loaders = options.fixtureDir ? await fixtureLoaders(options.fixtureDir) : await liveLoaders();
  const report = await buildReport(options, loaders);
  if (options.json && !options.markdown) console.log(JSON.stringify(report, null, 2));
  else console.log(renderMarkdown(report));
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    console.error(error instanceof Error ? error.message : error);
    process.exit(1);
  });
}
