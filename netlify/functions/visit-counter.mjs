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

const PAGES = new Set(["/", "/about-us/", "/blog/", "/bus-depot-ev-charging-scotland/", "/commercial-battery-storage-solar-pv/", "/commercial-ev-charging-installation/", "/commercial-led-lighting/", "/commercial-solar-pv-bradford/", "/commercial-solar-pv-installation/", "/compliance/", "/contact-us-wakefield-electricians/", "/cummins-turbo-technologies/", "/dc-ev-charging-installation-reading/", "/eicr-fixed-wire-testing/", "/eicr-wakefield-ensuring-electrical-safety-for-your-business-with-econ-electrical-ltd/", "/electrical-contractors-for-schools-councils-and-public-buildings/", "/electrical-installation/", "/electrical-subcontracting-what-we-take-on-for-main-contractors/", "/emergency-lighting-testing-what-every-business-needs-to-know/", "/enquire/", "/enquiry-received/", "/ev-installation/", "/factory-and-warehouse-electrical-fit-outs-yorkshire/", "/factory-led-lighting-nottingham/", "/free-site-energy-assessment/", "/free-site-energy-assessment/thank-you/", "/high-bay-led-lighting-upgrades-factories-warehouses/", "/home-solar-battery-installation/", "/how-often-does-a-commercial-building-need-an-eicr/", "/how-to-choose-a-commercial-electrical-contractor/", "/industrial-electrical-contractors/", "/led-lighting-wakefield/", "/led-lighting/", "/logistics-depot-ev-charging/", "/machine-installations-and-moves-keeping-production-running/", "/pat-testing-for-businesses-how-often-and-what-the-law-requires/", "/planned-preventative-maintenance-commercial-electrical-systems/", "/powering-productivity-when-is-it-time-for-a-3-phase-upgrade-in-yorkshire/", "/privacy-notice/", "/projects/", "/renewables/", "/saint-flooring-group/", "/school-led-grants/", "/solar-panels-for-businesses-why-2026-is-the-year-for-commercial-solar-in-yorkshire/", "/surge-protection-is-your-yorkshire-business-one-lightning-strike-away-from-disaster/", "/swan-civil-engineering/", "/thank-you/", "/the-importance-of-cctv-systems-as-the-days-get-shorter/", "/thermal-imaging-how-commercial-electricians-in-yorkshire-prevent-costly-downtime/", "/why-ev-charging-solutions-are-essential-for-wakefield-businesses/", "/workplace-and-fleet-ev-charging-installation/"]);

/* ---------------------------------------------------------------------------
 * The Friday website review, shared by weekly-review.mjs (which sends it on the
 * schedule) and visit-counter.mjs (which sends it late if the schedule ever
 * fails to fire). build.py writes this file into both, so it lives once here.
 *
 * Everything it reads is in the site-stats store:
 *   day/YYYY-MM-DD        the day's tallies, written by the visit counter
 *   lead/YYYY-MM-DD/REF   one short record per form sent, written by
 *                         submission-created.js
 * and it writes:
 *   sent/YYYY-MM-DD       a marker, so a week is only ever sent once
 *   week/YYYY-MM-DD       the week's totals, kept for comparing over time
 * ------------------------------------------------------------------------- */

