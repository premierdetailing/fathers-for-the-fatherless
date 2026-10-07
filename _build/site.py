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

def give_href(amount=None, monthly=True, purpose=None):
    """Every give control on every page routes through here."""
    if not GIVE["url"]:
        if purpose:
            subj = "I want to give toward %s" % purpose
        elif amount:
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

def give_attrs(amount=None, monthly=True, purpose=None):
    h = html.escape(give_href(amount, monthly, purpose))
    return 'href="%s"%s' % (h, ' target="_blank" rel="noopener"' if GIVE["url"] else "")

CLAIMS = []
def C(text, note=""):
    CLAIMS.append((text if len(text) < 150 else text[:147] + "...", note))
    return text

def photo(what):
    return '<div class="ph"><i>Photo needed: %s</i></div>' % html.escape(what)

# ---- real media, sent by Joe 6 Oct 2026. Metadata stripped (no GPS, no device, no date).
# Every photo ships as AVIF + WebP + JPEG at two widths; the browser takes the smallest it can use.
# The children are never named on the site, and no picture is tied to a name.
def pic(base, widths, sizes, alt, w, h, eager=False):
    srcset = lambda ext: ", ".join("%s-%d.%s %dw" % (base, x, ext, x) for x in widths)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return ('<picture><source type="image/avif" srcset="%s" sizes="%s">'
            '<source type="image/webp" srcset="%s" sizes="%s">'
            '<img src="%s-%d.jpg" srcset="%s" sizes="%s" alt="%s" width="%d" height="%d" %s decoding="async"></picture>'
            % (srcset("avif"), sizes, srcset("webp"), sizes, base, widths[0], srcset("jpg"), sizes,
               html.escape(alt), w, h, load))

SCHOOL = ["images/field/school-%02d" % i for i in range(1, 11)]
KID_ALT = "A student at the school in La Ceiba"

def kid_row(n):
    imgs = "".join(pic(s_, (320, 560), "(max-width:820px) 33vw, 170px", KID_ALT, 320, 500) for s_ in SCHOOL[:n])
    return ('<figure class="kids kids-row">%s<figcaption><a href="education.html">Students at the school '
            'in La Ceiba.</a></figcaption></figure>' % imgs)

def school_grid():
    imgs = "".join(pic(s_, (320, 560), "(max-width:820px) 50vw, 190px", KID_ALT, 320, 500) for s_ in SCHOOL)
    return '<figure class="kids">%s<figcaption>Students at the school in La Ceiba.</figcaption></figure>' % imgs

def logo_pic():
    return ('<img src="images/logo-navy-268.png" srcset="images/logo-navy-268.png 1x, images/logo-navy-520.png 2x" '
            'alt="Fathers for the Fatherless. This is What Hope Looks Like." width="268" height="295" fetchpriority="high">')

def church_video():
    return ('<figure class="vid"><video controls playsinline preload="none" '
            'poster="images/field/church-service-poster-540.webp" width="540" height="960">'
            '<source src="images/field/church-service.mp4" type="video/mp4"></video></figure>')

def tabernacle_img():
    return ('<figure class="wide">%s</figure>'
            % pic("images/field/tabernacle", (720, 1320), "(max-width:1050px) 100vw, 1000px",
                  "The tabernacle under construction: block walls up, no roof yet", 1320, 714))

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
         'family=Archivo:wght@600;700;800&family=Newsreader:opsz,wght@'
         '6..72,400;6..72,500&display=swap">')

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
<meta property="og:image" content="https://fathersforthefatherless.org/images/logo-navy-520.png">
<link rel="icon" href="images/mark-navy-80.png">
{FONTS}
<link rel="stylesheet" href="css/paloma.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{ICONS}
<div class="w">
  <header class="top">
    <a class="mk" href="index.html"><img src="images/mark-navy-80.png" alt="" width="40" height="40">Fathers for the Fatherless</a>
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
# 6 Oct, Joe: kids on the front page, fewer headings, fewer words, keep it simple.
# Then: "the pictures of the kids at the top is a little awkwardly placed" -> three options for the
# top of the page only, the rest of the site unchanged. FFTF_HOME picks one: a / b / c.
# "now" (the default) is the version Joe called great, so nothing changes until he picks.
HOME = os.environ.get("FFTF_HOME", "now")

