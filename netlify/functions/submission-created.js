'use strict';

/**
 * Emails a website enquiry to the office, and a confirmation to the customer.
 *
 * Netlify runs this automatically the moment a form is submitted. It is not
 * reachable from the web and takes no arguments of its own: Netlify calls it
 * with the submission, this builds the emails out of it and hands them to Resend.
 *
 * It covers every form on the site (the project enquiry, the contact form and
 * the site energy assessment) and sends two emails for each:
 *
 *   1. To Jonathan: the enquiry laid out to be read in ten seconds, with the
 *      customer in Reply-To so hitting reply goes straight to them.
 *   2. To the customer: an instant "we have got it, a member of our team will
 *      be in touch within one working day", with a copy of the options they
 *      picked. It comes from the address on the website; a reply goes to Jonathan.
 *
 * Why this exists rather than Netlify's own notification emails: from 3 November
 * 2026 Netlify only lets you notify addresses belonging to members of your
 * Netlify team, it cannot email the customer at all, and the email it sends is a
 * flat dump of field names.
 *
 * Nothing here is load bearing for the enquiry itself. Netlify stores every
 * submission before this runs, so if Resend is down or the key is wrong the
 * enquiry is still safe in the dashboard and this just logs the failure. The two
 * emails are sent separately, so one failing never stops the other.
 *
 * Netlify only calls this for submissions that passed its spam checks. Even so,
 * the customer email never repeats anything typed into a free text box: only
 * answers that match one of the form's own options are echoed back, and the
 * greeting uses a first name only if it looks like one. Otherwise the form could
 * be used to send our email, with someone else's words in it, to a stranger.
 *
 * FORMS and SITE are written in by build.py from the pages themselves, so the
 * labels in the emails are always the labels on the form. Do not edit them here.
 */

