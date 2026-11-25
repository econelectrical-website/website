/* The visit counter behind the Friday website review.
 *
 * The page script (site.js) sends a short note here when a page opens, when
 * someone clicks one of the things that matter (the phone number, WhatsApp,
 * email, an enquiry button, an accreditation logo, a link to another site) and
 * when a form is started or sent. Each note adds one to a tally for that day,
 * kept in Netlify Blobs under day/YYYY-MM-DD.
 *
 * Nothing about the visitor is kept: no cookies, no IP address, no identifier.
 * The only things recorded are the page, the website they came from, the kind
 * of device (from the browser's own description of itself, read here and then
 * dropped) and what was clicked. Robots and anything that does not look like a
 * real page on this site are ignored or filed as "not found".
 *
 * PAGES is written in by build.py from the pages it built. Do not edit it here.
 */
import { getStore } from '@netlify/blobs';

const PAGES = new Set(__PAGES__);

// __REVIEW_LIB__
const FORMS = new Set(['enquiry', 'contact', 'site-assessment']);
const CLICKS = new Set(['call', 'whatsapp', 'email', 'enquire', 'assessment', 'contact', 'verify', 'outbound']);
const LIVE = new Set(['econelectrical.co.uk', 'www.econelectrical.co.uk']);
const HOSTS = new Set([...LIVE, 'econ-electrical.netlify.app']);
const ROBOT = /bot\b|bot\/|crawl|spider|slurp|bingpreview|facebookexternalhit|embedly|headless|lighthouse|pagespeed|gtmetrix|python|curl|wget|node-fetch|axios|go-http|java\/|monitor|uptime|pingdom|scanner|preview/i;
const MAX_NOT_FOUND = 60;

/* Which search engine, social site or AI assistant a visit came from, by the
   address of the page that sent it. Anything else is "other" and the site's
   name is kept, so new sources show up in the review on their own. */
const SOURCES = [
  [/(^|\.)gemini\.google\./, 'ai'],
  [/(^|\.)google\./, 'google'],
  [/(^|\.)bing\.com$/, 'bing'],
  [/(^|\.)(duckduckgo\.com|search\.yahoo\.com|yahoo\.com|ecosia\.org|search\.brave\.com|startpage\.com)$/, 'search'],
  [/(^|\.)(linkedin\.com|lnkd\.in)$/, 'linkedin'],
  [/(^|\.)(facebook\.com|fb\.com|fb\.me|messenger\.com)$/, 'facebook'],
  [/(^|\.)instagram\.com$/, 'instagram'],
  [/(^|\.)(t\.co|x\.com|twitter\.com)$/, 'x'],
  [/(^|\.)(chatgpt\.com|openai\.com|perplexity\.ai|claude\.ai|copilot\.microsoft\.com|you\.com|phind\.com|meta\.ai|deepseek\.com|grok\.com)$/, 'ai'],
  [/(^|\.)(mail\.google\.com|outlook\.live\.com|outlook\.office\.com|outlook\.office365\.com)$/, 'email'],
  [/(^|\.)(whatsapp\.com|wa\.me)$/, 'whatsapp'],
];

const clean = (v, max, re) => String(v == null ? '' : v).toLowerCase().slice(0, max).replace(re, '');
const bump = (obj, k, n = 1) => { obj[k] = (obj[k] || 0) + n; };
const sub = (obj, k) => (obj[k] = obj[k] || {});

function device(ua) {
  if (/ipad|tablet|kindle|silk|playbook|(android(?!.*mobile))/i.test(ua)) return 'tablet';
  if (/mobi|iphone|ipod|android|blackberry|opera mini|iemobile/i.test(ua)) return 'phone';
  return 'computer';
}

const TAGS = {
  'google-ads': 'google-ads', 'bing-ads': 'bing-ads', google: 'google', bing: 'bing', linkedin: 'linkedin',
  facebook: 'facebook', fb: 'facebook', instagram: 'instagram', ig: 'instagram', email: 'email',
  newsletter: 'email', whatsapp: 'whatsapp', chatgpt: 'ai', 'chatgpt.com': 'ai', perplexity: 'ai',
};

function source(tag, host) {
  if (tag) {
    if (TAGS[tag]) return TAGS[tag];
    if (tag.startsWith('short:')) return tag;
    return 'tag:' + tag;
  }
  if (!host) return 'direct';
  for (const [re, name] of SOURCES) if (re.test(host)) return name;
  return 'other';
}

/* Turns one note into changes to the day's tally. Returns null for anything
   that should not be counted. Kept apart from the storage so it can be tested. */