_HERO_TEXT = """<div>
    <h1>Fathers who will <span class="hl">stand in the gap</span> for their own homes.</h1>
    <p class="lede">Since 2006 we have been teaching the men of five Honduran churches to lead their families from the Word.</p>
    <div class="acts"><a class="btn" href="give.html">Give to the work</a><a class="btn-o" href="mission-trips.html">Come on a trip</a></div>
  </div>"""

_CHURCH_LIST = '<ul class="churches">%s</ul>' % "".join(
    '<li><b>%s</b><span>%s, since %s</span></li>' % (html.escape(c['city']), html.escape(c['who']), html.escape(c['since']))
    for c in CITIES)

def _talanga_fig():
    return ('<figure class="tall">%s<figcaption>Talanga.</figcaption></figure>'
            % pic("images/field/outside", (560, 1000), "(max-width:820px) 100vw, 400px",
                  "Children outside the church in Talanga", 1000, 1289))

def _classroom_pic(sizes):
    return pic("images/field/classroom", (720, 1320), sizes, "Students working at their desks in a classroom", 1320, 964)

def _kids_lower(n=6):
    imgs = "".join(pic(s_, (320, 560), "(max-width:820px) 33vw, 130px", KID_ALT, 320, 500) for s_ in SCHOOL[:n])
    return ('<section class="sec-loose"><div class="w"><figure class="kids kids-row kids-low">%s'
            '<figcaption><a href="education.html">Some of the students at the school in La Ceiba.</a></figcaption>'
            '</figure></div></section>' % imgs)

_CHURCHES_WITH_TALANGA = f"""<section class="sec-loose"><div class="w"><div class="split split-r">
  <div>
    <h2>Five churches, five men who stay.</h2>
    {_CHURCH_LIST}
  </div>
  {_talanga_fig()}
</div></div></section>"""

_VIDEO_SECTION = f"""<section class="sec-loose"><div class="w"><div class="split">
  {church_video()}
  <div>
    <p class="lede">The children leading the singing at a service.</p>
    <p class="lede">Giving pays for the teaching, and for doctor and dentist visits that families there cannot afford. <a href="mission.html">Read the mission.</a></p>
  </div>
</div></div></section>"""

_TABERNACLE_SECTION = f"""<section class="sec-loose"><div class="w">
  {tabernacle_img()}
  <p class="lede" style="margin-top:18px">The tabernacle walls are up. It still needs a roof. <a href="give.html#tabernacle">Help finish it.</a></p>
</div></section>"""

_ASK = '<section class="sec">%s</section>' % ask(
    "For the cost of a few coffee shop visits a month, you can make a difference.", "Give to the work", 'href="give.html"')