const FORMS = {
  "enquiry": {
    "to": [
      "jonathan@econelectrical.co.uk"
    ],
    "cc": [],
    "title": "Project Enquiry",
    "subject": "Project enquiry",
    "reply": {
      "from": "Econ Electrical <info@econelectrical.co.uk>",
      "reply_to": [
        "jonathan@econelectrical.co.uk"
      ],
      "subject": "Your enquiry with Econ Electrical",
      "kicker": "Enquiry received",
      "preheader": "A member of our team will be in touch within one working day.",
      "intro": "Your enquiry has come through safely and is with us now.",
      "promise": "A member of our team will be in touch within one working day.",
      "summary_heading": "Your enquiry",
      "echo": [
        [
          "interests",
          "Interested in"
        ],
        [
          "site_type",
          "Type of site"
        ],
        [
          "stage",
          "Project"
        ],
        [
          "timescale",
          "Start"
        ],
        [
          "next_step",
          "First step"
        ],
        [
          "contact_method",
          "Contact by"
        ],
        [
          "contact_time",
          "Best time"
        ]
      ],
      "extra": "Got drawings, a spec or photos of the site? Reply to this email with them attached."
    },
    "fields": [
      [
        "What do you need?",
        [
          {
            "name": "interests",
            "label": "Interested in",
            "type": "chips",
            "options": [
              [
                "install",
                "Electrical installation or fit out"
              ],
              [
                "maintenance",
                "Planned or reactive maintenance"
              ],
              [
                "subcontract",
                "Sub contract work (main contractors)"
              ],
              [
                "solar",
                "Solar PV"
              ],
              [
                "battery",
                "Battery storage"
              ],
              [
                "ev",
                "EV charging"
              ],
              [
                "led",
                "LED lighting"
              ],
              [
                "testing",
                "EICR and testing"
              ],
              [
                "emergency",
                "Emergency lighting"
              ],
              [
                "pat",
                "PAT testing"
              ],
              [
                "home",
                "Home solar and battery"
              ],
              [
                "advice",
                "Not sure yet, need advice"
              ]
            ]
          },
          {
            "name": "site_type",
            "label": "Type of site",
            "type": "select",
            "options": [
              "Factory or industrial unit",
              "Warehouse or distribution",
              "Office or commercial",
              "Retail, leisure or hospitality",
              "School, college or public building",
              "Healthcare",
              "Farm or rural business",
              "Building site, new build or refurb",
              "Home",
              "Other"
            ]
          },
          {
            "name": "location",
            "label": "Site location",
            "type": "text"
          }
        ]
      ],
      [
        "Where are you up to?",
        [
          {
            "name": "stage",
            "label": "Project",
            "type": "radio",
            "options": [
              "Live, ready to go",
              "Pricing or tendering",
              "Early days, just exploring"
            ]
          },
          {
            "name": "timescale",
            "label": "Start",
            "type": "radio",
            "options": [
              "As soon as possible",
              "Within 3 months",
              "3 to 6 months",
              "6 months or more",
              "Not sure yet"
            ]
          },
          {
            "name": "next_step",
            "label": "Wants first",
            "type": "radio",
            "options": [
              "A call to talk it through",
              "A site survey",
              "A quote from drawings or a spec",
              "Just some information for now"
            ]
          }
        ]
      ],
      [
        "Your details",
        [
          {
            "name": "name",
            "label": "Name",
            "type": "text"
          },
          {
            "name": "company",
            "label": "Company",
            "type": "text"
          },
          {
            "name": "email",
            "label": "Email",
            "type": "email"
          },
          {
            "name": "phone",
            "label": "Phone",
            "type": "tel"
          },
          {
            "name": "contact_method",
            "label": "Contact by",
            "type": "radio",
            "options": [
              "Phone call",
              "Email",
              "WhatsApp"
            ]
          },
          {
            "name": "contact_time",
            "label": "Best time",
            "type": "radio",
            "options": [
              "Morning",
              "Afternoon",
              "Any time"
            ]
          }
        ]
      ],
      [
        "Anything else?",
        [
          {
            "name": "message",
            "label": "Message",
            "type": "textarea"
          },
          {
            "name": "heard",
            "label": "Heard about us",
            "type": "select",
            "options": [
              "Google search",
              "Google Maps or reviews",
              "Recommended by someone",
              "LinkedIn",
              "Facebook or Instagram",
              "Saw our van or one of our jobs",
              "Leaflet or letter",
              "Worked with us before",
              "Other"
            ]
          }
        ]
      ]
    ]
  },
  "site-assessment": {
    "to": [
      "jonathan@econelectrical.co.uk"
    ],
    "cc": [],
    "title": "Site Energy Assessment Request",
    "subject": "Site assessment",
    "reply": {
      "from": "Econ Electrical <info@econelectrical.co.uk>",
      "reply_to": [
        "jonathan@econelectrical.co.uk"
      ],
      "subject": "Your free site energy assessment request",
      "kicker": "Request received",
      "preheader": "A member of our team will be in touch within one working day to book your site visit.",
      "intro": "Your request for a free site energy assessment has come through safely, along with your site details.",
      "promise": "A member of our team will be in touch within one working day to book your site visit.",
      "summary_heading": "",
      "echo": [],
      "extra": "If you did not attach a year of electricity bills, reply to this email with whatever you have. It is the one thing that speeds the report up."
    },
    "fields": [
      [
        "About you",
        [
          {
            "name": "business",
            "label": "Business name",
            "type": "text"
          },
          {
            "name": "name",
            "label": "Your name",
            "type": "text"
          },
          {
            "name": "role",
            "label": "Your role",
            "type": "select",
            "options": [
              "Owner or Director",
              "Facilities or Site Manager",
              "Operations Manager",
              "Finance",
              "Energy or Sustainability",
              "Maintenance or Engineering",
              "Something else"
            ]
          },
          {
            "name": "email",
            "label": "Email",
            "type": "email"
          },
          {
            "name": "phone",
            "label": "Phone",
            "type": "tel"
          },
          {
            "name": "decision",
            "label": "Who signs off a decision like this",
            "type": "select",
            "options": [
              "I do",
              "I do, with a colleague",
              "A colleague or another director",
              "Head office or a parent company",
              "The landlord",
              "Not sure yet"
            ]
          },
          {
            "name": "decision_contact",
            "label": "Their name and email",
            "type": "text"
          }
        ]
      ],
      [
        "The site",
        [
          {
            "name": "site_address",
            "label": "Site address",
            "type": "text"
          },
          {
            "name": "postcode",
            "label": "Postcode",
            "type": "text"
          },
          {
            "name": "tenure",
            "label": "Do you own or lease it",
            "type": "select",
            "options": [
              "We own the building",
              "We lease the building"
            ]
          },
          {
            "name": "lease_years",
            "label": "Years left on the lease",
            "type": "select",
            "options": [
              "Less than 5 years",
              "5 to 10 years",
              "10 to 15 years",
              "More than 15 years",
              "Not sure"
            ]
          },
          {
            "name": "landlord",
            "label": "Landlord name and contact",
            "type": "text"
          },
          {
            "name": "sector",
            "label": "What happens on site",
            "type": "select",
            "options": [
              "Factory or manufacturing",
              "Warehouse or distribution",
              "Workshop or garage",
              "Depot or transport yard",
              "Cold storage",
              "Food production",
              "Offices",
              "Retail or trade counter",
              "Leisure or hospitality",
              "School, college or public building",
              "Something else"
            ]
          },
          {
            "name": "hours",
            "label": "When the site is running",
            "type": "select",
            "options": [
              "Weekdays, roughly 9 to 5",
              "Weekdays, early starts or late finishes",
              "Two shifts",
              "Three shifts or 24 hours",
              "Six or seven days a week",
              "Seasonal or it varies"
            ]
          }
        ]
      ],
      [
        "Your electricity",
        [
          {
            "name": "mpan",
            "label": "MPAN, your supply number",
            "type": "text"
          },
          {
            "name": "bills",
            "label": "Your electricity bills",
            "type": "file"
          },
          {
            "name": "loa",
            "label": "Letter of Authority",
            "type": "checkbox"
          }
        ]
      ],
      [
        "Your roof",
        [
          {
            "name": "roof",
            "label": "Roof type",
            "type": "select",
            "options": [
              "Metal sheet or profile",
              "Flat roof",
              "Tiles or slate",
              "Fibre cement or asbestos",
              "A mix of types",
              "Not sure"
            ]
          },
          {
            "name": "roof_age",
            "label": "Rough age of the roof",
            "type": "select",
            "options": [
              "Under 10 years",
              "10 to 25 years",
              "Over 25 years",
              "Not sure"
            ]
          },
          {
            "name": "roof_photo",
            "label": "Photo of the roof",
            "type": "file"
          }
        ]
      ],
      [
        "Anything else",
        [
          {
            "name": "notes",
            "label": "Anything we should know",
            "type": "textarea"
          }
        ]
      ]
    ]
  },
  "contact": {
    "to": [
      "jonathan@econelectrical.co.uk"
    ],
    "cc": [],
    "title": "Website Enquiry",
    "subject": "Website enquiry",
    "reply": {
      "from": "Econ Electrical <info@econelectrical.co.uk>",
      "reply_to": [
        "jonathan@econelectrical.co.uk"
      ],
      "subject": "Your message to Econ Electrical",
      "kicker": "Message received",
      "preheader": "A member of our team will be in touch within one working day.",
      "intro": "Your message has come through safely and is with us now.",
      "promise": "A member of our team will be in touch within one working day.",
      "summary_heading": "",
      "echo": [],
      "extra": "If there is anything you would like to add, just reply to this email."
    },
    "fields": [
      [
        "The enquiry",
        [
          {
            "name": "name",
            "label": "Name",
            "type": "text"
          },
          {
            "name": "company",
            "label": "Company",
            "type": "text"
          },
          {
            "name": "email",
            "label": "Email",
            "type": "email"
          },
          {
            "name": "phone",
            "label": "Phone",
            "type": "tel"
          },
          {
            "name": "message",
            "label": "Message",
            "type": "textarea"
          }
        ]
      ]
    ]
  }
};
const SITE = {
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
};

