"""Static site generator for obscur4.online (English-only, DECISIONS D12).

    python build.py            # production build -> public/ (noindex until release.json "indexable" is true)
    python build.py --release  # same, but also enforces the release gates and makes the site indexable

Standard library only. Output is plain static HTML for Cloudflare Pages (see README.md).
Copy lives in content.py (ID/EN tuples; this build uses the EN side) and content_platform.py.
"""
import hashlib
import html
import json
import re
import shutil
import sys
from pathlib import Path

from content import BUNDLE, CHROME, COMPARE, LURE, NOT_FOUND, PAGES, PATH, SITE, DOMAIN
from content_platform import PLATFORM

ROOT = Path(__file__).parent
OUT = ROOT / "public"
ASSETS = ROOT / "assets"
CFG = json.loads((ROOT / "release.json").read_text(encoding="utf-8"))
RELEASE = "--release" in sys.argv
# Base path for hosting under a sub-path, e.g. GitHub Pages project sites: python build.py --base /testobscura
BASE = sys.argv[sys.argv.index("--base") + 1].rstrip("/") if "--base" in sys.argv else ""
INDEXABLE = RELEASE and CFG.get("indexable", False)
CONTACT_EMAIL = CFG.get("contact_email") or ""
ORIGIN = f"https://{DOMAIN}"
PROBLEMS = []

ROUTES = {
    "home": "/", "awareness": "/awareness-phishing/", "mobile": "/mobile-assessment/", "how": "/how-we-work/",
    "platform": "/platform/", "partners": "/partners/", "about": "/about/", "contact": "/contact/",
    "privacy": "/privacy/", "sent": "/contact/sent/",
}
NAV = [("awareness", "Awareness & phishing"), ("mobile", "Mobile assessment"), ("how", "How we work"),
       ("platform", "Platform"), ("partners", "Partners"), ("about", "About")]


# ------------------------------------------------------------------ text helpers
def E(v):
    """English side of a (ID, EN) tuple; plain strings pass through."""
    return v[1] if isinstance(v, tuple) else v


def rich(text, link=None):
    out = html.escape(E(text), quote=False)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"==(.+?)==", r'<em class="hl">\1</em>', out)
    if "{{HOLD" in out:
        PROBLEMS.append(f"HOLD left in copy: {out[:80]}")
    if CONTACT_EMAIL:
        e = html.escape(CONTACT_EMAIL)
        out = out.replace("{{CONTACT_EMAIL}}", f'<a href="mailto:{e}">{e}</a>')
    elif "{{CONTACT_EMAIL}}" in out:
        PROBLEMS.append("contact_email missing in release.json")
    if link:
        out = re.sub(r"\[(.+?)\]", rf'<a href="{link}">\1</a>', out)
    return out


def esc(v):
    return html.escape(E(v))


def plain(text):
    return re.sub(r"\{\{.+?\}\}", "", E(text)).replace("**", "").replace("==", "").strip()


def to(key, query=""):
    return BASE + ROUTES[key] + query


def req(topic):
    return to("contact", f"?topic={topic}")


def check_hero(h, sub):
    if len(plain(h).split()) > 12:
        PROBLEMS.append(f"hero headline > 12 words: {plain(h)}")
    if sub and len(plain(sub).split()) > 25:
        PROBLEMS.append(f"hero subline > 25 words: {plain(sub)}")


# ------------------------------------------------------------------ assets
def emit_assets():
    out = {}
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    for name in ("site.css", "motion.js", "site.js"):
        data = (ASSETS / name).read_bytes()
        stem, ext = name.rsplit(".", 1)
        hashed = f"{stem}.{hashlib.sha256(data).hexdigest()[:10]}.{ext}"
        (OUT / "assets" / hashed).write_bytes(data)
        out[name] = f"{BASE}/assets/{hashed}"
    shutil.copy(ASSETS / "favicon.svg", OUT / "assets" / "favicon.svg")
    return out


# ------------------------------------------------------------------ page shell
def page(key, title, desc, body, assets, form=False, index=True, closing_cta=True):
    path = ROUTES.get(key, "/")
    robots = "" if (INDEXABLE and index) else '<meta name="robots" content="noindex">'
    nav = "".join(f'<li><a href="{to(k)}"{" aria-current=\"page\"" if k == key else ""}>{html.escape(lbl)}</a></li>'
                  for k, lbl in NAV)
    sheet = "".join(f'<li><a href="{to(k)}"{" aria-current=\"page\"" if k == key else ""}>{html.escape(lbl)}</a></li>'
                    for k, lbl in [("home", "Home")] + NAV + [("contact", "Contact")])
    ld = ""
    if key == "home":
        ld = '<script type="application/ld+json">' + json.dumps(
            {"@context": "https://schema.org", "@type": "Organization", "name": SITE, "url": ORIGIN + "/",
             "email": CONTACT_EMAIL}) + "</script>"
    form_js = f'<script src="{assets["site.js"]}" defer></script>' if form else ""
    mcta = "" if key in ("contact", "sent") or not closing_cta else (
        f'<div class="mcta" data-mcta><a class="btn btn-primary" href="{to("contact")}">{esc(CHROME["nav_button"])}</a></div>')
    d = html.escape(plain(desc)[:160], quote=True)
    t = html.escape(plain(title), quote=True)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
{robots}
<link rel="canonical" href="{ORIGIN}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{ORIGIN}{path}">
<meta name="twitter:card" content="summary">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#fbfbfa">
<link rel="icon" href="{BASE}/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{assets['site.css']}">
<script src="{assets['motion.js']}"></script>
{form_js}
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header" data-header>
  <div class="wrap header-row">
    <a class="brand" href="{BASE}/" aria-label="{SITE} home">obscur<span class="brand-4">4</span></a>
    <nav class="nav" aria-label="Main" data-nav><ul>{nav}</ul><span class="nav-ind" aria-hidden="true"></span></nav>
    <a class="btn btn-primary btn-sm header-cta" href="{to('contact')}">{esc(CHROME['nav_button'])}</a>
    <details class="msheet" data-sheet>
      <summary><span class="when-closed">Menu</span><span class="when-open">{esc(CHROME['menu_close'])}</span></summary>
      <div class="msheet-panel">
        <nav aria-label="Main"><ul>{sheet}</ul></nav>
        <a class="btn btn-primary" href="{to('contact')}">{esc(CHROME['nav_button'])}</a>
      </div>
    </details>
  </div>
  <div class="progress" aria-hidden="true"><span></span></div>