if HOME == "a":
    # A. The classroom photo takes the logo's place in the opening. Headshots move below the churches, smaller.
    _home = f"""<div class="w"><div class="hero hero-photo">
  {_HERO_TEXT}
  <figure class="hero-img">{_classroom_pic("(max-width:820px) 100vw, 480px")}<figcaption>In class.</figcaption></figure>
</div></div>
{_CHURCHES_WITH_TALANGA}
{_kids_lower(6)}
{_VIDEO_SECTION}
{_TABERNACLE_SECTION}
{_ASK}"""
elif HOME == "b":
    # B. The children singing take the logo's place in the opening. Tap to hear them. Headshots lower.
    _home = f"""<div class="w"><div class="hero hero-vid">
  {_HERO_TEXT}
  <div class="hero-v">{church_video()}<p class="cap-v">The children leading the singing at a service.</p></div>
</div></div>
{_CHURCHES_WITH_TALANGA}
{_kids_lower(6)}
<section class="sec-loose"><div class="w">
  <figure class="wide">{_classroom_pic("(max-width:1050px) 100vw, 1000px")}<figcaption>In class.</figcaption></figure>
</div></section>
{_TABERNACLE_SECTION}
{_ASK}"""
elif HOME == "c":
    # C. The opening stays as it is (logo). Under it, three real scenes at their own shapes.
    # The headshots live on the Education page only.
    _strip = (
        '<figure class="candid">'
        f'<div>{_classroom_pic("(max-width:820px) 100vw, 360px")}<figcaption>In class.</figcaption></div>'
        f'<div>{pic("images/field/outside", (560, 1000), "(max-width:820px) 100vw, 210px", "Children outside the church in Talanga", 1000, 1289)}<figcaption>Talanga.</figcaption></div>'
        f'<div>{pic("images/field/tabernacle", (720, 1320), "(max-width:820px) 100vw, 480px", "The tabernacle under construction: block walls up, no roof yet", 1320, 714)}'
        '<figcaption>The tabernacle. It still needs a roof. <a href="give.html#tabernacle">Help finish it.</a></figcaption></div>'
        '</figure>')
    _home = f"""<div class="w"><div class="hero">
  {_HERO_TEXT}
  <div class="lg">{logo_pic()}</div>
</div></div>
<section class="sec-tight"><div class="w">{_strip}</div></section>
<section class="sec-loose"><div class="w narrow">
  <h2>Five churches, five men who stay.</h2>
  {_CHURCH_LIST}
  <p class="lede" style="margin-top:22px">The students at the school in La Ceiba are on the <a href="education.html">education page</a>.</p>
</div></section>
{_VIDEO_SECTION}
{_ASK}"""
else:
    _home = f"""<div class="w"><div class="hero">
  {_HERO_TEXT}
  <div class="lg">{logo_pic()}</div>
</div></div>

<section class="sec-tight"><div class="w">
  {kid_row(6)}
</div></section>

{_CHURCHES_WITH_TALANGA}
{_VIDEO_SECTION}
{_TABERNACLE_SECTION}
{_ASK}"""

PAGES["index.html"] = ("Fathers for the Fatherless",
  "Equipping fathers and planting churches in Honduras since 2006.", _home)

# ---------------------------------------------------------------- MISSION
PAGES["mission.html"] = ("The mission | Fathers for the Fatherless",
  "To equip, engage and edify the Body of Christ even unto the ends of the world.",
  f"""<div class="w"><div class="hero-plain">
  <p class="kick">The mission</p>
  <h1>To equip, engage, and edify the Body of Christ.</h1>
  <p class="lede">Since 2006 we have been privileged to serve the Lord by ministering to the people of Honduras. When we arrived, we were grieved to find that centuries of religious influence had failed to produce faithful men with the training to lead godly homes. It quickly became clear that God was searching for men who would stand in the gap for Him.</p>
</div></div>

<section class="arc arc-flat"><div class="w">
  <div class="three">{three_cells(THREE)}</div>
</div></section>

<section class="sec"><div class="w narrow">
  <p class="lede">We start with the foundation: training fathers to restore their marriages, love their wives and children, and lead their families in righteousness, and training pastors to disciple the fathers in their churches.</p>
  <p class="lede">It is slow work, and any work is only as strong as its foundation. <a href="index.html">See the five churches.</a></p>
</div></section>""")

# ---------------------------------------------------------------- EDUCATION
PAGES["education.html"] = ("Education | Fathers for the Fatherless",
  "Verse-by-verse teaching, leadership training and schooling in Honduras.",
  f"""<div class="w"><div class="hero-plain">
  <h1>Putting the Word in a father&rsquo;s hands.</h1>
  <p class="lede">This part of the work we do ourselves.</p>
</div></div>
<section class="sec-tight"><div class="w">
  <ul class="plain">
    <li><b>Discipleship.</b> {C("Verse-by-verse teaching that turns Scripture into daily obedience.")}</li>
    <li><b>Leadership.</b> {C("Equipping men to lead their families and churches.")}</li>
    <li><b>Schooling.</b> Taught alongside the mission workers, starting with the most important Book of all.</li>
    <li><b>At home.</b> {C("Teaching fathers to lead prayer and the Word inside their own homes.")}</li>
  </ul>
  <figure class="wide">{pic("images/field/classroom", (720, 1320), "(max-width:1050px) 100vw, 1000px", "Students working at their desks in a classroom", 1320, 964)}<figcaption>In class.</figcaption></figure>
  {school_grid()}
</div></section>""")

