#!/usr/bin/env python3
"""
Fathers for the Fatherless, page builder (PALOMA).

The files it writes ARE the website; this just stops ten pages from drifting
apart. Run from the repo root:   python3 _build/site.py

Every claim nobody at the ministry has confirmed goes through C(). The build
writes CONFIRM-SHEET.md listing all of them.

Rebuilt 6 Oct 2026 to carry Joe's 25 Sep corrections into the generator:
  - Joe Young off the site entirely (his instruction)
  - no officers, no directors; Hyatt Browning Shirkey off entirely
  - health and dental care are FUNDED by the ministry, not delivered by it
  - the giving switch (GIVE) and the tax-status switch (TAX_STATUS)
  - American spelling, and the de-AI copy pass
The build refuses to write anything if one of those regresses (see guards()).
"""
import os, re, html, datetime
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = "fathers4thefatherless@gmail.com"
YEAR = datetime.date.today().year

# ---------------------------------------------------------------------------
# THE GIVING SWITCH. Paste the processor's URL into "url", rebuild, done.
# Empty = every give control sends an email with the amount in the subject.
# ---------------------------------------------------------------------------
GIVE = {
    "url":          "",   # <<< THE ONLY REQUIRED EDIT
    "provider":     "",   # name shown to donors, e.g. "Givelify"
    "amount_param": "",   # e.g. "amount"    if the processor takes ?amount=25
    "freq_param":   "",   # e.g. "frequency"
    "freq_monthly": "",   # e.g. "monthly"
    "freq_once":    "",   # e.g. "once"
    "one_time_url": "",   # only if one-time giving lives at a different URL
}

# Fill ONLY with the wording on the IRS determination letter, once the ministry
# has sent it in writing. Empty renders nothing anywhere.
TAX_STATUS = ""

def give_href(amount=None, monthly=True):
    """Every give control on every page routes through here."""
    if not GIVE["url"]:
        if amount:
            subj = "I want to give $%s %s to Fathers for the Fatherless" % (
                amount, "a month" if monthly else "once")
        else:
            subj = "I want to give %sto Fathers for the Fatherless" % ("" if monthly else "a one-time gift ")
        return "mailto:%s?subject=%s" % (EMAIL, quote(subj))
    base = GIVE["url"] if (monthly or not GIVE["one_time_url"]) else GIVE["one_time_url"]
    q = []
    if amount and GIVE["amount_param"]:
        q.append("%s=%s" % (GIVE["amount_param"], amount))
    if GIVE["freq_param"]:
        val = GIVE["freq_monthly"] if monthly else GIVE["freq_once"]
        if val:
            q.append("%s=%s" % (GIVE["freq_param"], val))
    return base + (("&" if "?" in base else "?") + "&".join(q) if q else "")

def give_attrs(amount=None, monthly=True):
    h = html.escape(give_href(amount, monthly))
    return 'href="%s"%s' % (h, ' target="_blank" rel="noopener"' if GIVE["url"] else "")

CLAIMS = []
def C(text, note=""):
    CLAIMS.append((text if len(text) < 150 else text[:147] + "...", note))
    return text

def photo(what):
    return '<div class="ph"><i>Photo needed: %s</i></div>' % html.escape(what)

NAV = [("index.html", "Home"), ("mission.html", "The mission"),
       ("mission-trips.html", "Go"), ("give.html", "Give"),
       ("updates.html", "Updates"), ("about.html", "About"),
       ("contact.html", "Contact")]

CITIES = [
    dict(city="Guaimaca", region=C("Central Honduras"), who=C("Bro. Andrew Finnicum"),
         since=C("2010"), blurb=C("A growing congregation in central Honduras where fathers are being "
                 "discipled and families are being restored through Scripture.")),
    dict(city="La Ceiba", region="Northern coast", who=C("Bro. Edwin Rodriguez"), since="2006",
         blurb="A port city named after the giant ceiba tree near the dock, and the fourth most "
               "populous city in Honduras. Our longest-running field location. A mission house is in renovation."),
    dict(city="Talanga", region=C("Central region"), who=C("Bro. Misael Alvarado"),
         since=C("2014"), blurb=C("A church in the central region, where the pastor is teaching the "
                 "fathers in his own congregation.")),
    dict(city="La Ermita", region=C("Western Honduras"), who=C("Bro. Cristobal Alvarado"),
         since=C("2018"), blurb=C("The newest of the five churches, in western Honduras.")),
    dict(city="Danlí", region="El Paraíso, eastern Honduras", who=C("Jimmy Welch"),
         since=C("2016"), blurb=C("Families are being reached. Marriages restored through the "
                 "principles of Scripture.")),
]