</header>
<main id="main">
{body}
</main>
{mcta}
{footer()}
</body>
</html>
"""


def footer():
    mail = (f'<li><a href="mailto:{html.escape(CONTACT_EMAIL)}">{html.escape(CONTACT_EMAIL)}</a></li>' if CONTACT_EMAIL else "")
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-about">
        <a class="brand" href="{BASE}/">obscur<span class="brand-4">4</span></a>
        <p>{esc(CHROME['tagline'])}</p>
      </div>
      <div><h2>{esc(CHROME['footer_services'])}</h2><ul>
        <li><a href="{to('awareness')}">Awareness &amp; phishing</a></li>
        <li><a href="{to('mobile')}">Mobile assessment</a></li></ul></div>
      <div><h2>{esc(CHROME['footer_company'])}</h2><ul>
        <li><a href="{to('how')}">How we work</a></li>
        <li><a href="{to('platform')}">Platform</a></li>
        <li><a href="{to('partners')}">Partners</a></li>
        <li><a href="{to('about')}">About</a></li></ul></div>
      <div><h2>Contact</h2><ul>
        <li><a href="{to('contact')}">{esc(CHROME['nav_button'])}</a></li>{mail}</ul></div>
    </div>
    <div class="footer-base"><span>&copy; {SITE}</span><span><a href="{to('privacy')}">Privacy notice</a> &middot; <a href="#main">{esc(CHROME['to_top'])}</a></span></div>
  </div>
</footer>"""


# ------------------------------------------------------------------ building blocks
def btns(items):
    return '<div class="actions">' + "".join(
        f'<a class="btn {"btn-primary" if i == 0 else "btn-ghost"}" href="{u}">{esc(t)}</a>'
        for i, (t, u) in enumerate(items)) + "</div>"


KICKERS = {
    "home": ("obscur4", "Security awareness and mobile assessment"),
    "awareness": ("Lead service", "Managed programme"),
    "mobile": ("Specialist service", "Evidence-grade assessment"),
    "how": ("How we work", "Authorization, evidence, data"),
    "platform": ("Platform", "Infrastructure overview"),
    "partners": ("Partners", "Referral, resale, delivery"),
    "about": ("About", "One platform, two services"),
    "contact": ("Contact", "We reply by email"),
    "privacy": ("Privacy notice", "Effective 8 October 2026"),
}


def kicker(key):
    if key not in KICKERS:
        return ""
    l, r = KICKERS[key]
    return (f'<p class="kicker" data-scene="kicker"><span>{html.escape(l)}</span>'
            f'<span class="dots" aria-hidden="true"></span><span class="kr">{html.escape(r)}</span></p>')


def hero(h, sub, ctas, art="", key=None):
    check_hero(h, sub)
    lede = f'<p class="lede">{rich(sub)}</p>' if sub else ""
    kick = kicker(key)
    if art:
        return f"""<section class="hero"><div class="wrap grid">
  <div class="hero-copy c-1-7">{kick}<h1>{rich(h)}</h1>{lede}{btns(ctas) if ctas else ""}</div>
  <div class="hero-art c-8-12">{art}</div>
</div></section>"""
    return f"""<section class="hero hero-plain"><div class="wrap">
  {kick}<h1>{rich(h)}</h1>{lede}{btns(ctas) if ctas else ""}
</div></section>"""


_BAND_N = [0]


def band(inner, cls="", sid=None):
    _BAND_N[0] += 1
    i = f' id="{sid or "s" + str(_BAND_N[0])}"'
    return f'<section class="band {cls}"{i}><div class="wrap">{inner}</div></section>'


def head(h2, intro=None, label=None):
    lab = f'<p class="label">{esc(label)}</p>' if label else ""
    p = f"<p>{rich(intro)}</p>" if intro else ""
    return f'<div class="section-head">{lab}<h2>{rich(h2)}</h2>{p}</div>'


def split(h2, inner, intro=None):
    return f'<div class="grid"><div class="c-1-5">{head(h2, intro)}</div><div class="c-6-12">{inner}</div></div>'


def rows(items, cls=""):
    lis = []
    for it in items:
        if isinstance(it, tuple) and len(it) == 2 and isinstance(it[0], tuple):
            lis.append(f"<li><div><h3>{esc(it[0])}</h3><p>{rich(it[1])}</p></div></li>")
        else:
            lis.append(f"<li><div><p class=\"row-text\">{rich(it)}</p></div></li>")
    return f'<ul class="rows {cls}">' + "".join(lis) + "</ul>"


def closing(h2, ctas, art=""):
    if art:
        inner = f'<div class="grid"><div class="c-1-6"><h2>{rich(h2)}</h2>{btns(ctas)}</div><div class="c-8-12">{art}</div></div>'
    else:
        inner = f"<h2>{rich(h2)}</h2>{btns(ctas)}"
    return f'<section class="closing"><div class="wrap">{inner}</div></section>'


# ------------------------------------------------------------------ graphics-led components
import illustrations as I


