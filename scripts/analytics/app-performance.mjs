#!/usr/bin/env node

import { execFile } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);
const DEFAULT_SITE_URL = 'sc-domain:endmilerouting.co.uk';
const DEFAULT_BING_SITE_URL = 'https://endmilerouting.co.uk/';
const DEFAULT_BING_API_KEY = 'f9541b772ec346ea816b0395881232e0';
const DEFAULT_GA4_PROPERTY = 'properties/531529105';
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
    surface: stringFlag(flags, 'surface') ?? 'app',
    tenantId: stringFlag(flags, 'tenant-id'),
    channel: stringFlag(flags, 'channel'),
    corridor: stringFlag(flags, 'corridor'),
    sshDb: stringFlag(flags, 'ssh-db'),
    sshDbDir: stringFlag(flags, 'ssh-db-dir') ?? '/opt/endmile',
    sshDbUser: stringFlag(flags, 'ssh-db-user') ?? 'endmile',
    sshDbName: stringFlag(flags, 'ssh-db-name') ?? 'endmile',
    siteUrl: stringFlag(flags, 'site-url') ?? DEFAULT_SITE_URL,
    bingApiKey: stringFlag(flags, 'bing-api-key') ?? process.env.BING_API_KEY ?? DEFAULT_BING_API_KEY,
    bingSiteUrl: stringFlag(flags, 'bing-site-url') ?? DEFAULT_BING_SITE_URL,
    noBing: Boolean(flags.get('no-bing')),
    query: stringFlag(flags, 'query'),
    limit: numberFlag(flags, 'limit', 15),
    ga4Property: stringFlag(flags, 'ga4-property') ?? DEFAULT_GA4_PROPERTY,
    googleCloudConfig: stringFlag(flags, 'google-cloud-config'),
    gscGoogleCloudConfig: stringFlag(flags, 'gsc-google-cloud-config'),
    ga4GoogleCloudConfig: stringFlag(flags, 'ga4-google-cloud-config'),
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
  const [
    gscRows,
    ga4AcquisitionRows,
    ga4EventRows,
    endpointRows,
    apiRows,
    recentSearchesRows,
    userRows,
    savingsRows,
    savedJourneysRows,
    bingData,
  ] = await Promise.all([
    loaders.gsc(options, range),
    loaders.ga4Acquisition(options, range),
    loaders.ga4Events(options, range),
    loaders.endpoint(options, range),
    loaders.api(options, range),
    loaders.recentSearches(options, range),
    loaders.users(options, range),
    loaders.savings(options, range),
    loaders.savedJourneys(options, range),
    loaders.bing ? loaders.bing(options, range) : null,
  ]);

  const acquisition = summarizeAcquisition(ga4AcquisitionRows, gscRows, bingData, options);
  const searchHealth = summarizeSearchHealth(endpointRows, apiRows);
  const corridors = summarizeCorridors(recentSearchesRows, options);
  const valueDelivered = summarizeValueDelivered(savingsRows, savedJourneysRows);
  const usersAndTenants = summarizeUsersAndTenants(userRows, endpointRows, options);

  return {
    generatedAt: new Date().toISOString(),
    dateRange: range,
    filters: publicFilters(options),
    acquisition,
    searchHealth,
    corridors,
    valueDelivered,
    usersAndTenants,
    opportunities: findOpportunities(acquisition, searchHealth, corridors, usersAndTenants),
  };
}

