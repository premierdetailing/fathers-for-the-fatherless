#!/usr/bin/env python3
"""
Fathers for the Fatherless — page builder (PALOMA).

The files it writes ARE the website; this just stops ten pages from drifting
apart. Run from the repo root:   python3 _build/site.py

Every claim nobody at the ministry has confirmed goes through C(). The build
writes CONFIRM-SHEET.md listing all of them. Nothing here is invented: each
C() string came off the previous build and is reproduced so the ministry can
tick it or kill it, not so it can quietly ship again.
"""
import os, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = "fathers4thefatherless@gmail.com"
YEAR = datetime.date.today().year

CLAIMS = []
def C(text, note=""):
    CLAIMS.append((text if len(text) < 150 else text[:147] + "...", note))
    return text

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
         since=C("2014"), blurb=C("Active church planting and leadership training. Pastors equipped to "
                 "disciple the fathers in their congregations.")),
    dict(city="La Ermita", region=C("Western Honduras"), who=C("Bro. Cristobal Alvarado"),
         since=C("2018"), blurb=C("A community where the Word is taking root. Families hearing "
                 "Gospel-centred teaching, many of them for the first time.")),
    dict(city="Danli", region="El Paraiso, eastern Honduras", who=C("Jimmy Welch"),
         since=C("2016"), blurb=C("Families are being reached. Marriages restored through the "
                 "principles of Scripture.")),
]

THREE = [
    ("dove", "d1", "Engage",
     "Our commitment goes beyond financial support or long-distance assistance. A majority of our "
     "directors and officers have personally travelled to Honduras, with trips every year. We count "
     "many of them among our dearest friends."),
    ("book", "d2", "Equip",
     "We equip men, young and old alike, to accept and fulfill the calling of leadership God has "
     "placed upon their lives, and to leave a legacy of faith their children can follow."),
    ("house", "d3", "Edify",
     "The work will not be finished in a day, or in one short-term missions trip. If these men apply "
     "the principles of God's Word to their lives, we will not and cannot forsake them."),
]

PROGRAMS = [
    ("education.html", "book", "Education",
     C("Verse-by-verse teaching, leadership training, literacy, and teaching fathers to lead worship "
       "and the Word inside their own homes.")),
    ("mission-trips.html", "dove", "Mission trips",
     "Teams travel to Honduras to teach, build, and work beside the Honduran brothers who are there "
     "the rest of the year."),
    ("health-care.html", "house", "Health care",
     C("Checkups and diagnosis, essential medicine, maternal and child care, and mobile clinics that "
       "reach villages the roads forget.")),
    ("dental-care.html", "tree", "Dental care",
     C("Cleanings, extractions and pain relief, and simple oral-health teaching so families can care "
       "for themselves.")),
]

