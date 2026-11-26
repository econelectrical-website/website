# Wakefield landing pages.
#
# The main site presents Econ as a regional contractor working across the UK, so its
# service pages name no town. These pages are the exception: one page per service,
# written for businesses in and around Wakefield, where Econ is based. They are kept
# out of the main menu and reached from Google, from the "Electricians in Wakefield"
# link in the footer and from each other, so the rest of the site stays national.
#
# Each page is written fresh rather than copied from the main service page, so Google
# sees two different pages for two different searches and does not treat one as a
# duplicate of the other. Only real work is claimed: projects named here are already
# public on the site.
#
# House style: British English, no hyphens or dashes in the text, no "free quote".

HUB = 'commercial-electricians-wakefield'

# The Google rating shown on these pages, checked on Google on 26 November 2026
# (4.9 from 91 reviews). Update it if it changes.
GOOGLE_RATING = '4.9'

# Shown in the "Across the Wakefield District" panel on every page.
PLACES = ['Wakefield City Centre', 'Ossett', 'Horbury', 'Normanton', 'Castleford', 'Pontefract',
          'Featherstone', 'Knottingley', 'Hemsworth', 'Wakefield 41', 'Wakefield Europort', 'Calder Park']
DISTRICT = {
    'h2': 'Across the Wakefield District',
    'p': ('Our office is at The Courtyard, 225 Denby Dale Road, close to junction 39 of the M1. We work right '
          'across the district, and on sites throughout Yorkshire and the UK.'),
}