def lure(mini=False):
    """The real artifact: an Indonesian lure. Only the markers and pins animate (graphic), never the text."""
    body = html.escape(LURE["body"])
    mark2 = '<span class="cue" data-n="2" data-a="0.5" data-b="0.66">hari ini</span>'
    body = body.replace("hari ini", mark2, 1) if "hari ini" in body else f'<span class="cue" data-n="2" data-a="0.5" data-b="0.66">{body}</span>'
    cues = "".join(f'<li data-a="{0.3 + i * 0.2:.2f}" data-b="{0.42 + i * 0.2:.2f}">{esc(c)}</li>' for i, c in enumerate(LURE["cues"]))
    return f"""<figure class="art lure{' lure-mini' if mini else ''}" data-scene="art">
  <figcaption class="art-label">{esc(LURE['label'])}</figcaption>
  <div class="mail" lang="id">
    <div class="mail-bar" aria-hidden="true"><span></span><span></span><span></span></div>
    <div class="mail-head">
      <div class="mail-from"><span class="avatar" aria-hidden="true">LP</span>
        <div><strong>{html.escape(LURE['from_name'])}</strong><br><span class="cue" data-n="1" data-a="0.3" data-b="0.46">&lt;{html.escape(LURE['from_addr'])}&gt;</span><br><span class="mail-to">{html.escape(LURE['to'])}</span></div></div>
      <p class="mail-subj">{html.escape(LURE['subject'])}</p>
    </div>
    <div class="mail-body"><p>{body}</p><span class="mail-btn">{html.escape(LURE['button'])}</span>
      <p class="mail-link"><span class="cue" data-n="3" data-a="0.7" data-b="0.86">{html.escape(LURE['link'])}</span></p></div>
  </div>
  <ol class="cues">{cues}</ol>
  {'' if mini else f'<p class="art-caption">{esc(LURE["caption"])}</p>'}
</figure>"""


def bundle():
    items = "".join(f'<li><span class="file-ico" aria-hidden="true"></span><span class="file-name">{html.escape(n)}</span>'
                    f'<span class="file-note">{esc(note)}</span></li>' for n, note in BUNDLE["items"])
    return f"""<figure class="art bundle" data-scene="bundle">
  <figcaption class="art-label">{esc(BUNDLE['label'])}</figcaption>
  <div class="manifest"><div class="manifest-head"><span class="folder" aria-hidden="true"></span><strong>evidence-bundle</strong></div>
  <ul class="files">{items}</ul></div>
</figure>"""


def compare_scene():
    cols = "".join(f'<th scope="col">{esc(c)}</th>' for c in COMPARE["cols"])
    body = ""
    for r, row in enumerate(COMPARE["rows"]):
        cells = f'<th scope="row">{esc(row[0])}</th>'
        for c in range(1, 4):
            cls = ' class="is-diff"' if (r, c) == (1, 2) else (' class="is-out"' if (r, c) == (1, 3) else "")
            cells += f"<td{cls}>{esc(row[c])}</td>"
        body += f"<tr>{cells}</tr>"
    return f"""<figure class="art" data-scene="compare">
  <figcaption class="art-label">{esc(COMPARE['label'])}</figcaption>
  <div class="compare-wrap"><table class="compare"><caption class="sr-only">{esc(COMPARE['title'])}</caption><thead><tr>{cols}</tr></thead><tbody>{body}</tbody></table></div>
  <div class="verdict"><p>{esc(COMPARE['verdict'])}</p></div>
</figure>"""


def icon_items(items, icons, cls="icon-grid"):
    out = ""
    for i, ((t, b), ic) in enumerate(zip(items, icons)):
        out += f'<div class="ii">{I.icon(ic, 0.05 + i * 0.08, 0.5 + i * 0.08)}<h3>{esc(t)}</h3><p>{rich(b)}</p></div>'
    return f'<div class="{cls}" data-scene="art">{out}</div>'


def check_list(items):
    lis = "".join(f'<li>{I.icon("check", 0.1 + i * 0.1, 0.25 + i * 0.1, "ico-check")}<span>{rich(it)}</span></li>' for i, it in enumerate(items))
    return f'<ul class="checks" data-scene="art">{lis}</ul>'


def statement(label, text, ico=None):
    icon_html = f'<div class="statement-ico" data-scene="art">{I.icon(ico, 0, 0.7)}</div>' if ico else ""
    return f'<div class="statement">{icon_html}<p class="label">{esc(label)}</p><p class="statement-text">{rich(text)}</p></div>'


def media(h2, text_html, art, flip=False, intro=None):
    a = f'<div class="media-art">{art}</div>'
    t = f'<div class="media-text">{head(h2, intro)}{text_html}</div>'
    return f'<div class="media{" media-flip" if flip else ""}">{t}{a}</div>'


def teaser(compact=True, with_list=True):
    layers = PAGES["how"]["layers"]
    lst = "".join(f"<li>{esc(l)}</li>" for l in layers) if with_list else ""
    ol = f'<ol class="teaser-list">{lst}</ol>' if with_list else ""
    return f'<div class="teaser{" teaser-solo" if not with_list else ""}" data-scene="teaser">{I.stack_svg(compact)}{ol}</div>'