# ---------------------------------------------------------------- HEALTH
PAGES["health-care.html"] = ("Health care | Fathers for the Fatherless",
  "Giving that pays for doctor visits and medicine for families in Honduras.",
  f"""<div class="w"><div class="hero-plain">
  <h1>We do not run clinics. We pay the bill.</h1>
  <p class="lede">A family can know exactly what is wrong and still not be able to do anything about it. Giving closes that gap.</p>
</div></div>
<section class="sec-tight"><div class="w narrow">
  <ul class="plain">
    <li><b>The pastor knows</b> who is sick. He lives there.</li>
    <li><b>Giving covers</b> the doctor visit and the prescription.</li>
    <li><b>The family goes</b> to a real doctor, at a real clinic.</li>
  </ul>
  <p class="lede">Giving pays for the care. It does not pay us to deliver it.</p>
  <div class="acts"><a class="btn" href="give.html">Give toward care</a></div>
</div></section>""")

# ---------------------------------------------------------------- DENTAL
PAGES["dental-care.html"] = ("Dental care | Fathers for the Fatherless",
  "Giving that pays for dental treatment for families in Honduras.",
  f"""<div class="w"><div class="hero-plain">
  <h1>Pain that gets endured because it cannot be paid for.</h1>
</div></div>
<section class="sec-tight"><div class="w narrow">
  <p class="lede">We do not run a dental clinic. When the pastor hears about a tooth that has hurt for a year, giving pays a dentist to treat it, properly. Children get seen early, before a small problem becomes a lifelong one.</p>
  <p class="lede"><a href="give.html">Give toward it.</a></p>
</div></section>""")

# ---------------------------------------------------------------- TRIPS
PAGES["mission-trips.html"] = ("Go to Honduras | Fathers for the Fatherless",
  "Travel to Honduras to teach, build and work beside the Honduran brothers.",
  f"""<div class="w"><div class="hero-plain">
  <h1>Come and see what God is doing.</h1>
  <p class="lede">A trip is mostly showing up, and staying close to the men who are there the rest of the year. {C("Mornings in the Word. Afternoons in the work.")}</p>
</div></div>
<section class="sec-tight"><div class="w narrow">
  <ol class="plain">
    <li><b>Write to us</b> and say you want to come.</li>
    <li><b>Pick a field:</b> {C("Guaimaca, La Ceiba, Talanga, La Ermita or Danlí.")}</li>
    <li><b>Reach out early.</b> {C("Dates are approximate and fill quickly.")}</li>
  </ol>
  <div class="acts"><a class="btn" href="mailto:{EMAIL}?subject={quote('I want to come on a trip to Honduras')}">Write to us about a trip</a></div>
</div></section>""")

# ---------------------------------------------------------------- GIVE
if GIVE["url"]:
    _how = ("Giving is handled securely through %s." % html.escape(GIVE["provider"] or "the ministry's giving page"))
else:
    _how = ("An online giving page is being set up. Until then, any button here opens an email to the ministry, "
            "and someone will tell you how to send the gift.")
_tiers = "".join(
    f'<div class="tier"><div class="amt">${a}</div><div class="per">per month</div>'
    f'<h4>{html.escape(t)}</h4>'
    f'<p style="margin-top:14px"><a class="btn-o" {give_attrs(a, True)}>Give ${a} a month</a></p></div>'
    for a, t, b in TIERS)
PAGES["give.html"] = ("Give | Fathers for the Fatherless",
  "Support the work of equipping fathers and planting churches in Honduras.",
  f"""<div class="w"><div class="hero-plain">
  <h1>Help a father lead his own home.</h1>
  <p class="lede">For the cost of a few coffee shop visits a month, you can make a difference.</p>
</div></div>
<section class="sec-tight"><div class="w">
  <div class="tiers">{_tiers}</div>
  <p class="lede" style="margin-top:24px">{_how} Any amount is welcome. <a {give_attrs(None, False)}>Give once.</a></p>
</div></section>
<section class="sec-loose" id="tabernacle"><div class="w">
  <h2>The tabernacle still needs a roof.</h2>
  {tabernacle_img()}
  <p class="lede" style="margin-top:18px">The walls are up. Finishing it takes money the church does not have, and {C("a gift marked for it goes to the building", "restricted-gift promise: confirm the ministry tracks gifts marked for the tabernacle")}.</p>
  <div class="acts"><a class="btn-o" {give_attrs(None, False, "the tabernacle")}>Give toward the tabernacle</a></div>
</div></section>""")