THREE = [
    ("dove", "d1", "Engage",
     "Our commitment goes beyond financial support or long-distance assistance. The men behind this "
     "work have personally traveled to Honduras, and they go back every year. We count many of the "
     "men there among our dearest friends."),
    ("book", "d2", "Equip",
     "We equip men, young and old alike, to accept and fulfill the calling of leadership God has "
     "placed upon their lives, and to leave a legacy of faith their children can follow."),
    ("house", "d3", "Edify",
     "The work will not be finished in a day, or in one short-term missions trip. If these men apply "
     "the principles of God's Word to their lives, we will not and cannot forsake them."),
]

PROGRAMS = [
    ("education.html", "book", "Education",
     "Verse-by-verse teaching, leadership training, schooling alongside the mission workers, and "
     "teaching fathers to lead the Word inside their own homes."),
    ("mission-trips.html", "dove", "Mission trips",
     "Teams travel to Honduras to work beside the Honduran brothers who are there the rest of "
     "the year."),
    ("health-care.html", "house", "Health care",
     "We do not run clinics. Giving pays for a family to see a doctor and fill a prescription when "
     "they could not have afforded either."),
    ("dental-care.html", "tree", "Dental care",
     "We do not run a dental clinic. Giving pays for the work to be done, so pain gets treated "
     "instead of endured."),
]

# Amounts and the four labels confirmed by Joe, 25 Sep. Descriptions kept directional:
# what a gift "goes toward", never what it buys.
TIERS = [
    ("25", "Discipleship materials", "Goes toward the books and materials fathers are trained from."),
    ("50", "Pastoral training", "Goes toward training the pastors who disciple those fathers."),
    ("100", "Church planting", "Goes toward planting a church and keeping it going."),
    ("250", "Mission outreach trip", "Goes toward the cost of getting a team to the field."),
]

ICONS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<symbol id="i-tree" viewBox="0 0 64 80"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M32 74V42"/><path d="M32 74c-5-4-10-6-15-7"/><path d="M32 74c5-4 10-6 15-7"/><path d="M8 38C16 22 48 22 56 38"/><path d="M15 45c6-11 28-11 34 0"/><path d="M32 46l-8-8M32 46l9-9"/></g></symbol>
<symbol id="i-house" viewBox="0 0 64 72"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M6 32 32 10l26 22"/><path d="M13 32v30h38V32"/><path d="M26 62V46h12v16"/></g></symbol>
<symbol id="i-dove" viewBox="0 0 64 56"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 40c8-17 26-22 41-15 4 2 9 0 12-5 0 13-8 20-19 22-13 2-26 2-34-2Z"/><path d="M20 33c6-6 15-7 22-3"/></g></symbol>
<symbol id="i-book" viewBox="0 0 64 60"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M32 16c-6-5-16-6-25-4v34c9-2 19-1 25 4"/><path d="M32 16c6-5 16-6 25-4v34c-9-2-19-1-25 4"/><path d="M32 16v34"/></g></symbol>
</defs></svg>"""

def ico(n, w=46, h=42):
    return '<svg width="%d" height="%d" aria-hidden="true"><use href="#i-%s"/></svg>' % (w, h, n)

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Archivo:wght@400;600;700;800&family=Newsreader:ital,opsz,wght@'
         '0,6..72,400;0,6..72,500;1,6..72,400&display=swap">')

def head(title, desc, page):
    nav = "".join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == page else '', t)
                  for h, t in NAV)
    canon = "" if page == "index.html" else page
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#0E2243">
<link rel="canonical" href="https://fathersforthefatherless.org/{canon}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="https://fathersforthefatherless.org/images/logo-navy.png">
<link rel="icon" href="images/mark-navy.png">
{FONTS}
<link rel="stylesheet" href="css/paloma.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{ICONS}
<div class="w">
  <header class="top">
    <a class="mk" href="index.html"><img src="images/mark-navy.png" alt="" width="40" height="40">Fathers for the Fatherless</a>
    <nav aria-label="Main">{nav}</nav>
  </header>
</div>
<main id="main">"""