TIERS = [
    ("$25", C("Discipleship materials"), C("Covers discipleship materials for one father for a full month of training.")),
    ("$50", C("Pastoral training"), C("Supports one pastor's leadership training and equipping programme.")),
    ("$100", C("Church planting"), C("Helps plant and sustain a Gospel-centred church in Honduras.")),
    ("$250", C("Mission outreach trip"), C("Funds a full mission outreach trip: travel, materials, field presence.")),
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
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta name="theme-color" content="#0E2243">
<link rel="canonical" href="https://fathersforthefatherless.org/%s">
<meta property="og:type" content="website">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:image" content="https://fathersforthefatherless.org/images/logo-navy.png">
<link rel="icon" href="images/mark-navy.png">
%s
<link rel="stylesheet" href="css/paloma.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
%s
<div class="w">
  <header class="top">
    <a class="mk" href="index.html"><img src="images/mark-navy.png" alt="" width="40" height="40">Fathers for the Fatherless</a>
    <nav aria-label="Main">%s</nav>
  </header>
</div>
<main id="main">""" % (html.escape(title), html.escape(desc), page, html.escape(title),
                       html.escape(desc), FONTS, ICONS, nav)

FOOT = """</main>
<div class="w">
  <footer class="ft">
    <div>
      <h5>Fathers for the Fatherless</h5>
      <p>Equipping fathers, planting churches and restoring families in Honduras since 2006.</p>
    </div>
    <div><h5>The work</h5><ul>
      <li><a href="mission.html">The mission</a></li>
      <li><a href="education.html">Education</a></li>
      <li><a href="health-care.html">Health care</a></li>
      <li><a href="dental-care.html">Dental care</a></li>
      <li><a href="mission-trips.html">Mission trips</a></li>
    </ul></div>
    <div><h5>Write to us</h5><ul>
      <li><a href="mailto:%s">%s</a></li>
      <li><a href="give.html">Give to the work</a></li>
      <li><a href="contact.html">Contact the ministry</a></li>
      <li><a href="about.html">About us</a></li>
    </ul></div>
    <p class="fine">&copy; %d Fathers for the Fatherless. A non-profit organisation.</p>
  </footer>
</div>
</body>
</html>""" % (EMAIL, EMAIL, YEAR)

def cities_block():
    out = ['<section class="field"><div class="w"><p class="kick">Where we work</p>',
           '<h2>Five cities, five men who stay.</h2>',
           '<p class="lede">Each location is led by a brother who lives among the people, '
           'knows their names, and does not leave.</p><div class="pgrid">']
    for n, c in enumerate(CITIES, 1):
        out.append("""<article class="pc">
  <div class="ring"><div class="num">%d</div><span>Photograph<br>%s</span></div>
  <h4>%s</h4>
  <p class="who">%s</p>
  <p class="rg">%s &middot; since %s</p>
  <p>%s</p>
</article>""" % (n, html.escape(c['city']), html.escape(c['city']), html.escape(c['who']),
                 html.escape(c['region']), html.escape(c['since']), html.escape(c['blurb'])))
    out.append("</div></div></section>")
    return "\n".join(out)

def ask(line="For the cost of a few coffee shop visits a month, you can make a difference.",
        label="Give to the work"):
    return ('<div class="w"><div class="ask"><p>%s</p>\n<a class="btn" href="give.html">%s</a></div></div>'
            % (html.escape(line), html.escape(label)))

def three_block(kick, align_left=False):
    style = ' style="text-align:left"' if align_left else ''
    cells = "".join('<div><div class="disc %s">%s</div><h3>%s</h3><p>%s</p></div>'
                    % (d, ico(i), t, html.escape(b)) for i, d, t, b in THREE)
    return '<p class="kick"%s>%s</p>\n<div class="three">%s</div>' % (style, kick, cells)

PAGES = {}

PAGES["index.html"] = ("Fathers for the Fatherless",
  "Equipping fathers, planting churches and restoring families in Honduras since 2006.",
  """<div class="w"><div class="hero">
  <div>
    <h1>Fathers who will <span class="hl">stand in the gap</span> for their own homes.</h1>
    <p class="lede">Since 2006, in Honduras. We equip men to accept the calling of leadership God has placed on their lives.</p>
    <div class="acts"><a class="btn" href="give.html">Give to the work</a><a class="btn-o" href="mission-trips.html">Come on a trip</a></div>
  </div>
  <div class="lg"><img src="images/logo-navy.png" alt="Fathers for the Fatherless. This is What Hope Looks Like." width="268" height="365"></div>
</div></div>

<section class="arc"><div class="w">%s</div></section>

%s

<section class="sec-loose"><div class="w">
  <p class="kick">What the work looks like</p>
  <h2>Four ways the work goes on.</h2>
  <div class="four">%s</div>
  <div class="ph"><i>Photograph &mdash; wide &mdash; the work on the ground</i></div>
</div></section>

<section class="sec"><div class="w">
  <div class="letter">
    <div class="av"><span>Portrait<br>H. Finnicum</span></div>
    <div><h4>Howard Finnicum</h4><div class="role">President</div>
      <p>Has been training believers for parts of five decades. After labouring faithfully in a local church for most of that time, he now splits his time between Roanoke, Virginia and serving as the main overseer of the work in Honduras.</p></div>
  </div>
</div></section>

<section class="sec">%s</section>""" % (
    three_block("Engage &middot; Equip &middot; Edify"),
    cities_block(),
    "".join('<a class="card" href="%s"><div class="ic">%s</div><h3>%s</h3><p>%s</p></a>'
            % (h, ico(i, 34, 32), t, html.escape(b)) for h, i, t, b in PROGRAMS),
    ask()))

PAGES["mission.html"] = ("The mission | Fathers for the Fatherless",
  "To equip, engage and edify the Body of Christ even unto the ends of the world.",
  """<div class="w"><div class="hero-plain">
  <p class="kick">The mission</p>
  <h1>To equip, engage, and edify the Body of Christ.</h1>
  <p class="lede">Since 2006 we have been privileged to serve the Lord by ministering to the people of Honduras in Central America. When we arrived, we were grieved to find that centuries of religious influence in the nation had failed to produce faithful men with the training necessary to lead godly homes and inspire righteousness in the churches.</p>
  <p class="lede">It quickly became clear that God was searching for men who would stand in the gap for Him.</p>
</div></div>

<section class="arc arc-flat"><div class="w">%s</div></section>

<section class="sec-loose"><div class="w">
  <h2>Getting the foundation right.</h2>
  <p class="lede" style="max-width:62ch">Wherever we labour, whether in Central America, the United States, or anywhere else God sends us, we are committed to starting with a strong foundation. That means training fathers how to restore their marriages, love their wives and children, and lead their families in righteousness. It also means training pastors how to be examples to the flock, disciple the fathers in the church, and preach the truths of the Word of God.</p>
  <p class="lede" style="max-width:62ch">This can be a slow process, but we know that any work is only as strong as its foundation. Through the joint effort of church and home, God is raising up a new generation of godly children in the nation of Honduras.</p>
  <div class="ph"><i>Photograph &mdash; men at a discipleship meeting</i></div>
</div></section>

%s

<section class="sec">%s</section>""" % (three_block("Three parts, one mission", True), cities_block(), ask()))

def programme(kick, h1, lede, items, steps, photo):
    cards = "".join('<div class="card"><div class="ic">%s</div><h3>%s</h3><p>%s</p></div>'
                    % (ico(i, 34, 32), t, html.escape(b)) for i, t, b in items)
    stepsh = "".join('<div class="step"><div class="n">%d</div><h3>%s</h3><p>%s</p></div>'
                     % (n, t, html.escape(b)) for n, (t, b) in enumerate(steps, 1))
    return """<div class="w"><div class="hero-plain">
  <p class="kick">%s</p><h1>%s</h1><p class="lede">%s</p>
  <div class="acts"><a class="btn" href="give.html">Give to the work</a><a class="btn-o" href="contact.html">Ask a question</a></div>
</div></div>
<section class="sec-tight"><div class="w">
  <div class="four">%s</div>
  <div class="ph"><i>%s</i></div>
</div></section>
<section class="arc arc-flat"><div class="w">
  <p class="kick" style="text-align:left">How it goes</p>
  <div class="steps">%s</div>
</div></section>
<section class="sec">%s</section>""" % (kick, h1, html.escape(lede), cards, photo, stepsh, ask())

PAGES["education.html"] = ("Education | Fathers for the Fatherless",
  "Verse-by-verse teaching, leadership training and literacy in Honduras.",
  programme("Education", "Putting the Word in a father&rsquo;s hands.",
    C("Concise, practical and Gospel-centred teaching, built for real life in the home and the church."),
    [("book", "Biblical discipleship", C("Verse-by-verse teaching that turns Scripture into daily obedience and lasting change.")),
     ("house", "Leadership training", C("Equipping men to lead their families and churches with integrity and courage.")),
     ("tree", "Literacy and learning", C("Helping children and adults read, starting with the most important Book of all.")),
     ("dove", "Family discipleship", C("Teaching fathers to lead worship, prayer and the Word inside their own homes."))],
    [("Identify", C("Find the men who are willing.")), ("Teach", C("Open the Word with them, week after week.")),
     ("Equip", C("Put the tools in their hands.")), ("Multiply", C("They teach the next man, and their own children."))],
    "Photograph &mdash; a teaching session"))

PAGES["health-care.html"] = ("Health care | Fathers for the Fatherless",
  "Checkups, medicine, maternal care and mobile clinics in Honduras.",
  programme("Health care", "Where the nearest clinic is hours away.",
    C("Care that meets real needs, brought to the communities that cannot travel to it."),
    [("house", "Checkups and diagnosis", C("Trained workers assess and treat illness before it spreads.")),
     ("book", "Medicine and supplies", C("Essential medications families simply cannot afford.")),
     ("dove", "Maternal and child care", C("Protecting mothers and the youngest, most vulnerable lives.")),
     ("tree", "Mobile clinics", C("We bring care to the villages the roads forget."))],
    [("We travel", C("Out to the community, not the other way round.")), ("We assess", C("One person at a time.")),
     ("We treat", C("With what we carried in.")), ("We share Christ", C("Because that is why we came."))],
    "Photograph &mdash; a clinic day"))

PAGES["dental-care.html"] = ("Dental care | Fathers for the Fatherless",
  "Cleanings, extractions, pain relief and oral health teaching in Honduras.",
  programme("Dental care", "Ending the kind of pain that steals sleep.",
    C("Real relief, free of charge, in villages where there is no dentist."),
    [("tree", "Cleanings and checkups", C("Preventive care that keeps small problems from becoming agony.")),
     ("house", "Extractions and pain relief", C("Ending the kind of pain that steals sleep, work and hope.")),
     ("book", "Oral health teaching", C("Simple habits and supplies so families can care for themselves.")),
     ("dove", "Care with the Gospel", C("Every chair is a chance to share the love of Christ."))],
    [("We set up", C("Wherever there is room and light.")), ("We treat", C("Whoever comes through the door.")),
     ("We teach", C("So the next problem never starts.")), ("We point to Christ", C("Every time."))],
    "Photograph &mdash; a dental clinic day"))

PAGES["mission-trips.html"] = ("Go to Honduras | Fathers for the Fatherless",
  "Travel to Honduras to teach, build and work beside the Honduran brothers.",
  programme("Go", "Come and see what God is doing.",
    "Every trip is built around presence: showing up, staying close, and pointing to Christ.",
    [("book", "Open the Word", C("Teach and be taught, in homes, churches and around tables.")),
     ("house", "Serve hands-on", C("Build, repair, treat and labour beside Honduran brothers.")),
     ("dove", "Build friendships", C("Leave with names, faces and relationships that last for years.")),
     ("tree", "Live with purpose", C("Simple days, full hearts, every hour aimed at the Gospel."))],
    [("Write to us", "Email the ministry and say you want to come."),
     ("Pick a field", C("Guaimaca and La Ceiba, Talanga, or Danli.")),
     ("Prepare", C("Dates are approximate and fill quickly. Reach out early.")),
     ("Go", C("Mornings in the Word. Afternoons in the work."))],
    "Photograph &mdash; a team on the ground"))

PAGES["give.html"] = ("Give | Fathers for the Fatherless",
  "Support the work of equipping fathers and planting churches in Honduras.",
  """<div class="w"><div class="hero-plain">
  <p class="kick">Give</p>
  <h1>A father equipped. A church planted. A family restored.</h1>
  <p class="lede">For the cost of a few coffee shop visits a month, you can make a difference.</p>
</div></div>
<section class="sec-tight"><div class="w">
  <h2>What a monthly gift does.</h2>
  <div class="tiers">%s</div>
  <p class="lede" style="max-width:60ch;margin-top:26px">Custom amounts are welcome, and one-time gifts are put to immediate use.</p>
  <div class="form">
    <h3 style="margin:0 0 8px">How to give today</h3>
    <p class="note">Write to the ministry and someone will tell you how to send a gift.
    <!-- BUILD NOTE: replace this block with the real Donorbox (or equivalent) embed the day the
         ministry supplies a campaign URL. Never describe a checkout that does not exist. --></p>
    <a class="btn" href="mailto:%s?subject=I%%20want%%20to%%20give%%20to%%20Fathers%%20for%%20the%%20Fatherless">Email the ministry to give</a>
  </div>
</div></section>
<section class="arc arc-flat"><div class="w">
  <p class="kick" style="text-align:left">Three ways in</p>
  <div class="three">
    <div><div class="disc d1">%s</div><h3>Pray</h3><p>For the men being discipled, and for the families being put back together.</p></div>
    <div><div class="disc d2">%s</div><h3>Give</h3><p>Monthly or once. Both reach the same work.</p></div>
    <div><div class="disc d3">%s</div><h3>Go</h3><p>Teams travel every year. There is a place for you.</p></div>
  </div>
</div></section>
<section class="sec">%s</section>""" % (
    "".join('<div class="tier"><div class="amt">%s</div><div class="per">per month</div><h4>%s</h4><p>%s</p></div>'
            % (a, html.escape(t), html.escape(b)) for a, t, b in TIERS),
    EMAIL, ico("book"), ico("dove"), ico("house"),
    ask("The work will not stop. Will you be part of it?", "Email the ministry")))

PAGES["updates.html"] = ("Updates from the field | Fathers for the Fatherless",
  "Reports from the work in Honduras.",
  """<div class="w"><div class="hero-plain">
  <p class="kick">From the field</p><h1>What is happening in Honduras.</h1>
  <p class="lede">Reports from the work, written when there is something real to report.</p>
</div></div>
<section class="sec-tight"><div class="w">
  <article class="letter" style="display:block">
    <p class="role">%s &middot; La Ceiba</p>
    <h4 style="margin-bottom:12px">The La Ceiba mission house</h4>
    <p>The mission house in La Ceiba is in active renovation. Work is progressing steadily as we prepare it to serve as a permanent base of operations for church planting and discipleship work in the region.</p>
    <p>La Ceiba is Honduras's fourth most populous city and the eco-tourism capital of the country, which makes it a city of real strategic importance for the Gospel. Directors have personally travelled to assess progress, meet with the local men we are discipling, and plan the next phase of outreach.</p>
  </article>
  <div class="ph"><i>Photograph &mdash; the mission house, renovation in progress</i></div>
</div></section>
<section class="sec">%s</section>""" % (C("Spring 2026"), ask()))

PAGES["about.html"] = ("About | Fathers for the Fatherless",
  "Who we are and why the work exists.",
  """<div class="w"><div class="hero-plain">
  <p class="kick">About</p><h1>A small team with a long commitment.</h1>
  <p class="lede">Every person involved has personally invested in this ministry, with their time, their money, and their presence on the field.</p>
</div></div>
<section class="sec-tight"><div class="w">
  <div class="letter">
    <div class="av"><span>Portrait<br>H. Finnicum</span></div>
    <div><h4>Howard Finnicum</h4><div class="role">President</div>
      <p>Has been training believers for parts of five decades. After labouring faithfully in a local church for most of that time, he now splits his time between Roanoke, Virginia and serving as the main overseer of the work in Honduras. He has three grown children and 16 grandchildren, and he serves God faithfully with his wife of over thirty years.</p></div>
  </div>
  <div class="letter">
    <div class="av"><span>Portrait<br>H. B. Shirkey</span></div>
    <div><h4>Hyatt Browning Shirkey</h4><div class="role">Chief counsel</div>
      <p>&nbsp;<!-- BUILD NOTE: the ministry's current site leaves this bio as unedited template text.
         It has to be written by him, not by us. --></p></div>
  </div>
  <div class="letter">
    <div class="av"><span>Portrait<br>J. Young</span></div>
    <div><h4>%s</h4><div class="role">%s</div>
      <p>%s</p></div>
  </div>
</div></section>
<section class="arc arc-flat"><div class="w">
  <p class="kick" style="text-align:left">What makes the work what it is</p>
  <div class="three">
    <div><div class="disc d1">%s</div><h3>Long-term</h3><p>We go back every year. We measure the work in generations, not trips.</p></div>
    <div><div class="disc d2">%s</div><h3>Theological</h3><p>We open the Word. The teaching is the work, not a wrapper around it.</p></div>
    <div><div class="disc d3">%s</div><h3>On the ground</h3><p>A majority of our directors and officers have personally travelled to Honduras.</p></div>
  </div>
</div></section>
%s
<section class="sec">%s</section>""" % (
    C("Joe Young"), C("Chief Operating Officer"),
    C("Oversees operations and administration for the ministry. Committed to the mission of equipping "
      "fathers and planting churches in Honduras and wherever else God opens the door."),
    ico("house"), ico("book"), ico("dove"), cities_block(), ask()))

PAGES["contact.html"] = ("Contact | Fathers for the Fatherless",
  "Write to the ministry about giving, going to Honduras, or praying for the work.",
  """<div class="w"><div class="hero-plain">
  <p class="kick">Contact</p><h1>Write to us.</h1>
  <p class="lede">About giving, about coming on a trip, or about praying for the work. A real person reads it.</p>
</div></div>
<section class="sec-tight"><div class="w">
  <form class="form" action="https://formsubmit.co/%s" method="POST">
    <input type="hidden" name="_subject" value="Message from fathersforthefatherless.org">
    <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
    <label for="name">Your name</label>
    <input id="name" name="name" type="text" required autocomplete="name">
    <label for="email">Your email</label>
    <input id="email" name="email" type="email" required autocomplete="email">
    <label for="msg">Message</label>
    <textarea id="msg" name="message" required></textarea>
    <p class="note">Your name, email and message are sent to the ministry's own inbox and are not used for anything else.</p>
    <button class="btn" type="submit" style="border:0;cursor:pointer">Send it</button>
  </form>
  <p class="lede" style="margin-top:24px">Or write directly to <a href="mailto:%s">%s</a>.</p>
</div></section>
<section class="sec">%s</section>""" % (EMAIL, EMAIL, EMAIL, ask()))


def build():
    for page, (title, desc, bodyhtml) in PAGES.items():
        open(os.path.join(ROOT, page), "w", encoding="utf-8").write(
            head(title, desc, page) + "\n" + bodyhtml + "\n" + FOOT)

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
    print("CONFIRM-SHEET.md: %d unconfirmed claims" % len(rows))
    print("NOT PUSHED. This does not go live until the confirm sheet comes back.")


CONFIRM_TEMPLATE = """# Confirm sheet - Fathers for the Fatherless

**Generated %s by `_build/site.py`. %d items.**

Everything below is on the site the ministry is running today, and **none of it has
been confirmed by anyone at the ministry in writing.** It is reproduced here so it
can be ticked or killed, one line at a time.

**This site does not ship until this sheet comes back.** The build is finished; the
facts are what is outstanding.

| OK? | Claim | Note |
|---|---|---|
%s

## Deliberately NOT carried over from the previous build

Each of these was on the old pages and is left off until the ministry says otherwise.
Every one is a financial or impact representation on a page that asks for money.

- "100%% of your gift goes directly to the field" / "No overhead bureaucracy" / "100%% to the Field"
- "400+ Fathers Discipled" and "12 Churches Planted"
- "500+ Patients treated in the field" (dental) and "1,000+ Patients seen in the field" (health)
- "0 Dentists in many villages we serve"
- "Secure & Flexible" and "Cancel anytime" giving language, while no payment processor exists
- "We Respond Within 48 Hours"
- "Each location is led by a Honduran brother" - the five names published under it are not all Honduran
- "We don't send tourists. We send disciples" - reads as a quotation with nobody to attribute it to
- The four named outcome stories on the education page (a father returns home, a pastor is equipped,
  a child learns to read, a marriage restored) - real people or composites is the question

## Still needed from the ministry

- Who owns `fathersforthefatherless.org` - registrar, login, renewal date. **The cutover is blocked on this.**
- A real donate processor, or a decision to stay on email.
- 501(c)(3) determination letter and EIN, if gifts are to be described as tax-deductible.
- A mailing address and a phone number. The site has neither, and never has.
- Real photographs. Every slot is labelled with the picture it is waiting for.
- The vector logo (.ai / .eps / .svg). The current files are cut out of JPEGs.
- Hyatt Browning Shirkey's bio. His slot on the current site is unedited template text.
"""

if __name__ == "__main__":
    build()