const REVIEW = {
  "to": [
    "jonathan@econelectrical.co.uk"
  ],
  "from": "Econ Electrical Website <website@econelectrical.co.uk>",
  "first_end": "2026-11-26",
  "site": {
    "domain": "https://econelectrical.co.uk",
    "legal": "Econ Electrical Ltd",
    "phone": "01924 677085",
    "phone_href": "+441924677085",
    "email": "info@econelectrical.co.uk",
    "hours_text": "Monday to Friday, 7:30am to 5pm",
    "address": [
      "The Courtyard",
      "225 Denby Dale Road",
      "Wakefield",
      "WF2 7AJ"
    ]
  },
  "titles": {
    "/": "Home page",
    "/about-us/": "About Econ Electrical",
    "/projects/": "Projects",
    "/contact-us-wakefield-electricians/": "Contact page",
    "/blog/": "News and advice",
    "/electrical-installation/": "Electrical Installation",
    "/renewables/": "Commercial Solar, Battery and EV Charging",
    "/compliance/": "Electrical Compliance and Testing",
    "/industrial-electrical-contractors/": "Industrial Electrical Contractors in Yorkshire",
    "/commercial-ev-charging-installation/": "Commercial EV Charging Installation",
    "/commercial-solar-pv-installation/": "Commercial Solar PV and Battery Storage",
    "/eicr-fixed-wire-testing/": "Commercial EICR and Fixed Wire Testing",
    "/commercial-led-lighting/": "Commercial LED Lighting Upgrades",
    "/home-solar-battery-installation/": "Home Solar and Battery Storage Yorkshire",
    "/ev-installation/": "London Bus Depot EV Fleet Charging",
    "/factory-led-lighting-nottingham/": "Factory LED Lighting Retrofit, Nottingham",
    "/commercial-solar-pv-bradford/": "Commercial Solar PV Installation, Bradford",
    "/cummins-turbo-technologies/": "Cummins Turbo Technologies, Huddersfield",
    "/bus-depot-ev-charging-scotland/": "Bus Depot EV Charging, Scotland",
    "/led-lighting/": "High Bay Factory Lighting, BM Packaging",
    "/dc-ev-charging-installation-reading/": "Four Bay DC EV Charging in Reading",
    "/logistics-depot-ev-charging/": "Logistics Depot EV Charging",
    "/swan-civil-engineering/": "Industrial Workshop Fit Out, Liverpool",
    "/saint-flooring-group/": "Distribution Warehouse Fit Out, Wakefield",
    "/electrical-subcontracting-what-we-take-on-for-main-contractors/": "Electrical Subcontracting Explained",
    "/how-to-choose-a-commercial-electrical-contractor/": "Choosing an Electrical Contractor",
    "/electrical-contractors-for-schools-councils-and-public-buildings/": "Electrical Contractors for Schools",
    "/surge-protection-is-your-yorkshire-business-one-lightning-strike-away-from-disaster/": "Surge Protection for Your Business",
    "/powering-productivity-when-is-it-time-for-a-3-phase-upgrade-in-yorkshire/": "When to Upgrade to 3 Phase Power",
    "/solar-panels-for-businesses-why-2026-is-the-year-for-commercial-solar-in-yorkshire/": "Commercial Solar Panels in Yorkshire",
    "/thermal-imaging-how-commercial-electricians-in-yorkshire-prevent-costly-downtime/": "Thermal Imaging for Your Business",
    "/machine-installations-and-moves-keeping-production-running/": "Machine Installations and Moves",
    "/commercial-battery-storage-solar-pv/": "Commercial Battery Storage and Solar",
    "/high-bay-led-lighting-upgrades-factories-warehouses/": "High Bay LED Lighting Upgrades",
    "/pat-testing-for-businesses-how-often-and-what-the-law-requires/": "PAT Testing for Businesses",
    "/workplace-and-fleet-ev-charging-installation/": "Workplace and Fleet EV Charging",
    "/planned-preventative-maintenance-commercial-electrical-systems/": "Planned Electrical Maintenance",
    "/emergency-lighting-testing-what-every-business-needs-to-know/": "Emergency Lighting Testing",
    "/how-often-does-a-commercial-building-need-an-eicr/": "How Often Does a Building Need an EICR?",
    "/factory-and-warehouse-electrical-fit-outs-yorkshire/": "Factory and Warehouse Fit Outs",
    "/led-lighting-wakefield/": "LED Lighting Wakefield",
    "/the-importance-of-cctv-systems-as-the-days-get-shorter/": "Commercial CCTV Systems",
    "/eicr-wakefield-ensuring-electrical-safety-for-your-business-with-econ-electrical-ltd/": "EICR Wakefield for Your Business",
    "/why-ev-charging-solutions-are-essential-for-wakefield-businesses/": "EV Charging for Wakefield Businesses",
    "/school-led-grants/": "School LED Lighting Grants",
    "/privacy-notice/": "Privacy Notice",
    "/thank-you/": "Message sent (thank you page)",
    "/free-site-energy-assessment/": "Free Site Energy Assessment for Businesses",
    "/free-site-energy-assessment/thank-you/": "Assessment requested (thank you page)",
    "/enquire/": "Project enquiry form",
    "/enquiry-received/": "Enquiry sent (thank you page)"
  },
  "form_pages": {
    "enquiry": "/enquire/",
    "contact": "/contact-us-wakefield-electricians/",
    "site-assessment": "/free-site-energy-assessment/"
  }
};