export function summarizeAcquisition(ga4AcquisitionRows = [], gscData = [], bingData = null, options = {}) {
  const channels = new Map();
  let totalSessions = 0;
  let totalActiveUsers = 0;
  let totalNewUsers = 0;

  for (const row of ga4AcquisitionRows) {
    const rawChannel = row.channelGroup || row.sourceMedium || 'Direct';
    const channel = classifyChannel(rawChannel, row.sourceMedium);
    const sessions = number(row.sessions);
    const activeUsers = number(row.activeUsers);
    const newUsers = number(row.newUsers);

    totalSessions += sessions;
    totalActiveUsers += activeUsers;
    totalNewUsers += newUsers;

    const entry = channels.get(channel) ?? {
      channel,
      sessions: 0,
      activeUsers: 0,
      newUsers: 0,
      topSources: new Map(),
    };
    entry.sessions += sessions;
    entry.activeUsers += activeUsers;
    entry.newUsers += newUsers;

    if (row.sourceMedium) {
      entry.topSources.set(row.sourceMedium, (entry.topSources.get(row.sourceMedium) ?? 0) + sessions);
    }
    channels.set(channel, entry);
  }

  const channelList = [...channels.values()]
    .map((c) => ({
      channel: c.channel,
      sessions: c.sessions,
      activeUsers: c.activeUsers,
      newUsers: c.newUsers,
      share: rate(c.sessions, totalSessions),
      topSource: [...c.topSources.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] ?? 'direct',
    }))
    .sort((a, b) => b.sessions - a.sessions);

  // SEO Queries from GSC
  const gscRows = Array.isArray(gscData) ? gscData : (gscData.rows ?? []);
  const gscSiteTotals = (!Array.isArray(gscData) && gscData.totals) ? gscData.totals : null;

  const filteredGsc = options.query
    ? gscRows.filter((r) => (r.query ?? '').toLowerCase().includes(options.query.toLowerCase()))
    : gscRows;

  const seoTotals = gscSiteTotals ?? filteredGsc.reduce((acc, row) => ({
    clicks: acc.clicks + number(row.clicks),
    impressions: acc.impressions + number(row.impressions),
    weightedPosition: acc.weightedPosition + number(row.position) * number(row.impressions),
  }), { clicks: 0, impressions: 0, weightedPosition: 0 });

  return {
    totals: {
      sessions: totalSessions,
      activeUsers: totalActiveUsers,
      newUsers: totalNewUsers,
      returningUsers: Math.max(totalActiveUsers - totalNewUsers, 0),
      returningRate: rate(Math.max(totalActiveUsers - totalNewUsers, 0), totalActiveUsers),
    },
    channels: channelList,
    seo: {
      clicks: seoTotals.clicks,
      impressions: seoTotals.impressions,
      ctr: rate(seoTotals.clicks, seoTotals.impressions),
      position: seoTotals.position !== undefined ? round(seoTotals.position, 1) : (seoTotals.impressions ? round(seoTotals.weightedPosition / seoTotals.impressions, 1) : 0),
      topQueries: filteredGsc.slice(0, options.limit ?? 15),
    },
  };
}

export function classifyChannel(channelGroup = '', sourceMedium = '') {
  const cg = channelGroup.toLowerCase();
  const sm = sourceMedium.toLowerCase();

  if (sm.includes('linkedin') || cg.includes('linkedin')) return 'LinkedIn';
  if (sm.includes('chatgpt') || sm.includes('perplexity') || sm.includes('claude') || sm.includes('copilot') || sm.includes('gemini') || sm.includes('openai') || /\bai\b/.test(sm)) return 'AI Referral';
  if (sm.includes('guide.endmilerouting.co.uk') || sm.includes('guide')) return 'B2C Guide Widget';
  if (cg.includes('organic search') || sm.includes('google') || sm.includes('bing')) return 'Organic Search';
  if (cg.includes('organic social') || cg.includes('paid social') || sm.includes('twitter') || sm.includes('reddit')) return 'Social';
  if (cg.includes('email') || sm.includes('email')) return 'Email / Invite';
  if (cg.includes('referral')) return 'Referral';
  if (cg.includes('direct') || sm.includes('(direct)')) return 'Direct';
  return channelGroup || 'Other';
}