def workspaces():
    """Platform hero: model lanes as separate workspaces, each with its own key, limit and log, around one core."""
    P = PLATFORM
    body = '<circle class="ws-core" cx="260" cy="200" r="40"/>'
    for i, (name, _, _) in enumerate(P["lanes"]):
        x = 40 + i * 160
        body += f'<path class="ws-link" d="M{x + 60} 120 C{x + 60} 160, 260 150, 260 160"/>'
        body += f'<circle class="flow-dot" r="4" data-curve="{x + 60},120,{x + 60},160,260,150,260,160" data-off="{i / 3:.2f}"/>'
        body += (f'<g class="ws" transform="translate({x} 20)"><rect class="ws-card" width="120" height="100" rx="12"/>'
                 f'<g transform="translate(12 14) scale(0.5)">{I.icon_paths("key")}</g>'
                 f'<g transform="translate(46 14) scale(0.5)">{I.icon_paths("gauge")}</g>'
                 f'<g transform="translate(80 14) scale(0.5)">{I.icon_paths("log")}</g>'
                 f'<rect class="ws-bar" x="14" y="62" width="92" height="8" rx="4"/><rect class="ws-bar" x="14" y="78" width="62" height="8" rx="4"/></g>')
    body += '<g transform="translate(242 182) scale(0.75)" class="ws-core-ico">' + I.icon_paths("nodes") + "</g>"
    body += '<path class="ws-link" d="M260 240 V300"/><rect class="ws-ledger" x="200" y="300" width="120" height="44" rx="10"/>'
    body += '<rect class="ws-bar" x="216" y="314" width="88" height="7" rx="3.5"/><rect class="ws-bar" x="216" y="327" width="60" height="7" rx="3.5"/>'
    body += '<circle class="flow-dot" r="4" data-from="260,240" data-to="260,300" data-off="0.5"/>'
    return (f'<figure class="art workspaces" data-scene="flow" aria-hidden="true"><svg viewBox="0 0 520 360" fill="none" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</svg></figure>')


def model_diag(kind, i):
    a = 0.05 + i * 0.1
    if kind == 0:   # referral, then delivery under your name
        body = (I.pop('<circle cx="40" cy="60" r="18"/>', a, a + 0.1, "pf") + I.ring(40, 60, 18, a, a + 0.2)
                + I.ln("M60 60 H150", a + 0.2, a + 0.4, "b dash") + I.pop('<circle cx="170" cy="60" r="20"/>', a + 0.4, a + 0.5, "bf")
                + I.ln("M170 86 C170 110, 40 110, 40 82", a + 0.5, a + 0.7, "dash")
                + '<circle class="flow-dot" r="4" data-from="60,60" data-to="150,60"/>')
    elif kind == 1:  # resell as part of a portfolio
        body = (I.ln("M20 30 H90 V90 H20 Z", a, a + 0.2) + I.ln("M34 46 H76 M34 60 H70 M34 74 H62", a + 0.15, a + 0.3)
                + I.pop('<rect x="120" y="30" width="70" height="60" rx="10"/>', a + 0.3, a + 0.45, "tf")
                + I.ln("M120 30 H190 V90 H120 Z", a + 0.3, a + 0.5, "b") + I.ln("M90 60 H120", a + 0.5, a + 0.6, "b")
                + '<circle class="flow-dot" r="4" data-from="90,60" data-to="120,60"/>')
    else:           # referral only, independence kept
        body = (I.pop('<circle cx="40" cy="60" r="18"/>', a, a + 0.1, "pf") + I.ring(40, 60, 18, a, a + 0.2)
                + I.ln("M60 60 H150", a + 0.2, a + 0.4, "dash") + I.ln("M104 30 V90", a + 0.4, a + 0.5, "b")
                + I.pop('<circle cx="170" cy="60" r="20"/>', a + 0.5, a + 0.6, "pf") + I.ring(170, 60, 20, a + 0.5, a + 0.7, "b")
                + '<circle class="flow-dot" r="4" data-from="60,60" data-to="150,60"/>')
    return (f'<figure class="art ill model-diag" data-scene="art flow" aria-hidden="true"><svg viewBox="0 0 210 120" fill="none" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</svg></figure>')


# ------------------------------------------------------------------ pages
STORY = [
    ("It starts with one message.",
     "Lures are written from message types common in Indonesian workplaces: parcel deliveries, bank notices, tax, a note from a manager."),
    ("The signs are marked.",
     "Every lure carries the signs staff should learn to notice: a sender that does not match its domain, time pressure, a link to somewhere else."),
    ("The campaign reaches every target group.",
     "Campaigns are scoped and authorized first, then launched from our platform to the groups you choose."),
    ("Results come back by group.",
     "Reports show how each group responded, and training follows where it is needed. Person-level results stay with administrators you designate."),
    ("Every step leaves evidence.",
     "Each campaign ends in a platform-generated report your audit and risk teams can follow."),
]


def home():
    p = PAGES["home"]
    body = hero(p["hero_h"], p["hero_sub"], [(p["cta1"], req("awareness")), (p["cta2"], to("how"))], I.network(), key="home")
    steps = "".join(f'<li data-step><span class="step-mark" aria-hidden="true"></span><h3>{html.escape(t)}</h3><p>{html.escape(b)}</p></li>' for t, b in STORY)
    body += f"""<section class="story" data-scene="story"><div class="wrap">
  <div class="story-head"><p class="label">How a campaign works</p><h2>From one message to evidence your auditors can follow</h2></div>
  <div class="story-grid">
    <ol class="story-steps">{steps}</ol>
    <div class="story-stage">{I.story_stage()}</div>
  </div>
</div></section>"""
    body += band(f"""{head(p['services_h'])}
<div class="services">
  <a class="panel panel-lead" href="{to('awareness')}">{I.inbox_report()}<p class="label">Lead service</p><h3>{esc(p['svc_a_t'])}</h3><p>{rich(p['svc_a_b'])}</p><span class="textlink">{esc(p['more'])}</span></a>
  <a class="panel" href="{to('mobile')}">{I.cap_runtime()}<p class="label">Specialist service</p><h3>{esc(p['svc_b_t'])}</h3><p>{rich(p['svc_b_b'])}</p><span class="textlink">{esc(p['more'])}</span></a>
</div>""", cls="band-paper")
    body += band(f"""{head(p['trust_h'], p['problem_b'])}{icon_items(p['trust'], ['lock', 'hash', 'eye-off'], 'icon-grid icon-grid-3')}
<p class="more-link"><a class="textlink" href="{to('how')}">{esc(p['trust_link'])}</a></p>""")
    h = PAGES["how"]
    body += band(f"""<div class="grid"><div class="c-1-5">{head(h['layers_h'], h['layers_intro'])}<a class="textlink" href="{to('platform')}">See the platform</a></div>
<div class="c-6-12">{teaser()}</div></div>""", cls="band-paper")
    body += band(statement(p["who_h"], p["who_b"], "users"))
    body += closing(p["closing_h"], [(p["closing_a"], req("awareness")), (p["closing_b"], req("mobile"))], lure(mini=True))
    return p["meta_title"], p["meta_desc"], body