const FROM = 'Econ Electrical Website <website@econelectrical.co.uk>';
const INBOX = 'https://app.netlify.com/projects/econ-electrical/forms';

const BLACK = '#111111';
const GREY = '#6b6b6b';
const RULE = '#e2e2e2';
const GREEN = '#9eca84';

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/* A file field arrives as an object, but which keys it carries has changed
   before now, so every spelling we have seen is accepted and a bare string
   still works. */
function asFile(v) {
  if (!v) return null;
  if (typeof v === 'string') {
    return /^https?:\/\//.test(v) ? { url: v, name: v.split('/').pop() } : null;
  }
  if (typeof v === 'object' && v.url) {
    return { url: v.url, name: v.filename || v.name || 'attachment', size: v.size, type: v.type };
  }
  return null;
}

function mb(bytes) {
  if (!bytes && bytes !== 0) return '';
  const m = bytes / 1048576;
  return ' (' + (m < 0.1 ? '<0.1' : m.toFixed(1)) + ' MB)';
}

function when(iso) {
  const d = iso ? new Date(iso) : new Date();
  if (isNaN(d)) return '';
  return d.toLocaleString('en-GB', {
    timeZone: 'Europe/London', day: 'numeric', month: 'long', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  }).replace(',', ' at');
}

/* The value of one field. Tick box groups can arrive several ways: as the plain
   field the page script fills in ("Solar PV; EV charging"), or, if the script did
   not run, as the boxes themselves (name_ticked[], or name[] from before they
   were renamed) in either a list or a single string. All of them come out as one
   list. A semicolon separates them because some answers contain commas. */
