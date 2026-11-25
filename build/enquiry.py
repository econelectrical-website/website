"""The project enquiry page: where every "Enquire Now" button on the site lands.

The contact page stays as it was for general messages. This page is for someone
with a job in mind, and it asks the handful of things Jonathan needs to judge an
enquiry before he picks up the phone: what it is, where, how real it is, and how
the person wants to be contacted. Nearly all of it is ticks and taps, so it is
quicker to fill in than typing a message, and it reads the same way every time.
"""

PATH = '/enquire/'
THANKS = '/enquiry-received/'
NAME = 'enquiry'

HERO = {
    'title': 'Project Enquiry | Electrical Contractors Wakefield | Econ Electrical',
    'description': ('Tell us about your electrical, solar, battery or EV charging project in two '
                    'minutes, mostly ticks. A member of our team will be in touch within one working day.'),
    'kicker': 'Project Enquiry',
    'h1': 'Tell Us About Your Project',
    'lede': ('Two minutes, mostly ticks. A member of our team will be in touch within one '
             'working day.'),
}

# The interest chips carry a short key as well as their label, so a button on, say,
# the EV charging page can open this form with EV charging already ticked
# (/enquire/?about=ev). The label is what lands in the email.
INTERESTS = [
    ('install', 'Electrical installation or fit out'),
    ('maintenance', 'Planned or reactive maintenance'),
    ('subcontract', 'Sub contract work (main contractors)'),
    ('solar', 'Solar PV'),
    ('battery', 'Battery storage'),
    ('ev', 'EV charging'),
    ('led', 'LED lighting'),
    ('testing', 'EICR and testing'),
    ('emergency', 'Emergency lighting'),
    ('pat', 'PAT testing'),
    ('home', 'Home solar and battery'),
    ('advice', 'Not sure yet, need advice'),
]

# Which chip each page's buttons pre-tick. A page that is not listed opens the form
# with nothing ticked.
PAGE_INTEREST = {
    'electrical-installation': 'install',
    'industrial-electrical-contractors': 'install',
    'compliance': 'testing',
    'eicr-fixed-wire-testing': 'testing',
    'commercial-solar-pv-installation': 'solar',
    'commercial-ev-charging-installation': 'ev',
    'commercial-led-lighting': 'led',
    'home-solar-battery-installation': 'home',
}

# The questions, in four short groups. Types:
#   chips   tick any number; at least one is needed (checked by the page script)
#   radio   tap one
#   select  a drop down
# Everything else is an ordinary input. 'phone_if' names the answers to the
# contact question that make a phone number necessary.
FIELDS = [
    ('What do you need?', [
        {'name': 'interests', 'short': 'Interested in', 'label': 'What are you interested in?', 'type': 'chips',
         'required': True, 'hint': 'Tick all that apply', 'options': INTERESTS},
        {'name': 'site_type', 'short': 'Type of site', 'label': 'Type of site', 'type': 'select', 'required': True,
         'options': ['Factory or industrial unit', 'Warehouse or distribution', 'Office or commercial',
                     'Retail, leisure or hospitality', 'School, college or public building',
                     'Healthcare', 'Farm or rural business', 'Building site, new build or refurb',
                     'Home', 'Other']},
        {'name': 'location', 'short': 'Site location', 'label': 'Site postcode or town', 'type': 'text', 'optional': True,
         'placeholder': 'Where the work is', 'autocomplete': 'postal-code'},
    ]),
    ('Where are you up to?', [
        {'name': 'stage', 'short': 'Project', 'label': 'Is this a live project?', 'type': 'radio', 'required': True,
         'options': ['Live, ready to go', 'Pricing or tendering', 'Early days, just exploring']},
        {'name': 'timescale', 'short': 'Start', 'label': 'When would you like to start?', 'type': 'radio', 'required': True,
         'options': ['As soon as possible', 'Within 3 months', '3 to 6 months', '6 months or more',
                     'Not sure yet']},
        {'name': 'next_step', 'short': 'Wants first', 'label': 'What would you like from us first?', 'type': 'radio',
         'required': True,
         'options': ['A call to talk it through', 'A site survey', 'A quote from drawings or a spec',
                     'Just some information for now']},
    ]),
    ('Your details', [
        {'name': 'name', 'short': 'Name', 'label': 'Your name', 'type': 'text', 'required': True,
         'placeholder': 'Your name', 'autocomplete': 'name'},
        {'name': 'company', 'short': 'Company', 'label': 'Company', 'type': 'text', 'optional': True,
         'placeholder': 'Company name', 'autocomplete': 'organization'},
        {'name': 'email', 'short': 'Email', 'label': 'Email', 'type': 'email', 'required': True,
         'placeholder': 'you@company.co.uk', 'autocomplete': 'email'},
        {'name': 'phone', 'short': 'Phone', 'label': 'Phone', 'type': 'tel', 'optional': True,
         'placeholder': 'Best number to reach you', 'autocomplete': 'tel'},
        {'name': 'contact_method', 'short': 'Contact by', 'label': 'How should we get back to you?', 'type': 'radio',
         'required': True, 'options': ['Phone call', 'Email', 'WhatsApp'],
         'phone_if': ['Phone call', 'WhatsApp']},
        {'name': 'contact_time', 'short': 'Best time', 'label': 'Best time to reach you', 'type': 'radio', 'optional': True,
         'options': ['Morning', 'Afternoon', 'Any time']},
    ]),
    ('Anything else?', [
        {'name': 'message', 'short': 'Message', 'label': 'Tell us about the job', 'type': 'textarea', 'optional': True,
         'full': True,
         'placeholder': 'The size of the site, what is there now, any deadlines or drawings you have'},
        {'name': 'heard', 'short': 'Heard about us', 'label': 'How did you hear about us?', 'type': 'select', 'optional': True,
         'options': ['Google search', 'Google Maps or reviews', 'Recommended by someone', 'LinkedIn',
                     'Facebook or Instagram', 'Saw our van or one of our jobs', 'Leaflet or letter',
                     'Worked with us before', 'Other']},
    ]),
]

# What happens after they press send, shown beside the form so nobody wonders.
# The first step depends on whether the instant confirmation email is switched on.
def next_steps(auto_reply):
    first = (('Straight away', 'A confirmation lands in your inbox with a copy of what you picked.')
             if auto_reply else
             ('Straight away', 'Your enquiry comes straight through to our team.'))
    return [first,
            ('Within one working day', 'A member of our team gets in touch, by phone or email, whichever you chose.'),
            ('Then', 'If it suits, we survey the site or price from your drawings, and send a clear written quote.')]