export function summarizeSearchHealth(endpointRows = [], apiRows = []) {
  let totalSearches = 0;
  let successfulSearches = 0;
  let errorSearches = 0;
  let cacheHits = 0;
  let totalDurationSum = 0;
  let p50Duration = 0;
  let p95Duration = 0;

  for (const row of endpointRows) {
    const count = number(row.searches);
    totalSearches += count;
    cacheHits += number(row.cache_hits);
    totalDurationSum += number(row.avg_duration_ms) * count;
    if (number(row.status_code) >= 200 && number(row.status_code) < 300) {
      successfulSearches += count;
    } else {
      errorSearches += count;
    }
    if (row.p50_duration_ms) p50Duration = Math.max(p50Duration, number(row.p50_duration_ms));
    if (row.p95_duration_ms) p95Duration = Math.max(p95Duration, number(row.p95_duration_ms));
  }

  const ojpCalls = apiRows
    .filter((row) => row.service === 'ojp')
    .reduce((sum, row) => sum + number(row.calls), 0);

  const motisCalls = apiRows
    .filter((row) => row.service === 'motis')
    .reduce((sum, row) => sum + number(row.calls), 0);

  const osrmCalls = apiRows
    .filter((row) => row.service === 'osrm')
    .reduce((sum, row) => sum + number(row.calls), 0);

  return {
    totalSearches,
    successfulSearches,
    errorSearches,
    successRate: rate(successfulSearches, totalSearches),
    cacheHits,
    cacheHitRate: rate(cacheHits, totalSearches),
    avgDurationMs: totalSearches > 0 ? Math.round(totalDurationSum / totalSearches) : 0,
    p50DurationMs: p50Duration,
    p95DurationMs: p95Duration,
    upstreamEngines: {
      ojpCalls,
      ojpCostPounds: round((ojpCalls * OJP_COST_MILLI_PENCE) / 100_000, 4),
      motisCalls,
      osrmCalls,
    },
    byStatus: endpointRows.map((r) => ({
      statusCode: number(r.status_code),
      clientSurface: r.client_surface,
      searches: number(r.searches),
      cacheHits: number(r.cache_hits),
      avgDurationMs: number(r.avg_duration_ms),
      p95DurationMs: number(r.p95_duration_ms),
    })),
  };
}

export function summarizeCorridors(recentSearchesRows = [], options = {}) {
  const corridorMap = new Map();

  for (const row of recentSearchesRows) {
    const origin = (row.origin_name ?? 'Unknown Origin').trim();
    const dest = (row.dest_name ?? 'Unknown Dest').trim();
    const key = `${origin} -> ${dest}`;

    if (options.corridor && !key.toLowerCase().includes(options.corridor.toLowerCase())) {
      continue;
    }

    const count = number(row.search_count ?? row.searches ?? 1);
    const uniqueUsers = number(row.unique_users ?? 1);

    const entry = corridorMap.get(key) ?? {
      origin,
      dest,
      searches: 0,
      uniqueUsers: 0,
      modes: new Set(),
    };
    entry.searches += count;
    entry.uniqueUsers += uniqueUsers;
    if (row.selected_modes) {
      if (Array.isArray(row.selected_modes)) {
        row.selected_modes.forEach((m) => entry.modes.add(m));
      } else if (typeof row.selected_modes === 'object') {
        Object.keys(row.selected_modes).forEach((m) => entry.modes.add(m));
      }
    }
    corridorMap.set(key, entry);
  }

  const list = [...corridorMap.values()]
    .map((c) => ({
      corridor: `${c.origin} -> ${c.dest}`,
      origin: c.origin,
      dest: c.dest,
      searches: c.searches,
      uniqueUsers: c.uniqueUsers,
      modes: [...c.modes],
    }))
    .sort((a, b) => b.searches - a.searches)
    .slice(0, options.limit ?? 15);

  return {
    totalDistinctCorridors: corridorMap.size,
    topCorridors: list,
  };
}

export function summarizeValueDelivered(savingsRows = [], savedJourneysRows = []) {
  const savings = savingsRows.reduce((acc, row) => ({
    co2SavedGrams: acc.co2SavedGrams + number(row.total_co2_saved_grams ?? row.co2_saved_grams),
    costSavedPence: acc.costSavedPence + number(row.total_cost_saved_pence ?? row.cost_saved_pence),
    timeSavedMs: acc.timeSavedMs + number(row.total_time_saved_ms ?? row.time_difference_ms),
    journeysCompared: acc.journeysCompared + number(row.journeys_compared ?? 1),
  }), { co2SavedGrams: 0, costSavedPence: 0, timeSavedMs: 0, journeysCompared: 0 });

  const totalSavedRoutes = savedJourneysRows.reduce((sum, row) => sum + number(row.total_saves ?? 1), 0);
  const alertsEnabled = savedJourneysRows.reduce((sum, row) => sum + (row.alert_enabled ? number(row.total_saves ?? 1) : 0), 0);

  return {
    totalCostSavedPounds: round(savings.costSavedPence / 100, 2),
    totalCo2SavedKg: round(savings.co2SavedGrams / 1000, 1),
    totalTimeSavedHours: round(savings.timeSavedMs / (1000 * 60 * 60), 1),
    journeysCompared: savings.journeysCompared,
    savedRoutesCount: totalSavedRoutes,
    alertsEnabledCount: alertsEnabled,
  };
}

