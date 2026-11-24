"""The Free Site Energy Assessment page: its words, and the form it asks.

This is a lead page rather than a service page. Someone arrives from a solar or EV
page, or from a link Jonathan sends them, and the job of the page is to get a real
site into the diary. So the offer is stated plainly, the report is described by what
it actually contains, and the form is the point of the page rather than an
afterthought at the bottom.

The form is written as data rather than markup so the questions can be changed
without touching the generator, and so the Netlify form definition and the visible
fields cannot drift apart.

On the questions. Every one of these is something the assessment genuinely cannot be
done without, which is the test for whether a field earns its place:

- the MPAN and the bills are what the whole report is calculated from. Without a
  year of real consumption, any figure in the report is a guess dressed up as a
  number, which is the one thing it must never be
- the lease questions decide whether the job is possible at all. A tenant with four
  years left and no landlord consent cannot have a 25 year asset bolted to the roof,
  and finding that out on the site visit wastes everyone's day
- the hours the site runs decide how much of the generation is used on site rather
  than exported, which moves the saving more than the panel count does
- the roof type decides the mounting system, and on fibre cement or asbestos it
  decides whether we can walk on it at all

Dropdowns wherever a dropdown will do, because Jonathan asked for it and because a
field someone has to think about in free text is a field they abandon.
"""

NAME = 'site-assessment'          # the Netlify form name; also the submission label
PATH = '/free-site-energy-assessment/'
THANKS = '/free-site-energy-assessment/thank-you/'

HERO = {
    'kicker': 'Free, No Obligation',
    'h1': 'Free Site Energy Assessment',
    'lede': 'See what solar, battery storage and EV charging could save your business '
            'before you spend a penny. We look at your electricity use, your roof and '
            'your power supply, then send you a clear report.',
    'title': 'Free Site Energy Assessment for Businesses | Econ Electrical',
    'description': 'A free, no obligation energy assessment for commercial and industrial '
                   'sites. We review your electricity use, roof and supply, then report on '
                   'solar, battery storage and EV charging with costs, payback and grants.',
}

# What the report contains. Written as promises the report has to keep, because this
# list is what the person is agreeing to when they fill the form in.
REPORT_SHOWS = [
    ('sun', 'How much of your power solar could supply',
     'Measured against your actual consumption through the year, not a generic yield figure, '
     'with the saving that comes with it.'),
    ('layers', 'The right system and battery size',
     'A roof layout showing where the panels go, how many, and the battery size that suits '
     'how your site actually runs.'),
    ('tag', 'Budget cost, payback and 25 year return',
     'What it costs, how long it takes to pay for itself and what it is worth across the '
     'life of the system.'),
    ('plug-zap', 'EV charging for staff, fleet and visitors',
     'What each group needs, where the chargers go, and which grants you qualify for.'),
    ('gauge', 'Whether your supply can take it',
     'Your incoming supply, your spare capacity, and whether the network operator needs to '
     'be involved before anything is installed.'),
    ('handshake', 'Ways to pay for it',
     'Buy it outright, finance it, or a power purchase agreement with nothing upfront where '
     'you only pay for the power it generates.'),
]

PROCESS = [
    ('You fill in the form', 'Five minutes. The more of it you can answer, the more use the '
     'report is, but tell us what you know and we will chase the rest.'),
    ('We review your electricity', 'We read your bills and, with your permission, pull your '
     'half hourly usage from your supplier so we can see how your site really behaves.'),
    ('We visit the site', 'About an hour. We look at the roof, the incoming supply and the '
     'distribution boards, and we take our own measurements.'),
    ('We talk you through it', 'You get the report, and we walk through it with you. If the '
     'answer is that it is not worth doing, we will tell you that too.'),
]