PAGES = {
    HUB: {
        'name': 'Commercial Electricians',
        'short': 'Commercial Electricians',
        'icon': 'building-2',
        'blurb': 'Installation, testing and maintenance for every kind of business premises.',
        'title': 'Commercial Electricians in Wakefield | Econ Electrical',
        'description': ('NICEIC approved commercial electricians based in Wakefield. Installations, EICRs, LED lighting, '
                        'solar, EV charging and maintenance for local businesses. Rated 4.9 on Google.'),
        'kicker': 'Commercial Electricians, Wakefield',
        'h1': 'Commercial Electricians in Wakefield',
        'lede': ('Installation, testing, maintenance and renewables for Wakefield businesses, from a NICEIC approved '
                 'team based on Denby Dale Road.'),
        'hero': 'about-vans', 'hero_alt': 'Econ Electrical branded electric vans', 'hero_dim': True,
        'chips': ['Rated %s on Google' % GOOGLE_RATING, 'NICEIC Approved', 'Based in Wakefield', 'Reply Within One Working Day'],
        'intro_h2': 'Your Electrical Contractor, Just Down the Road',
        'intro': [
            'When the power to a production line trips, your insurer asks for an EICR or a new unit needs fitting out, '
            'you want electricians who answer the phone, turn up when they say they will and leave the job certified '
            'and tidy. That is what Econ Electrical has built its name on in Wakefield.',
            'We look after factories, warehouses, offices, schools and shops across the district, from single '
            'installations to planned maintenance across several sites. Every job is carried out by our own NICEIC '
            'approved team, with one point of contact from your first call to the final certificate.',
        ],
        'points': [
            ('map-pin', 'Based in Wakefield', 'Our office is on Denby Dale Road, so your site is never far from our team.'),
            ('badge-check', 'Fully Accredited', 'NICEIC Approved Contractor, MCS certified and SafeContractor accredited.'),
            ('users', 'Trusted Locally', 'Local businesses trust us with their sites. Read what they say in our Google reviews.'),
            ('timer', 'Work Around You', 'Early starts, evenings and weekends, so your business keeps running.'),
        ],
        'includes_h2': 'Everything Electrical, From One Team',
        'includes_intro': ('One contractor for the whole building, so there is one number to call and one set of '
                           'certificates.'),
        'includes': ['Electrical installations and fit outs', 'Three phase power and distribution', 'EICRs and fixed wire testing',
                     'Emergency lighting and PAT testing', 'LED lighting upgrades', 'Solar PV and battery storage',
                     'EV charging for staff and fleets', 'Planned and reactive maintenance'],
        'includes_img': 'home-about-site', 'includes_alt': 'Econ Electrical engineers on site',
        'proof_h2': 'Work Close to Home',
        'proof': ['saint-flooring-group', 'cummins-turbo-technologies', 'commercial-solar-pv-bradford'],
        'quote': 'saint-flooring-group',
        'process': [
            ('Enquire', 'Tell us what you need. A member of our team will be in touch within one working day.'),
            ('Visit', 'We come out to your premises, look at the job and talk it through with you.'),
            ('Quote', 'You get a clear written quote, so you know exactly what is included before any work starts.'),
            ('Deliver', 'Our own team carries out the work, tests it and hands over full certification.'),
        ],
        'faqs': [
            ('Do you cover the whole Wakefield district?', 'Yes. We work right across the district, including the city '
             'centre, Ossett, Horbury, Normanton, Castleford, Pontefract and the business parks by the M1 and M62. We '
             'also work throughout Yorkshire and the rest of the UK.'),
            ('Can you work outside our opening hours?', 'Yes. We regularly work early mornings, evenings and weekends so '
             'shops, offices and production lines are not disrupted.'),
            ('Are you NICEIC approved?', 'Yes. Econ Electrical is a NICEIC Approved Contractor, MCS certified for solar PV '
             'and battery storage, and SafeContractor accredited. Our NICEIC and MCS registrations can be checked online.'),
            ('How quickly will we hear back?', 'A member of our team will be in touch within one working day of your '
             'enquiry. If it is urgent, call us on 01924 677085.'),
        ],
        'interest': 'install',
        'cta_h': 'Need an Electrician in Wakefield?',
        'cta_p': ('Tell us about your premises and what you need, and a member of our team will be in touch within one '
                  'working day.'),
        'cta_img': 'card-saint',
    },

    'industrial-electrical-contractors-wakefield': {
        'name': 'Industrial Electrical',
        'short': 'Industrial Electrical',
        'icon': 'factory',
        'blurb': 'Fit outs, machine power and distribution for working industrial sites.',
        'title': 'Industrial Electrical Contractors Wakefield | Econ Electrical',
        'description': ('Industrial electrical contractors in Wakefield. Factory and warehouse fit outs, machine power and '
                        'distribution, planned around your production by a NICEIC approved team.'),
        'kicker': 'Industrial Electrical, Wakefield',
        'h1': 'Industrial Electrical Contractors in Wakefield',
        'lede': ('Factory and warehouse fit outs, machine power and distribution for industrial sites across Wakefield, '
                 'planned around your production.'),
        'hero': 'home-cta-warehouse', 'hero_alt': 'Warehouse with switchgear and high bay lighting',
        'chips': ['Factory Fit Outs', 'Machine Power', 'Shutdowns Planned Around You', 'NICEIC Certified'],
        'intro_h2': 'Built for Sites That Cannot Stop',
        'intro': [
            'From the distribution sheds around Wakefield Europort to the units on Wakefield 41 and the works across '
            'Normanton and Castleford, this district runs on industry. When your site needs new power, a new line or a '
            'complete fit out, every hour of downtime costs you money.',
            'Econ was started by two electricians who spent years working side by side on industrial sites, so we know '
            'how a working plant runs. We plan shutdowns around shift changes, evenings and weekends, carry out the work '
            'with our own team and hand over full NICEIC certification at the end.',
        ],
        'points': [
            ('factory', 'Industrial Experience', 'Production lines, workshops, warehouses and distribution centres.'),
            ('timer', 'Downtime Kept to a Minimum', 'Shutdowns planned around your shifts, with evening and weekend working.'),
            ('layers', 'Power for Growth', 'Supplies, distribution boards and containment sized for what comes next.'),
            ('shield-check', 'Safety First', 'RAMS for every job, from a SafeContractor accredited team.'),
        ],
        'includes_h2': 'What We Install on Industrial Sites',
        'includes_intro': 'From a single machine supply to a whole new building, we cover the complete electrical package.',
        'includes': ['New unit and warehouse fit outs', 'Three phase distribution boards', 'Supplies and isolation for machinery',
                     'Containment: tray, basket and trunking', 'LED high bay lighting', 'RCBO and surge protection',
                     'Charge points for staff and fleets', 'Testing, certification and maintenance'],
        'includes_img': 'saint-7', 'includes_alt': 'Cable tray and containment above a new enclosure',
        'proof_h2': 'Industrial Projects We Have Delivered',
        'proof': ['saint-flooring-group', 'cummins-turbo-technologies', 'swan-civil-engineering'],
        'quote': 'cummins-turbo-technologies',
        'process': [
            ('Survey', 'We walk the site with you, look at the supply and the equipment, and agree what needs to happen.'),
            ('Plan', 'We design the installation and plan every shutdown around your shifts and deliveries.'),
            ('Install', 'Our team works to programme, keeping walkways clear and your people safe.'),
            ('Certify', 'Full NICEIC certification, then maintenance from the team that did the work.'),
        ],
        'faqs': [
            ('Can you fit out a new industrial unit from scratch?', 'Yes. At Saint Flooring Group’s new warehouse in '
             'Wakefield we designed and installed the lighting, power and containment throughout, including LED high bays '
             'and EV charging.'),
            ('Can you add power for new machinery without stopping production?', 'Usually, yes. We prepare as much as we '
             'can while you run, then make the final connections during a planned shutdown, often at a weekend.'),
            ('Do you work on industrial sites outside Wakefield?', 'Yes. Wakefield is home, but we deliver industrial '
             'projects across the UK, from Huddersfield and Liverpool to Nottingham.'),
            ('Can you maintain the installation afterwards?', 'Yes. We provide planned preventative maintenance and '
             'reactive support, so the team that installed your system can keep it running.'),
        ],
        'interest': 'install',
        'cta_h': 'Got Work Planned on Your Site?',
        'cta_p': 'Tell us about your site and what you need, and we will plan the work around your production.',
        'cta_img': 'card-swan',
    },

    'commercial-eicr-testing-wakefield': {
        'name': 'EICR and Testing',
        'short': 'EICR and Testing',
        'icon': 'clipboard-check',
        'blurb': 'EICRs, fixed wire, emergency lighting and PAT testing with clear reports.',
        'title': 'Commercial EICR and Testing in Wakefield | Econ Electrical',
        'description': ('Commercial EICRs, fixed wire testing, emergency lighting and PAT testing in Wakefield. Clear '
                        'reports, out of hours testing and remedial work from NICEIC approved electricians.'),
        'kicker': 'Electrical Testing, Wakefield',
        'h1': 'Commercial EICR and Electrical Testing in Wakefield',
        'lede': ('EICRs, fixed wire testing, emergency lighting and PAT testing for Wakefield businesses and landlords, '
                 'with clear reports and remedial work done properly.'),
        'hero': 'compliance-hero', 'hero_alt': 'Electrician inspecting a commercial electrical installation',
        'chips': ['Commercial EICRs', 'Reports for Landlords', 'Out of Hours Testing', 'Remedial Works'],
        'intro_h2': 'Stay Compliant Without the Hassle',
        'intro': [
            'Your insurer wants a current EICR, a tenant is asking for certificates, or nobody can remember when the '
            'building was last tested. Whatever has prompted it, we make electrical testing straightforward for '
            'businesses across Wakefield.',
            'We test offices, shops, warehouses, factories, schools and commercial lets, working in sections or out of '
            'hours so you can keep trading. Every observation is explained in plain English, and any remedial work is '
            'quoted clearly before anything is done.',
        ],
        'points': [
            ('clipboard-check', 'Thorough Testing', 'Boards, circuits, protective devices, earthing and bonding all checked.'),
            ('timer', 'Little Disruption', 'Testing in sections, early mornings, evenings or weekends.'),
            ('file-text', 'Reports You Can Understand', 'Clear findings, with an itemised quote for any remedial work.'),
            ('calendar-check', 'Never Miss a Date', 'We keep your test dates on record and remind you when the next one is due.'),
        ],
        'includes_h2': 'The Testing We Carry Out',
        'includes_intro': 'One contractor for all of your testing, so everything is recorded in one place.',
        'includes': ['Commercial EICRs', 'Fixed wire testing on industrial sites', 'EICRs for commercial landlords and lets',
                     'Emergency lighting testing', 'PAT testing', 'Thermal imaging surveys',
                     'Remedial works and recertification', 'Testing across several sites'],
        'includes_img': 'compliance-thermal', 'includes_alt': 'Thermal imaging survey of a distribution board',
        'proof_h2': '',
        'proof': [],
        'quote': '',
        'process': [
            ('Book', 'We agree the scope, the timings and any areas that cannot be switched off.'),
            ('Inspect', 'We inspect and test the installation, in sections or out of hours where needed.'),
            ('Report', 'You receive a clear report, with every observation explained.'),
            ('Put Right', 'We carry out any remedial work and confirm the installation is satisfactory.'),
        ],
        'faqs': [
            ('How often do we need an EICR?', 'Industry guidance recommends inspecting most commercial premises, such as '
             'offices and shops, at least every 5 years, and industrial sites every 3 years. Your report will also give a '
             'recommended date for the next inspection, based on what we find.'),
            ('Do commercial landlords need an EICR?', 'Landlords and tenants have duties to keep electrical installations '
             'safe under the Electricity at Work Regulations 1989, and a current EICR is the recognised way to show it. '
             'Many leases and insurers also ask for one.'),
            ('Can you test our emergency lighting and appliances on the same visit?', 'Yes. We can combine your EICR with '
             'emergency lighting and PAT testing, so you have one visit, one contractor and one set of records.'),
            ('What if our report comes back unsatisfactory?', 'We explain each observation, give you an itemised quote for '
             'the remedial work and, once it is done, confirm the installation is satisfactory.'),
        ],
        'interest': 'testing',
        'cta_h': 'Is Your EICR Due?',
        'cta_p': 'Tell us about your building and we will advise on the testing you need and when it is due.',
        'cta_img': 'compliance-testing',
    },

    'commercial-solar-panels-wakefield': {
        'name': 'Commercial Solar and Batteries',
        'short': 'Solar and Battery Storage',
        'icon': 'sun',
        'blurb': 'MCS certified solar PV and battery storage, sized from your own energy data.',
        'title': 'Commercial Solar Panels in Wakefield | Econ Electrical',
        'description': ('MCS certified commercial solar panels and battery storage for Wakefield businesses. Systems '
                        'designed from your own energy data, with a free site energy assessment.'),
        'kicker': 'Commercial Solar PV, Wakefield',
        'h1': 'Commercial Solar Panels and Battery Storage in Wakefield',
        'lede': ('MCS certified solar PV and battery storage for Wakefield businesses, designed from your own energy data '
                 'to bring your bills down.'),
        'hero': 'solarbradford-1', 'hero_alt': 'The completed 50kW solar array on the roof at Manningham Concrete in Bradford',
        'chips': ['MCS Certified', 'Free Site Energy Assessment', 'Battery Storage', 'Approvals Handled'],
        'intro_h2': 'Put Your Roof to Work',
        'intro': [
            'Wakefield has no shortage of big roofs over factories, warehouses and offices that use most of their power '
            'in daylight hours. That is where solar earns its keep: every unit you generate on your own roof is a unit '
            'you do not have to buy from the grid.',
            'We design every system from your half hourly energy data, so it is sized to pay you back rather than simply '
            'fill the roof. Battery storage can hold surplus generation for later in the day, cut expensive peaks and '
            'keep critical equipment running.',
        ],
        'results': [('50kW', 'roof mounted system for Manningham Concrete in Bradford'),
                    ('2 weeks', 'to install, from start to finish'),
                    ('2/3', 'roughly how much of the site’s electricity now comes from the roof')],
        'points': [
            ('sun', 'Designed From Your Data', 'Sized from your half hourly readings, not guesswork.'),
            ('badge-check', 'MCS Certified', 'Accredited installations, usually needed for Smart Export Guarantee payments.'),
            ('battery-charging', 'Battery Storage', 'Store surplus solar, cut peak charges and protect critical loads.'),
            ('file-text', 'Approvals Handled', 'Network operator applications and certification all done for you.'),
        ],
        'includes_h2': 'What Your System Includes',
        'includes_intro': 'From the first assessment to monitoring, one team delivers the whole system.',
        'includes': ['Free site energy assessment', 'System design and savings modelling', 'Arrays on the roof or on the ground',
                     'Inverters and switchgear', 'Battery storage', 'Network operator applications', 'Generation monitoring',
                     'Maintenance and aftercare'],
        'includes_img': 'solarbradford-4', 'includes_alt': 'DC isolators and switchgear for a commercial solar PV system',
        'proof_h2': 'A Recent Solar Project',
        'proof': ['commercial-solar-pv-bradford'],
        'quote': '',
        'assess': True,
        'process': [
            ('Assess', 'We look at your bills, your half hourly data and your roof, at no charge.'),
            ('Design', 'We model the system and the savings, so you can see the return before you commit.'),
            ('Install', 'Our MCS certified team installs and commissions the system safely.'),
            ('Monitor', 'You can see what you generate, and we keep the system performing.'),
        ],
        'faqs': [
            ('Is our building suitable for solar panels?', 'Most commercial roofs can take solar, but orientation, shading, '
             'the roof covering and the structure all matter. We check these during the free site energy assessment and '
             'will tell you honestly if solar is not right for your building.'),
            ('How much could solar save our business?', 'It depends on how much power you use in daylight hours and the size '
             'of system your roof can take. We model your savings from your own half hourly data before you commit.'),
            ('Will we need planning permission?', 'Many rooftop systems on commercial buildings fall under permitted '
             'development, but there are limits, and listed buildings and conservation areas have extra rules. We check '
             'this with you as part of the design.'),
            ('Can batteries be added now or later?', 'Either. Battery storage can be installed alongside the panels or added '
             'to an existing system later on.'),
        ],
        'interest': 'solar',
        'cta_h': 'Find Out What Your Roof Could Save',
        'cta_p': ('Book a free site energy assessment and we will show you what solar and battery storage could do for '
                  'your Wakefield site.'),
        'cta_img': 'renewables-hero',
        'cta_assess': True,
    },

    'commercial-ev-charger-installation-wakefield': {
        'name': 'EV Charging',
        'short': 'EV Charging',
        'icon': 'plug-zap',
        'blurb': 'Workplace, visitor and fleet charging designed around your supply.',
        'title': 'Commercial EV Charger Installation Wakefield | Econ Electrical',
        'description': ('Workplace, visitor and fleet EV charger installation for Wakefield businesses. Supply checks, load '
                        'management and certified installs from NICEIC approved electricians.'),
        'kicker': 'EV Charging, Wakefield',
        'h1': 'EV Charger Installation for Wakefield Businesses',
        'lede': ('Workplace, visitor and fleet charging for Wakefield businesses, designed around your vehicles and your '
                 'electrical supply.'),
        'hero': 'busdepot-2', 'hero_alt': 'Wall mounted EV chargers installed by Econ Electrical',
        'chips': ['Workplace Charging', 'Fleet Charging', 'Load Management', 'Smart Chargers'],
        'intro_h2': 'Charging That Works for Your Site',
        'intro': [
            'More of your staff, visitors and vans are going electric. The right charging setup keeps them moving and adds '
            'value to your premises. The wrong one trips breakers, needs an expensive supply upgrade or sits unused.',
            'We start with your electrical supply and how your vehicles are actually used, then design the right mix of '
            'chargers, with load management where it avoids a costly upgrade. Whether you need a few chargers for staff '
            'or charging for a whole fleet, we handle the survey, design, installation and commissioning.',
        ],
        'points': [
            ('plug-zap', 'The Right Chargers', 'AC chargers for staff and visitors, rapid DC chargers for fleets on a quick turnaround.'),
            ('gauge', 'Supply Checked First', 'We check your capacity before recommending equipment.'),
            ('shield-check', 'Safe and Compliant', 'Correct earthing, protection and certification on every installation.'),
            ('route', 'Ready to Grow', 'Ducting and containment sized for the chargers you add later.'),
        ],
        'includes_h2': 'What We Install',
        'includes_intro': 'One team takes care of everything, from checking your supply to looking after the chargers.',
        'includes': ['Supply checks and site surveys', 'Workplace and visitor chargers', 'Fleet and depot charging',
                     'Rapid DC chargers', 'Load management', 'Network operator applications',
                     'Smart charger setup and access control', 'Maintenance and support'],
        'includes_img': 'devitechdcac-1', 'includes_alt': 'A DC rapid charger installed at a logistics depot',
        'proof_h2': 'EV Charging Projects We Have Delivered',
        'proof': ['saint-flooring-group', 'dc-ev-charging-installation-reading', 'ev-installation'],
        'quote': '',
        'process': [
            ('Survey', 'We check your supply, your parking and who will be charging, and when.'),
            ('Design', 'We choose the chargers and design the cabling, containment and load management.'),
            ('Install', 'We install, test and commission everything and set up the smart features you need.'),
            ('Support', 'Certification, handover and maintenance to keep every charger working.'),
        ],
        'faqs': [
            ('How many chargers can our premises support?', 'It depends on your incoming supply and how much of it you '
             'already use. We check your maximum demand during the survey and, where it helps, use load management so '
             'more chargers can share the same supply.'),
            ('Can you install rapid chargers for our fleet?', 'Yes. We install DC rapid chargers as well as AC chargers, '
             'including four DC chargers for Devitech in Reading.'),
            ('Can we charge staff or visitors to use them?', 'Yes. Smart chargers let you control who can charge and pass '
             'the cost of the electricity on to drivers if you choose.'),
            ('Do we need approval from the network operator?', 'Larger installations may need to be notified to, or '
             'approved by, Northern Powergrid, the network operator for Wakefield. We find out during the survey and deal '
             'with the application on your behalf.'),
        ],
        'interest': 'ev',
        'cta_h': 'Ready to Add EV Charging?',
        'cta_p': 'Arrange a site survey and we will design charging that suits your vehicles and your supply.',
        'cta_img': 'renewables-ev',
    },

    'commercial-led-lighting-wakefield': {
        'name': 'LED Lighting',
        'short': 'LED Lighting',
        'icon': 'lightbulb',
        'blurb': 'High bay, office and external LED lighting that cuts running costs.',
        'title': 'Commercial LED Lighting in Wakefield | Econ Electrical',
        'description': ('Commercial LED lighting upgrades in Wakefield. High bay, office and external lighting with smart '
                        'controls, installed out of hours to cut your energy bills.'),
        'kicker': 'LED Lighting, Wakefield',
        'h1': 'Commercial LED Lighting Upgrades in Wakefield',
        'lede': ('High bay, office and external LED lighting for Wakefield businesses, designed to cut your energy bills '
                 'and give your people better light.'),
        'hero': 'saint-4', 'hero_alt': 'Warehouse with new high bay LED lighting in Wakefield',
        'chips': ['High Bay LEDs', 'Lighting Design', 'Smart Controls', 'Evening and Weekend Installs'],
        'intro_h2': 'Cut the Cost of Keeping the Lights On',
        'intro': [
            'In most warehouses, factories and offices the lights run for long hours every day, and older fluorescent, '
            'sodium or metal halide fittings burn through energy while they do it. Swapping them for well designed LED '
            'lighting is one of the quickest ways a business can bring its bills down.',
            'We design the new layout around your racking, workstations and walkways, add sensors where they will save '
            'you money, and install out of hours so you never have to stop. When Saint Flooring Group opened their new '
            'warehouse in Wakefield, we fitted LED high bays throughout.',
        ],
        'results': [('55%', 'reduction in energy costs at BM Packaging'), ('40%', 'increase in light levels on the factory floor')],
        'points': [
            ('lightbulb', 'Designed for Your Space', 'Fittings, spacing and mounting heights planned around how the space is used.'),
            ('activity', 'Smart Controls', 'Presence and daylight sensors that dim or switch off lights when they are not needed.'),
            ('timer', 'No Downtime', 'Evening and weekend installs, with MEWPs for safe work at height.'),
            ('leaf', 'Lower Running Costs', 'Less energy used and far fewer replacements at height.'),
        ],
        'includes_h2': 'What Your Upgrade Includes',
        'includes_intro': 'We handle the whole upgrade, from measuring your current light levels to the final certificate.',
        'includes': ['Light level surveys and layouts', 'LED high bays for warehouses and factories', 'LED panels for offices and classrooms',
                     'External and car park lighting', 'Sensors that dim or switch off unused lights', 'Emergency lighting upgrades',
                     'MEWPs and safe access at height', 'Certificates and handover'],
        'includes_img': 'bm-packaging-2', 'includes_alt': 'New LED high bay lighting across a factory floor in Huddersfield',
        'proof_h2': 'Lighting Projects We Have Delivered',
        'proof': ['saint-flooring-group', 'led-lighting', 'factory-led-lighting-nottingham'],
        'quote': 'led-lighting',
        'process': [
            ('Survey', 'We measure your current light levels, running hours and energy use.'),
            ('Design', 'We plan the layout and controls, and set out what the upgrade should save you.'),
            ('Install', 'We fit the new lights around your working hours, safely and tidily.'),
            ('Handover', 'You get your certificates, a clear handover and support for years to come.'),
        ],
        'faqs': [
            ('How much could an LED upgrade save us?', 'It depends on your current lighting and how long it runs. At BM '
             'Packaging in Huddersfield, our upgrade cut energy costs by 55%. We show you the expected savings before you '
             'commit.'),
            ('Will we have to close while you install?', 'No. We regularly install in the evenings and at weekends so your '
             'business keeps running.'),
            ('Can you reuse our existing circuits?', 'Often, yes. We check their condition during the survey and reuse them '
             'where it is safe to do so.'),
            ('Can our emergency lighting be done at the same time?', 'Yes, and it makes sense to. While we are working on '
             'your lighting we can check emergency lighting coverage and swap older fittings for LED.'),
        ],
        'interest': 'led',
        'cta_h': 'Ready for Better Light and Lower Bills?',
        'cta_p': 'Arrange a lighting survey and we will show you what an upgrade could save your premises.',
        'cta_img': 'home-cta-warehouse',
    },

    'electrical-maintenance-wakefield': {
        'name': 'Electrical Maintenance',
        'short': 'Electrical Maintenance',
        'icon': 'wrench',
        'blurb': 'Planned maintenance and reactive support from a team that knows your site.',
        'title': 'Electrical Maintenance in Wakefield | Econ Electrical',
        'description': ('Planned preventative maintenance and reactive electrical support for Wakefield businesses. '
                        'Thermal imaging, testing and repairs from NICEIC approved electricians.'),
        'kicker': 'Electrical Maintenance, Wakefield',
        'h1': 'Electrical Maintenance for Wakefield Businesses',
        'lede': ('Planned preventative maintenance and reactive support for factories, warehouses, offices and schools '
                 'across Wakefield.'),
        'hero': 'installation-reactive', 'hero_alt': 'Electrician diagnosing a fault at a distribution board',
        'chips': ['Planned Maintenance', 'Reactive Support', 'Thermal Imaging', 'Testing and Records'],
        'intro_h2': 'Fewer Breakdowns, Fewer Surprises',
        'intro': [
            'Electrical faults rarely pick a good moment. A tripped board can stop a production line, close a shop floor or '
            'leave a school without power. Planned maintenance finds the problems before they find you, and when something '
            'does go wrong you want an electrician who already knows your site.',
            'We put together a maintenance plan that suits your building and your budget, from thermal imaging of '
            'distribution boards to emergency lighting tests and EICRs, all recorded in one place. Because we are based in '
            'Wakefield, our team is close by when you need us.',
        ],
        'points': [
            ('calendar-check', 'Planned Around You', 'Visits scheduled to suit your shifts and opening hours.'),
            ('thermometer', 'Thermal Imaging', 'Hot spots in boards and connections found before they fail.'),
            ('wrench', 'Reactive Support', 'Fast fault finding and repairs from a team that knows your site.'),
            ('file-text', 'One Set of Records', 'Tests, certificates and reminders kept together for your insurer and auditors.'),
        ],
        'includes_h2': 'What a Maintenance Plan Covers',
        'includes_intro': 'Every plan is built around your site, and can include any of the following.',
        'includes': ['Planned preventative maintenance', 'Reactive fault finding and repairs', 'Thermal imaging surveys',
                     'EICRs and fixed wire testing', 'Emergency lighting testing', 'PAT testing',
                     'Machine and production line support', 'Lighting and small works'],
        'includes_img': 'installation-ppm', 'includes_alt': 'Engineer recording test results at a distribution board',
        'proof_h2': 'Ongoing Support in Action',
        'proof': ['cummins-turbo-technologies'],
        'quote': 'cummins-turbo-technologies',
        'process': [
            ('Review', 'We walk your site, look at your records and agree what needs checking, and how often.'),
            ('Plan', 'We set out a maintenance schedule and a clear list of tasks.'),
            ('Maintain', 'Our engineers carry out each visit and report back clearly.'),
            ('Respond', 'If something fails between visits, you call a team that already knows your site.'),
        ],
        'faqs': [
            ('What does a planned maintenance plan include?', 'It depends on your site, but most plans cover visual '
             'inspections, thermal imaging of distribution boards, emergency lighting tests, PAT testing and keeping your '
             'EICR up to date, with a report after every visit.'),
            ('Do you provide reactive support?', 'Yes. When something goes wrong we diagnose and repair the fault, and the '
             'engineers who come out already know your site.'),
            ('Can maintenance happen outside working hours?', 'Yes. We schedule visits early, late or at weekends so your '
             'operation is not disrupted.'),
            ('Do you support production lines?', 'Yes. We provide ongoing electrical maintenance support on the assembly '
             'lines at Cummins Turbo Technologies in Huddersfield.'),
        ],
        'interest': 'maintenance',
        'cta_h': 'Keep Your Site Running',
        'cta_p': 'Tell us about your premises and we will put together a maintenance plan that suits it.',
        'cta_img': 'installation-ppm',
    },

    'home-solar-battery-wakefield': {
        'name': 'Home Solar and Batteries',
        'short': 'Home Solar and Batteries',
        'icon': 'house',
        'blurb': 'Premium solar, battery and EV charging systems for exceptional homes.',
        'title': 'Home Solar and Battery Storage in Wakefield | Econ Electrical',
        'description': ('Premium home solar panels, battery storage and EV charging in Wakefield, designed as one SolaX '
                        'system and installed by MCS certified electricians based in the city.'),
        'kicker': 'Home Solar and Batteries, Wakefield',
        'h1': 'Home Solar and Battery Storage in Wakefield',
        'lede': ('Premium solar panels, battery storage and EV charging for homes in and around Wakefield, designed as one '
                 'SolaX system by MCS certified electricians.'),
        'hero': 'renewables-solar', 'hero_alt': 'Solar panels installed on a roof',
        'chips': ['MCS Certified', 'SolaX Systems', 'Backup Power', 'Based in Wakefield'],
        'intro_h2': 'A Home Energy System Done Properly',
        'intro': [
            'Solar panels and a battery are a long term investment in your home, so who designs and fits them matters. We '
            'are electricians first, based in Wakefield, and we design every system around your roof, your household and '
            'the way you use energy.',
            'Your panels, battery, EV charger and heat pump can all run as one SolaX system, controlled from one app, with '
            'our trusted partner fitting the heat pump into the same setup. Everything is MCS certified, neatly installed '
            'and properly handed over.',
        ],
        'points': [
            ('sun', 'Premium Panels', 'All black panels designed around your roof.'),
            ('battery-charging', 'Battery Storage', 'Keep daytime solar for the evening, and charge on cheaper overnight rates.'),
            ('shield-check', 'Backup Power', 'Keep essential circuits, or the whole home, running in a power cut.'),
            ('plug-zap', 'EV Charging', 'Charge your car from the sun or on the cheapest rates, automatically.'),
        ],
        'includes_h2': 'Everything Handled, Scaffold to Switch On',
        'includes_intro': 'One team manages every stage, so there are no gaps between trades.',
        'includes': ['A home visit and a system designed for you', 'Scaffolding organised for you', 'Solar panel installation',
                     'Battery and inverter fitted neatly', 'EV charger installation', 'Backup power setup',
                     'MCS certificate and grid notification', 'Heat pump installed by our trusted partner'],
        'includes_img': 'about-vans', 'includes_alt': 'Econ Electrical branded electric vans',
        'proof_h2': '',
        'proof': [],
        'quote': '',
        'process': [
            ('Consultation', 'We visit your home, look at your roof and talk through how you use energy.'),
            ('Design', 'We design the system and show you the expected savings before you commit.'),
            ('Installation', 'One team handles the scaffold, panels, battery and electrics, and leaves your home tidy.'),
            ('Aftercare', 'MCS certification, app setup and support whenever you need it.'),
        ],
        'faqs': [
            ('Do I pay VAT on solar panels and a battery?', 'Not at the moment. Solar panels fitted to homes in Great '
             'Britain are zero rated for VAT, as are batteries fitted alongside them. The zero rate is currently due to end '
             'on 31 March 2027.'),
            ('Will the battery work in a power cut?', 'Yes, if the system is designed with backup. We can back up your '
             'essential circuits or the whole house, and the battery switches over by itself when the grid goes down.'),
            ('Will I be paid for the power I export?', 'You can be. Because our installations are MCS certified, you can join '
             'a Smart Export Guarantee tariff with an energy supplier and earn from the electricity you send to the grid.'),
            ('Do you install outside Wakefield?', 'Yes. We design and install home systems across West Yorkshire as well '
             'as in Wakefield itself.'),
        ],
        'interest': 'home',
        'cta_h': 'Plan Your Home Energy System',
        'cta_p': ('Book a design consultation at your home and we will show you exactly what solar panels and a battery '
                  'could do for you.'),
        'cta_img': 'home-energy-art',
    },
}

ORDER = [HUB, 'industrial-electrical-contractors-wakefield', 'commercial-eicr-testing-wakefield',
         'commercial-solar-panels-wakefield', 'commercial-ev-charger-installation-wakefield',
         'commercial-led-lighting-wakefield', 'electrical-maintenance-wakefield', 'home-solar-battery-wakefield']