def foot():
    tax = (" " + html.escape(TAX_STATUS)) if TAX_STATUS else ""
    return f"""</main>
<div class="w">
  <footer class="ft">
    <div>
      <h5>Fathers for the Fatherless</h5>
      <p>Equipping fathers and planting churches in Honduras since 2006.</p>
    </div>
    <div><h5>The work</h5><ul>
      <li><a href="mission.html">The mission</a></li>
      <li><a href="education.html">Education</a></li>
      <li><a href="health-care.html">Health care</a></li>
      <li><a href="dental-care.html">Dental care</a></li>
      <li><a href="mission-trips.html">Mission trips</a></li>
    </ul></div>
    <div><h5>Write to us</h5><ul>
      <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><a href="give.html">Give</a></li>
      <li><a href="contact.html">Contact the ministry</a></li>
      <li><a href="about.html">About us</a></li>
    </ul></div>
    <p class="fine">&copy; {YEAR} Fathers for the Fatherless. A non-profit organization.{tax}</p>
  </footer>
</div>
</body>
</html>"""

def cities_block():
    out = ['<section class="field" id="churches"><div class="w"><p class="kick">Where we work</p>',
           '<h2>Five churches, five men who stay.</h2>',
           '<p class="lede">Each church has its own pastor, living among the people he serves, '
           'and he does not leave.</p><div class="pgrid">']
    for n, c in enumerate(CITIES, 1):
        out.append(f"""<article class="pc">
  <div class="ring"><div class="num">{n}</div><span>Photo needed:<br>{html.escape(c['city'])}</span></div>
  <h4>{html.escape(c['city'])}</h4>
  <p class="who">{html.escape(c['who'])}</p>
  <p class="rg">{html.escape(c['region'])} &middot; since {html.escape(c['since'])}</p>
  <p>{html.escape(c['blurb'])}</p>
</article>""")
    out.append("</div></div></section>")
    return "\n".join(out)

def ask(line, label, href):
    return ('<div class="w"><div class="ask"><p>%s</p>\n<a class="btn" %s>%s</a></div></div>'
            % (html.escape(line), href, html.escape(label)))

def three_cells(items):
    return "".join('<div><div class="disc %s">%s</div><h3>%s</h3><p>%s</p></div>'
                   % (d, ico(i), t, html.escape(b)) for i, d, t, b in items)

def cards(items, link=False):
    if link:
        return "".join('<a class="card" href="%s"><div class="ic">%s</div><h3>%s</h3><p>%s</p></a>'
                       % (h, ico(i, 34, 32), t, html.escape(b)) for h, i, t, b in items)
    return "".join('<div class="card"><div class="ic">%s</div><h3>%s</h3><p>%s</p></div>'
                   % (ico(i, 34, 32), t, html.escape(b)) for i, t, b in items)

def steps(items):
    return "".join('<div class="step"><div class="n">%d</div><h3>%s</h3><p>%s</p></div>'
                   % (n, t, html.escape(b)) for n, (t, b) in enumerate(items, 1))

HOWARD_SHORT = ("Has been training believers for parts of five decades. After laboring faithfully in a "
                "local church for most of that time, he now splits his time between Roanoke, Virginia "
                "and overseeing the whole of the work in Honduras.")

PAGES = {}

# ---------------------------------------------------------------- HOME
PAGES["index.html"] = ("Fathers for the Fatherless",
  "Equipping fathers and planting churches in Honduras since 2006.",
  f"""<div class="w"><div class="hero">
  <div>
    <h1>Fathers who will <span class="hl">stand in the gap</span> for their own homes.</h1>
    <p class="lede">Since 2006 we have worked in Honduras with the men of five churches, teaching them to lead their own families from the Word.</p>
    <div class="acts"><a class="btn" href="give.html">Give to the work</a><a class="btn-o" href="mission-trips.html">Come on a trip</a></div>
  </div>
  <div class="lg"><img src="images/logo-navy.png" alt="Fathers for the Fatherless. This is What Hope Looks Like." width="268" height="365"></div>
</div></div>

<section class="arc"><div class="w">
  <p class="kick">Engage &middot; Equip &middot; Edify</p>
  <div class="three">{three_cells(THREE)}</div>
</div></section>

{cities_block()}

<section class="sec-loose"><div class="w">
  <h2>What the giving pays for.</h2>
  <div class="four">{cards(PROGRAMS, link=True)}</div>
  {photo("a wide shot of the work on the ground")}
</div></section>

<section class="sec"><div class="w">
  <div class="letter">
    <div class="av"><span>Photo needed:<br>H. Finnicum</span></div>
    <div><h4>Howard Finnicum</h4><div class="role">Leads the work</div>
      <p>{C(HOWARD_SHORT)}</p></div>
  </div>
</div></section>

<section class="sec">{ask("For the cost of a few coffee shop visits a month, you can make a difference.", "Give to the work", 'href="give.html"')}</section>""")