function listOf(data, name) {
  const out = [];
  const add = v => {
    if (Array.isArray(v)) v.forEach(add);
    else if (v != null && String(v).trim() !== '') {
      String(v).split(/\s*;\s*/).forEach(p => { if (p.trim()) out.push(p.trim()); });
    }
  };
  add(data[name]);
  for (const alt of [name + '_ticked[]', name + '_ticked', name + '[]']) {
    if (!out.length) add(data[alt]);
  }
  return out.filter((v, i) => out.indexOf(v) === i);
}

function valueOf(data, f) {
  if (f.type === 'chips') return listOf(data, f.name).join(', ');
  return data[f.name];
}

/* Only an answer the form itself offers is ever repeated back to the customer.
   Tick box answers are found by looking for each offered answer in what came in,
   so they are recognised however the list was joined on the way. */
function allowed(f, value) {
  if (!f.options) return [];
  const opts = f.options.map(o => (Array.isArray(o) ? o[1] : o));
  if (f.type === 'chips') {
    const joined = (Array.isArray(value) ? value : [value]).join(' ; ');
    return opts.filter(o => joined.indexOf(o) !== -1);
  }
  return opts.indexOf(value) !== -1 ? [value] : [];
}

/* The rows above the detail in Jonathan's email: the few things that decide
   what to do with it. A contact message has nothing to summarise: the message
   is the whole of it. */
function flags(form, data) {
  const out = [];
  if (form === 'site-assessment') {
    const tenure = data.tenure || '';
    if (/lease/i.test(tenure)) {
      const years = data.lease_years ? ', ' + data.lease_years.toLowerCase() + ' left' : '';
      out.push(['Tenure', 'Leasehold' + years + '. Landlord consent needed']);
    } else if (tenure) {
      out.push(['Tenure', 'Owns the building']);
    }
    const bills = asFile(data.bills);
    out.push(['Bills', bills ? 'Attached' : 'Not attached, we will have to ask']);
    out.push(['Half hourly data', data.loa ? 'Authorised, send the LOA' : 'Not authorised, bills only']);
    if (data.decision) out.push(['Sign off', data.decision]);
  }
  if (form === 'enquiry') {
    if (data.stage) out.push(['Project', esc(data.stage)]);
    if (data.timescale) out.push(['Start', esc(data.timescale)]);
    if (data.next_step) out.push(['Wants first', esc(data.next_step)]);
    const how = [data.contact_method, data.contact_time && data.contact_time !== 'Any time'
      ? data.contact_time.toLowerCase() : ''].filter(Boolean).join(', ');
    if (how) out.push(['Contact by', esc(how)]);
  }
  return out;
}

/* The plain text alternative is built from the same rows as the HTML, so a line
   break written as a tag has to come back as a real one. */
function plain(v) {
  return String(v).replace(/<br\s*\/?>/gi, '\n    ').replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"');
}

function rowsHtml(pairs) {
  return pairs.map(([k, v]) => `
    <tr>
      <td style="padding:9px 16px 9px 0;vertical-align:top;width:190px;color:${GREY};
                 font:400 13px/1.5 Arial,sans-serif;border-bottom:1px solid ${RULE};">${esc(k)}</td>
      <td style="padding:9px 0;vertical-align:top;color:${BLACK};
                 font:400 15px/1.5 Arial,sans-serif;border-bottom:1px solid ${RULE};">${v}</td>
    </tr>`).join('');
}