export function summarizeUsersAndTenants(userRows = [], endpointRows = [], options = {}) {
  let newUsersInWindow = 0;
  const tenants = new Map();

  for (const row of userRows) {
    newUsersInWindow += number(row.new_users_count ?? 1);
    const tenantId = row.tenant_id ?? 'individual';
    const tenantName = row.tenant_name ?? (tenantId === 'individual' ? 'Individual / Public' : `Tenant ${tenantId}`);
    const entry = tenants.get(tenantId) ?? {
      tenantId,
      tenantName,
      userCount: 0,
      searches: 0,
    };
    entry.userCount += number(row.user_count ?? 1);
    entry.searches += number(row.searches ?? 0);
    tenants.set(tenantId, entry);
  }

  const tenantList = [...tenants.values()]
    .sort((a, b) => b.userCount - a.userCount)
    .slice(0, options.limit ?? 15);

  return {
    newUsersInWindow,
    tenants: tenantList,
  };
}

export function findOpportunities(acquisition, searchHealth, corridors, usersAndTenants) {
  const highTrafficLowConversionChannels = acquisition.channels
    .filter((c) => c.sessions >= 10 && c.activeUsers / c.sessions < 0.2)
    .slice(0, 5);

  const errorStatusAlerts = searchHealth.byStatus
    .filter((s) => s.statusCode >= 400 && s.searches > 0)
    .slice(0, 5);

  const topCorridorsWithoutSaves = corridors.topCorridors
    .filter((c) => c.searches >= 5)
    .slice(0, 5);

  return {
    highTrafficLowConversionChannels,
    errorStatusAlerts,
    topCorridorsWithoutSaves,
  };
}

