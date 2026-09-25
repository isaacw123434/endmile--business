#!/usr/bin/env node

import assert from 'node:assert/strict';
import { mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';

import {
  buildReport,
  classifyChannel,
  dateRange,
  fixtureLoaders,
  parseArgs,
  renderMarkdown,
  summarizeAcquisition,
  summarizeCorridors,
  summarizeSearchHealth,
  summarizeUsersAndTenants,
  summarizeValueDelivered,
} from './app-performance.mjs';

test('parseArgs reads CLI flags and options', () => {
  const options = parseArgs([
    '--days', '14',
    '--surface', 'app',
    '--tenant-id', 'tenant-123',
    '--channel', 'linkedin',
    '--corridor', 'London -> Manchester',
    '--ssh-db', 'deploy@155.133.23.54',
    '--limit', '20',
    '--json',
  ]);

  assert.equal(options.days, 14);
  assert.equal(options.surface, 'app');
  assert.equal(options.tenantId, 'tenant-123');
  assert.equal(options.channel, 'linkedin');
  assert.equal(options.corridor, 'London -> Manchester');
  assert.equal(options.sshDb, 'deploy@155.133.23.54');
  assert.equal(options.limit, 20);
  assert.equal(options.json, true);
});

test('dateRange calculates expected trailing range', () => {
  const range = dateRange({ days: 7 }, new Date('2026-09-14T12:00:00Z'));
  assert.deepEqual(range, { from: '2026-09-08', to: '2026-09-14' });
});

test('classifyChannel maps sources and mediums to recognizable channels', () => {
  assert.equal(classifyChannel('Organic Social', 'linkedin.com / referral'), 'LinkedIn');
  assert.equal(classifyChannel('Referral', 'chatgpt.com / referral'), 'AI Referral');
  assert.equal(classifyChannel('Referral', 'guide.endmilerouting.co.uk / referral'), 'B2C Guide Widget');
  assert.equal(classifyChannel('Organic Search', 'google / organic'), 'Organic Search');
  assert.equal(classifyChannel('Direct', '(direct) / (none)'), 'Direct');
  assert.equal(classifyChannel('Email', 'sendgrid / email'), 'Email / Invite');
});

test('summarizeAcquisition groups channels and SEO metrics correctly', () => {
  const acquisition = summarizeAcquisition([
    { channelGroup: 'Direct', sourceMedium: '(direct) / (none)', sessions: 50, activeUsers: 40, newUsers: 30 },
    { channelGroup: 'Organic Social', sourceMedium: 'linkedin.com / social', sessions: 30, activeUsers: 25, newUsers: 20 },
    { channelGroup: 'Referral', sourceMedium: 'chatgpt.com / referral', sessions: 20, activeUsers: 15, newUsers: 10 },
  ], [
    { query: 'best corporate multimodal journey planner uk', page: 'https://endmilerouting.co.uk/', clicks: 5, impressions: 100, ctr: 0.05, position: 3.2 },
  ]);

  assert.equal(acquisition.totals.sessions, 100);
  assert.equal(acquisition.totals.activeUsers, 80);
  assert.equal(acquisition.totals.newUsers, 60);
  assert.equal(acquisition.totals.returningUsers, 20);
  assert.equal(acquisition.channels.length, 3);
  assert.equal(acquisition.channels[0].channel, 'Direct');
  assert.equal(acquisition.channels[1].channel, 'LinkedIn');
  assert.equal(acquisition.channels[2].channel, 'AI Referral');
  assert.equal(acquisition.seo.clicks, 5);
  assert.equal(acquisition.seo.impressions, 100);
});

test('summarizeSearchHealth aggregates status codes, cache rates, and durations', () => {
  const health = summarizeSearchHealth([
    {
      status_code: 200,
      client_surface: 'app',
      searches: 90,
      cache_hits: 45,
      avg_duration_ms: 1200,
      p50_duration_ms: 900,
      p95_duration_ms: 2500,
    },
    {
      status_code: 500,
      client_surface: 'app',
      searches: 10,
      cache_hits: 0,
      avg_duration_ms: 4000,
      p50_duration_ms: 3500,
      p95_duration_ms: 8000,
    },
  ], [
    { service: 'ojp', calls: 150 },
    { service: 'motis', calls: 80 },
    { service: 'osrm', calls: 100 },
  ]);

  assert.equal(health.totalSearches, 100);
  assert.equal(health.successfulSearches, 90);
  assert.equal(health.errorSearches, 10);
  assert.equal(health.successRate, 0.9);
  assert.equal(health.cacheHitRate, 0.45);
  assert.equal(health.upstreamEngines.ojpCalls, 150);
  assert.equal(health.upstreamEngines.ojpCostPounds, 0.063);
});

test('summarizeCorridors aggregates popular origin-destination routes', () => {
  const corridors = summarizeCorridors([
    { origin_name: 'Leeds', dest_name: 'Manchester Piccadilly', searches: 15, unique_users: 10, selected_modes: ['train', 'walk'] },
    { origin_name: 'London Euston', dest_name: 'Birmingham New Street', searches: 25, unique_users: 18, selected_modes: ['train'] },
  ]);

  assert.equal(corridors.totalDistinctCorridors, 2);
  assert.equal(corridors.topCorridors[0].corridor, 'London Euston -> Birmingham New Street');
  assert.equal(corridors.topCorridors[0].searches, 25);
  assert.equal(corridors.topCorridors[1].corridor, 'Leeds -> Manchester Piccadilly');
});

test('summarizeValueDelivered aggregates TCO pence and CO2 grams to £ and kg', () => {
  const value = summarizeValueDelivered([
    { total_co2_saved_grams: 450000, total_cost_saved_pence: 85000, total_time_saved_ms: 3600000, journeys_compared: 30 },
  ], [
    { total_saves: 12, alert_enabled: true },
    { total_saves: 8, alert_enabled: false },
  ]);

  assert.equal(value.totalCostSavedPounds, 850.00);
  assert.equal(value.totalCo2SavedKg, 450.0);
  assert.equal(value.totalTimeSavedHours, 1.0);
  assert.equal(value.savedRoutesCount, 20);
  assert.equal(value.alertsEnabledCount, 12);
});

test('buildReport joins all fixture data into full markdown report', async () => {
  const fixtureDir = await mkdtemp(path.join(os.tmpdir(), 'endmile-app-performance-'));
  try {
    await writeFile(path.join(fixtureDir, 'gsc.json'), JSON.stringify([
      { query: 'endmile travel', page: 'https://endmilerouting.co.uk/', clicks: 12, impressions: 200, ctr: 0.06, position: 2.1 },
    ]), 'utf8');

    await writeFile(path.join(fixtureDir, 'ga4-acquisition.json'), JSON.stringify([
      { channelGroup: 'Direct', sourceMedium: '(direct) / (none)', sessions: 40, activeUsers: 30, newUsers: 20 },
      { channelGroup: 'Organic Social', sourceMedium: 'linkedin.com / post', sessions: 25, activeUsers: 20, newUsers: 15 },
    ]), 'utf8');

    await writeFile(path.join(fixtureDir, 'ga4-events.json'), JSON.stringify([
      { eventName: 'page_view', pagePath: '/planner', eventCount: 150 },
      { eventName: 'search_performed', pagePath: '/planner', eventCount: 60 },
    ]), 'utf8');

    await writeFile(path.join(fixtureDir, 'endpoint-calls.json'), JSON.stringify([
      { status_code: 200, client_surface: 'app', client_feature: 'journey_search', searches: 50, cache_hits: 20, avg_duration_ms: 1500, p50_duration_ms: 1200, p95_duration_ms: 3200 },
    ]), 'utf8');

    await writeFile(path.join(fixtureDir, 'api-calls.json'), JSON.stringify([
      { service: 'ojp', calls: 40 },
      { service: 'motis', calls: 30 },
      { service: 'osrm', calls: 50 },
    ]), 'utf8');

    await writeFile(path.join(fixtureDir, 'recent-searches.json'), JSON.stringify([
      { origin_name: 'Leeds Station', dest_name: 'London Kings Cross', searches: 20, unique_users: 14, selected_modes: ['train'] },
    ]), 'utf8');

    await writeFile(path.join(fixtureDir, 'users.json'), JSON.stringify([
      { tenant_id: 'acme-corp', tenant_name: 'Acme Corp', user_count: 8, new_users_count: 2, searches: 40 },
      { tenant_id: 'individual', tenant_name: 'Individual', user_count: 22, new_users_count: 10, searches: 35 },
    ]), 'utf8');

    await writeFile(path.join(fixtureDir, 'savings.json'), JSON.stringify([
      { total_co2_saved_grams: 120000, total_cost_saved_pence: 45000, total_time_saved_ms: 1800000, journeys_compared: 25 },
    ]), 'utf8');

    await writeFile(path.join(fixtureDir, 'saved-journeys.json'), JSON.stringify([
      { total_saves: 6, alert_enabled: true },
    ]), 'utf8');

    await writeFile(path.join(fixtureDir, 'bing.json'), JSON.stringify({ traffic: [{ Clicks: 3, Impressions: 40 }] }), 'utf8');

    const options = parseArgs(['--fixture-dir', fixtureDir, '--days', '28']);
    const loaders = await fixtureLoaders(fixtureDir);
    const report = await buildReport(options, loaders);

    assert.equal(report.searchHealth.totalSearches, 50);
    assert.equal(report.searchHealth.successRate, 1.0);
    assert.equal(report.acquisition.totals.sessions, 65);
    assert.equal(report.corridors.topCorridors[0].corridor, 'Leeds Station -> London Kings Cross');
    assert.equal(report.valueDelivered.totalCostSavedPounds, 450);
    assert.equal(report.usersAndTenants.tenants[0].tenantName, 'Individual');
    assert.equal(report.usersAndTenants.tenants[1].tenantName, 'Acme Corp');

    const md = renderMarkdown(report);
    assert.match(md, /EndMile App & Core Routing Performance/);
    assert.match(md, /Leeds Station -> London Kings Cross/);
    assert.match(md, /Acme Corp/);
    assert.match(md, /£450/);
  } finally {
    await rm(fixtureDir, { recursive: true, force: true });
  }
});
