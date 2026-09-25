import assert from 'node:assert/strict';
import test from 'node:test';

import {
  dateRange,
  formatJuliesBicycleExport,
  parseArgs,
  renderMarkdown,
  summarizeVenueEngagement,
} from './venue-co2-report.mjs';

test('parseArgs reads venue flags correctly', () => {
  const options = parseArgs([
    '--venue-id', 'harrogate-theatre',
    '--venue-name', 'Harrogate Theatre',
    '--days', '14',
    '--from', '2026-09-01',
    '--to', '2026-09-14',
    '--markdown',
    '--json',
  ]);

  assert.equal(options.venueId, 'harrogate-theatre');
  assert.equal(options.venueName, 'Harrogate Theatre');
  assert.equal(options.days, 14);
  assert.equal(options.from, '2026-09-01');
  assert.equal(options.to, '2026-09-14');
  assert.equal(options.markdown, true);
  assert.equal(options.json, true);
});

test('dateRange calculates expected dates', () => {
  const custom = dateRange({ from: '2026-09-01', to: '2026-09-15' });
  assert.deepEqual(custom, { from: '2026-09-01', to: '2026-09-15' });

  const defaultRange = dateRange({ days: 7 }, new Date('2026-09-25T12:00:00Z'));
  assert.equal(defaultRange.to, '2026-09-25');
  assert.equal(defaultRange.from, '2026-09-18');
});

test('summarizeVenueEngagement calculates modal split and carbon accurately', () => {
  const sampleSearches = [
    { chosen_mode: 'transit', distance_km: 20, origin_town: 'Leeds' },
    { chosen_mode: 'transit', distance_km: 30, origin_town: 'Leeds' },
    { chosen_mode: 'drive', distance_km: 15, origin_town: 'York' },
    { chosen_mode: 'walk', distance_km: 2, origin_town: 'Local' },
  ];

  const summary = summarizeVenueEngagement(sampleSearches, {
    venueId: 'harrogate-theatre',
    venueName: 'Harrogate Theatre',
  });

  assert.equal(summary.totalSearches, 4);
  assert.equal(summary.modes.transit, 2);
  assert.equal(summary.modes.drive, 1);
  assert.equal(summary.modes.walk, 1);
  assert.equal(summary.totalPassengerKm, 67);
  assert.ok(summary.co2SavedKg > 0);
  assert.ok(summary.carbonSavingsPercent > 0);
  assert.equal(summary.topCorridors[0].origin, 'Leeds');
  assert.equal(summary.topCorridors[0].count, 2);
});

test('formatJuliesBicycleExport generates valid ACE reporting structure', () => {
  const summary = {
    venueId: 'harrogate-theatre',
    totalSearches: 10,
    modes: { transit: 7, drive: 2, walk: 1, cycle: 0 },
    totalCo2Kg: 25.5,
    co2SavedKg: 40.2,
    carbonSavingsPercent: 61,
    topCorridors: [{ origin: 'Leeds', count: 5 }],
    dateRange: { from: '2026-08-01', to: '2026-08-31' },
  };

  const jb = formatJuliesBicycleExport(summary);

  assert.equal(jb.audienceTravelTrips, 10);
  assert.equal(jb.modalSplit.publicTransportPercent, 70);
  assert.equal(jb.modalSplit.privateVehiclePercent, 20);
  assert.equal(jb.modalSplit.activeTravelPercent, 10);
  assert.equal(jb.juliesBicycleCategory, 'Scope 3 Audience Travel');
});

test('renderMarkdown outputs expected headings and tables', () => {
  const report = {
    summary: {
      venueId: 'harrogate-theatre',
      venueName: 'Harrogate Theatre',
      totalSearches: 100,
      totalPassengerKm: 2500,
      co2SavedKg: 150.5,
      carbonSavingsPercent: 55,
      topCorridors: [{ origin: 'Leeds', count: 40 }],
    },
    jb: {
      audienceTravelTrips: 100,
      modalSplit: {
        publicTransportPercent: 65,
        privateVehiclePercent: 25,
        activeTravelPercent: 10,
      },
      totalAudienceEmissionsTonnes: '0.220',
      divertedEmissionsTonnesAvoided: '0.150',
    },
    dateRange: { from: '2026-09-01', to: '2026-09-25' },
  };

  const md = renderMarkdown(report);
  assert.match(md, /Harrogate Theatre/);
  assert.match(md, /Julie's Bicycle Scope 3 Declaration/);
  assert.match(md, /65%/);
  assert.match(md, /Leeds/);
});