const SOURCE_NAMES = {
  google: 'Google search', 'google-ads': 'Google Ads', bing: 'Bing', 'bing-ads': 'Bing Ads',
  search: 'Other search engines', ai: 'AI assistants', linkedin: 'LinkedIn', facebook: 'Facebook',
  instagram: 'Instagram', x: 'X', email: 'Links in emails', whatsapp: 'Links sent on WhatsApp',
  direct: 'Typed in, bookmarks or apps', other: 'Other websites',
};
const CLICK_NAMES = [
  ['call', 'Phone number'], ['whatsapp', 'WhatsApp'], ['email', 'Email address'],
  ['enquire', 'Enquiry buttons'], ['assessment', 'Free site assessment'], ['contact', 'Contact page'],
  ['verify', 'Accreditation checks'], ['outbound', 'Links to other sites'],
];
const FORM_NAMES = { enquiry: 'Project enquiry', 'site-assessment': 'Site assessment', contact: 'Contact form' };
const DAY_MS = 86400000;

function londonDate(d = new Date()) {
  const parts = new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Europe/London', year: 'numeric', month: '2-digit', day: '2-digit',
  }).formatToParts(d);
  const get = t => parts.find(p => p.type === t).value;
  return get('year') + '-' + get('month') + '-' + get('day');
}

function shiftDate(ymd, days) {
  const d = new Date(ymd + 'T12:00:00Z');
  d.setUTCDate(d.getUTCDate() + days);
  return d.toISOString().slice(0, 10);
}

/* The seven dates ending on (and including) `end`. */
function weekTo(end) {
  return Array.from({ length: 7 }, (_, i) => shiftDate(end, i - 6));
}

/* The week the most recent Friday 7am review covers: the Friday to Thursday
   before it. */
function dueWeek(now = new Date()) {
  const back = (now.getUTCDay() - 5 + 7) % 7;
  const due = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() - back, 7, 0, 0));
  if (due > now) due.setUTCDate(due.getUTCDate() - 7);
  return { due, end: londonDate(new Date(due.getTime() - 12 * 3600000)) };
}

function addInto(target, src) {
  for (const [k, v] of Object.entries(src || {})) {
    if (typeof v === 'number') target[k] = (target[k] || 0) + v;
    else if (v && typeof v === 'object') addInto(target[k] = target[k] || {}, v);
  }
  return target;
}

const sum = obj => Object.values(obj || {}).reduce((a, b) => a + (typeof b === 'number' ? b : 0), 0);
const ranked = (obj, n) => Object.entries(obj || {}).filter(([, v]) => v > 0)
  .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, n);

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function pageName(path) {
  const t = REVIEW.titles[path];
  if (t) return t;
  return path.length > 48 ? path.slice(0, 46) + '…' : path;
}

function sourceName(key) {
  if (SOURCE_NAMES[key]) return SOURCE_NAMES[key];
  if (key.startsWith('short:')) return 'Short link /' + key.slice(6) + ' (QR code or print)';
  if (key.startsWith('tag:')) return 'Tagged link: ' + key.slice(4);
  return key;
}

/* The same names, as they read in the middle of a sentence. */
function inSentence(key) {
  const words = {
    direct: 'typing the address in or a bookmark', other: 'other websites', search: 'other search engines',
    email: 'links in emails', whatsapp: 'links sent on WhatsApp',
  };
  if (words[key]) return words[key];
  if (key.startsWith('short:')) return 'the short link /' + key.slice(6);
  if (key.startsWith('tag:')) return 'a tagged link (' + key.slice(4) + ')';
  return sourceName(key);
}

