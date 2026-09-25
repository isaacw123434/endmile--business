#!/usr/bin/env node

import assert from 'node:assert/strict';
import { mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';

import {
  buildReport,
  dateRange,
  fixtureLoaders,
  parseArgs,
  renderMarkdown,
  summarizeApi,
  summarizeBing,
} from './guide-performance.mjs';

test('parseArgs reads date range and filters', () => {
  const options = parseArgs([
    '--days', '14',
    '--surface', 'guide',
    '--venue-id', '130231837',
    '--page', 'guide.endmilerouting.co.uk/venues/',
    '--ssh-db', 'deploy@155.133.23.54',
    '--bing-api-key', 'custom-bing-key',
    '--bing-site-url', 'https://custom.site/',
    '--gsc-google-cloud-config', 'C:/Users/isaac/.gcloud-endmile-gsc',
    '--ga4-google-cloud-config', 'C:/Users/isaac/.gcloud-endmile-analytics',
    '--venue-data', 'data/venues/master_venues.json',
    '--json',
  ]);

  assert.equal(options.days, 14);
  assert.equal(options.surface, 'guide');
  assert.equal(options.venueId, '130231837');
  assert.equal(options.page, 'guide.endmilerouting.co.uk/venues/');
  assert.equal(options.sshDb, 'deploy@155.133.23.54');
  assert.equal(options.sshDbDir, '/opt/endmile');
  assert.equal(options.bingApiKey, 'custom-bing-key');
  assert.equal(options.bingSiteUrl, 'https://custom.site/');
  assert.equal(options.noBing, false);
  assert.equal(options.gscGoogleCloudConfig, 'C:/Users/isaac/.gcloud-endmile-gsc');
  assert.equal(options.ga4GoogleCloudConfig, 'C:/Users/isaac/.gcloud-endmile-analytics');
  assert.equal(options.venueData, 'data/venues/master_venues.json');
  assert.equal(options.json, true);
});

test('dateRange defaults to the requested trailing day count', () => {
  const range = dateRange({ days: 7 }, new Date('2026-08-13T12:00:00Z'));

  assert.deepEqual(range, { from: '2026-08-07', to: '2026-08-13' });
});

test('summarizeApi reports surface counts and OJP cost', () => {
  const api = summarizeApi([
    {
      client_surface: 'guide',
      client_feature: 'live_widget',
      source_kind: 'venue',
      source_id: '130231837',
      searches: 4,
      cache_hits: 1,
      avg_duration_ms: 8000,
      p50_duration_ms: 7000,
      p95_duration_ms: 21000,
    },
  ], [
    { service: 'ojp', calls: 10 },
  ]);

  assert.equal(api.searches, 4);
  assert.equal(api.cacheHitRate, 0.25);
  assert.equal(api.ojpCalls, 10);
  assert.equal(api.ojpCostPounds, 0.0042);
  assert.equal(api.bySurface[0].clientSurface, 'guide');
  assert.equal(api.bySurface[0].sourceLabel, 'Unknown venue (130231837)');
});

test('summarizeBing filters by date range and groups queries and pages', () => {
  const venueLookup = new Map([['26301254', 'Leeds Grand Theatre']]);
  const summary = summarizeBing({
    traffic: [
      { Date: '/Date(1787875200000)/', Clicks: 1, Impressions: 10 },
      { Date: '/Date(1788480000000)/', Clicks: 2, Impressions: 20 },
    ],
    queries: [
      { Query: 'closest park and ride to leeds grand theatre', Clicks: 1, Impressions: 5, AvgImpressionPosition: 4, Date: '/Date(1788480000000)/' },
      { Query: 'polar museum walk', Clicks: 0, Impressions: 10, AvgImpressionPosition: 2, Date: '/Date(1788480000000)/' },
    ],
    pages: [
      { Query: 'https://guide.endmilerouting.co.uk/venues/leeds-grand-theatre-26301254/', Clicks: 1, Impressions: 5, AvgImpressionPosition: 4, Date: '/Date(1788480000000)/' },
    ],
    crawl: [
      { InIndex: 150, CrawledPages: 12, CrawlErrors: 0, Code2xx: 150 },
    ],
  }, { from: '2026-09-01', to: '2026-09-10' }, venueLookup);

  assert.equal(summary.totals.clicks, 2);
  assert.equal(summary.totals.impressions, 20);
  assert.equal(summary.totals.ctr, 0.1);
  assert.equal(summary.queries.length, 2);
  assert.equal(summary.queries[0].query, 'closest park and ride to leeds grand theatre');
  assert.equal(summary.queries[0].clicks, 1);
  assert.equal(summary.pages.length, 1);
  assert.equal(summary.pages[0].venueName, 'Leeds Grand Theatre');
  assert.equal(summary.crawl.inIndex, 150);
});

test('buildReport joins fixture rows into opportunities', async () => {
  const fixtureDir = await mkdtemp(path.join(os.tmpdir(), 'endmile-guide-performance-'));
  try {
    await writeFixture(fixtureDir, 'gsc.json', [
      {
        query: 'leicester magistrates court parking',
        page: 'https://guide.endmilerouting.co.uk/venues/leicester-magistrates-court-130231837/',
        clicks: 1,
        impressions: 50,
        ctr: 0.02,
        position: 11.5,
      },
    ]);
    await writeFixture(fixtureDir, 'ga4.json', [
      {
        eventName: 'page_view',
        pageLocation: 'https://guide.endmilerouting.co.uk/venues/leicester-magistrates-court-130231837/',
        eventCount: 12,
      },
      {
        eventName: 'live_search_error',
        pageLocation: 'https://guide.endmilerouting.co.uk/venues/leicester-magistrates-court-130231837/',
        eventCount: 2,
      },
    ]);
    await writeFixture(fixtureDir, 'endpoint-calls.json', [
      {
        client_surface: 'guide',
        client_feature: 'live_widget',
        source_kind: 'venue',
        source_id: '130231837',
        searches: 3,
        cache_hits: 0,
        avg_duration_ms: 15000,
        p50_duration_ms: 14000,
        p95_duration_ms: 22000,
      },
    ]);
    await writeFixture(fixtureDir, 'api-calls.json', [{ service: 'ojp', calls: 6 }]);
    await writeFixture(fixtureDir, 'master-venues.json', [{
      id: 130231837,
      name: "Leicester Magistrates' Court",
    }]);
    await writeFixture(fixtureDir, 'bing.json', {
      traffic: [
        { Date: '/Date(1788480000000)/', Clicks: 1, Impressions: 15 },
      ],
      queries: [
        { Query: 'leicester magistrates court parking', Clicks: 1, Impressions: 15, AvgImpressionPosition: 2, Date: '/Date(1788480000000)/' },
      ],
      pages: [
        { Query: 'https://guide.endmilerouting.co.uk/venues/leicester-magistrates-court-130231837/', Clicks: 1, Impressions: 15, AvgImpressionPosition: 2, Date: '/Date(1788480000000)/' },
      ],
      crawl: [
        { InIndex: 120, CrawledPages: 10, CrawlErrors: 0, Code2xx: 120 },
      ],
    });

    const report = await buildReport(
      parseArgs([
        '--fixture-dir', fixtureDir,
        '--venue-data', path.join(fixtureDir, 'master-venues.json'),
        '--days', '28',
      ]),
      await fixtureLoaders(fixtureDir),
    );

    assert.equal(report.seo.rows[0].venueId, '130231837');
    assert.equal(report.seo.rows[0].venueName, "Leicester Magistrates' Court");
    assert.equal(report.bing.totals.clicks, 1);
    assert.equal(report.bing.totals.impressions, 15);
    assert.equal(report.bing.pages[0].venueName, "Leicester Magistrates' Court");
    assert.equal(report.engagement.byEvent.live_search_error, 2);
    assert.equal(report.api.searches, 3);
    assert.equal(report.api.bySurface[0].sourceLabel, "Leicester Magistrates' Court (130231837)");
    assert.equal(report.opportunities.weakCtr.length, 1);
    assert.equal(report.opportunities.widgetErrors.length, 1);
    assert.equal(report.opportunities.slowApi.length, 1);
    assert.match(renderMarkdown(report), /EndMile Guide Performance/);
    assert.match(renderMarkdown(report), /Bing Search Performance/);
    assert.match(renderMarkdown(report), /Leicester Magistrates' Court \(130231837\)/);
  } finally {
    await rm(fixtureDir, { recursive: true, force: true });
  }
});

async function writeFixture(dir, name, rows) {
  await writeFile(path.join(dir, name), JSON.stringify(rows), 'utf8');
}