export function renderMarkdown(report) {
  const lines = [
    '# EndMile App & Core Routing Performance',
    '',
    `**Reporting Range:** ${report.dateRange.from} to ${report.dateRange.to}`,
    `**Generated:** ${report.generatedAt}`,
    '',
    '## 1. Executive Summary',
    `- **Total App Searches:** ${report.searchHealth.totalSearches.toLocaleString()}`,
    `- **Search Success Rate:** ${percent(report.searchHealth.successRate)}`,
    `- **Cache Hit Rate:** ${percent(report.searchHealth.cacheHitRate)} (p50: ${report.searchHealth.p50DurationMs}ms, p95: ${report.searchHealth.p95DurationMs}ms)`,
    `- **Total Sessions (GA4):** ${report.acquisition.totals.sessions.toLocaleString()}`,
    `- **Active Users:** ${report.acquisition.totals.activeUsers.toLocaleString()} (${percent(report.acquisition.totals.returningRate)} returning)`,
    `- **Total TCO Cost Saved vs Driving:** £${report.valueDelivered.totalCostSavedPounds.toLocaleString()}`,
    `- **Total Carbon Saved:** ${report.valueDelivered.totalCo2SavedKg.toLocaleString()} kg CO2`,
    '',
    '## 2. Traffic Acquisition & Referral Sources',
    table(
      ['Channel', 'Top Source / Medium', 'Sessions', 'Share', 'Active Users', 'New Users'],
      report.acquisition.channels.map((c) => [
        c.channel,
        c.topSource,
        c.sessions,
        percent(c.share),
        c.activeUsers,
        c.newUsers,
      ]),
    ),
    '',
  ];

  if (report.acquisition.seo.clicks > 0 || report.acquisition.seo.impressions > 0) {
    lines.push(
      '### Organic Search Acquisition (Google/Bing)',
      `- **Search Clicks:** ${report.acquisition.seo.clicks}`,
      `- **Impressions:** ${report.acquisition.seo.impressions}`,
      `- **Average CTR:** ${percent(report.acquisition.seo.ctr)}`,
      `- **Average Position:** ${report.acquisition.seo.position}`,
      '',
    );
  }

  lines.push(
    '## 3. Search & Engine Health',
    table(
      ['HTTP Status', 'Client Surface', 'Searches', 'Cache Hits', 'Avg Duration (ms)', 'p95 Duration (ms)'],
      report.searchHealth.byStatus.map((s) => [
        s.statusCode,
        s.clientSurface,
        s.searches,
        s.cacheHits,
        s.avgDurationMs,
        s.p95DurationMs,
      ]),
    ),
    '',
    `**Upstream Engines:** OJP Calls: ${report.searchHealth.upstreamEngines.ojpCalls} (£${report.searchHealth.upstreamEngines.ojpCostPounds}), MOTIS Calls: ${report.searchHealth.upstreamEngines.motisCalls}, OSRM Calls: ${report.searchHealth.upstreamEngines.osrmCalls}`,
    '',
    '## 4. Top Corridors Searched',
    table(
      ['Corridor (Origin -> Destination)', 'Search Count', 'Unique Users'],
      report.corridors.topCorridors.map((c) => [
        c.corridor,
        c.searches,
        c.uniqueUsers,
      ]),
    ),
    '',
    '## 5. Value Realisation & B2B ROI',
    `- **TCO Cost Saved:** £${report.valueDelivered.totalCostSavedPounds.toLocaleString()} across ${report.valueDelivered.journeysCompared} compared routes`,
    `- **Carbon Saved:** ${report.valueDelivered.totalCo2SavedKg.toLocaleString()} kg CO2 (${report.valueDelivered.totalTimeSavedHours}h total travel delta)`,
    `- **Saved Routes:** ${report.valueDelivered.savedRoutesCount} (${report.valueDelivered.alertsEnabledCount} disruption alerts active)`,
    '',
  );

  if (report.usersAndTenants.tenants.length > 0) {
    lines.push(
      '## 6. Corporate Tenants & User Cohorts',
      table(
        ['Tenant / Organization', 'User Count', 'Searches'],
        report.usersAndTenants.tenants.map((t) => [
          t.tenantName,
          t.userCount,
          t.searches,
        ]),
      ),
      '',
    );
  }

  lines.push(
    '## 7. Opportunities & Diagnostic Action Items',
  );

  if (report.opportunities.errorStatusAlerts.length > 0) {
    lines.push(
      '### Routing Errors Detected',
      ...report.opportunities.errorStatusAlerts.map(
        (e) => `- Status ${e.statusCode} on surface ${e.clientSurface} (${e.searches} occurrences, p95 ${e.p95DurationMs}ms). Inspect server logs for backend timeouts or bad origin/dest coordinates.`,
      ),
    );
  } else {
    lines.push('- No elevated search status errors detected.');
  }

  if (report.opportunities.highTrafficLowConversionChannels.length > 0) {
    lines.push(
      '### Acquisition Funnel Drop-off',
      ...report.opportunities.highTrafficLowConversionChannels.map(
        (c) => `- Channel **${c.channel}** has ${c.sessions} sessions but only ${c.activeUsers} active users (<20% activation). Check landing page CTA to search route planner.`,
      ),
    );
  }

  return `${lines.join('\n')}\n`;
}

// ─── Loaders & Database Adapters ─────────────────────────────────────────────

export async function fixtureLoaders(fixtureDir) {
  return {
    gsc: () => readJson(path.join(fixtureDir, 'gsc.json')),
    ga4Acquisition: () => readJson(path.join(fixtureDir, 'ga4-acquisition.json')),
    ga4Events: () => readJson(path.join(fixtureDir, 'ga4-events.json')),
    endpoint: () => readJson(path.join(fixtureDir, 'endpoint-calls.json')),
    api: () => readJson(path.join(fixtureDir, 'api-calls.json')),
    recentSearches: () => readJson(path.join(fixtureDir, 'recent-searches.json')),
    users: () => readJson(path.join(fixtureDir, 'users.json')),
    savings: () => readJson(path.join(fixtureDir, 'savings.json')),
    savedJourneys: () => readJson(path.join(fixtureDir, 'saved-journeys.json')),
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
    ga4Acquisition: loadGa4AcquisitionRows,
    ga4Events: loadGa4EventRows,
    endpoint: loadEndpointRows,
    api: loadApiRows,
    recentSearches: loadRecentSearchesRows,
    users: loadUserRows,
    savings: loadSavingsRows,
    savedJourneys: loadSavedJourneysRows,
    bing: loadBingRows,
  };
}