ASSURANCES = [
    ('badge-check', 'MCS certificate on every solar install',
     'Issued on completion, which is what Smart Export Guarantee payments depend on.'),
    ('clipboard-check', 'We handle the network operator application',
     'The G99 or G98 paperwork is ours to deal with, not yours.'),
    ('shield-check', 'No obligation and no sales pressure',
     'The assessment is free and it is yours to keep, whether you use us or not.'),
]

# Form fields. type: text, email, tel, select, file, textarea, checkbox.
# A field marked 'lease' only matters to a tenant, and the script hides that group
# until someone says they lease. None of them are required in the HTML: a required
# field that script has hidden blocks submission in a way the person cannot see or fix.
FIELDS = [
    ('About you', None, [
        {'name': 'business', 'label': 'Business name', 'type': 'text', 'required': True,
         'placeholder': 'Registered or trading name', 'autocomplete': 'organization'},
        {'name': 'name', 'label': 'Your name', 'type': 'text', 'required': True,
         'placeholder': 'First and last name', 'autocomplete': 'name'},
        {'name': 'role', 'label': 'Your role', 'type': 'select', 'required': True,
         'options': ['Owner or Director', 'Facilities or Site Manager', 'Operations Manager',
                     'Finance', 'Energy or Sustainability', 'Maintenance or Engineering',
                     'Something else']},
        {'name': 'email', 'label': 'Email', 'type': 'email', 'required': True,
         'placeholder': 'you@company.co.uk', 'autocomplete': 'email'},
        {'name': 'phone', 'label': 'Phone', 'type': 'tel', 'required': True,
         'placeholder': 'Best number to reach you', 'autocomplete': 'tel'},
        {'name': 'decision', 'label': 'Who signs off a decision like this', 'type': 'select',
         'required': True,
         'options': ['I do', 'I do, with a colleague', 'A colleague or another director',
                     'Head office or a parent company', 'The landlord', 'Not sure yet']},
        {'name': 'decision_contact', 'label': 'Their name and email', 'type': 'text',
         'optional': True, 'full': True,
         'placeholder': 'Only if the decision is not yours, so we can include them',
         'help': 'We will not contact them without asking you first.'},
    ]),
    ('The site', 'If you have more than one site, start with the one you most want looked at '
                 'and tell us about the others at the bottom.', [
        {'name': 'site_address', 'label': 'Site address', 'type': 'text', 'required': True,
         'full': True, 'placeholder': 'Street and town', 'autocomplete': 'street-address'},
        {'name': 'postcode', 'label': 'Postcode', 'type': 'text', 'required': True,
         'placeholder': 'WF2 7AJ', 'autocomplete': 'postal-code'},
        {'name': 'tenure', 'label': 'Do you own or lease it', 'type': 'select', 'required': True,
         'options': ['We own the building', 'We lease the building'],
         'help': 'This matters more than people expect, see below.'},
        {'name': 'lease_years', 'label': 'Years left on the lease', 'type': 'select',
         'lease': True, 'optional': True,
         'options': ['Less than 5 years', '5 to 10 years', '10 to 15 years',
                     'More than 15 years', 'Not sure']},
        {'name': 'landlord', 'label': 'Landlord name and contact', 'type': 'text',
         'lease': True, 'optional': True, 'placeholder': 'Company or agent, and a contact if you have one'},
        {'name': 'sector', 'label': 'What happens on site', 'type': 'select', 'required': True,
         'options': ['Factory or manufacturing', 'Warehouse or distribution', 'Workshop or garage',
                     'Depot or transport yard', 'Cold storage', 'Food production',
                     'Offices', 'Retail or trade counter', 'Leisure or hospitality',
                     'School, college or public building', 'Something else']},
        {'name': 'hours', 'label': 'When the site is running', 'type': 'select', 'required': True,
         'options': ['Weekdays, roughly 9 to 5', 'Weekdays, early starts or late finishes',
                     'Two shifts', 'Three shifts or 24 hours', 'Six or seven days a week',
                     'Seasonal or it varies'],
         'help': 'This decides how much of the generation you use yourself rather than export, '
                 'which moves the saving more than the number of panels does.'},
    ]),
    ('Your electricity', 'This is what the whole report is calculated from. Without real '
                         'consumption we would be guessing, and a guess is no use to you.', [
        {'name': 'mpan', 'label': 'MPAN, your supply number', 'type': 'text', 'required': True,
         'full': True, 'placeholder': '13 digits',
         'help': 'On your bill, usually in a grid marked Supply Number. It starts with S.'},
        {'name': 'bills', 'label': 'Your electricity bills', 'type': 'file', 'optional': True,
         'full': True, 'accept': '.pdf,.jpg,.jpeg,.png,.csv,.xlsx',
         'help': 'The last 12 months if you have them, or just the latest bill. '
                 'PDF, spreadsheet or a photo, whatever is easiest.'},
        {'name': 'loa', 'label': 'Letter of Authority', 'type': 'checkbox', 'full': True,
         'text': 'I am happy to sign a Letter of Authority so Econ Electrical can request my '
                 'half hourly usage data from my supplier.',
         'help': 'Half hourly data shows us what your site does hour by hour. It makes the '
                 'report far more accurate, and it is the quickest route if you cannot find '
                 'a year of bills. It gives us read only access to usage, nothing else.'},
    ]),
    ('Your roof', None, [
        {'name': 'roof', 'label': 'Roof type', 'type': 'select', 'required': True,
         'options': ['Metal sheet or profile', 'Flat roof', 'Tiles or slate',
                     'Fibre cement or asbestos', 'A mix of types', 'Not sure']},
        {'name': 'roof_age', 'label': 'Rough age of the roof', 'type': 'select', 'optional': True,
         'options': ['Under 10 years', '10 to 25 years', 'Over 25 years', 'Not sure'],
         'help': 'Panels last 25 years or more, so a roof near the end of its life is worth '
                 'knowing about before anything goes on it.'},
        {'name': 'roof_photo', 'label': 'Photo of the roof', 'type': 'file', 'optional': True,
         'full': True, 'accept': 'image/*',
         'help': 'Optional, but it saves a lot of guesswork. A photo from the yard or an '
                 'upstairs window is plenty. If you have a drone shot, even better.'},
    ]),
    ('Anything else', None, [
        {'name': 'notes', 'label': 'Anything we should know', 'type': 'textarea', 'optional': True,
         'full': True,
         'placeholder': 'Other sites, plans to expand, a machine going in, a deadline you are '
                        'working to, or anything you already know you want'},
    ]),
]

