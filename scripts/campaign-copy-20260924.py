"""Apply the broader CRM positioning to the static export and hydrated modules."""
from pathlib import Path
import html
import json
import re
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
COPY = {
    'LodgeHelm — Turn every safari enquiry into a confirmed booking': 'LodgeHelm: keep the conversation going, even after hours',
    'Turn every safari enquiry into a confirmed booking.': 'Keep the conversation going. Even after hours.',
    'LodgeHelm is the commercial copilot for safari lodges — capture every enquiry from web, email and WhatsApp, quote in minutes, and never let a booking slip through the cracks.': "Bring guest enquiries, quotes and follow-ups together. Configure overnight replies using your lodge's information, build quotes from your rates and see where enquiries drop off before booking.",
    'Built for boutique safari lodges and operators': 'Working with safari businesses across southern and eastern Africa',
    'Every enquiry that slips through is a safari someone else gets to host.': 'Give each guest conversation a clear next step.',
    'Now your lodge answers every call, too. A personalized voice agent picks up day or night — so a missed ring never becomes a safari someone else gets to host.': "Overnight replies use the lodge information you provide and ask for missing trip details. Your team reviews the exchange and confirms availability. We check the setup with you before activation.",
    'Enquiries scattered everywhere': 'Keep the conversation together',
    'Web forms, email and WhatsApp pile up in different places — and something always falls through the cracks.': 'Bring enquiries from your connected website form, email and WhatsApp routes into one shared record.',
    'A slow reply loses the booking': 'Start the conversation after hours',
    'Guests book the lodge that answers first. Every hour you wait, a high-value trip quietly cools off.': 'Configure overnight replies to answer from your property information and collect missing dates or guest numbers.',
    'No system, no follow-up': 'Make the next action visible',
    "Quotes get sent and forgotten. No reminders, no visibility — warm leads go cold while you're out on a drive.": 'Keep the quote and its follow-up task with the enquiry, so the next person can see what needs attention.',
    'See every enquiry, quote in minutes, and let LodgeHelm chase the follow-ups — so no booking slips away while you\'re out on a drive.': 'Read the guest conversation, prepare a quote from your rates and give the team a clear follow-up task.',
    'Capture every enquiry': 'Bring enquiries together',
    'Web, email and WhatsApp enquiries land in one shared inbox — every lead owned, nothing missed, with SLA timers so warm leads get answered fast.': 'Connected web, email and WhatsApp enquiries share one inbox, with the conversation and its owner visible to the team.',
    'Quote in minutes': 'Quote from your rates',
    'Build a branded, templated quote in a few taps — and know the moment your guest opens it.': 'Prepare a branded quote using the rates and fees you have entered, then see when the guest views it.',
    'Never drop a follow-up': 'Keep follow-ups in view',
    'Yes — sending your branded quote now.': "I'll check those dates and prepare your quote.",
    'One inbox for every channel': 'One shared enquiry view',
    'Web, email and WhatsApp enquiries land in a single triage queue — nothing missed, every lead owned, with SLA timers so warm leads get answered fast.': 'See connected enquiries, their conversation history and who is responsible for the next action.',
    'Quote in minutes, not hours': 'Quotes built from your rates',
    'Quote from your rates, not hours': 'Quotes built from your rates',
    'Build a branded, templated quote in a few taps — and know the moment a guest opens it.': 'Use the rates and fees you enter to prepare a branded guest quote. Track when it is viewed.',
    'Follow-up on autopilot': 'A clear follow-up for the team',
    "Automatic nudges and reminders mean no warm enquiry is ever left to go cold — the system chases so your team doesn't have to.": 'Quote rules create follow-up tasks for your team. The guest conversation and quote stay together for whoever responds next.',
    'Africa-real by design': 'See the booking journey',
    'Multi-currency, WhatsApp-first, and built for trade-agent bookings and patchy connectivity — not bolted on after.': 'See enquiry progression and bookings by source, so you know where to investigate a drop-off.',
    'A single recovered safari pays for it': 'A result from our work',
    '5 min': '63%',
    'to a branded quote, not hours': 'measured booking conversion. Individual results vary.',
    '1 trip': 'Rates',
    'Your rates': 'Rates',
    'Team tasks': 'Tasks',
    'recovered covers the year': 'provide the prices in each guest quote',
    'of enquiries captured & chased': 'keep the next follow-up visible',
    'It captures every enquiry from your website, email and WhatsApp into one inbox, helps you build and send branded quotes in minutes, and chases the follow-ups automatically — so no booking slips through the cracks.': 'It brings connected enquiries into one inbox, builds quotes from your entered rates and creates follow-up tasks. Overnight replies can be configured using your lodge information, with availability confirmed by your team.',
    'No. LodgeHelm is built to be picked up in minutes — and we set you up personally on a short call, so your reservations team can start using it the same day.': "We help you set it up around your team. We'll walk through the enquiry, quote and follow-up together before you begin.",
    'Most lodges are up and running within a day. We import your existing enquiries, connect your channels, and walk you through it on a quick onboarding call.': "We'll confirm the setup steps after checking your rates and enquiry channels. We check the connection and a sample exchange with you before activation.",
    'Yes. WhatsApp is first-class, your website enquiry form plugs straight in, and email enquiries land in the same inbox. Multi-currency and trade-agent bookings are built in, not bolted on.': "LodgeHelm supports connected website forms, email and WhatsApp. We'll check your existing setup and agree which route to connect first.",
    "Yes. Every lodge's data is fully isolated, encrypted in transit and at rest, and handled in line with POPIA and GDPR.": "Each organisation has its own access controls. We'll discuss your team's access and the information needed for the enquiry routes you connect.",
    'Start Converting Every Enquiry Today': 'See how LodgeHelm fits your team',
    "Stop losing bookings between enquiry and confirmation — capture every enquiry, quote in minutes, and follow up until it's won.": 'Look at a guest enquiry, a rate-based quote and the next follow-up with Melusi. We will work through what would fit your lodge.',
    # Until the existing Calendly event is corrected, avoid promising a
    # duration on a link that still displays 30 minutes.
    'Book a 15-minute call': 'Book a walkthrough',
}