# ---------------------------------------------------------------- MISSION
MISSION_THREE = [
    ("dove", "d1", "Engage", "The men behind this work have personally traveled to Honduras, and they go "
     "back every year. We count many of the men there among our dearest friends."),
    ("book", "d2", "Equip", "We equip men, young and old alike, to leave a legacy of faith their children can follow."),
    ("house", "d3", "Edify", "If these men apply the principles of God's Word to their lives, we will not "
     "and cannot forsake them."),
]
PAGES["mission.html"] = ("The mission | Fathers for the Fatherless",
  "To equip, engage and edify the Body of Christ even unto the ends of the world.",
  f"""<div class="w"><div class="hero-plain">
  <p class="kick">The mission</p>
  <h1>To equip, engage, and edify the Body of Christ.</h1>
  <p class="lede">Since 2006 we have been privileged to serve the Lord by ministering to the people of Honduras in Central America. When we arrived, we were grieved to find that centuries of religious influence in the nation had failed to produce faithful men with the training necessary to lead godly homes and inspire righteousness in the churches.</p>
  <p class="lede">It quickly became clear that God was searching for men who would stand in the gap for Him.</p>
</div></div>

<section class="sec"><div class="w">
  <h2>Getting the foundation right.</h2>
  <p class="lede" style="max-width:62ch">Wherever we labor, whether in Central America, the United States, or anywhere else God sends us, we are committed to starting with a strong foundation. That means training fathers how to restore their marriages, love their wives and children, and lead their families in righteousness. It also means training pastors how to be examples to the flock, disciple the fathers in the church, and preach the truths of the Word of God.</p>
  <p class="lede" style="max-width:62ch">This can be a slow process, but we know that any work is only as strong as its foundation. Through the joint effort of church and home, God is raising up a new generation of godly children in the nation of Honduras.</p>
</div></section>

<section class="arc arc-flat" style="margin-top:52px"><div class="w">
  <div class="three">{three_cells(MISSION_THREE)}</div>
</div></section>

<section class="sec"><div class="w">
  {photo("men at a discipleship meeting")}
  <p class="lede" style="margin-top:26px">The work happens in five churches, each with its own pastor. <a href="index.html#churches">See where they are.</a></p>
</div></section>""")

# ---------------------------------------------------------------- EDUCATION
PAGES["education.html"] = ("Education | Fathers for the Fatherless",
  "Verse-by-verse teaching, leadership training and schooling in Honduras.",
  f"""<div class="w"><div class="hero-plain">
  <h1>Putting the Word in a father&rsquo;s hands.</h1>
  <p class="lede">{C("Concise, practical and Gospel-centered teaching, built for real life in the home and the church.")} This part of the work we do ourselves.</p>
</div></div>
<section class="sec-tight"><div class="w">
  <div class="four">{cards([
     ("book", "Biblical discipleship", C("Verse-by-verse teaching that turns Scripture into daily obedience and lasting change.")),
     ("house", "Leadership training", C("Equipping men to lead their families and churches with integrity and courage.")),
     ("tree", "Schooling", "Taught alongside the mission workers, starting with the most important Book of all."),
     ("dove", "Family discipleship", C("Teaching fathers to lead prayer and the Word inside their own homes."))])}</div>
  {photo("a teaching session, men with Bibles open")}
</div></section>
<section class="arc arc-flat" style="margin-top:52px"><div class="w">
  <p class="kick" style="text-align:left">How a father is taught</p>
  <div class="steps">{steps([
     ("Identify", "Find the men who are willing."),
     ("Teach", "Open the Word with them, week after week, for as long as it takes."),
     ("Equip", "Put the tools in their hands."),
     ("Multiply", "They teach the next man. And their own children.")])}</div>
</div></section>""")