FAQS = [
    ('Is it really free?',
     'Yes, and there is no obligation at the end of it. We do these because a site we have '
     'surveyed properly is a site we can quote accurately, and because roughly half the '
     'buildings we look at turn out to be worth doing. The report is yours either way.'),
    ('What if the answer is that solar is not worth it?',
     'Then the report says so, and it says why. A north facing roof, a short lease or a site '
     'that only draws power at night can all make the numbers not work. We would rather tell '
     'you that than sell you something that disappoints you.'),
    ('We lease the building. Is there any point?',
     'Often yes, but the landlord has to agree, because the system is attached to their '
     'building for 25 years. It is worth knowing early, which is why we ask about the lease '
     'on the form. Shorter leases can still work through a power purchase agreement.'),
    ('Why do you need a year of bills?',
     'Because the saving depends on when you use power, not just how much. A site running two '
     'shifts uses far more of its own generation than one that shuts at four, and that changes '
     'the payback by years. A single bill tells us a quarter of the story.'),
    ('What is a Letter of Authority?',
     'A short form that lets us ask your supplier for your half hourly usage data. It is read '
     'only and covers usage, nothing else. You can withdraw it at any time, and it saves you '
     'digging a year of bills out of a filing cabinet.'),
    ('How long does the site visit take?',
     'About an hour for most sites. We look at the roof, the incoming supply and the '
     'distribution boards. We do not need to interrupt what you are doing.'),
]
