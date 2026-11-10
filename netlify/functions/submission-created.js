'use strict';

/**
 * Emails a website enquiry to the office.
 *
 * Netlify runs this automatically the moment a form is submitted. It is not
 * reachable from the web and takes no arguments of its own: Netlify calls it
 * with the submission, this builds an email out of it and hands that to Resend.
 *
 * It covers both forms on the site, the contact form and the site energy
 * assessment, and routes each to whoever deals with it.
 *
 * Why this exists rather than Netlify's own notification emails: from 3 November
 * 2026 Netlify only lets you notify addresses belonging to members of your
 * Netlify team, there is no way to put one person in To and the rest in Cc, and
 * the email it sends is a flat dump of field names. This sends a mail that can
 * be read in ten seconds, puts the client in Reply-To so hitting reply goes to
 * them, and keeps the office addresses out of Netlify's hands entirely.
 *
 * Nothing here is load bearing for the enquiry itself. Netlify stores every
 * submission before this runs, so if Resend is down or the key is wrong the
 * enquiry is still safe in the dashboard and this just logs the failure.
 *
 * FORMS is written in by build.py from the pages themselves, so the labels in
 * the email are always the labels on the form. Do not edit it here.
 */

const FORMS = {
  "site-assessment": {
    "to": [
      "jonathan@econelectrical.co.uk"
    ],
    "cc": [],
    "title": "Site Energy Assessment Request",
    "subject": "Site assessment",
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
            "type": "select"
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
            "type": "select"
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
            "type": "select"
          },
          {
            "name": "lease_years",
            "label": "Years left on the lease",
            "type": "select"
          },
          {
            "name": "landlord",
            "label": "Landlord name and contact",
            "type": "text"
          },
          {
            "name": "sector",
            "label": "What happens on site",
            "type": "select"
          },
          {
            "name": "hours",
            "label": "When the site is running",
            "type": "select"
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
            "type": "select"
          },
          {
            "name": "roof_age",
            "label": "Rough age of the roof",
            "type": "select"
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

const FROM = 'Econ Electrical Website <website@econelectrical.co.uk>';
const INBOX = 'https://app.netlify.com/projects/econ-electrical/forms';

const BLACK = '#111111';
const GREY = '#6b6b6b';
const RULE = '#e2e2e2';

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

/* The three things that decide whether this site is worth a visit and whether
   the report can actually be calculated. Robert reads this and nothing else
   before deciding what to do with it, so it goes above the detail. A contact
   enquiry has nothing to summarise: the message is the whole of it. */
function flags(form, data) {
  if (form !== 'site-assessment') return [];
  const out = [];
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
  const groups = cfg.fields.map(([heading, fields]) => {
    const pairs = [];
    for (const f of fields) {
      const raw = data[f.name];
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
      } else {
        pairs.push([f.label, esc(raw).replace(/\n/g, '<br>')]);
      }
    }
    return pairs.length ? { heading, pairs } : null;
  }).filter(Boolean);

  /* The headline is whatever best identifies the enquiry: a business for an
     assessment, the person's name for a contact message. */
  const business = data.business || data.name || 'New enquiry';
  const where = [data.site_address, data.postcode, data.company].filter(Boolean).join(', ');
  const rows = flags(form, data);

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
    <div style="font:700 26px/1.25 Arial,sans-serif;color:${BLACK};padding:10px 0 4px;">${esc(business)}</div>
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
      Submitted ${esc(when(meta.created_at))} from the website.
      <a href="${INBOX}" style="color:${GREY};">All submissions</a>
    </div>
  </td></tr>

</table>
</td></tr></table>
</body></html>`;

  const text = [
    cfg.title.toUpperCase(),
    business, where, '',
    ...rows.map(([k, v]) => k + ': ' + plain(v)),
    '',
    ...groups.flatMap(g => ['', g.heading.toUpperCase(),
      ...g.pairs.map(([k, v]) => '  ' + k + ': ' + plain(v))]),
    '',
    ...(files.length ? ['ATTACHMENTS', ...files.map(f => '  ' + f.name + ' ' + f.url), ''] : []),
    'Submitted ' + when(meta.created_at) + ' from the website.',
  ].join('\n');

  const subject = cfg.subject + ': ' + business + (data.postcode ? ', ' + data.postcode : '');
  return { subject, html, text };
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
  const { subject, html, text } = buildEmail(form, data, { created_at: payload.created_at });

  const body = { from: FROM, to: cfg.to, subject, html, text };
  /* An empty Cc is left off rather than sent as an empty list. */
  if (cfg.cc && cfg.cc.length) body.cc = cfg.cc;
  /* So that replying goes to the client rather than to a no reply address. */
  if (data.email) body.reply_to = [data.email];

  try {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      console.error('submission-created: Resend refused the email',
                    res.status, await res.text());
    } else {
      console.log('submission-created: emailed', subject);
    }
  } catch (err) {
    console.error('submission-created: could not reach Resend', err);
  }

  /* Always 200. A failed email must never look like a failed submission. */
  return { statusCode: 200, body: 'ok' };
};

/* Exported so the sample in the repo is rendered by the same code that sends
   the real thing, rather than by a copy that drifts. */
exports.buildEmail = buildEmail;