function buildEmail(form, data, meta) {
  const cfg = FORMS[form];
  const files = [];
  const summary = flags(form, data);
  const groups = cfg.fields.map(([heading, fields]) => {
    const pairs = [];
    for (const f of fields) {
      const raw = valueOf(data, f);
      if (raw === undefined || raw === null || raw === '') continue;
      if (f.type === 'file') {
        const file = asFile(raw);
        if (!file) continue;
        files.push(file);
        pairs.push([f.label, `<a href="${esc(file.url)}" style="color:${BLACK};">${esc(file.name)}</a>` +
                             `<span style="color:${GREY};">${mb(file.size)}</span>`]);
      } else if (f.type === 'checkbox') {
        pairs.push([f.label, 'Yes']);
      } else if (f.name === 'email') {
        pairs.push([f.label, `<a href="mailto:${esc(raw)}" style="color:${BLACK};">${esc(raw)}</a>`]);
      } else if (f.name === 'phone') {
        pairs.push([f.label, `<a href="tel:${esc(String(raw).replace(/\s+/g, ''))}" style="color:${BLACK};">${esc(raw)}</a>`]);
      } else if (f.type === 'chips') {
        pairs.push([f.label, listOf(data, f.name).map(esc).join('<br>')]);
      } else {
        pairs.push([f.label, esc(raw).replace(/\n/g, '<br>')]);
      }
    }
    /* A row that only repeats one in the summary above is left out. */
    const fresh = pairs.filter(([k, v]) => !summary.some(([sk, sv]) => sk === k && sv === v));
    return fresh.length ? { heading, pairs: fresh } : null;
  }).filter(Boolean);

  /* The headline is whatever best identifies the enquiry: the business, or the
     person's name when no business was given. Under it, who and where. */
  const headline = data.business || data.company || data.name || 'New enquiry';
  const place = data.postcode || data.location || '';
  const where = [headline !== data.name ? data.name : '', data.site_address, place]
    .filter(Boolean).join(', ');
  const rows = summary;

  const sections = groups.map(g => `
    <tr><td style="padding:30px 0 10px;">
      <div style="font:700 11px/1 Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:${GREY};">${esc(g.heading)}</div>
    </td></tr>
    <tr><td><table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;">${rowsHtml(g.pairs)}</table></td></tr>`).join('');

  const html = `<!doctype html>
<html><body style="margin:0;padding:0;background:#f4f4f4;">
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background:#f4f4f4;">
<tr><td align="center" style="padding:24px 12px;">
<table role="presentation" cellpadding="0" cellspacing="0" width="640" style="max-width:640px;width:100%;background:#ffffff;">

  <tr><td style="background:${BLACK};padding:18px 28px;">
    <span style="font:700 15px/1 Arial,sans-serif;letter-spacing:.22em;color:#ffffff;">ECON ELECTRICAL</span>
  </td></tr>

  <tr><td style="padding:30px 28px 0;">
    <div style="font:700 11px/1 Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:${GREY};">${esc(cfg.title)}</div>
    <div style="font:700 26px/1.25 Arial,sans-serif;color:${BLACK};padding:10px 0 4px;">${esc(headline)}</div>
    ${where ? `<div style="font:400 15px/1.5 Arial,sans-serif;color:${GREY};">${esc(where)}</div>` : ''}
  </td></tr>

  ${rows.length ? `<tr><td style="padding:24px 28px 0;">
    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;background:#f7f7f7;">
      <tr><td style="padding:4px 18px 10px;">
        <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;">
          ${rowsHtml(rows)}
        </table>
      </td></tr>
    </table>
  </td></tr>` : ''}

  <tr><td style="padding:0 28px;">
    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;">${sections}</table>
  </td></tr>

  <tr><td style="padding:28px;">
    <div style="font:400 13px/1.6 Arial,sans-serif;color:${GREY};border-top:1px solid ${RULE};padding-top:18px;">
      Reply to this email and it goes straight to ${esc(data.email || 'the sender')}.<br>
      Submitted ${esc(when(meta.created_at))} from the website. Ref ${esc(reference(meta))}.
      <a href="${INBOX}" style="color:${GREY};">All submissions</a>
    </div>
  </td></tr>

</table>
</td></tr></table>
</body></html>`;

  const text = [
    cfg.title.toUpperCase(),
    headline, where, '',
    ...rows.map(([k, v]) => k + ': ' + plain(v)),
    '',
    ...groups.flatMap(g => ['', g.heading.toUpperCase(),
      ...g.pairs.map(([k, v]) => '  ' + k + ': ' + plain(v))]),
    '',
    ...(files.length ? ['ATTACHMENTS', ...files.map(f => '  ' + f.name + ' ' + f.url), ''] : []),
    'Submitted ' + when(meta.created_at) + ' from the website. Ref ' + reference(meta) + '.',
  ].join('\n');

  const subject = cfg.subject + ': ' + headline + (place ? ', ' + place : '') +
    (form === 'enquiry' && data.stage ? ' (' + data.stage + ')' : '');
  return { subject, html, text };
}