def awareness():
    p = PAGES["awareness"]
    body = hero(p["hero_h"], p["hero_sub"], [(p["cta1"], req("awareness")), (p["cta2"], req("awareness"))], lure(), key="awareness")
    body += band(media(p["problem_h"], f'<p class="prose">{rich(p["problem_b"])}</p>', I.inbox_report()), cls="band-paper")
    icons = ["doc", "pen", "send", "screen", "report"]
    st = "".join(f'<li class="tl-station"><div class="tl-node">{I.icon(icons[i], 0, 1)}</div><h3>{esc(t)}</h3><p>{rich(b)}</p></li>'
                 for i, (t, b) in enumerate(p["steps"]))
    body += band(f"""{head(p['how_h'])}<div class="timeline" data-scene="timeline">
  <div class="tl-track" aria-hidden="true"><span class="tl-fill"></span><span class="tl-dot"></span></div>
  <ol class="tl">{st}</ol></div>""")
    arts = [I.single(), I.cycle()]
    offers = "".join(f'<div class="offer">{arts[i]}<p class="label">{"Entry" if i == 0 else "Annual"}</p><h3>{esc(t)}</h3><p>{rich(b)}</p></div>'
                     for i, (t, b) in enumerate(p["offers"]))
    body += band(f'{head(p["ways_h"])}<div class="offers">{offers}</div>', cls="band-paper")
    body += band(f'{head(p["get_h"])}{check_list(p["get"])}')
    body += band(statement(p["who_h"], p["who_b"], "users"), cls="band-paper")
    body += closing(p["closing_h"], [(p["closing_cta"], req("awareness"))])
    return p["meta_title"], p["hero_sub"], body


def mobile():
    p = PAGES["mobile"]
    body = hero(p["hero_h"], p["hero_sub"], [(p["cta1"], req("mobile")), (p["cta2"], to("how"))], I.phone_scan(), key="mobile")
    body += band(media(p["problem_h"], f'<p class="prose">{rich(p["problem_b"])}</p>', I.cap_attribution()), cls="band-paper")
    tabs = "".join(f'<button class="tab" role="tab" id="tab-{i}" aria-controls="panel-{i}" aria-selected="{"true" if i == 0 else "false"}">'
                   f'<span class="tab-n" aria-hidden="true"></span>{esc(t)}<span class="tab-bar" aria-hidden="true"></span></button>'
                   for i, (t, _) in enumerate(p["what"]))
    panels = "".join(f'<div class="tabpanel" role="tabpanel" id="panel-{i}" aria-labelledby="tab-{i}">{I.CAPS[i]()}'
                     f'<h3>{esc(t)}</h3><p>{rich(b)}</p></div>' for i, (t, b) in enumerate(p["what"]))
    body += band(f'{head(p["what_h"])}<div class="explorer" data-tabs><div class="tablist" role="tablist" aria-label="{esc(p["what_h"])}">{tabs}</div>'
                 f'<div class="panels">{panels}</div></div>')
    body += band(f"{head(COMPARE['title'])}{compare_scene()}", cls="band-paper")
    pipe_icons = ["lock", "doc", "phone", "report"]
    pipe = "".join(f'<li><div class="pipe-node">{I.icon(pipe_icons[i], 0.1 + i * 0.15, 0.4 + i * 0.15)}</div><h3>{esc(s)}</h3></li>'
                   for i, s in enumerate(p["how_steps"]))
    body += band(f'{head(p["how_h"])}<ol class="pipe" data-scene="art" aria-label="{html.escape(E(p["how_alt"]), quote=True)}">{pipe}</ol>')
    formats = "".join(f'<div class="format"><h3>{esc(t)}</h3><p>{rich(b)}</p></div>' for t, b in p["formats"])
    body += band(f"""<div class="media"><div class="media-text">{head(p['get_h'])}{check_list(p['get'])}<div class="formats">{formats}</div>
<p class="muted note">{rich(p['formats_note'])}</p></div><div class="media-art">{bundle()}</div></div>""", cls="band-paper")
    body += band(f'<div class="duo">{statement(p["who_h"], p["who_b"], "users")}{statement(p["trust_h"], p["trust_b"], "shield")}</div>')
    body += closing(p["closing_h"], [(p["closing_cta"], req("mobile"))])
    return p["meta_title"], p["hero_sub"], body


def how():
    p = PAGES["how"]
    body = hero(p["hero_h"], p["hero_sub"], [], teaser(compact=False, with_list=False), key="how")
    arts = {"authorization": I.authorization(), "evidence": I.evidence_chain(), "data-handling": I.isolation()}
    for i, (sid, title, items) in enumerate(p["sections"]):
        body += band(media(title, check_list(items), arts[sid], flip=bool(i % 2)), cls="band-paper" if i % 2 else "", sid=sid)
    xs = "".join(f'<li>{I.icon("eye-off", 0.1 + i * 0.12, 0.4 + i * 0.12, "ico-x")}<span>{rich(it)}</span></li>' for i, it in enumerate(p["not"]))
    body += band(f'{head(p["not_h"])}<ul class="checks checks-x" data-scene="art">{xs}</ul>'
                 f'<p class="more-link"><a class="textlink" href="{to("platform")}">See the platform</a></p>')
    body += closing(p["band_h"], [(p["band_cta"], req("briefing"))])
    return p["meta_title"], p["hero_sub"], body