# ---------------------------------------------------------------- HEALTH
PAGES["health-care.html"] = ("Health care | Fathers for the Fatherless",
  "Giving that pays for doctor visits and medicine for families in Honduras.",
  f"""<div class="w"><div class="hero-plain">
  <h1>We do not run clinics. We pay the bill.</h1>
  <p class="lede">A family in these communities can know exactly what is wrong and still not be able to do anything about it. Giving is what closes that gap.</p>
  <div class="acts"><a class="btn" href="give.html">Give toward care</a></div>
</div></div>
<section class="arc arc-flat"><div class="w">
  <p class="kick" style="text-align:left">How the money reaches a family</p>
  <div class="steps">{steps([
     ("The pastor knows", "He lives there. He knows who is sick."),
     ("The cost is covered", "Giving pays for the care. It does not pay us to deliver it."),
     ("The family goes", "To a real doctor, at a real clinic."),
     ("The church is there", "The people who helped are the people who worship beside them on Sunday.")])}</div>
</div></section>
<section class="sec"><div class="w">
  <div class="four">{cards([
     ("house", "Seeing a doctor", "The visit itself is out of reach for many families. Giving covers it."),
     ("book", "Medicine", "A prescription is only useful if it can be filled. Giving fills it."),
     ("dove", "Mothers and children", "The people in a household least able to wait for care."),
     ("tree", "Getting there", "Cost and distance both keep people away. We can only remove one of them.")])}</div>
  {photo("a family in one of the five communities")}
</div></section>""")

# ---------------------------------------------------------------- DENTAL
PAGES["dental-care.html"] = ("Dental care | Fathers for the Fatherless",
  "Giving that pays for dental treatment for families in Honduras.",
  f"""<div class="w"><div class="hero-plain">
  <h1>Pain that gets endured because it cannot be paid for.</h1>
  <p class="lede">We do not run a dental clinic. We fund the treatment, so the work gets done instead of put off another year.</p>
</div></div>
<section class="sec-tight"><div class="w">
  <div class="four">{cards([
     ("house", "The appointment", "Giving pays for a dentist to see someone who has been waiting years."),
     ("tree", "Extractions and relief", "Ending the kind of pain that keeps a man up at night and out of work."),
     ("book", "Children&rsquo;s teeth", "Treated early, before a small problem becomes a lifelong one."),
     ("dove", "Help from the church", "The help arrives through the congregation, not from strangers.")])}</div>
</div></section>
<section class="sec"><div class="w">
  <h2>From toothache to treatment.</h2>
  <div class="steps">{steps([
     ("The need is known", "The pastor hears it first."),
     ("The cost is covered", "Giving pays for the treatment."),
     ("The work is done", "By a dentist, properly."),
     ("The pain stops", "Which is the whole point.")])}</div>
  {photo("the community a dental gift reached")}
</div></section>""")

# ---------------------------------------------------------------- TRIPS
PAGES["mission-trips.html"] = ("Go to Honduras | Fathers for the Fatherless",
  "Travel to Honduras to teach, build and work beside the Honduran brothers.",
  f"""<div class="w"><div class="hero-plain">
  <h1>Come and see what God is doing.</h1>
  <p class="lede">A trip is mostly showing up, and staying close to the men who are there the rest of the year.</p>
  <div class="acts"><a class="btn" href="mailto:{EMAIL}?subject={quote('I want to come on a trip to Honduras')}">Write to us about a trip</a></div>
</div></div>
<section class="sec-tight"><div class="w">
  {photo("a team on the ground with the men they came to serve")}
  <div class="four">{cards([
     ("book", "Open the Word", C("Teach and be taught, in homes and in the churches.")),
     ("house", "Serve hands-on", C("Build and repair beside the Honduran brothers.")),
     ("dove", "Build friendships", C("Come home knowing names, and keep writing to them for years.")),
     ("tree", "Stay in touch", "The relationships do not end when the plane leaves.")])}</div>
</div></section>
<section class="arc arc-flat" style="margin-top:52px"><div class="w">
  <p class="kick" style="text-align:left">Getting on a trip</p>
  <div class="steps">{steps([
     ("Write to us", "Email the ministry and say you want to come."),
     ("Pick a field", C("Guaimaca and La Ceiba, Talanga, La Ermita or Danlí.")),
     ("Prepare", C("Dates are approximate and fill quickly, so reach out early.")),
     ("Go", C("Mornings in the Word. Afternoons in the work."))])}</div>
</div></section>""")