function niceDate(ymd, withYear) {
  const d = new Date(ymd + 'T12:00:00Z');
  return d.toLocaleDateString('en-GB', {
    timeZone: 'UTC', day: 'numeric', month: 'long', ...(withYear ? { year: 'numeric' } : {}),
  });
}

function shortDay(iso) {
  const d = new Date(iso);
  if (isNaN(d)) return '';
  return d.toLocaleDateString('en-GB', { timeZone: 'Europe/London', weekday: 'short', day: 'numeric', month: 'short' });
}

function range(start, end) {
  const a = new Date(start + 'T12:00:00Z');
  const b = new Date(end + 'T12:00:00Z');
  const sameMonth = a.getUTCMonth() === b.getUTCMonth();
  const left = a.toLocaleDateString('en-GB', { timeZone: 'UTC', day: 'numeric', ...(sameMonth ? {} : { month: 'long' }) });
  return left + ' to ' + niceDate(end);
}

/* "Up 12% on last week" style wording. Small numbers move by whole visits, so
   below twenty last week the change is given as a count, not a percentage. */
function change(cur, prev, hasPrev) {
  if (!hasPrev) return { text: 'First week of counting', tone: 'flat' };
  const diff = cur - prev;
  if (!diff) return { text: 'Same as last week', tone: 'flat' };
  const size = prev >= 20 ? Math.round(Math.abs(diff) / prev * 100) + '%' : String(Math.abs(diff));
  if (size === '0%') return { text: 'Same as last week', tone: 'flat' };
  return { text: (diff > 0 ? '▲ Up ' : '▼ Down ') + size + ' on last week', tone: diff > 0 ? 'up' : 'down' };
}

/* Everything the email shows, worked out from the raw tallies. Kept apart from
   the storage and the sending so the samples are drawn by the same code. */
function summarise({ end, days, prevDays, leads, prevLeads = [] }) {
  const dates = weekTo(end);
  const cur = days.reduce((acc, d) => addInto(acc, d || {}), {});
  const prev = prevDays.reduce((acc, d) => addInto(acc, d || {}), {});
  const hasPrev = prevDays.some(Boolean);
  const firstDay = dates[days.findIndex(Boolean)];
  const sends = sum(cur.forms && cur.forms.send);
  const enquiries = leads.length || sends;
  const prevEnquiries = (prev.forms && sum(prev.forms.send)) || 0;
  const clicks = cur.clicks || {};
  const pclicks = prev.clicks || {};
  const tot = {
    visits: sum(cur.landings), views: sum(cur.views), enquiries,
    calls: sum(clicks.call) + sum(clicks.whatsapp),
  };
  const ptot = {
    visits: sum(prev.landings), views: sum(prev.views), enquiries: prevLeads.length || prevEnquiries,
    calls: sum(pclicks.call) + sum(pclicks.whatsapp),
  };
  return {
    start: dates[0], end, dates, cur, prev, hasPrev, leads, tot, ptot,
    partial: !hasPrev && firstDay && firstDay !== dates[0] ? firstDay : '',
    empty: !days.some(Boolean),
  };
}

const FONT = "'Helvetica Neue',Helvetica,Arial,sans-serif";
const INK = '#0b0b0b';
const BODY = '#3d3d3d';
const MUTED = '#8c8c8c';
const HAIR = '#e8e8e6';
const PAGE = '#efefec';
const FOOT = '#f7f7f5';
const UP = '#3f7a2a';