def platform():
    P = PLATFORM
    body = hero(P["hero_h"], P["hero_sub"], [(P["band_cta"], req("briefing"))], workspaces(), key="platform")
    rows_html = ""
    for i, (name, desc) in enumerate(P["layers"]):
        stamp = '<span class="stamp">authorized</span>' if i == 1 else ""
        rows_html += f'<li data-step><span class="step-mark" aria-hidden="true"></span><h3>{html.escape(name)}{stamp}</h3><p>{html.escape(desc)}</p></li>'
    body += f"""<section class="band band-paper layers-band" data-scene="layerscroll"><div class="wrap">
  {head(P['stack_h'], P['stack_intro'])}
  <div class="layers-grid"><div class="layers-stage">{I.stack_svg(False)}</div><ol class="layer-list">{rows_html}</ol></div>
  <p class="feedback">{I.icon("cycle", 0, 0.6, "ico-inline")}{html.escape(P['feedback'])}</p>
</div></section>"""
    lanes = "".join(f'<div class="lane"><h3>{html.escape(n)}</h3><p>{html.escape(sub)}</p><ul class="chips">'
                    + "".join(f'<li class="chip">{html.escape(t)}</li>' for t in tasks) + "</ul></div>" for n, sub, tasks in P["lanes"])
    body += band(f'{head(P["lanes_h"], P["lanes_intro"])}{I.routing()}<div class="lanes">{lanes}</div>')
    body += band(f'{head(P["provider_h"], P["provider_intro"])}' + icon_items(P["provider"], ["layers", "key", "gauge", "log", "eye-off", "swap"], "icon-grid icon-grid-3"), cls="band-paper")
    body += band(f'{head(P["controls_h"])}' + icon_items(P["controls"], ["key", "shield", "log", "lock"], "icon-grid icon-grid-4"))
    c_t, c_items = P["boundary_client"]
    i_t, i_items = P["boundary_internal"]
    body += band(f"""{head(P['boundary_h'])}<div class="boundary">
<div class="side">{I.icon("users", 0, 0.6)}<h3>{html.escape(c_t)}</h3><ul>{"".join(f"<li>{html.escape(x)}</li>" for x in c_items)}</ul></div>
<div class="wall" aria-hidden="true"></div>
<div class="side side-dark">{I.icon("box", 0, 0.6)}<h3>{html.escape(i_t)}</h3><ul>{"".join(f"<li>{html.escape(x)}</li>" for x in i_items)}</ul></div></div>""", cls="band-paper")
    body += closing(P["band_h"], [(P["band_cta"], req("briefing"))])
    return P["meta_title"], P["hero_sub"], body


def partners():
    p = PAGES["partners"]
    body = hero(p["hero_h"], p["hero_sub"], [(p["cta"], req("partner"))], I.hub(), key="partners")
    body += band(statement(p["why_h"], p["why_b"], "link"), cls="band-paper")
    labels = ["Referral, then delivery", "Resell", "Referral only"]
    models = "".join(f'<div class="model">{model_diag(i, i)}<p class="label">{labels[i]}</p><h3>{esc(t)}</h3><p>{rich(b)}</p></div>'
                     for i, (t, b) in enumerate(p["models"]))
    body += band(f'{head(p["models_h"])}<div class="models">{models}</div><p class="muted note">{rich(p["terms"])}</p>')
    body += closing(p["cta"], [(p["cta"], req("partner"))])
    return p["meta_title"], p["hero_sub"], body


def about():
    p = PAGES["about"]
    body = hero(p["hero_h"], p["hero_sub"], [], I.split_platform(), key="about")
    ops = "".join(f"<li><span class=\"step-mark\" aria-hidden=\"true\"></span>{rich(it)}</li>" for it in p["operate"])
    body += band(f"""<div class="ring-wrap" data-scene="ring"><div>{head(p['operate_h'])}<ol class="ring-list">{ops}</ol></div>
<div class="ring-art">{I.ring_svg(["doc", "send", "report", "cycle"])}</div></div>""", cls="band-paper")
    body += band(f'<div class="duo">{statement(p["lang_h"], p["lang_b"], "chat")}{statement(p["material_h"], p["material_b"], "shield")}</div>')
    if E(p.get("company_h", ("", ""))):
        body += band(split(p["company_h"], f'<p class="prose">{rich(p["company_b"])}</p>'))
    body += closing(p["cta"], [(p["cta"], to("contact"))])
    return p["meta_title"], p["hero_sub"], body


