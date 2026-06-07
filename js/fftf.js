/* ============================================================
   FATHERS FOR THE FATHERLESS — shared chrome + interactions
   Injects nav, footer, donation drawer, and floating Donate button,
   then wires scroll state, mobile menu, reveal-on-scroll, count-up,
   arrow carousels, and the donation drawer.
   ============================================================ */
(function () {
  'use strict';

  var EMBLEM = 'images/fftf-emblem.png';

  // ----- Primary navigation (program pages) -----
  var NAV = [
    { label: 'Mission Trips', href: 'mission-trips.html' },
    { label: 'Education',     href: 'education.html' },
    { label: 'Health Care',   href: 'health-care.html' },
    { label: 'Dental Care',   href: 'dental-care.html' }
  ];

  var here = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
  function isActive(href) { return href.toLowerCase() === here; }

  function navLinksHTML(mobile) {
    return NAV.map(function (n) {
      var cls = mobile ? '' : 'nav-link';
      if (isActive(n.href)) cls += ' active';
      return '<a href="' + n.href + '" class="' + cls.trim() + '">' + n.label + '</a>';
    }).join('');
  }

  // ----- NAV -----
  var navHost = document.getElementById('site-nav');
  if (navHost) {
    navHost.innerHTML =
      '<nav class="nav" id="nav">' +
        '<div id="trip-banner" style="position:relative;background:rgba(200,137,42,0.1);border-bottom:1px solid rgba(200,137,42,0.18);padding:7px 32px;text-align:center;font-family:var(--sans);font-size:11px;letter-spacing:1.5px;color:rgba(237,228,215,0.7);text-transform:uppercase;">' +
          '<span style="color:var(--gold);font-weight:700;">Next Trip &mdash; Summer 2026 &middot; Honduras</span>' +
          '&nbsp;&nbsp;&middot;&nbsp;&nbsp;<a href="mission-trips.html" style="color:rgba(237,228,215,0.6);border-bottom:1px solid rgba(200,137,42,0.3);">Join us</a>' +
        '</div>' +
        '<div class="nav-inner">' +
          '<a href="index.html" class="nav-brand" aria-label="Fathers for the Fatherless home"><img src="' + EMBLEM + '" alt="Fathers for the Fatherless"></a>' +
          '<div class="nav-links">' + navLinksHTML(false) +
            '<a href="#" onclick="openDonateDrawer(50);return false;" class="nav-cta">Donate Now</a>' +
          '</div>' +
          '<button class="hamburger" id="hamburger" aria-label="Open menu"><span></span><span></span><span></span></button>' +
        '</div>' +
      '</nav>' +
      '<div class="mobile-panel" id="mobilePanel" aria-hidden="true">' +
        '<button class="mobile-close" id="mobileClose" aria-label="Close menu">&times;</button>' +
        '<a href="index.html">Home</a>' + navLinksHTML(true) +
        '<a href="#" onclick="openDonateDrawer(50);return false;" class="nav-cta" style="margin-top:14px;">Donate Now</a>' +
      '</div>';
  }

  // ----- FOOTER -----
  var footHost = document.getElementById('site-footer');
  if (footHost) {
    footHost.innerHTML =
      '<section class="pre-footer dot-bg" aria-label="Support the Mission">' +
        '<div class="container">' +
          '<span class="overline-block" style="color:rgba(200,137,42,0.7);margin-bottom:12px;">Est. 2006 &mdash; Honduras</span>' +
          '<h2>The work continues.</h2><p class="subline">Will you be part of it?</p>' +
          '<button class="btn btn-gold" onclick="openDonateDrawer(50)">Donate Now &mdash; It Reaches the Field</button>' +
        '</div>' +
      '</section>' +
      '<div class="section-divider"></div>' +
      '<footer class="footer dot-bg">' +
        '<div class="footer-mission">' +
          '<img class="footer-logo" src="' + EMBLEM + '" alt="Fathers for the Fatherless">' +
          '<p class="footer-tagline">To equip, engage, and edify the Body of Christ even unto the ends of the world.</p>' +
          '<div class="footer-social">' +
            '<a href="https://www.facebook.com/fathersforthefatherless" target="_blank" rel="noopener" class="social-icon" aria-label="Facebook">F</a>' +
            '<a href="https://twitter.com" target="_blank" rel="noopener" class="social-icon" aria-label="X">&#120143;</a>' +
          '</div>' +
        '</div>' +
        '<div class="footer-rule"></div>' +
        '<div class="footer-grid">' +
          '<div class="footer-col"><h5>Programs</h5><ul>' +
            '<li><a href="mission-trips.html">Mission Trips</a></li>' +
            '<li><a href="education.html">Education</a></li>' +
            '<li><a href="health-care.html">Health Care</a></li>' +
            '<li><a href="dental-care.html">Dental Care</a></li>' +
          '</ul></div>' +
          '<div class="footer-col"><h5>Support</h5><ul>' +
            '<li><a href="#" onclick="openDonateDrawer(50);return false;">Donate Now</a></li>' +
            '<li><a href="#" onclick="openDonateDrawer(50);return false;">Monthly Giving</a></li>' +
            '<li><a href="mailto:fathers4thefatherless@gmail.com">Prayer Partner</a></li>' +
            '<li><a href="mission-trips.html">Go on a Trip</a></li>' +
          '</ul></div>' +
          '<div class="footer-col"><h5>Ministry</h5><ul>' +
            '<li><a href="index.html#mission-pillars">The Mission</a></li>' +
            '<li><a href="index.html#testimonials">From the Field</a></li>' +
            '<li><a href="index.html#where-we-work">Where We Work</a></li>' +
            '<li><a href="index.html#faq">FAQ</a></li>' +
          '</ul></div>' +
          '<div class="footer-col"><h5>Contact</h5><ul>' +
            '<li><a href="mailto:fathers4thefatherless@gmail.com">Contact Us</a></li>' +
            '<li><a href="mailto:fathers4thefatherless@gmail.com">Email</a></li>' +
          '</ul></div>' +
        '</div>' +
        '<div class="footer-legal">Fathers for the Fatherless &mdash; Est. 2006 &mdash; Honduras Field Ministry &mdash; 100% of gifts reach the field.<br>&middot; Gospel-Centered &middot; Non-Profit &middot; Donor Funded</div>' +
      '</footer>';
  }

  // ----- DRAWER + FAB (appended to body) -----
  var chrome = document.createElement('div');
  chrome.innerHTML =
    '<button class="donate-fab" onclick="openDonateDrawer(50)" aria-label="Donate now">' +
      '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 21s-8.5-5.2-8.5-11.2A4.3 4.3 0 0 1 12 6.2a4.3 4.3 0 0 1 8.5 3.6C20.5 15.8 12 21 12 21Z" fill="#1C2B3A"/></svg> Donate Now</button>' +
    '<div id="drawer-overlay" onclick="closeDonateDrawer()" aria-hidden="true"></div>' +
    '<div id="donate-drawer" role="dialog" aria-labelledby="drawer-amount" aria-hidden="true"><div class="drawer-inner">' +
      '<img class="drawer-logo" src="' + EMBLEM + '" alt="Fathers for the Fatherless">' +
      '<p class="drawer-overline">You\'re joining the mission</p>' +
      '<h3 id="drawer-amount">$50 / month</h3>' +
      '<p id="drawer-impact">Sustains a pastor\'s leadership training.</p>' +
      '<div class="drawer-freq" role="group" aria-label="Giving frequency">' +
        '<button type="button" class="freq-btn active" data-freq="month" onclick="setFreq(\'month\')">Monthly</button>' +
        '<button type="button" class="freq-btn" data-freq="once" onclick="setFreq(\'once\')">One-Time</button>' +
      '</div>' +
      '<div class="drawer-amts">' +
        '<button type="button" class="amt-btn" data-amt="25" onclick="setAmt(25)">$25</button>' +
        '<button type="button" class="amt-btn active" data-amt="50" onclick="setAmt(50)">$50</button>' +
        '<button type="button" class="amt-btn" data-amt="100" onclick="setAmt(100)">$100</button>' +
        '<button type="button" class="amt-btn" data-amt="250" onclick="setAmt(250)">$250</button>' +
      '</div>' +
      '<div class="drawer-form">' +
        '<input type="text" placeholder="First Name" autocomplete="given-name">' +
        '<input type="text" placeholder="Last Name" autocomplete="family-name">' +
        '<input type="email" class="full-row" placeholder="Email Address" autocomplete="email">' +
      '</div>' +
      '<p class="drawer-stripe-note">100% reaches the field &middot; Secure giving &middot; Cancel anytime</p>' +
      '<button class="drawer-continue" onclick="proceedDonation()">Continue to Secure Giving</button>' +
      '<button class="drawer-close" onclick="closeDonateDrawer()">&times; Close</button>' +
    '</div></div>';
  while (chrome.firstChild) document.body.appendChild(chrome.firstChild);

  // ----- Nav scroll state + mobile menu -----
  var navEl = document.getElementById('nav');
  function onScroll() { if (navEl) navEl.classList.toggle('scrolled', window.scrollY > 60); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var ham = document.getElementById('hamburger');
  var panel = document.getElementById('mobilePanel');
  var mclose = document.getElementById('mobileClose');
  if (ham && panel) {
    ham.addEventListener('click', function () { panel.classList.add('open'); });
    if (mclose) mclose.addEventListener('click', function () { panel.classList.remove('open'); });
    panel.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { panel.classList.remove('open'); }); });
  }

  // ----- Reveal on scroll -----
  // Stagger grouped children so they cascade in left-to-right
  ['.feature-grid', '.steps', '.stat-band', '.tier-grid', '.timeline'].forEach(function (sel) {
    document.querySelectorAll(sel).forEach(function (group) {
      Array.prototype.slice.call(group.children).forEach(function (el, i) {
        if (el.classList.contains('reveal')) el.style.transitionDelay = (i * 0.09) + 's';
      });
    });
  });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });

  // ----- Count-up -----
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function runCount(el) {
    var raw = el.textContent.trim();
    var m = raw.match(/^(\D*)(\d[\d,]*)(.*)$/);
    if (!m) return;
    var pre = m[1], suf = m[3], end = parseInt(m[2].replace(/,/g, ''), 10);
    if (reduce || end > 100000) { el.textContent = raw; return; }
    var dur = 1400, t0 = null;
    function tick(now) {
      if (t0 === null) t0 = now;
      var p = Math.min((now - t0) / dur, 1);
      var e = 1 - Math.pow(1 - p, 3);
      el.textContent = pre + Math.round(end * e).toLocaleString() + suf;
      if (p < 1) requestAnimationFrame(tick); else el.textContent = raw;
    }
    requestAnimationFrame(tick);
  }
  var countIO = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { runCount(e.target); countIO.unobserve(e.target); } });
  }, { threshold: 0.5 });
  document.querySelectorAll('.count-up').forEach(function (t) { countIO.observe(t); });

  // ----- Arrow carousels -----
  var CH_L = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var CH_R = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  function makeCarousel(host) {
    var cards = Array.prototype.slice.call(host.children);
    if (!cards.length) return;
    var carousel = document.createElement('div'); carousel.className = 'carousel';
    var viewport = document.createElement('div'); viewport.className = 'carousel-viewport';
    var track = document.createElement('div'); track.className = 'carousel-track';
    cards.forEach(function (c) { c.classList.remove('reveal'); c.classList.add('visible'); track.appendChild(c); });
    viewport.appendChild(track);
    var prev = document.createElement('button'); prev.type = 'button'; prev.className = 'carousel-arrow prev'; prev.setAttribute('aria-label', 'Previous'); prev.innerHTML = CH_L;
    var next = document.createElement('button'); next.type = 'button'; next.className = 'carousel-arrow next'; next.setAttribute('aria-label', 'Next'); next.innerHTML = CH_R;
    carousel.appendChild(prev); carousel.appendChild(viewport); carousel.appendChild(next);
    host.parentNode.replaceChild(carousel, host);
    var offset = 0;
    function step() { var f = track.firstElementChild; var g = parseInt(getComputedStyle(track).columnGap, 10) || 24; return (f ? f.offsetWidth : 300) + g; }
    function maxOffset() { return Math.max(0, track.scrollWidth - viewport.clientWidth); }
    function apply() {
      var mx = maxOffset();
      offset = Math.max(0, Math.min(offset, mx));
      track.style.transform = 'translateX(' + (-offset) + 'px)';
      var none = mx <= 0;
      prev.style.display = none ? 'none' : ''; next.style.display = none ? 'none' : '';
      prev.disabled = offset <= 0; next.disabled = offset >= mx - 1;
    }
    prev.addEventListener('click', function () { offset -= step(); apply(); });
    next.addEventListener('click', function () { offset += step(); apply(); });
    window.addEventListener('resize', function () { offset = 0; apply(); });
    apply();
  }
  document.querySelectorAll('.js-carousel').forEach(makeCarousel);

  // ----- Donation drawer -----
  var DONATE_URL = ''; // paste Donorbox/Stripe link to accept real payments
  var don = { amount: 50, freq: 'month' };
  var DON_IMPACT = {
    25: "Covers a month of discipleship materials for one father.",
    50: "Sustains a pastor's leadership training.",
    100: "Helps plant and sustain a church in Honduras.",
    250: "Funds a full mission outreach — travel and materials."
  };
  function render() {
    var suf = don.freq === 'month' ? ' / month' : ' one-time';
    var amt = document.getElementById('drawer-amount');
    if (amt) amt.textContent = '$' + don.amount + suf;
    var imp = document.getElementById('drawer-impact');
    if (imp) imp.textContent = DON_IMPACT[don.amount] || "Reaches a father and family in Honduras.";
    document.querySelectorAll('.amt-btn').forEach(function (b) { b.classList.toggle('active', parseInt(b.dataset.amt, 10) === don.amount); });
    document.querySelectorAll('.freq-btn').forEach(function (b) { b.classList.toggle('active', b.dataset.freq === don.freq); });
  }
  window.setAmt = function (a) { don.amount = a; render(); };
  window.setFreq = function (f) { don.freq = f; render(); };
  window.openDonateDrawer = function (a) {
    if (a) don.amount = a; render();
    var d = document.getElementById('donate-drawer');
    d.style.bottom = '0';
    document.getElementById('drawer-overlay').style.display = 'block';
    d.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  };
  window.closeDonateDrawer = function () {
    var d = document.getElementById('donate-drawer');
    d.style.bottom = '-110%';
    document.getElementById('drawer-overlay').style.display = 'none';
    d.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  };
  window.proceedDonation = function () {
    if (DONATE_URL) {
      var sep = DONATE_URL.indexOf('?') > -1 ? '&' : '?';
      window.location.href = DONATE_URL + sep + 'amount=' + don.amount + '&recurring=' + (don.freq === 'month');
      return;
    }
    window.closeDonateDrawer();
  };
})();