# The homepage presents the whole CRM. Overnight replies remain one feature.
# Resolve both the original export and the earlier campaign-led wording to
# this approved positioning, so rerunning the script cannot restore it.
POSITIONING = {
    'LodgeHelm: keep the conversation going, even after hours': 'LodgeHelm | CRM for safari lodges and operators',
    'Keep the conversation going. Even after hours.': 'The CRM built for safari lodges and operators.',
    "Bring guest enquiries, quotes and follow-ups together. Configure overnight replies using your lodge's information, build quotes from your rates and see where enquiries drop off before booking.": 'Manage guest enquiries, conversations, quotes and follow-ups in one place, from first contact to confirmed booking.',
    'Give each guest conversation a clear next step.': 'Keep the whole guest journey in view.',
    'Overnight replies use the lodge information you provide and ask for missing trip details. Your team reviews the exchange and confirms availability. We check the setup with you before activation.': "From a guest's first enquiry to a confirmed booking, give your team a shared record of the conversation, quote, booking stage and next step.",
    'Keep the conversation together': 'One record for each enquiry',
    'Bring enquiries from your connected website form, email and WhatsApp routes into one shared record.': 'Bring connected website, email and WhatsApp enquiries into a shared CRM, with conversation history and an owner.',
    'Start the conversation after hours': 'See where each booking stands',
    'Configure overnight replies to answer from your property information and collect missing dates or guest numbers.': 'Track enquiries through qualification, quoting and booking, with clear stages for your team.',
    'Make the next action visible': 'Know what happens next',
    'Keep the quote and its follow-up task with the enquiry, so the next person can see what needs attention.': 'Keep quotes and follow-up tasks with the enquiry, so the next person can pick up the conversation.',
    'Read the guest conversation, prepare a quote from your rates and give the team a clear follow-up task.': 'Manage guest conversations, prepare quotes from your rates and track each enquiry through to booking.',
    'Bring enquiries together': 'Manage your enquiries',
    'One shared enquiry view': 'A shared CRM for your team',
    'See the booking journey': 'Bookings and reporting',
    'See enquiry progression and bookings by source, so you know where to investigate a drop-off.': 'Follow enquiry stages and review bookings by source to see where your team wins business and where guests drop off.',
    'It brings connected enquiries into one inbox, builds quotes from your entered rates and creates follow-up tasks. Overnight replies can be configured using your lodge information, with availability confirmed by your team.': "LodgeHelm is a CRM for safari lodges and operators. It keeps connected guest enquiries, conversations, quotes and follow-up tasks together, with a booking pipeline and reports to help your team see what's happening.",
    'Does it work with WhatsApp and our website?': 'Can it respond to enquiries overnight?',
    "LodgeHelm supports connected website forms, email and WhatsApp. We'll check your existing setup and agree which route to connect first.": 'Overnight replies can be configured to use your lodge information and collect missing trip details. Your team can review the conversation in the CRM and confirm availability. We check the connection and a sample exchange with you before activation.',
    'Look at a guest enquiry, a rate-based quote and the next follow-up with Melusi. We will work through what would fit your lodge.': 'Explore the CRM, prepare a quote and follow an enquiry through the booking pipeline with Melusi.',
    # This accordion text is only rendered after the follow-up step is opened.
    'Automatic reminders and SLA timers chase every warm enquiry, so nothing quietly goes cold.': 'Keep follow-up tasks beside the quote and conversation, with a clear next action for the team.',
    'Response time, quotes sent, conversion and source — run the commercial side of your lodge on numbers, not memory.': 'Review enquiry response times, quotes, conversion and sources to see how your booking pipeline is performing.',
    # The closing banner was still the template's voice-agent pitch. Voice is
    # roadmap-only, so it must never be offered here (positioning lock).
    'Start Answering Every Call Today': 'See LodgeHelm with your own enquiries',
    'Launch your AI voice agent in minutes and deliver better customer experiences — without increasing costs.': 'Walk through a guest enquiry, a quote from your rates and the booking pipeline with Melusi.',
}
COPY = {old: POSITIONING.get(new, new) for old, new in COPY.items()} | POSITIONING