def contact():
    p = PAGES["contact"]
    lab = {k: E(v) for k, v in p["labels"].items()}

    def field(name, control, required, hint=""):
        star = ' <span class="req" aria-hidden="true">*</span>' if required else ""
        hint_html = f'<p class="hint" id="hint-{name}">{hint}</p>' if hint else ""
        return (f'<div class="field" data-field="{name}"><label for="f-{name}">{html.escape(lab[name])}{star}</label>'
                f'{control}{hint_html}<p class="err" id="err-{name}" hidden></p></div>')

    def opts(items):
        return f'<option value="">{esc(p["choose"])}</option>' + "".join(f'<option value="{v}">{esc(t)}</option>' for v, t in items)

    def d(name, hint=False):
        return f'aria-describedby="err-{name}' + (f' hint-{name}' if hint else "") + '"'

    topic_icons = {"awareness": "inbox", "mobile": "phone", "partner": "link", "briefing": "chat", "other": "spark"}
    topics = "".join(f'<label class="pill pill-ico"><input type="radio" name="topic" value="{v}" required><span>{I.icon(topic_icons[v], 0, 0.01)}{esc(t)}</span></label>'
                     for v, t in p["topics"])
    reply = "".join(f'<label class="pill"><input type="radio" name="reply_language" value="{v}"{" checked" if v == "en" else ""}><span>{html.escape(t)}</span></label>'
                    for v, t in (("en", "English"), ("id", "Bahasa Indonesia")))
    form = f"""<form class="request-form" id="request-form" action="{BASE}/api/request" method="post"
  data-err-required="{esc(p['err_required'])}" data-err-email="{esc(p['err_email'])}" data-err-consent="{esc(p['err_consent'])}"
  data-err-format="{esc(p['err_format'])}" data-err-message-len="{esc(p['err_message_len'])}" data-err-phone="{esc(p['err_phone'])}">
  <input type="hidden" name="lang" value="en"><input type="hidden" name="ts" value="">
  <fieldset class="field" data-field="topic" aria-describedby="err-topic"><legend>{html.escape(lab['topic'])} <span class="req" aria-hidden="true">*</span></legend>
    <div class="choices choices-topics">{topics}</div><p class="err" id="err-topic" hidden></p></fieldset>
  <div class="form-row">
    {field("name", f'<input id="f-name" name="name" type="text" autocomplete="name" required maxlength="100" {d("name")}>', True)}
    {field("email", f'<input id="f-email" name="email" type="email" autocomplete="email" required maxlength="254" {d("email")}>', True)}
  </div>
  <div class="form-row">
    {field("organization", f'<input id="f-organization" name="organization" type="text" autocomplete="organization" required maxlength="150" {d("organization")}>', True)}
    {field("role", f'<input id="f-role" name="role" type="text" autocomplete="organization-title" maxlength="100" {d("role")}>', False)}
  </div>
  <div class="form-row">
    {field("org_type", f'<select id="f-org_type" name="org_type" {d("org_type")}>{opts(p["org_types"])}</select>', False)}
    {field("phone", f'<input id="f-phone" name="phone" type="tel" autocomplete="tel" maxlength="20" {d("phone")}>', False)}
  </div>
  {field("platform", f'<select id="f-platform" name="platform" {d("platform")}>{opts(p["platforms"])}</select>', False)}
  {field("message", f'<textarea id="f-message" name="message" rows="6" required maxlength="2000" {d("message", True)}></textarea>', True, rich(p["helper"]))}
  <fieldset class="field" data-field="reply_language" aria-describedby="err-reply_language"><legend>{html.escape(lab['reply_language'])}</legend>
    <div class="choices">{reply}</div><p class="err" id="err-reply_language" hidden></p></fieldset>
  <div class="field field-consent" data-field="consent"><label class="choice"><input id="f-consent" type="checkbox" name="consent" value="yes" required aria-describedby="err-consent">
    <span>{rich(p['consent'], to('privacy'))}</span></label><p class="err" id="err-consent" hidden></p></div>
  <div class="hp" aria-hidden="true"><label for="f-website">Website</label><input id="f-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
  <div class="form-error" id="form-error" role="alert" hidden>{rich(p['err_server'])}</div>
  <button class="btn btn-primary" type="submit">{esc(p['submit'])}</button>
</form>
<div class="form-success" id="form-success" tabindex="-1" hidden>{I.done()}<p>{rich(p['success'])}</p></div>
<div class="sr-live" aria-live="polite" id="form-live"></div>"""
    stages = [("You send a request", "We reply to the email address you give, in the language you choose."),
              ("We agree scope", "If there is a fit, we agree scope and record written authorization before any work starts."),
              ("Work runs through the platform", "Everything from the first campaign or test to the report comes out of the platform.")]
    jl = "".join(f'<li><span class="j-node" aria-hidden="true"></span><h3>{html.escape(t)}</h3><p>{html.escape(b)}</p></li>' for t, b in stages)
    aside = f"""<aside class="contact-aside"><p class="label">What happens next</p>
<div class="journey-wrap" data-scene="journey"><span class="journey-rail" aria-hidden="true"></span><ol class="journey">{jl}</ol></div>
<p class="aside-mail">{rich(p['alt'])}</p></aside>"""
    body = hero(p["hero_h"], p["hero_sub"], [], I.send(), key="contact")
    body += band(f'<div class="contact-grid"><div class="form-card"><h2 class="form-title">{esc(p["form_h"])}</h2><p class="muted">{esc(p["required_note"])}</p>{form}</div>{aside}</div>', cls="band-paper")
    return p["meta_title"], p["hero_sub"], body


def privacy():
    p = PAGES["privacy"]
    secs = "".join(f"<li><h2>{esc(t)}</h2><p>{rich(b)}</p></li>" for t, b in p["sections"])
    toc = "".join(f'<li><a href="#s{i + 1}">{esc(t)}</a></li>' for i, (t, _) in enumerate(p["sections"]))
    secs = "".join(f'<li id="s{i + 1}"><h2>{esc(t)}</h2><p>{rich(b)}</p></li>' for i, (t, b) in enumerate(p["sections"]))
    body = hero(p["hero_h"], None, [], I.isolation(), key="privacy")
    body += band(f'<div class="legal-grid"><nav class="legal-toc" aria-label="Sections"><p class="label">On this page</p><ol>{toc}</ol></nav>'
                 f'<div><p class="effective">{rich(p["effective"])}</p><ol class="legal">{secs}</ol></div></div>', cls="band-paper")
    return p["meta_title"], p["sections"][0][1], body


def sent():
    c = PAGES["contact"]
    body = f"""<section class="sent"><div class="wrap sent-grid"><div>{I.done()}</div><div><p class="label">Request sent</p><h1>{rich(c['success'])}</h1>
{btns([(c['back_home'], BASE + '/')])}</div></div></section>"""
    return PAGES["sent"]["meta_title"], c["success"], body


BUILDERS = {"home": home, "awareness": awareness, "mobile": mobile, "how": how, "platform": platform,
            "partners": partners, "about": about, "contact": contact, "privacy": privacy, "sent": sent}