async function loadGscRows(options, range) {
  const token = await googleAccessToken(options, options.gscGoogleCloudConfig);
  const url = `https://searchconsole.googleapis.com/webmasters/v3/sites/${encodeURIComponent(options.siteUrl)}/searchAnalytics/query`;

  const [totalsJson, queriesJson] = await Promise.all([
    googlePost(url, token, {
      startDate: range.from,
      endDate: range.to,
    }),
    googlePost(url, token, {
      startDate: range.from,
      endDate: range.to,
      dimensions: ['query', 'page'],
      rowLimit: 5000,
    }),
  ]);

  const siteRow = totalsJson.rows?.[0] ?? null;
  const totals = siteRow ? {
    clicks: number(siteRow.clicks),
    impressions: number(siteRow.impressions),
    ctr: number(siteRow.ctr),
    position: number(siteRow.position),
  } : null;

  const rows = (queriesJson.rows ?? []).map((row) => ({
    query: row.keys?.[0] ?? '',
    page: row.keys?.[1] ?? '',
    clicks: row.clicks,
    impressions: row.impressions,
    ctr: row.ctr,
    position: row.position,
  }));

  return { totals, rows };
}

async function loadGa4AcquisitionRows(options, range) {
  const token = await googleAccessToken(options, options.ga4GoogleCloudConfig);
  const body = {
    dateRanges: [{ startDate: range.from, endDate: range.to }],
    dimensions: [
      { name: 'sessionDefaultChannelGroup' },
      { name: 'sessionSourceMedium' },
    ],
    metrics: [
      { name: 'sessions' },
      { name: 'activeUsers' },
      { name: 'newUsers' },
    ],
    limit: '1000',
  };
  const json = await googlePost(`https://analyticsdata.googleapis.com/v1beta/${options.ga4Property}:runReport`, token, body);
  return (json.rows ?? []).map((row) => ({
    channelGroup: row.dimensionValues?.[0]?.value ?? '',
    sourceMedium: row.dimensionValues?.[1]?.value ?? '',
    sessions: row.metricValues?.[0]?.value ?? 0,
    activeUsers: row.metricValues?.[1]?.value ?? 0,
    newUsers: row.metricValues?.[2]?.value ?? 0,
  }));
}

async function loadGa4EventRows(options, range) {
  const token = await googleAccessToken(options, options.ga4GoogleCloudConfig);
  const body = {
    dateRanges: [{ startDate: range.from, endDate: range.to }],
    dimensions: [{ name: 'eventName' }, { name: 'pagePath' }],
    metrics: [{ name: 'eventCount' }],
    limit: '5000',
  };
  const json = await googlePost(`https://analyticsdata.googleapis.com/v1beta/${options.ga4Property}:runReport`, token, body);
  return (json.rows ?? []).map((row) => ({
    eventName: row.dimensionValues?.[0]?.value ?? '',
    pagePath: row.dimensionValues?.[1]?.value ?? '',
    eventCount: row.metricValues?.[0]?.value ?? 0,
  }));
}

async function loadBingRows(options) {
  if (options.noBing || !options.bingApiKey) return null;
  const siteUrl = options.bingSiteUrl || DEFAULT_BING_SITE_URL;
  const apiKey = options.bingApiKey;
  try {
    const res = await fetch(`https://ssl.bing.com/webmaster/api.svc/json/GetRankAndTrafficStats?siteUrl=${encodeURIComponent(siteUrl)}&apikey=${apiKey}`);
    const json = res.ok ? await res.json() : { d: [] };
    return { traffic: json.d || [] };
  } catch {
    return null;
  }
}

async function loadEndpointRows(options, range) {
  const sql = endpointRemoteSql(options, range);
  if (options.sshDb) return loadRemoteRows(options, sql);
  const pool = await createPool();
  try {
    const result = await pool.query(sql);
    return result.rows;
  } finally {
    await pool.end();
  }
}