# ---------------------------------------------------------------- GIVE
if GIVE["url"]:
    _how = ("Giving is handled securely through %s. Choose an amount above, or give once below."
            % html.escape(GIVE["provider"] or "the ministry's giving page"))
else:
    _how = ("An online giving page is being set up. Until it is ready, write to the ministry and "
            "someone will tell you how to send a gift.")
_tiers = "".join(
    f'<div class="tier"><div class="amt">${a}</div><div class="per">per month</div>'
    f'<h4>{html.escape(t)}</h4><p>{html.escape(b)}</p>'
    f'<p style="margin-top:16px"><a class="btn-o" {give_attrs(a, True)}>Give ${a} a month</a></p></div>'
    for a, t, b in TIERS)
PAGES["give.html"] = ("Give | Fathers for the Fatherless",
  "Support the work of equipping fathers and planting churches in Honduras.",
  f"""<div class="w"><div class="hero-plain">
  <p class="kick">Give</p>
  <h1>Help a father lead his own home.</h1>
  <p class="lede">For the cost of a few coffee shop visits a month, you can make a difference.</p>
</div></div>
<section class="sec-tight"><div class="w">
  <h2>Choose an amount, or send what you can.</h2>
  <div class="tiers">{_tiers}</div>
  <div class="form">
    <h3 style="margin:0 0 8px">How to give today</h3>
    <p class="note">{_how}</p>
    <p class="note">Custom amounts are welcome, and one-time gifts are put to immediate use.</p>
    <a class="btn" {give_attrs(None, False)}>Make a one-time gift</a>
  </div>
</div></section>
<section class="sec"><div class="w">
  <p class="lede" style="max-width:60ch">Not everyone can give every month. Pray for the men being discipled and the families being put back together, and if you can come to Honduras yourself, <a href="mission-trips.html">come</a>.</p>
</div></section>""")

# ---------------------------------------------------------------- UPDATES
PAGES["updates.html"] = ("Updates from the field | Fathers for the Fatherless",
  "Reports from the work in Honduras.",
  f"""<div class="w"><div class="hero-plain">
  <p class="kick">From the field</p><h1>What is happening in Honduras.</h1>
  <p class="lede">Reports from the work, written when there is something to report.</p>
</div></div>
<section class="sec-tight"><div class="w">
  <article class="letter" style="display:block">
    <p class="role">Reported {C("spring 2026")} &middot; La Ceiba</p>
    <h4 style="margin-bottom:12px">The La Ceiba mission house</h4>
    <p>In {C("spring 2026")} the mission house in La Ceiba was in active renovation, being prepared as a permanent base for church planting and discipleship in the region.</p>
    <p>La Ceiba is the eco-tourism capital of Honduras, which makes it a city that matters for the Gospel. Men from the work traveled out to see the progress, meet with the local men being discipled, and plan the next phase of outreach.</p>
  </article>
  {photo("the mission house, renovation in progress")}
  <p class="lede" style="margin-top:26px">Want to know how the house is coming along now? <a href="contact.html">Write to us and ask.</a></p>
</div></section>""")

# ---------------------------------------------------------------- ABOUT
PAGES["about.html"] = ("About | Fathers for the Fatherless",
  "Who does the work, and why it exists.",
  f"""<div class="w"><div class="hero-plain">
  <h1>No board. No staff. Men who show up.</h1>
  <p class="lede">There are no officers and no directors. There is Howard Finnicum, who leads the whole of the work, one pastor in each church, and men who help because they want to.</p>
</div></div>
<section class="sec-tight"><div class="w">
  <div class="letter">
    <div class="av"><span>Photo needed:<br>H. Finnicum</span></div>
    <div><h4>Howard Finnicum</h4><div class="role">Leads the work</div>
      <p>{HOWARD_SHORT} In recent years he has ministered across the nation of Honduras, searching for pastors and fathers who will rise to the challenge of leading the next generation. {C("He has three grown children and 16 grandchildren, and he serves God faithfully with his wife of over thirty years.")}</p></div>
  </div>
  <div class="letter">
    <div class="av"><span>Photo needed:<br>the five pastors</span></div>
    <div><h4>One pastor to each church</h4><div class="role">Guaimaca &middot; La Ceiba &middot; Talanga &middot; La Ermita &middot; Danlí</div>
      <p>Each of the five churches has its own pastor, living in that community and known to the families there. They are the work. <a href="index.html#churches">See where they are.</a></p></div>
  </div>
</div></section>
<section class="sec"><div class="w">
  <p class="lede" style="max-width:60ch">We go back every year, and we measure the work in generations rather than trips. The teaching is the work, not a wrapper around it.</p>
</div></section>""")