# ------------------------------------------------------------------ quality gates (BUILD-BRIEF §8)
BANNED = [r"real devices?", r"physical devices?", r"emulator-only", r"agentic", r"AI-powered", r"\bAI\b",
          r"KnowBe4", r"Check Point", r"\bLucy\b", r"Vanta", r"Drata", r"Semgrep", r"Snyk", r"NowSecure", r"appaudix",
          r"Ostorlab", r"Appknox", r"eShard", r"Spentera", r"Protergo", r"SysTech", r"Digiserve", r"GoPhish",
          r"Slack", r"Telegram", r"WhatsApp", r"\bpilot\b", r"Anthropic", r"Claude", r"OpenAI", r"Gemini",
          r"placeholder", r"lorem", r"TODO", r"\bTBD\b"]
PRICE = re.compile(r"(Rp|IDR|US\$|USD|\$)\s?\d")
CITE = re.compile(r"\[(D\d|S\d|L\d|G\d|PRF|CAP|PER|MKT|NFR|PRD|Kickoff|BUILD-BRIEF)[^\]]*\]")


def gate(path, doc):
    text = re.sub(r"<head>.*?</head>", " ", doc, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", " ", text, flags=re.S)))
    for pat in BANNED:
        if re.search(pat, text, flags=0 if pat in (r"\bAI\b", r"TODO", r"\bTBD\b") else re.I):
            PROBLEMS.append(f"{path}: banned term /{pat}/")
    if PRICE.search(text):
        PROBLEMS.append(f"{path}: price-like text")
    if CITE.search(text):
        PROBLEMS.append(f"{path}: citation residue")
    if "{{" in doc:
        PROBLEMS.append(f"{path}: unrendered token")


# ------------------------------------------------------------------ static files
def write(rel, doc):
    path = OUT / rel.lstrip("/")
    if rel.endswith("/"):
        path = path / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(doc, encoding="utf-8")
    return path


def extras(assets):
    nf = f"""<section class="sent"><div class="wrap sent-grid"><div>{I.lost()}</div><div><p class="label">Error 404</p><h1>{html.escape(E(NOT_FOUND['title']))}</h1>
<p class="muted">The page may have moved. These are the main places to go from here.</p>
{btns([('Home', BASE + '/'), ('Make a request', to('contact'))])}</div></div></section>"""
    doc = page("404", "Page not found | obscur4", "Page not found.", nf, assets, index=False, closing_cta=False)
    gate("404.html", doc)
    (OUT / "404.html").write_text(doc, encoding="utf-8")

    urls = "".join(f"<url><loc>{ORIGIN}{r}</loc></url>" for k, r in ROUTES.items() if k != "sent")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                     + urls + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n" if INDEXABLE
                                    else "User-agent: *\nDisallow: /\n", encoding="utf-8")
    wk = OUT / ".well-known"
    wk.mkdir(exist_ok=True)
    contact_line = f"mailto:{CONTACT_EMAIL}" if CONTACT_EMAIL else f"{ORIGIN}/contact/"
    (wk / "security.txt").write_text(f"Contact: {contact_line}\nExpires: {CFG['security_txt_expires']}\n"
                                     f"Preferred-Languages: en, id\nCanonical: {ORIGIN}/.well-known/security.txt\n", encoding="utf-8")
    headers = ["/*",
               "  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; "
               "connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'",
               "  Strict-Transport-Security: max-age=31536000; includeSubDomains",
               "  X-Content-Type-Options: nosniff",
               "  Referrer-Policy: strict-origin-when-cross-origin",
               "  Permissions-Policy: camera=(), microphone=(), geolocation=()",
               "  X-Frame-Options: DENY"]
    if not INDEXABLE:
        headers.append("  X-Robots-Tag: noindex")
    headers += ["", "/assets/*", "  Cache-Control: public, max-age=31536000, immutable", ""]
    (OUT / "_headers").write_text("\n".join(headers), encoding="utf-8")
    # Old bilingual URLs from the first preview point to their English pages.
    redirects = ["/en/* /:splat 301", "/kesadaran-phishing/ /awareness-phishing/ 301",
                 "/penilaian-aplikasi-mobile/ /mobile-assessment/ 301", "/cara-kerja/ /how-we-work/ 301",
                 "/mitra/ /partners/ 301", "/tentang/ /about/ 301", "/kontak/ /contact/ 301", "/privasi/ /privacy/ 301"]
    (OUT / "_redirects").write_text("\n".join(redirects) + "\n", encoding="utf-8")


def release_gates():
    if not CFG.get("legal_signed_off"):
        PROBLEMS.append("legal_signed_off is false in release.json (privacy notice + consent text)")
    attested = set(CFG.get("claims_attested", []))
    missing = [f"C{i}" for i in range(1, 13) if f"C{i}" not in attested]
    if missing:
        PROBLEMS.append("claims not attested (WEBSITE-SPEC §9): " + ", ".join(missing))


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    assets = emit_assets()
    for key, build in BUILDERS.items():
        _BAND_N[0] = 0
        title, desc, body = build()
        doc = page(key, E(title), E(desc), body, assets, form=(key == "contact"), index=(key != "sent"),
                   closing_cta=key not in ("privacy",))
        gate(ROUTES[key], doc)
        write(ROUTES[key], doc)
    extras(assets)
    if RELEASE:
        release_gates()
    mode = "RELEASE" if RELEASE else "BUILD"
    if PROBLEMS:
        unique = list(dict.fromkeys(PROBLEMS))
        print(f"[{mode}] {len(unique)} gate failure(s):")
        for p in unique:
            print("  -", p)
        sys.exit(1)
    print(f"[{mode}] OK: {len(list(OUT.rglob('*.html')))} HTML files in {OUT} "
          f"({'indexable' if INDEXABLE else 'noindex until release'})")


if __name__ == "__main__":
    main()