async function loadApiRows(options, range) {
  const sql = `SELECT service, COUNT(*)::int AS calls
       FROM api_calls
       WHERE created_at >= ${sqlLiteral(range.from)}::timestamptz AND created_at < (${sqlLiteral(range.to)}::date + INTERVAL '1 day')
       GROUP BY service
       ORDER BY calls DESC`;
  if (options.sshDb) return loadRemoteRows(options, jsonAggSql(sql));
  const pool = await createPool();
  try {
    const result = await pool.query(sql);
    return result.rows;
  } finally {
    await pool.end();
  }
}

async function loadRecentSearchesRows(options, range) {
  const sql = `SELECT origin_name, dest_name, COUNT(*)::int AS searches, COUNT(DISTINCT user_id)::int AS unique_users
       FROM (
         SELECT origin_name, dest_name, user_id::text AS user_id, searched_at FROM recent_searches
         UNION ALL
         SELECT origin_name, dest_name, anon_id AS user_id, searched_at FROM anonymous_recent_searches
       ) combined
       WHERE searched_at >= ${sqlLiteral(range.from)}::timestamptz AND searched_at < (${sqlLiteral(range.to)}::date + INTERVAL '1 day')
       GROUP BY origin_name, dest_name
       ORDER BY searches DESC
       LIMIT ${number(options.limit ?? 25)}`;
  if (options.sshDb) return loadRemoteRows(options, jsonAggSql(sql));
  const pool = await createPool();
  try {
    const result = await pool.query(sql);
    return result.rows;
  } finally {
    await pool.end();
  }
}

async function loadUserRows(options, range) {
  const sql = `SELECT
       u.tenant_id,
       COALESCE(t.name, 'Individual') AS tenant_name,
       COUNT(DISTINCT u.id)::int AS user_count,
       COUNT(DISTINCT CASE WHEN u.created_at >= ${sqlLiteral(range.from)}::timestamptz AND u.created_at < (${sqlLiteral(range.to)}::date + INTERVAL '1 day') THEN u.id END)::int AS new_users_count
       FROM users u
       LEFT JOIN tenants t ON t.id = u.tenant_id
       GROUP BY u.tenant_id, t.name
       ORDER BY user_count DESC`;
  if (options.sshDb) return loadRemoteRows(options, jsonAggSql(sql));
  const pool = await createPool();
  try {
    const result = await pool.query(sql);
    return result.rows;
  } finally {
    await pool.end();
  }
}

async function loadSavingsRows(options, range) {
  const sql = `SELECT
       SUM(GREATEST(co2_saved_grams, 0))::bigint AS total_co2_saved_grams,
       SUM(GREATEST(cost_saved_pence, 0))::bigint AS total_cost_saved_pence,
       SUM(GREATEST(-time_difference_ms, 0))::bigint AS total_time_saved_ms,
       COUNT(*)::bigint AS journeys_compared
       FROM journey_analytics
       WHERE created_at >= ${sqlLiteral(range.from)}::timestamptz AND created_at < (${sqlLiteral(range.to)}::date + INTERVAL '1 day')`;
  if (options.sshDb) return loadRemoteRows(options, jsonAggSql(sql));
  const pool = await createPool();
  try {
    const result = await pool.query(sql);
    return result.rows;
  } finally {
    await pool.end();
  }
}