compact = lambda s: re.sub(r'\s+', '', s)
heading_map = {compact(k):v for k,v in COPY.items()}
heading_map[compact('Real results from real customers')] = 'Working with safari businesses'

def static_heading(m):
    text = BeautifulSoup(m.group(2),'html.parser').get_text('',strip=True)
    replacement = heading_map.get(compact(text))
    if replacement: return m.group(1)+html.escape(replacement)+m.group(3)
    return m.group(0)

modified=[]
for f in [ROOT/'index.html',*(ROOT/'assets/js').glob('*.mjs')]:
    before=f.read_text();s=before
    if f.suffix=='.html':
        s=re.sub(r'(<h[1-6]\b[^>]*>)(.*?)(</h[1-6]>)',static_heading,s,flags=re.S)
        # The voice paragraph is split into animated characters in this export.
        def paragraph(m):
            text=BeautifulSoup(m.group(2),'html.parser').get_text('',strip=True)
            replacement=heading_map.get(compact(text))
            return m.group(1)+html.escape(replacement)+m.group(3) if replacement else m.group(0)
        s=re.sub(r'(<p\b[^>]*>)(.*?)(</p>)',paragraph,s,flags=re.S)
    for old,new in sorted(COPY.items(), key=lambda item:len(item[0]), reverse=True):
        s=s.replace(old,new).replace(old.replace('—','\\u2014'),new)
    if f.suffix=='.mjs':
        s=s.replace('children:[`Real results from `,l(`br`,{}),`real customers`]', 'children:`Working with safari businesses`')
        s=s.replace('children:`100%`','children:`Tasks`')
    else:
        s=re.sub(r'(?<=>)(\s*)100%(\s*)(?=</h2>)',r'\1Tasks\2',s)
    if s!=before:f.write_text(s);modified.append(f)

# Version the actual imports so cached Framer modules cannot restore old copy.
revision='crm-20260925-r3'
changed_names={f.name for f in modified if f.suffix=='.mjs'}
for f in [ROOT/'index.html',*(ROOT/'assets/js').glob('*.mjs')]:
    before=f.read_text();s=before
    for name in changed_names:
        s=re.sub(re.escape(name)+r'(?:\?v=[A-Za-z0-9-]+)?(?=["\x27`])',name+'?v='+revision,s)
    if f.name=='index.html':
        s=re.sub(r'src="assets/js/script_main\.jugZsNYD\.mjs(?:\?v=[A-Za-z0-9-]+)?"',
                 'src="assets/js/script_main.jugZsNYD.mjs?v='+revision+'"',s)
    if s!=before:f.write_text(s)

# Keep a concise record of what ships; no prospect data belongs in this repo.
print(json.dumps({'copyReplacements':len(COPY),'changedContentFiles':[str(f.relative_to(ROOT)) for f in modified]}))