# ---------------------------------------------------------------- CONTACT
PAGES["contact.html"] = ("Contact | Fathers for the Fatherless",
  "Write to the ministry about giving, going to Honduras, or praying for the work.",
  f"""<div class="w"><div class="hero-plain">
  <h1>Write to us.</h1>
  <p class="lede">About giving, about coming on a trip, or about praying for the work. A real person reads it.</p>
</div></div>
<section class="sec-tight"><div class="w">
  <form class="form" action="https://formsubmit.co/{EMAIL}" method="POST">
    <input type="hidden" name="_subject" value="Message from the Fathers for the Fatherless website">
    <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
    <label for="name">Your name</label>
    <input id="name" name="name" type="text" required autocomplete="name">
    <label for="email">Your email</label>
    <input id="email" name="email" type="email" required autocomplete="email">
    <label for="msg">Message</label>
    <textarea id="msg" name="message" required></textarea>
    <p class="note">Your name, email and message go to the ministry's own inbox and are not used for anything else.</p>
    <button class="btn" type="submit" style="border:0;cursor:pointer">Send it</button>
  </form>
  <p class="lede" style="margin-top:24px">Or write directly to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>""")


# ---------------------------------------------------------------- GUARDS
BRITISH = r"\b(organisation|organise|centred|centre|travelled|travelling|labour|labouring|laboured|programme|fulfil|colour|honour|favour|neighbour|realise|recognise|apologise)\b"
FORBIDDEN = [
    (r"Joe Young|J\. Young|Chief Operating", "Joe asked to come off the site (25 Sep)"),
    (r"Hyatt|Shirkey|Chief [Cc]oun", "Hyatt Browning Shirkey is off this build entirely (25 Sep)"),
    (r"directors and officers|[Dd]irectors have", "the ministry has no officers or directors"),
    (r"[Mm]obile clinic|We treat|assess and treat|whoever comes through the door|With what we carried",
     "health and dental are funded, not delivered"),
    (r"—|&mdash;", "em-dash"),
    (r"vercel\.live|_vercel/insights|feedback\.js", "Vercel's injected script captured into the source"),
    (r"100% of|Secure Giving|[Cc]ancel anytime|400\+|12 Churches|Within 48", "unverified money/impact claim"),
    (r"How it goes", "category heading that repeated on four pages"),
    (r">\s*Photograph\b", "unlabelled photo slot"),
    (r"premierdetailing|youngseo", "agency address on a client surface"),
]

def skeleton(s):
    body = s.split('<main id="main">', 1)[1]
    return " ".join(re.findall(r"<(section|h1|h2|div class=\"(?:hero|hero-plain|four|steps|tiers|three|letter|form|ph|ask|pgrid)\")", body))

def guards(out):
    bad = []
    for page, s in out.items():
        text = re.sub(r"<[^>]+>", " ", s)
        for m in re.finditer(BRITISH, text, re.I):
            bad.append("%s: British spelling %r" % (page, m.group(0)))
        for pat, why in FORBIDDEN:
            if re.search(pat, s):
                bad.append("%s: %s (/%s/)" % (page, why, pat))
        if len(re.findall(r"<h1[ >]", s)) != 1:
            bad.append("%s: needs exactly one h1" % page)
        for href in re.findall(r'href="([a-z\-]+\.html)', s):
            if href not in out:
                bad.append("%s: broken internal link %s" % (page, href))
        if "There are no officers" in s and page != "about.html":
            bad.append("%s: structure line belongs on About only" % page)
    sk = {}
    for page, s in out.items():
        sk.setdefault(skeleton(s), []).append(page)
    for k, pages in sk.items():
        if len(pages) > 1:
            bad.append("identical page skeletons: %s" % ", ".join(pages))
    asks = [p for p, s in out.items() if 'class="ask"' in s]
    if len(asks) > 1:
        bad.append("closing CTA band on more than one page: %s" % asks)
    gtw = sum(s.count("Give to the work") for s in out.values())
    if gtw > 5:
        bad.append('"Give to the work" appears %d times (cap 5)' % gtw)
    if not GIVE["url"] and sum(s.count("mailto:%s?subject=I%%20want%%20to%%20give" % EMAIL) for s in out.values()) < 5:
        bad.append("give switch: expected every give control to fall back to mailto")
    if bad:
        raise SystemExit("BUILD REFUSED:\n  " + "\n  ".join(bad))
    return gtw