async function loadSavedJourneysRows(options, range) {
  const sql = `SELECT
       COUNT(*)::int AS total_saves,
       SUM(CASE WHEN notification_enabled THEN 1 ELSE 0 END)::int AS alert_enabled
       FROM (
         SELECT id, notification_enabled, created_at FROM saved_journeys
         UNION ALL
         SELECT id, false AS notification_enabled, created_at FROM anonymous_saved_journeys
       ) combined
       WHERE created_at >= ${sqlLiteral(range.from)}::timestamptz AND created_at < (${sqlLiteral(range.to)}::date + INTERVAL '1 day')`;
  if (options.sshDb) return loadRemoteRows(options, jsonAggSql(sql));
  const pool = await createPool();
  try {
    const result = await pool.query(sql);
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
  if (options.surface) {
    clauses.push(`client_surface = ${sqlLiteral(options.surface)}`);
  }
  return jsonAggSql(`SELECT
      status_code,
      client_surface,
      client_feature,
      COUNT(*)::int AS searches,
      SUM(CASE WHEN cache_hit THEN 1 ELSE 0 END)::int AS cache_hits,
      ROUND(AVG(duration_ms))::int AS avg_duration_ms,
      ROUND(percentile_cont(0.5) WITHIN GROUP (ORDER BY duration_ms))::int AS p50_duration_ms,
      ROUND(percentile_cont(0.95) WITHIN GROUP (ORDER BY duration_ms))::int AS p95_duration_ms
    FROM endpoint_calls
    WHERE ${clauses.join(' AND ')}
    GROUP BY status_code, client_surface, client_feature
    ORDER BY searches DESC`);
}

function jsonAggSql(query) {
  return `SELECT COALESCE(json_agg(t), '[]'::json) FROM (${query}) t;`;
}

// ─── Google Auth & Helpers ───────────────────────────────────────────────────

async function googleAccessToken(options, cloudConfigPath) {
  if (process.env.GOOGLE_ACCESS_TOKEN) return process.env.GOOGLE_ACCESS_TOKEN.trim();
  const args = ['auth', 'application-default', 'print-access-token'];
  const command = process.platform === 'win32' ? 'cmd.exe' : 'gcloud';
  const commandArgs = process.platform === 'win32' ? ['/d', '/s', '/c', `gcloud ${args.join(' ')}`] : args;
  const effectiveConfig = cloudConfigPath ?? options.googleCloudConfig;
  const env = effectiveConfig
    ? { ...process.env, CLOUDSDK_CONFIG: path.resolve(effectiveConfig) }
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
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Google API ${response.status}: ${text}`);
  }
  return response.json();
}

async function createPool() {
  const require = createRequire(import.meta.url);
  const { Pool } = require('pg');
  const connectionString = process.env.ANALYTICS_DATABASE_URL || process.env.DATABASE_URL;
  if (!connectionString) {
    throw new Error('Database connection requires ANALYTICS_DATABASE_URL or DATABASE_URL, or use --ssh-db');
  }
  return new Pool({ connectionString });
}

async function readJson(filePath) {
  const content = await readFile(filePath, 'utf8');
  return JSON.parse(content);
}

function stringFlag(flags, name) {
  const val = flags.get(name);
  return typeof val === 'string' ? val : undefined;
}

function numberFlag(flags, name, fallback) {
  const val = flags.get(name);
  if (typeof val === 'number') return val;
  if (typeof val === 'string') {
    const parsed = Number(val);
    if (!Number.isNaN(parsed)) return parsed;
  }
  return fallback;
}

function parseIsoDate(str) {
  return new Date(str).toISOString().slice(0, 10);
}

function isoDate(date) {
  return date.toISOString().slice(0, 10);
}

function number(val) {
  const num = Number(val);
  return Number.isNaN(num) ? 0 : num;
}

function rate(numerator, denominator) {
  if (!denominator) return 0;
  return round(numerator / denominator, 4);
}

function round(val, decimals = 2) {
  const factor = 10 ** decimals;
  return Math.round(val * factor) / factor;
}

function percent(val) {
  return `${(round(val * 100, 1)).toFixed(1)}%`;
}

function table(headers, rows) {
  const headerLine = `| ${headers.join(' | ')} |`;
  const sepLine = `| ${headers.map(() => '---').join(' | ')} |`;
  const rowLines = rows.map((r) => `| ${r.map((c) => (c === undefined || c === null ? '' : String(c))).join(' | ')} |`);
  return [headerLine, sepLine, ...rowLines].join('\n');
}

function sqlLiteral(val) {
  return `'${String(val).replace(/'/g, "''")}'`;
}

function shellSingleQuote(val) {
  return `'${String(val).replace(/'/g, "'\\''")}'`;
}

function publicFilters(options) {
  return {
    days: options.days,
    from: options.from,
    to: options.to,
    surface: options.surface,
    tenantId: options.tenantId,
    channel: options.channel,
    corridor: options.corridor,
    limit: options.limit,
  };
}

// ─── Entry Point Execution ───────────────────────────────────────────────────

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const loaders = options.fixtureDir
    ? await fixtureLoaders(options.fixtureDir)
    : await liveLoaders();

  const report = await buildReport(options, loaders);
  if (options.json && !options.markdown) {
    console.log(JSON.stringify(report, null, 2));
  } else {
    console.log(renderMarkdown(report));
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    console.error(error instanceof Error ? error.message : error);
    process.exit(1);
  });
}
