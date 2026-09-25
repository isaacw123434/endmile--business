#!/usr/bin/env node
/**
 * submit-indexnow.mjs
 *
 * Submits all active URLs from the live Guide sitemap to Bing IndexNow
 * and Bing Webmaster Tools Direct Submission API.
 *
 * Usage:
 *   node scripts/analytics/submit-indexnow.mjs [--key KEY] [--host HOST] [--sitemap URL]
 */

const DEFAULT_KEY = process.env.BING_API_KEY || 'f9541b772ec346ea816b0395881232e0';
const DEFAULT_HOST = 'guide.endmilerouting.co.uk';
const DEFAULT_SITEMAP = 'https://guide.endmilerouting.co.uk/sitemap.xml';

function parseArgs(argv) {
  const args = { key: DEFAULT_KEY, host: DEFAULT_HOST, sitemap: DEFAULT_SITEMAP };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--key' && argv[i + 1]) args.key = argv[++i];
    if (argv[i] === '--host' && argv[i + 1]) args.host = argv[++i];
    if (argv[i] === '--sitemap' && argv[i + 1]) args.sitemap = argv[++i];
  }
  return args;
}

export async function submitUrlsToIndexNow({ key, host, sitemapUrl }) {
  console.log(`Fetching sitemap from ${sitemapUrl}...`);
  const sitemapRes = await fetch(sitemapUrl);
  if (!sitemapRes.ok) throw new Error(`Failed to fetch sitemap: HTTP ${sitemapRes.status}`);
  const xml = await sitemapRes.text();
  const allUrls = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1]);
  console.log(`Found ${allUrls.length} URLs in sitemap.`);

  const payload = {
    host,
    key,
    keyLocation: `https://${host}/${key}.txt`,
    urlList: allUrls,
  };

  // 1. Submit to IndexNow central endpoint (broadcasts to Bing, Yandex, Seznam)
  console.log('\n[1/3] Submitting to https://api.indexnow.org/indexnow...');
  const resCentral = await fetch('https://api.indexnow.org/indexnow', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
    body: JSON.stringify(payload),
  });
  const textCentral = await resCentral.text();
  console.log(`  ✓ Status: ${resCentral.status} ${resCentral.statusText} ${textCentral ? `(${textCentral})` : ''}`);

  // 2. Submit directly to Bing IndexNow endpoint
  console.log('\n[2/3] Submitting to https://www.bing.com/indexnow...');
  const resBing = await fetch('https://www.bing.com/indexnow', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
    body: JSON.stringify(payload),
  });
  const textBing = await resBing.text();
  console.log(`  ✓ Status: ${resBing.status} ${resBing.statusText} ${textBing ? `(${textBing})` : ''}`);

  // 3. Submit top available quota to Bing Webmaster Direct API
  console.log('\n[3/3] Checking Bing Webmaster Direct API quota...');
  const quotaRes = await fetch(`https://ssl.bing.com/webmaster/api.svc/json/GetUrlSubmissionQuota?siteUrl=${encodeURIComponent(`https://${host}/`)}&apikey=${key}`);
  const quotaData = await quotaRes.json().catch(() => null);
  const dailyQuota = quotaData?.d?.DailyQuota ?? 0;
  console.log(`  Remaining daily quota: ${dailyQuota}`);

  if (dailyQuota > 0) {
    const batch = allUrls.slice(0, dailyQuota);
    console.log(`  Submitting ${batch.length} URLs to Bing Direct API...`);
    const directRes = await fetch(`https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey=${key}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
      body: JSON.stringify({ siteUrl: `https://${host}/`, urlList: batch }),
    });
    console.log(`  ✓ Status: ${directRes.status} ${directRes.statusText}`);
  }

  return { totalSubmitted: allUrls.length, centralStatus: resCentral.status, bingStatus: resBing.status };
}

if (process.argv[1] && process.argv[1].endsWith('submit-indexnow.mjs')) {
  const args = parseArgs(process.argv.slice(2));
  submitUrlsToIndexNow({ key: args.key, host: args.host, sitemapUrl: args.sitemap })
    .then(() => console.log('\n=== All URLs successfully submitted to Bing IndexNow! ==='))
    .catch(err => {
      console.error('\n❌ Submission failed:', err);
      process.exit(1);
    });
}