# ---------------------------------------------------------------- UPDATES
PAGES["updates.html"] = ("Updates from the field | Fathers for the Fatherless",
  "Reports from the work in Honduras.",
  f"""<div class="w"><div class="hero-plain">
  <p class="kick">From the field</p><h1>What is happening in Honduras.</h1>
</div></div>
<section class="sec-tight"><div class="w narrow">
  <article class="letter" style="display:block;margin-top:0">
    <p class="role">October 2026</p>
    <h4 style="margin-bottom:12px">The tabernacle</h4>
    <p>The walls are up. It still needs a roof and the rest of the work to finish it. <a href="give.html#tabernacle">Give toward it.</a></p>
  </article>
  <article class="letter" style="display:block">
    <p class="role">{C("Spring 2026")} &middot; La Ceiba</p>
    <h4 style="margin-bottom:12px">The mission house</h4>
    <p>The mission house in La Ceiba was being renovated as a permanent base for church planting and discipleship in the region. Men from the work traveled out to see the progress and meet the local men being discipled. <a href="contact.html">Ask us how it is coming along.</a></p>
  </article>
</div></section>""")

# ---------------------------------------------------------------- ABOUT
PAGES["about.html"] = ("About | Fathers for the Fatherless",
  "Who does the work, and why it exists.",
  f"""<div class="w"><div class="hero-plain">
  <h1>No board. No staff. Men who show up.</h1>
  <p class="lede">There are no officers and no directors. There is Howard Finnicum, who leads the whole of the work, one pastor in each church, and men who help because they want to.</p>
</div></div>
<section class="sec-tight"><div class="w narrow">
  <figure class="couple">{pic("images/field/couple", (400, 800), "(max-width:820px) 100vw, 360px", "Howard and Patricia Finnicum", 800, 788)}<figcaption>Bro. and Sis. Finnicum, Howard and Patricia.</figcaption></figure>
  <div class="letter" style="display:block">
    <h4>Howard Finnicum</h4><div class="role">Leads the work</div>
    <p>{HOWARD_SHORT} {C("He has three grown children and 16 grandchildren, and he serves God faithfully with Patricia, his wife of over thirty years.")}</p>
  </div>
  <p class="lede" style="margin-top:28px">Each of the five churches has its own pastor, living in that community and known to the families there. They are the work. We go back every year.</p>
</div></section>""")

# ---------------------------------------------------------------- CONTACT
PAGES["contact.html"] = ("Contact | Fathers for the Fatherless",
  "Write to the ministry about giving, going to Honduras, or praying for the work.",
  f"""<div class="w"><div class="hero-plain">
  <h1>Write to us.</h1>
  <p class="lede">About giving, a trip, or prayer. A real person reads it.</p>
</div></div>
<section class="sec-tight"><div class="w narrow">
  <form class="form" action="https://formsubmit.co/{EMAIL}" method="POST">
    <input type="hidden" name="_subject" value="Message from the Fathers for the Fatherless website">
    <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
    <label for="name">Your name</label>
    <input id="name" name="name" type="text" required autocomplete="name">
    <label for="email">Your email</label>
    <input id="email" name="email" type="email" required autocomplete="email">
    <label for="msg">Message</label>
    <textarea id="msg" name="message" required></textarea>
    <button class="btn" type="submit" style="border:0;cursor:pointer">Send it</button>
  </form>
  <p class="lede" style="margin-top:24px">Or write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
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
    return " ".join(re.findall(r"<(section|h1|h2|ul|ol|figure|article|form|div class=\"(?:hero|hero-plain|four|steps|tiers|three|letter|form|ph|ask|pgrid)\")", body))

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