def build():
    out = {page: head(t, d, page) + "\n" + b + "\n" + foot() for page, (t, d, b) in PAGES.items()}
    gtw = guards(out)          # refuses before anything is written
    for page, s in out.items():
        open(os.path.join(ROOT, page), "w", encoding="utf-8").write(s)

    base = "https://fathersforthefatherless.org/"
    today = datetime.date.today().isoformat()
    urls = "".join("\n  <url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>"
                   % (base, "" if p == "index.html" else p, today,
                      "1.0" if p == "index.html" else "0.8") for p in PAGES)
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s\n</urlset>\n' % urls)
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
        "User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % base)

    seen, rows = set(), []
    for text, note in CLAIMS:
        if text in seen:
            continue
        seen.add(text)
        rows.append("| [ ] | %s | %s |" % (text.replace("|", "/"), note))
    open(os.path.join(ROOT, "CONFIRM-SHEET.md"), "w", encoding="utf-8").write(
        CONFIRM_TEMPLATE % (today, len(rows), "\n".join(rows)))

    print("built %d pages, sitemap (%d urls), robots.txt" % (len(PAGES), len(PAGES)))
    print("guards: pass  |  'Give to the work' x%d  |  give switch: %s  |  tax status: %s"
          % (gtw, "LIVE -> " + GIVE["url"] if GIVE["url"] else "email fallback",
             "set" if TAX_STATUS else "empty (renders nothing)"))
    print("CONFIRM-SHEET.md: %d unconfirmed claims" % len(rows))


CONFIRM_TEMPLATE = """# Confirm sheet - Fathers for the Fatherless

**Generated %s by `_build/site.py`. %d items.**

Each line below is on the new site and **has not been confirmed in writing by anyone
at the ministry.** Tick it or cross it out, one line at a time.

**This site does not replace the current one until this sheet comes back.**

Already settled with Joe (25 Sep) and not on this list: the ministry has no officers
or directors; health and dental care are paid for, not delivered, by the ministry;
the ministry does its own teaching; the four giving amounts and their labels.

| OK? | Claim | Note |
|---|---|---|
%s

## Deliberately NOT on the new site

Each of these was on an older version and stays off until the ministry says otherwise.

- "100%% of your gift goes directly to the field" / "No overhead bureaucracy"
- "400+ Fathers Discipled" and "12 Churches Planted"
- "500+ Patients treated" (dental) and "1,000+ Patients seen" (health)
- "Secure & Flexible" and "Cancel anytime", while no payment processor exists
- "We Respond Within 48 Hours"
- "Each location is led by a Honduran brother" (not all five are Honduran)
- "We don't send tourists. We send disciples" (a quotation with nobody to attribute it to)
- The four named outcome stories that were on the education page
- Any tax-deductible or 501(c)(3) wording

## Still needed from the ministry

- Who owns `fathersforthefatherless.org`: registrar, login, renewal date. **The switch-over is blocked on this.**
- A giving processor (Givelify, Donorbox, PayPal Giving, Tithe.ly...), or a decision to stay on email. One link and it is live.
- The 501(c)(3) determination letter, if gifts are to be described as tax-deductible.
- A mailing address and a phone number. Several states expect an address on a request for donations.
- Real photographs. Every slot on the site is labelled with the picture it is waiting for.
- The logo as a vector file (.ai / .eps / .svg).
- Is Jimmy Welch addressed as "Bro." like the other four pastors?
"""

if __name__ == "__main__":
    build()