function longhand(html) {
  return html.replace(/font:(\d{3}) ([\d.]+px)\/([\d.]+(?:px)?) ([^;"]+)/g,
    (m, weight, size, height, family) =>
      `font-family:${family};font-size:${size};line-height:${height};font-weight:${weight}`);
}

function label(text, extra) {
  return `<div style="font:700 11px/1.4 ${FONT};letter-spacing:2.2px;text-transform:uppercase;color:${MUTED};${extra || ''}">${esc(text)}</div>`;
}

function section(title, inner, note) {
  return `
  <tr><td class="px" style="padding:40px 48px 0;">
    ${label(title, `padding-bottom:12px;border-bottom:1px solid ${INK};`)}
    ${note ? `<div style="padding-top:12px;font:400 13px/1.6 ${FONT};color:${MUTED};">${note}</div>` : ''}
    ${inner}
  </td></tr>`;
}

function rows(items, empty) {
  if (!items.length) {
    return `<div style="padding:15px 0;border-bottom:1px solid ${HAIR};font:400 15px/1.6 ${FONT};color:${MUTED};">${esc(empty)}</div>`;
  }
  return `<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;">${
    items.map(([name, value, sub]) => `
    <tr>
      <td style="padding:13px 16px 13px 0;vertical-align:top;border-bottom:1px solid ${HAIR};font:400 15px/1.5 ${FONT};color:${INK};">${esc(name)}${
        sub ? `<div style="margin-top:3px;font:400 12.5px/1.5 ${FONT};color:${MUTED};">${esc(sub)}</div>` : ''}</td>
      <td align="right" style="padding:13px 0;vertical-align:top;white-space:nowrap;border-bottom:1px solid ${HAIR};font:700 15px/1.5 ${FONT};color:${INK};">${esc(value)}</td>
    </tr>`).join('')}
  </table>`;
}

function tile(name, value, ch) {
  const colour = ch.tone === 'up' ? UP : MUTED;
  return `<td class="tile" width="50%" style="width:50%;padding:22px 20px 20px 0;vertical-align:top;border-bottom:1px solid ${HAIR};">
      ${label(name)}
      <div style="margin-top:6px;font:400 40px/1.1 ${FONT};letter-spacing:-1px;color:${INK};">${esc(value)}</div>
      <div style="margin-top:6px;font:700 12px/1.4 ${FONT};color:${colour};">${esc(ch.text)}</div>
    </td>`;
}

function fromPages(byPage, n = 3) {
  const top = ranked(byPage, n);
  return top.length ? 'Mostly from ' + top.map(([p, c]) => pageName(p) + ' (' + c + ')').join(', ') : '';
}

function pct(part, whole) {
  return whole ? Math.round(part / whole * 100) + '%' : '';
}

function buildReviewEmail(s, opts = {}) {
  const { cur, tot, ptot, hasPrev } = s;
  const site = REVIEW.site.domain;
  const bare = site.replace(/^https?:\/\//, '');
  const img = path => esc(site + '/assets/img/' + path);
  const when = range(s.start, s.end);
  const test = opts.test ? 'Test: ' : '';
  const subject = test + 'Website review, ' + when + ': ' + tot.visits + ' visit' + (tot.visits === 1 ? '' : 's')
    + ', ' + tot.enquiries + ' enquir' + (tot.enquiries === 1 ? 'y' : 'ies');

  // One line that says what kind of week it was, in plain words.
  const topSource = ranked(cur.sources, 1)[0];
  const topPage = ranked(cur.views, 1)[0];
  const said = s.empty ? 'Nothing was counted this week.' : [
    `${tot.visits} visit${tot.visits === 1 ? '' : 's'}, ${tot.views} page view${tot.views === 1 ? '' : 's'} and ${tot.enquiries} enquir${tot.enquiries === 1 ? 'y' : 'ies'}.`,
    topSource ? `Most visitors came from ${inSentence(topSource[0])}.` : '',
    topPage ? `The most viewed page was ${topPage[0] === '/' ? 'the home page' : pageName(topPage[0])}.` : '',
  ].filter(Boolean).join(' ');

  const leads = s.leads.slice().sort((a, b) => String(a.at).localeCompare(String(b.at)));
  const leadItems = leads.slice(0, 20).map(l => {
    const who = [l.who, l.name && l.name !== l.who ? l.name : ''].filter(Boolean).join(', ') || 'No name given';
    const what = [FORM_NAMES[l.form] || l.form, (l.about || []).join(', '), l.stage, l.place].filter(Boolean).join(' · ');
    return [who, shortDay(l.at), what + (l.ref ? ' · Ref ' + l.ref : '')];
  });
  const leadNote = !s.leads.length && tot.enquiries
    ? 'Counted from the forms themselves. The full details are in your inbox.' : '';

  const pages = ranked(cur.views, 10).map(([p, v]) => {
    const started = (cur.landings || {})[p] || 0;
    return [pageName(p), String(v), started ? started + ' visit' + (started === 1 ? '' : 's') + ' started here' : ''];
  });

  const sources = ranked(cur.sources, 12).map(([k, v]) => {
    let sub = '';
    if (k === 'other') sub = ranked(cur.referrers, 5).map(([h, c]) => h + ' (' + c + ')').join(', ');
    if (k === 'google-ads' || k === 'bing-ads' || k.startsWith('short:')) {
      const landed = ranked((cur.landed_from || {})[k], 3).map(([p, c]) => pageName(p) + ' (' + c + ')');
      if (landed.length) sub = 'Landed on ' + landed.join(', ');
    }
    return [sourceName(k), v + (tot.visits ? ' · ' + pct(v, tot.visits) : ''), sub];
  });

  const clicks = CLICK_NAMES.map(([k, name]) => {
    const byPage = (cur.clicks || {})[k];
    const n = sum(byPage);
    if (!n) return null;
    let sub = fromPages(byPage);
    if (k === 'verify' || k === 'outbound') {
      const t = ranked(((cur.targets || {})[k]), 4).map(([h, c]) => h + ' (' + c + ')').join(', ');
      if (t) sub = t;
    }
    return [name, String(n), sub];
  }).filter(Boolean);

  /* How far people get with each form: opened the page, started filling it in,
     sent it. Plenty opening it and few starting is the sign a form asks too much. */
  const forms = Object.keys(FORM_NAMES).map(f => {
    const opened = (cur.views || {})[(REVIEW.form_pages || {})[f]] || 0;
    const started = ((cur.forms || {}).start || {})[f] || 0;
    const sent = ((cur.forms || {}).send || {})[f] || 0;
    if (!opened && !started && !sent) return null;
    return [FORM_NAMES[f], sent + ' sent', opened + ' opened the page · ' + started + ' started filling it in · ' + sent + ' sent it'];
  }).filter(Boolean);

  const dev = cur.devices || {};
  const devTotal = sum(dev);
  const devices = devTotal ? ['phone', 'computer', 'tablet'].filter(k => dev[k])
    .map(k => [k === 'phone' ? 'Phones' : k === 'computer' ? 'Computers' : 'Tablets', pct(dev[k], devTotal)]) : [];

  const lost = ranked(cur.notfound, 8).map(([p, c]) => [p, String(c)]);

  const tiles = [
    ['Visits', tot.visits, change(tot.visits, ptot.visits, hasPrev)],
    ['Page views', tot.views, change(tot.views, ptot.views, hasPrev)],
    ['Enquiries', tot.enquiries, change(tot.enquiries, ptot.enquiries, hasPrev)],
    ['Phone and WhatsApp taps', tot.calls, change(tot.calls, ptot.calls, hasPrev)],
  ];

  const html = `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<meta name="color-scheme" content="light only">
<meta name="supported-color-schemes" content="light only">
<title>${esc(subject)}</title>
<style>
  @media (max-width: 620px) {
    .px { padding-left: 26px !important; padding-right: 26px !important; }
    .h1 { font-size: 27px !important; }
    .stack { display: block !important; width: 100% !important; }
    .ref { text-align: left !important; padding-top: 8px !important; }
  }
  a[x-apple-data-detectors] { color: inherit !important; text-decoration: none !important; }
</style>
</head>
<body style="margin:0;padding:0;background:${PAGE};">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;mso-hide:all;">${esc(said)}</div>
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background:${PAGE};">
<tr><td align="center" style="padding:32px 12px;">
<!--[if mso]><table role="presentation" cellpadding="0" cellspacing="0" width="600" align="center"><tr><td><![endif]-->
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="width:100%;max-width:600px;background:#ffffff;">

  <tr><td align="center" bgcolor="#000000" style="background:#000000;padding:42px 24px 40px;">
    <a href="${esc(site)}" style="text-decoration:none;"><img src="${img('brand/econ-logo-email-192.png')}" width="89" height="96" alt="Econ Electrical" style="display:block;border:0;width:89px;height:96px;color:#ffffff;font:700 16px/1 ${FONT};"></a>
  </td></tr>
  <tr><td bgcolor="#9eca84" style="background:#9eca84;height:3px;line-height:3px;font-size:0;">&nbsp;</td></tr>

  <tr><td class="px" style="padding:46px 48px 0;">
    <table role="presentation" cellpadding="0" cellspacing="0" width="100%"><tr>
      <td class="stack" style="vertical-align:top;">${label(opts.test ? 'Website review, test run' : 'Weekly website review')}</td>
      <td class="stack ref" align="right" style="vertical-align:top;text-align:right;">${label(niceDate(opts.sentOn || londonDate(), true), 'letter-spacing:1.4px;')}</td>
    </tr></table>
    <h1 class="h1" style="margin:22px 0 0;font:400 31px/1.2 ${FONT};letter-spacing:-0.5px;color:${INK};">${esc(when)}</h1>
    <p style="margin:18px 0 0;font:400 15px/1.75 ${FONT};color:${BODY};">${esc(said)}</p>
    ${s.partial ? `<p style="margin:10px 0 0;font:400 13px/1.6 ${FONT};color:${MUTED};">Counting started on ${esc(niceDate(s.partial))}, so this first review covers part of the week.</p>` : ''}
  </td></tr>

  <tr><td class="px" style="padding:30px 48px 0;">
    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;border-top:1px solid ${INK};">
      <tr>${tile(...tiles[0])}${tile(...tiles[1])}</tr>
      <tr>${tile(...tiles[2])}${tile(...tiles[3])}</tr>
    </table>
  </td></tr>

  ${section('Enquiries', rows(leadItems, 'No enquiries this week.'), leadNote)}
  ${section('Most viewed pages', rows(pages, 'No page views counted this week.'))}
  ${section('Where visitors came from', rows(sources, 'No visits counted this week.'))}
  ${section('What people clicked', rows(clicks, 'Nobody clicked the phone number, WhatsApp, email or an enquiry button this week.'))}
  ${forms.length ? section('Forms', rows(forms, '')) : ''}
  ${devices.length ? section('Phones or computers', rows(devices, '')) : ''}
  ${lost.length ? section('Addresses that do not exist', rows(lost, ''), 'Someone tried these and got the page not found message. Worth a look in case a link somewhere is wrong.') : ''}

  <tr><td class="px" style="padding:40px 48px 44px;font:400 12.5px/1.75 ${FONT};color:${MUTED};">
    Counted anonymously by the website, without cookies. A visit is someone arriving from a search, an advert, another website or by typing the address in; page views count every page they open. Anyone who declines cookies, or whose browser asks not to be tracked, is not counted. This review arrives every Friday at 7am.
  </td></tr>

  <tr><td class="px" bgcolor="${FOOT}" style="background:${FOOT};padding:26px 48px 28px;border-top:1px solid ${HAIR};">
    <p style="margin:0;font:400 12px/1.8 ${FONT};color:${MUTED};">${esc(REVIEW.site.legal)}, ${esc(REVIEW.site.address.join(', '))}<br><a href="${esc(site)}" style="color:${INK};font-weight:700;text-decoration:none;">${esc(bare)}</a></p>
  </td></tr>

</table>
<!--[if mso]></td></tr></table><![endif]-->
</td></tr></table>
</body></html>`;

  const block = (title, items) => items.length
    ? [title.toUpperCase(), ...items.map(([a, b, c]) => '  ' + a + (b ? ': ' + b : '') + (c ? '\n    ' + c : '')), '']
    : [];
  const text = [
    (opts.test ? 'WEBSITE REVIEW, TEST RUN' : 'WEEKLY WEBSITE REVIEW') + '   ' + when, '',
    said, '',
    ...tiles.map(([n, v, ch]) => n + ': ' + v + ' (' + ch.text.replace(/^[▲▼] /, '') + ')'), '',
    ...block('Enquiries', leadItems.length ? leadItems : [['No enquiries this week.', '', '']]),
    ...block('Most viewed pages', pages),
    ...block('Where visitors came from', sources),
    ...block('What people clicked', clicks),
    ...block('Forms', forms),
    ...block('Phones or computers', devices),
    ...block('Addresses that do not exist', lost),
    'Counted anonymously by the website, without cookies.',
  ].join('\n');

  return { subject, html: longhand(html), text };
}

async function readDays(store, dates) {
  return Promise.all(dates.map(d => store.get('day/' + d, { type: 'json' }).catch(() => null)));
}

async function readLeads(store, dates) {
  const out = [];
  for (const d of dates) {
    const { blobs } = await store.list({ prefix: 'lead/' + d + '/' });
    const got = await Promise.all(blobs.map(b => store.get(b.key, { type: 'json' }).catch(() => null)));
    out.push(...got.filter(Boolean));
  }
  return out;
}

async function sendMail(mail) {
  const key = process.env.RESEND_API_KEY;
  if (!key) throw new Error('RESEND_API_KEY is not set');
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: REVIEW.from, to: REVIEW.to, subject: mail.subject, html: mail.html, text: mail.text }),
  });
  if (!res.ok) throw new Error('Resend refused the review: ' + res.status + ' ' + (await res.text()).slice(0, 300));
}