/* The first name, when the name field holds something that looks like one.
   Never a link, a number or a sentence: otherwise nothing, and the email simply
   says "Thank you." */
function firstName(name) {
  const first = String(name || '').trim().split(/\s+/)[0] || '';
  if (!/^[A-Za-zÀ-ɏ][A-Za-zÀ-ɏ'’-]{0,23}$/.test(first)) return '';
  return first.charAt(0).toUpperCase() + first.slice(1);
}

function validEmail(v) {
  return typeof v === 'string' && v.length <= 254 && /^[^\s@<>()",;:]+@[^\s@<>()",;:]+\.[A-Za-z]{2,}$/.test(v);
}

/* A short reference the customer can quote and Jonathan can search his inbox
   for: ECON, the date in London, and the end of Netlify's own submission id. */
function reference(meta) {
  let d = meta && meta.created_at ? new Date(meta.created_at) : new Date();
  if (isNaN(d)) d = new Date();
  const parts = new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Europe/London', year: '2-digit', month: '2-digit', day: '2-digit',
  }).formatToParts(d);
  const get = t => (parts.find(p => p.type === t) || {}).value || '';
  const tail = String((meta && meta.id) || '').replace(/[^a-z0-9]/gi, '').slice(-4).toUpperCase();
  return 'ECON-' + get('year') + get('month') + get('day') + (tail ? '-' + tail : '');
}

/* The confirmation the customer gets. Built to read like a letter from an
   established contractor rather than a form receipt: the black header carries
   the logo exactly as it appears on Econ's other material, the type is quiet
   and well spaced, and the only colour is the brand green rule under the logo.
   Only answers the form itself offered are echoed back. */
const FONT = "'Helvetica Neue',Helvetica,Arial,sans-serif";
const INK = '#0b0b0b';
const BODY = '#3d3d3d';
const MUTED = '#8c8c8c';
const HAIR = '#e8e8e6';
const PAGE = '#efefec';
const FOOT = '#f7f7f5';