export function apply(day, note, ua) {
  if (!note || typeof note !== 'object') return null;
  let path = String(note.p || '').split(/[?#]/)[0].slice(0, 160);
  if (!path.startsWith('/')) return null;
  const known = PAGES.has(path);
  const kind = device(ua || '');
  day.v = 1;

  if (note.e === 'view') {
    if (!known) {
      const lost = sub(day, 'notfound');
      const p = path.replace(/[^\w\/.%-]/g, '').slice(0, 100);
      if (p in lost || Object.keys(lost).length < MAX_NOT_FOUND) bump(lost, p);
      return day;
    }
    bump(sub(day, 'views'), path);
    if (note.l) {
      const host = clean(note.r, 80, /[^a-z0-9.-]/g).replace(/^www\./, '');
      const tag = clean(note.s, 40, /[^a-z0-9:_.\/-]/g);
      const from = source(tag, host);
      bump(sub(day, 'landings'), path);
      bump(sub(day, 'sources'), from);
      bump(sub(sub(day, 'landed_from'), from), path);
      if (from === 'other' && host) bump(sub(day, 'referrers'), host);
      bump(sub(day, 'devices'), kind);
    }
    return day;
  }
  if (!known) return null;
  if (note.e === 'click') {
    const k = String(note.k || '');
    if (!CLICKS.has(k)) return null;
    bump(sub(sub(day, 'clicks'), k), path);
    if (k === 'verify' || k === 'outbound') {
      const host = clean(note.x, 60, /[^a-z0-9.-]/g).replace(/^www\./, '');
      if (host) bump(sub(sub(day, 'targets'), k), host);
    }
    return day;
  }
  if (note.e === 'form') {
    const f = String(note.f || '');
    const k = String(note.k || '');
    if (!FORMS.has(f) || (k !== 'start' && k !== 'send')) return null;
    bump(sub(sub(day, 'forms'), k), f);
    return day;
  }
  return null;
}

/* Read, change and write back the day's tally. Two notes arriving at the same
   moment cannot overwrite each other: the write only succeeds if nobody else
   has written since it was read, and otherwise it reads again and retries. */
export async function record(store, note, ua, date = londonDate()) {
  const key = 'day/' + date;
  for (let i = 0; i < 6; i++) {
    const cur = await store.getWithMetadata(key, { type: 'json', consistency: 'strong' });
    const day = apply(cur && cur.data ? cur.data : {}, note, ua);
    if (!day) return false;
    const res = cur
      ? await store.setJSON(key, day, { onlyIfMatch: cur.etag })
      : await store.setJSON(key, day, { onlyIfNew: true });
    if (!res || res.modified !== false) return true;
    await new Promise(r => setTimeout(r, 40 + Math.random() * 160));
  }
  return false;
}

/* Netlify's scheduler has been known to stop firing on some sites without any
   error. So if the Friday review has not gone out two hours after it should
   have, the next note to arrive here sends it. Each copy of this function only
   checks once per week, and the marker stops it ever going twice. */
let lateChecked = '';
async function lateReview(store) {
  const { due, end } = dueWeek();
  if (lateChecked === end || end < REVIEW.first_end || Date.now() < due.getTime() + 2 * 3600000) return;
  const sent = await store.get('sent/' + end, { type: 'json', consistency: 'strong' });
  lateChecked = end;
  if (!sent) console.log('visit counter: the review for the week ending ' + end + ' was late,', await sendReview(store, { end, why: 'late' }));
}

export default async (req, context) => {
  if (req.method !== 'POST') return new Response(null, { status: 405 });
  const ua = req.headers.get('user-agent') || '';
  const origin = req.headers.get('origin');
  if (ROBOT.test(ua) || !ua) return new Response(null, { status: 204 });
  if (origin) {
    let host = '';
    try { host = new URL(origin).hostname; } catch (err) {}
    if (!HOSTS.has(host) && !host.endsWith('--econ-electrical.netlify.app')) return new Response(null, { status: 204 });
  }
  let note = null;
  try {
    const text = await req.text();
    if (text.length <= 2000) note = JSON.parse(text);
  } catch (err) {
    note = null;
  }
  if (note) {
    /* Only the real site counts towards the review. A deploy preview keeps its
       own tally, so testing a change never shows up in Jonathan's numbers. */
    let live = false;
    try { live = LIVE.has(new URL(req.url).hostname); } catch (err) {}
    const store = getStore({ name: live ? 'site-stats' : 'site-stats-test', consistency: 'strong' });
    const work = record(store, note, ua)
      .then(() => (live ? lateReview(store) : null))
      .catch(err => console.error('visit counter:', err && err.message));
    if (context && typeof context.waitUntil === 'function') context.waitUntil(work);
    else await work;
  }
  return new Response(null, { status: 204, headers: { 'cache-control': 'no-store' } });
};

export const config = { path: '/api/n', method: ['POST'] };