/* Leads hold a name, so they are only kept long enough for the reviews that
   need them. The day tallies hold nothing personal and are kept for a year and
   a bit, so a week can be compared with the same week last year. */
async function tidy(store, today) {
  const leadCut = shiftDate(today, -120);
  const dayCut = shiftDate(today, -400);
  for await (const page of store.list({ prefix: 'lead/', paginate: true })) {
    await Promise.all(page.blobs.filter(b => b.key.slice(5, 15) < leadCut).map(b => store.delete(b.key)));
  }
  for await (const page of store.list({ prefix: 'day/', paginate: true })) {
    await Promise.all(page.blobs.filter(b => b.key.slice(4, 14) < dayCut).map(b => store.delete(b.key)));
  }
}

/* Sends the review for the week ending `end`, once. The marker is claimed
   before anything is sent, so two runs at the same moment cannot both send it;
   if the send fails the claim is released and a later run can try again. A test
   run sends whatever it is asked for and leaves no marker. */
async function sendReview(store, { end, test = false, why = 'schedule' }) {
  const marker = 'sent/' + end;
  if (!test) {
    if (end < REVIEW.first_end) return 'too early';
    const claim = await store.setJSON(marker, { status: 'sending', at: new Date().toISOString(), by: why }, { onlyIfNew: true });
    if (claim && claim.modified === false) return 'already sent';
  }
  try {
    const dates = weekTo(end);
    const prevDates = weekTo(shiftDate(end, -7));
    const [days, prevDays, leads, prevLeads] = await Promise.all([
      readDays(store, dates), readDays(store, prevDates), readLeads(store, dates), readLeads(store, prevDates)]);
    const s = summarise({ end, days, prevDays, leads, prevLeads });
    const mail = buildReviewEmail(s, { test });
    await sendMail(mail);
    if (!test) {
      await store.setJSON(marker, { status: 'sent', at: new Date().toISOString(), by: why, subject: mail.subject });
      await store.setJSON('week/' + end, {
        start: s.start, end, totals: s.tot, sources: s.cur.sources || {}, views: s.cur.views || {},
        clicks: s.cur.clicks || {}, forms: s.cur.forms || {}, devices: s.cur.devices || {},
      });
      await tidy(store, londonDate()).catch(err => console.error('weekly review: tidy failed', err && err.message));
    }
    return 'sent: ' + mail.subject;
  } catch (err) {
    if (!test) await store.delete(marker).catch(() => {});
    throw err;
  }
}
/* ---------------------------------------------------------------------------- */

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