function longhand(html) {
  return html.replace(/font:(\d{3}) ([\d.]+px)\/([\d.]+(?:px)?) ([^;"]+)/g,
    (m, weight, size, height, family) =>
      `font-family:${family};font-size:${size};line-height:${height};font-weight:${weight}`);
}

function label(text, extra) {
  return `<div style="font:700 11px/1.4 ${FONT};letter-spacing:2.2px;text-transform:uppercase;color:${MUTED};${extra || ''}">${esc(text)}</div>`;
}

function buildReply(form, data, meta) {
  const cfg = FORMS[form];
  const r = cfg.reply;
  const byName = {};
  for (const [, fields] of cfg.fields) for (const f of fields) byName[f.name] = f;
  const rows = [];
  for (const [name, title] of (r.echo || [])) {
    const f = byName[name];
    if (!f) continue;
    const v = f.type === 'chips' ? listOf(data, name) : data[name];
    if (!v || (Array.isArray(v) && !v.length)) continue;
    const ok = allowed(f, v);
    if (ok.length) rows.push([title, ok]);
  }
  const first = firstName(data.name);
  const heading = first ? 'Thank you, ' + first + '.' : 'Thank you.';
  const ref = reference(meta);
  const site = SITE.domain;
  const bare = site.replace(/^https?:\/\//, '');
  const img = path => esc(site + '/assets/img/' + path);

  const summary = rows.length ? `
  <tr><td class="px" style="padding:40px 48px 0;">
    ${label(r.summary_heading, `padding-bottom:12px;border-bottom:1px solid ${INK};`)}
    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;">
      ${rows.map(([k, v]) => `
      <tr>
        <td class="lbl" style="padding:15px 16px 15px 0;width:150px;vertical-align:top;border-bottom:1px solid ${HAIR};font:700 10.5px/1.75 ${FONT};letter-spacing:1.6px;text-transform:uppercase;color:${MUTED};">${esc(k)}</td>
        <td style="padding:15px 0;vertical-align:top;border-bottom:1px solid ${HAIR};font:400 15px/1.6 ${FONT};color:${INK};">${v.map(esc).join('<br>')}</td>
      </tr>`).join('')}
    </table>
  </td></tr>` : '';

  const html = `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<meta name="color-scheme" content="light only">
<meta name="supported-color-schemes" content="light only">
<title>${esc(r.subject)}</title>
<style>
  @media (max-width: 620px) {
    .px { padding-left: 26px !important; padding-right: 26px !important; }
    .h1 { font-size: 27px !important; }
    .stack { display: block !important; width: 100% !important; }
    .gap { padding-top: 20px !important; }
    .lbl { width: 112px !important; }
    .ref { text-align: left !important; padding-top: 8px !important; }
  }
  a[x-apple-data-detectors] { color: inherit !important; text-decoration: none !important; }
</style>
</head>
<body style="margin:0;padding:0;background:${PAGE};">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;mso-hide:all;">${esc(r.preheader)}</div>
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
      <td class="stack" style="vertical-align:top;">${label(r.kicker)}</td>
      <td class="stack ref" align="right" style="vertical-align:top;text-align:right;">${label('Ref ' + ref, 'letter-spacing:1.4px;')}</td>
    </tr></table>
    <h1 class="h1" style="margin:22px 0 0;font:400 31px/1.2 ${FONT};letter-spacing:-0.5px;color:${INK};">${esc(heading)}</h1>
    <p style="margin:18px 0 0;font:400 15px/1.75 ${FONT};color:${BODY};">${esc(r.intro)}</p>
    <p style="margin:10px 0 0;font:700 15px/1.75 ${FONT};color:${INK};">${esc(r.promise)}</p>
  </td></tr>

  ${summary}

  ${r.extra ? `<tr><td class="px" style="padding:30px 48px 0;font:400 14px/1.75 ${FONT};color:${BODY};">${esc(r.extra)}</td></tr>` : ''}

  <tr><td class="px" style="padding:38px 48px 0;">
    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;border-top:1px solid ${HAIR};"><tr>
      <td class="stack" width="55%" style="padding:24px 16px 0 0;vertical-align:top;">
        ${label('Speak to us')}
        <a href="tel:${esc(SITE.phone_href)}" style="display:inline-block;margin-top:8px;font:700 21px/1.3 ${FONT};color:${INK};text-decoration:none;letter-spacing:0.2px;">${esc(SITE.phone)}</a>
        <div style="margin-top:4px;font:400 13px/1.6 ${FONT};color:${MUTED};">${esc(SITE.hours_text)}</div>
      </td>
      <td class="stack gap" width="45%" style="padding:24px 0 0;vertical-align:top;">
        ${label('Email')}
        <a href="mailto:${esc(SITE.email)}" style="display:inline-block;margin-top:8px;font:700 15px/1.5 ${FONT};color:${INK};text-decoration:none;">${esc(SITE.email)}</a>
      </td>
    </tr></table>
  </td></tr>

  <tr><td class="px" style="padding:42px 48px 46px;font:400 15px/1.75 ${FONT};color:${BODY};">
    Kind regards,<br><span style="font-weight:700;color:${INK};">The Econ Electrical team</span>
  </td></tr>

  <tr><td class="px" bgcolor="${FOOT}" style="background:${FOOT};padding:30px 48px 32px;border-top:1px solid ${HAIR};">
    <table role="presentation" cellpadding="0" cellspacing="0"><tr>
      <td style="padding-right:24px;vertical-align:middle;"><img src="${img('email/logo-niceic-dark-64.png')}" width="57" height="32" alt="NICEIC Approved Contractor" style="display:block;border:0;width:57px;height:32px;"></td>
      <td style="padding-right:24px;vertical-align:middle;"><img src="${img('email/logo-mcs-dark-64.png')}" width="83" height="32" alt="MCS Certified" style="display:block;border:0;width:83px;height:32px;"></td>
      <td style="vertical-align:middle;"><img src="${img('email/logo-safecontractor-dark-64.png')}" width="34" height="32" alt="SafeContractor Approved" style="display:block;border:0;width:34px;height:32px;"></td>
    </tr></table>
    <p style="margin:20px 0 0;font:400 12px/1.8 ${FONT};color:${MUTED};">${esc(SITE.legal)}, ${esc(SITE.address.join(', '))}<br><a href="${esc(site)}" style="color:${INK};font-weight:700;text-decoration:none;">${esc(bare)}</a></p>
  </td></tr>

</table>
<!--[if mso]></td></tr></table><![endif]-->
<p style="max-width:520px;margin:20px auto 0;font:400 11px/1.7 ${FONT};color:#9a9a9a;text-align:center;">You are receiving this because this email address was used on ${esc(bare)}. If that was not you, please ignore it and nothing more will be sent.</p>
</td></tr></table>
</body></html>`;

  const text = [
    r.kicker.toUpperCase() + '   Ref ' + ref, '',
    heading, '',
    r.intro,
    r.promise, '',
    ...(rows.length ? [r.summary_heading.toUpperCase(), ...rows.map(([k, v]) => '  ' + k + ': ' + v.join(', ')), ''] : []),
    ...(r.extra ? [r.extra, ''] : []),
    'Speak to us: ' + SITE.phone + ' (' + SITE.hours_text + ')',
    'Email: ' + SITE.email, '',
    'Kind regards,', 'The Econ Electrical team', '',
    SITE.legal + ', ' + SITE.address.join(', '),
    'NICEIC Approved Contractor, MCS Certified, SafeContractor Approved', bare,
  ].join('\n');

  return { subject: r.subject, html: longhand(html), text, ref };
}

async function send(key, body, what) {
  try {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      console.error('submission-created: Resend refused the ' + what, res.status, await res.text());
    } else {
      console.log('submission-created: sent the ' + what + ':', body.subject);
    }
  } catch (err) {
    console.error('submission-created: could not reach Resend for the ' + what, err);
  }
}

exports.handler = async function (event) {
  let payload;
  try {
    payload = JSON.parse(event.body).payload;
  } catch (err) {
    console.error('submission-created: could not read the submission', err);
    return { statusCode: 200, body: 'ignored' };
  }

  const form = payload.form_name;
  const cfg = FORMS[form];
  if (!cfg) {
    console.log('submission-created: no routing for form', form);
    return { statusCode: 200, body: 'unknown form' };
  }

  const key = process.env.RESEND_API_KEY;
  if (!key) {
    console.error('submission-created: RESEND_API_KEY is not set, no email sent. '
                  + 'The submission is still saved in Netlify.');
    return { statusCode: 200, body: 'no key' };
  }

  const data = payload.data || {};
  const jobs = [];

  /* 1. To the office. */
  const meta = { created_at: payload.created_at, id: payload.id };
  const office = buildEmail(form, data, meta);
  const toOffice = { from: FROM, to: cfg.to, subject: office.subject, html: office.html, text: office.text };
  /* An empty Cc is left off rather than sent as an empty list. */
  if (cfg.cc && cfg.cc.length) toOffice.cc = cfg.cc;
  /* So that replying goes to the client rather than to a no reply address. */
  if (validEmail(data.email)) toOffice.reply_to = [data.email];
  jobs.push(send(key, toOffice, 'office email'));

  /* 2. To the customer, so they know it arrived. A reply to it goes to Jonathan. */
  if (cfg.reply && validEmail(data.email)) {
    const mail = buildReply(form, data, meta);
    jobs.push(send(key, {
      from: cfg.reply.from, to: [data.email], reply_to: cfg.reply.reply_to,
      subject: mail.subject, html: mail.html, text: mail.text,
    }, 'customer confirmation'));
  }

  await Promise.all(jobs);

  /* Always 200. A failed email must never look like a failed submission. */
  return { statusCode: 200, body: 'ok' };
};

/* Exported so the samples in the repo are rendered by the same code that sends
   the real thing, rather than by a copy that drifts. */
exports.buildEmail = buildEmail;
exports.buildReply = buildReply;
