"""Animated graphics for obscur4.online. Graphics move; text never does.

Conventions (styled in site.css, driven by motion.js):
  class="ln"   stroked path drawn in; pathLength=100; data-a/data-b = start/end of its draw (0..1)
  class="pop"  shape that scales in between data-a and data-b
  stroke/fill modifiers: "b" blue stroke, "w" white stroke, "dash" dashed, "bf" blue fill, "pf" paper fill, "tf" tint fill
A figure with data-scene="art" plays its drawing once when it enters the viewport (stepped timing).
Every final state is the complete drawing (no-JS and reduced-motion visitors see it as-is).
"""
import math
import random


def _fig(view, body, cls="", scene="art", extra=""):
    return (f'<figure class="art ill {cls}" data-scene="{scene}" aria-hidden="true"{extra}>'
            f'<svg viewBox="{view}" fill="none" stroke-linecap="round" stroke-linejoin="round">{body}</svg></figure>')


def ln(d, a, b, cls=""):
    return f'<path class="ln {cls}" pathLength="100" data-a="{a}" data-b="{b}" d="{d}"/>'


def pop(shape, a, b, cls=""):
    return shape.replace("/>", f' class="pop {cls}" data-a="{a}" data-b="{b}"/>', 1)


def ring(cx, cy, r, a, b, cls=""):
    return ln(f"M{cx - r} {cy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0", a, b, cls)


# ---------------------------------------------------------------- icons (48 x 48 line icons)
ICONS = {
    "doc": "M14 6 H30 L38 14 V42 H14 Z|M30 6 V14 H38|M20 24 H32 M20 30 H32 M20 36 H27",
    "pen": "M10 38 L12 30 L32 10 L38 16 L18 36 Z|M28 14 L34 20|M10 43 H38",
    "send": "M6 24 L42 8 L32 42 L22 28 Z|M22 28 L42 8",
    "screen": "M6 10 H42 V32 H6 Z|M18 40 H30 M24 32 V40|M14 18 H26 M14 24 H34",
    "report": "M10 6 H38 V42 H10 Z|M16 16 H32|M16 24 H32|M16 32 H24",
    "shield": "M24 6 L38 12 V24 C38 33 32 39 24 42 C16 39 10 33 10 24 V12 Z|M18 24 L22 28 L30 20",
    "lock": "M12 22 H36 V42 H12 Z|M17 22 V15 A7 7 0 0 1 31 15 V22|M24 30 V34",
    "hash": "M18 8 L14 40 M32 8 L28 40|M10 18 H40 M8 30 H38",
    "link": "M20 28 L28 20|M22 14 L26 10 A7 7 0 0 1 38 22 L34 26|M26 34 L22 38 A7 7 0 0 1 10 26 L14 22",
    "users": "M18 22 A6 6 0 1 0 18 10 A6 6 0 1 0 18 22|M6 38 C6 30 12 26 18 26 C24 26 30 30 30 38|M32 22 A5 5 0 1 0 32 12|M34 26 C39 27 42 31 42 37",
    "cycle": "M40 24 A16 16 0 1 1 30 9|M30 4 L31 10 L25 12",
    "check": "M10 25 L20 35 L38 13",
    "phone": "M15 4 H33 A3 3 0 0 1 36 7 V41 A3 3 0 0 1 33 44 H15 A3 3 0 0 1 12 41 V7 A3 3 0 0 1 15 4 Z|M21 9 H27",
    "layers": "M24 6 L42 15 L24 24 L6 15 Z|M6 24 L24 33 L42 24|M6 33 L24 42 L42 33",
    "eye-off": "M6 24 C12 14 18 11 24 11 C30 11 36 14 42 24 C36 34 30 37 24 37 C18 37 12 34 6 24 Z|M8 8 L40 40",
    "key": "M18 30 A8 8 0 1 0 18 14 A8 8 0 1 0 18 30|M26 22 H42 M36 22 V28 M41 22 V27",
    "gauge": "M8 34 A16 16 0 1 1 40 34|M24 34 L32 20",
    "log": "M10 8 H38 V40 H10 Z|M16 16 H32 M16 22 H32 M16 28 H32 M16 34 H26",
    "nodes": "M12 12 A4 4 0 1 0 12 20 A4 4 0 1 0 12 12|M36 28 A4 4 0 1 0 36 36 A4 4 0 1 0 36 28|M12 32 A4 4 0 1 0 12 40 A4 4 0 1 0 12 32|M15 18 L33 30 M14 36 H32",
    "swap": "M10 16 H38 L32 10|M38 32 H10 L16 38",
    "inbox": "M6 26 L12 8 H36 L42 26 V40 H6 Z|M6 26 H16 L20 32 H28 L32 26 H42",
    "flag": "M12 42 V6|M12 8 H36 L30 16 L36 24 H12",
    "chat": "M8 10 H40 V32 H22 L14 40 V32 H8 Z",
    "box": "M24 6 L42 14 V34 L24 42 L6 34 V14 Z|M6 14 L24 22 L42 14|M24 22 V42",
    "spark": "M24 6 V16 M24 32 V42 M6 24 H16 M32 24 H42",
}


def icon(name, a=0.0, b=0.6, cls=""):
    parts = ICONS[name].split("|")
    step = (b - a) / len(parts)
    paths = "".join(ln(d, round(a + i * step, 3), round(a + (i + 1) * step, 3)) for i, d in enumerate(parts))
    return (f'<svg class="ico {cls}" viewBox="0 0 48 48" fill="none" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{paths}</svg>')


# ---------------------------------------------------------------- home hero: living organization network (loop)
def network(seed=7, n=30):
    """An organization: one connected graph of people; a message travels it; reported nodes ring blue (loop)."""
    rnd = random.Random(seed)
    W, H = 560, 460
    pts, tries = [], 0
    while len(pts) < n and tries < 6000:
        tries += 1
        x, y = rnd.uniform(46, W - 46), rnd.uniform(46, H - 46)
        if (x - W / 2) ** 2 / 1.3 + (y - H / 2) ** 2 > 200 ** 2:
            continue
        if all((x - a) ** 2 + (y - b) ** 2 > 62 ** 2 for a, b in pts):
            pts.append((round(x), round(y)))
    d2 = lambda i, j: (pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2
    # minimum spanning tree (Prim) keeps the organization connected; nearest neighbours add texture
    inside, edges = {0}, set()
    while len(inside) < len(pts):
        i, j = min(((i, j) for i in inside for j in range(len(pts)) if j not in inside), key=lambda e: d2(*e))
        edges.add(tuple(sorted((i, j)))); inside.add(j)
    for i in range(len(pts)):
        near = sorted((j for j in range(len(pts)) if j != i), key=lambda j: d2(i, j))[:2]
        for j in near:
            if d2(i, j) < 105 ** 2:
                edges.add(tuple(sorted((i, j))))
    edges = sorted(edges)
    lines = "".join(f'<line class="net-e" data-e="{i}-{j}" x1="{pts[i][0]}" y1="{pts[i][1]}" x2="{pts[j][0]}" y2="{pts[j][1]}"/>'
                    for i, j in edges)
    nodes = ""
    for i, (x, y) in enumerate(pts):
        lead = i % 7 == 0
        nodes += (f'<g class="net-n{" net-lead" if lead else ""}" data-i="{i}" transform="translate({x} {y})">'
                  f'<circle class="net-halo" r="{24 if lead else 18}"/><circle class="net-dot" r="{9 if lead else 6.5}"/></g>')
    data = ";".join(f"{x},{y}" for x, y in pts)
    adj = ";".join(f"{i},{j}" for i, j in edges)
    msg = ('<g class="net-msg"><rect x="-14" y="-10" width="28" height="20" rx="4"/>'
           '<path d="M-14 -10 L0 1 L14 -10"/></g>')
    rings = (f'<circle class="net-ring" cx="{W / 2}" cy="{H / 2}" r="214"/>'
             f'<circle class="net-ring" cx="{W / 2}" cy="{H / 2}" r="150"/>')
    return (f'<figure class="art net" data-scene="net" data-pts="{data}" data-edges="{adj}" aria-hidden="true">'
            f'<svg viewBox="0 0 {W} {H}" fill="none" stroke-linecap="round" stroke-linejoin="round">'
            f'{rings}<g class="net-edges">{lines}</g><g class="net-nodes">{nodes}</g>{msg}</svg></figure>')


# ---------------------------------------------------------------- home story stage (scroll scene, 5 steps)
def story_stage():
    """One object, transformed across five steps: lure -> marked signs -> campaign -> groups -> report."""
    card = ('<g class="st-card">'
            '<rect class="st-paper" x="150" y="70" width="260" height="210" rx="16"/>'
            '<path class="st-line" d="M150 108 H410"/>'
            '<circle class="st-av" cx="180" cy="89" r="10"/>'
            '<rect class="st-bar" x="198" y="84" width="120" height="10" rx="5"/>'
            '<rect class="st-bar" x="174" y="130" width="200" height="9" rx="4.5"/>'
            '<rect class="st-bar" x="174" y="150" width="170" height="9" rx="4.5"/>'
            '<rect class="st-btn" x="174" y="182" width="96" height="28" rx="6"/>'
            '<rect class="st-bar" x="174" y="232" width="150" height="9" rx="4.5"/>'
            '<rect class="st-mark m1" x="194" y="80" width="128" height="18" rx="5"/>'
            '<rect class="st-mark m2" x="290" y="145" width="58" height="19" rx="5"/>'
            '<rect class="st-mark m3" x="170" y="227" width="158" height="19" rx="5"/>'
            '<circle class="st-pin p1" cx="334" cy="89" r="9"/>'
            '<circle class="st-pin p2" cx="360" cy="154" r="9"/>'
            '<circle class="st-pin p3" cx="340" cy="236" r="9"/>'
            '</g>')
    people = ""
    for r in range(4):
        for c in range(6):
            i = r * 6 + c
            people += (f'<g class="st-p" data-i="{i}" data-r="{r}" data-c="{c}"><circle class="st-bg" r="13"/>'
                       f'<circle class="st-head" cy="-4" r="4.2"/><path class="st-body" d="M-7.5 8.5 a7.5 7 0 0 1 15 0"/></g>')
    groups = "".join(f'<rect class="st-group g{g}" x="{60 + g * 160}" y="128" width="120" height="172" rx="18"/>' for g in range(3))
    report = ('<g class="st-report"><rect class="st-paper" x="200" y="60" width="160" height="220" rx="12"/>'
              '<rect class="st-bar" x="224" y="96" width="112" height="9" rx="4.5"/>'
              '<rect class="st-bar" x="224" y="120" width="96" height="9" rx="4.5"/>'
              '<rect class="st-bar" x="224" y="144" width="104" height="9" rx="4.5"/>'
              '<rect class="st-bar" x="224" y="168" width="70" height="9" rx="4.5"/>'
              '<circle class="st-seal" cx="324" cy="244" r="22"/><path class="st-tick" d="M314 244 L321 251 L335 236"/></g>')
    dot = '<circle class="st-dot" r="8"/>'
    return (f'<div class="stage-svg" data-stage="story"><svg viewBox="0 0 560 360" fill="none" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{groups}{report}{card}{people}{dot}</svg></div>')


# ---------------------------------------------------------------- exploded isometric stack
def stack_svg(compact=False, cls="iso-svg"):
    w, h, gap, cx, top = (120, 18, 44, 140, 34) if compact else (150, 22, 56, 180, 44)
    vw, vh = (280, 340) if compact else (360, 430)
    body = f'<path class="iso-axis" d="M{cx},{top - h - 16} V{top + 6 * gap + h + 20}"/>'
    for i in range(7):
        cy = top + i * gap
        face = f"M{cx},{cy - h} L{cx + w},{cy} L{cx},{cy + h} L{cx - w},{cy} Z"
        edge = f"M{cx - w},{cy} V{cy + 6} L{cx},{cy + h + 6} L{cx + w},{cy + 6} V{cy}"
        gate = " is-gate" if i == 1 else ""
        body += (f'<g class="plate{gate}" data-i="{i}"><path class="plate-edge" d="{edge}"/>'
                 f'<path class="plate-face" d="{face}"/></g>')
    body += f'<g class="iso-probe"><circle r="7"/></g>'
    return (f'<svg class="{cls}" viewBox="0 0 {vw} {vh}" fill="none" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true" data-cx="{cx}" data-top="{top}" data-gap="{gap}">{body}</svg>')


# ---------------------------------------------------------------- page hero drawings (draw once)
def authorization():
    body = ln("M70 20 H250 V220 H70 Z", 0.0, 0.25)
    for i, y in enumerate((56, 80, 104, 128)):
        body += ln(f"M96 {y} H{224 - i * 16}", 0.2 + i * 0.05, 0.3 + i * 0.05)
    body += ln("M96 176 C112 156, 120 196, 136 172 S160 160, 172 178 S196 170, 206 172", 0.5, 0.72, "b")
    body += ln("M96 192 H224", 0.45, 0.52)
    body += pop('<circle cx="262" cy="196" r="30"/>', 0.74, 0.84, "tf")
    body += ring(262, 196, 22, 0.76, 0.9, "b")
    body += ln("M251 197 L259 205 L274 188", 0.88, 0.98, "b")
    return _fig("0 0 320 240", body)


def hub():
    nodes = [(60, 50), (60, 190), (300, 120)]
    body = ""
    for i, (x, y) in enumerate(nodes):
        a = 0.3 + i * 0.12
        body += ln(f"M{x} {y} L180 120", a, a + 0.16, "b dash")
        body += pop(f'<circle cx="{x}" cy="{y}" r="22"/>', 0.05 + i * 0.08, 0.15 + i * 0.08, "pf")
        body += ring(x, y, 22, 0.05 + i * 0.08, 0.2 + i * 0.08)
    body += pop('<circle cx="180" cy="120" r="34"/>', 0.7, 0.8, "bf")
    body += ln("M168 120 H192 M180 108 V132", 0.8, 0.9, "w")
    body += ('<circle class="flow-dot" r="4" data-from="60,50" data-to="180,120"/>'
             '<circle class="flow-dot" r="4" data-from="60,190" data-to="180,120" data-off="0.33"/>'
             '<circle class="flow-dot" r="4" data-from="300,120" data-to="180,120" data-off="0.66"/>')
    return _fig("0 0 360 240", body, "ill-flow", scene="art flow")


def split_platform():
    body = ln("M110 30 H250 V90 H110 Z", 0.0, 0.25, "b")
    body += pop('<rect x="126" y="46" width="108" height="28" rx="6"/>', 0.2, 0.3, "tf")
    body += ln("M180 90 V130 M180 130 H90 V170 M180 130 H270 V170", 0.3, 0.6, "b dash")
    body += ln("M40 170 H140 V220 H40 Z", 0.55, 0.75)
    body += ln("M220 170 H320 V220 H220 Z", 0.62, 0.82)
    body += pop('<circle cx="64" cy="195" r="8"/>', 0.8, 0.88, "bf")
    body += pop('<circle cx="244" cy="195" r="8"/>', 0.85, 0.93, "bf")
    body += ln("M82 195 H124 M262 195 H304", 0.85, 0.98)
    return _fig("0 0 360 240", body)


def send():
    body = ln("M40 120 L150 70 L118 160 Z", 0.0, 0.3, "b")
    body += ln("M150 70 L96 132", 0.2, 0.35, "b")
    body += ln("M160 110 C200 70, 230 170, 290 110", 0.35, 0.7, "dash")
    body += ln("M260 80 H330 V140 H260 Z", 0.65, 0.85)
    body += ln("M260 80 L295 108 L330 80", 0.8, 0.92)
    body += pop('<circle cx="330" cy="80" r="9"/>', 0.9, 0.98, "bf")
    body += '<circle class="flow-dot" r="5" data-curve="160,110,200,70,230,170,290,110"/>'
    return _fig("0 0 360 220", body, "ill-flow", scene="art flow")


def done():
    return _fig("0 0 120 120", pop('<circle cx="60" cy="60" r="44"/>', 0.0, 0.3, "tf") + ring(60, 60, 44, 0.0, 0.5, "b")
                + ln("M40 62 L54 76 L82 46", 0.5, 0.85, "b"), "ill-small")


def lost():
    return _fig("0 0 240 120", ln("M20 60 H90", 0.0, 0.3) + ln("M150 60 H220", 0.4, 0.7)
                + ln("M100 50 L110 60 L100 70 M140 50 L130 60 L140 70", 0.3, 0.45, "b")
                + pop('<circle cx="120" cy="60" r="4"/>', 0.7, 0.85, "bf"), "ill-small")


def inbox_report():
    """Awareness problem: an inbox; the lure that looks local is the one that gets reported."""
    body = ""
    for i, y in enumerate((24, 92, 160)):
        a = 0.05 + i * 0.12
        cls = "b" if i == 1 else ""
        body += ln(f"M24 {y} H300 V{y + 52} H24 Z", a, a + 0.2, cls)
        body += pop(f'<circle cx="52" cy="{y + 26}" r="12"/>', a + 0.15, a + 0.22, "tf" if i == 1 else "pf")
        body += ln(f"M78 {y + 18} H190 M78 {y + 34} H240", a + 0.2, a + 0.3)
    body += pop('<rect x="250" y="102" width="40" height="32" rx="8"/>', 0.62, 0.7, "bf")
    body += ln("M263 128 V110 M263 111 L278 115 L263 120", 0.7, 0.8, "w")
    return _fig("0 0 324 236", body)


def evidence_chain():
    body = ""
    for i, x in enumerate((24, 134, 244)):
        a = i * 0.25
        body += ln(f"M{x} 50 H{x + 88} V170 H{x} Z", a, a + 0.18, "b" if i == 1 else "")
        body += ln(f"M{x + 16} 76 H{x + 70} M{x + 16} 94 H{x + 60} M{x + 16} 112 H{x + 66}", a + 0.1, a + 0.22)
        if i < 2:
            body += ln(f"M{x + 92} 110 H{x + 106} M{x + 100} 104 L{x + 106} 110 L{x + 100} 116", a + 0.18, a + 0.26, "b")
    body += pop('<circle cx="178" cy="144" r="10"/>', 0.4, 0.48, "bf")
    body += ln("M288 190 C288 222, 110 222, 68 192 M68 192 L78 188 M68 192 L72 202", 0.8, 0.98, "dash")
    return _fig("0 0 360 236", body)


def isolation():
    body = ln("M24 30 H150 V160 H24 Z", 0.0, 0.2) + ln("M210 30 H336 V160 H210 Z", 0.1, 0.3)
    body += ln("M180 16 V176", 0.3, 0.45, "b")
    for i, x in enumerate((44, 230)):
        body += pop(f'<rect x="{x}" y="52" width="86" height="16" rx="4"/>', 0.35 + i * 0.05, 0.42 + i * 0.05, "tf")
        body += ln(f"M{x} 88 H{x + 64} M{x} 106 H{x + 78} M{x} 124 H{x + 54}", 0.4 + i * 0.05, 0.5 + i * 0.05)
    body += ln("M120 192 H240 V224 H120 Z", 0.6, 0.75, "b")
    body += pop('<rect x="134" y="202" width="40" height="12" rx="3"/>', 0.75, 0.82, "bf")
    body += pop('<rect x="184" y="202" width="42" height="12" rx="3"/>', 0.8, 0.88, "bf")
    body += ln("M87 160 V208 H120", 0.55, 0.65, "dash")
    return _fig("0 0 360 236", body)


def single():
    body = ln("M20 90 H120", 0.0, 0.4, "b dash") + pop('<circle cx="20" cy="90" r="9"/>', 0.0, 0.1, "bf")
    body += ln("M120 50 H170 V130 H120 Z", 0.4, 0.7) + ln("M132 74 H158 M132 90 H158 M132 106 H148", 0.65, 0.85)
    return _fig("0 0 190 180", body, "ill-small")


def cycle():
    body = ln("M90 20 A70 70 0 1 1 89.9 20", 0.0, 0.6, "b")
    for i, (x, y) in enumerate(((90, 20), (160, 90), (90, 160), (20, 90))):
        body += pop(f'<circle cx="{x}" cy="{y}" r="9"/>', 0.15 + i * 0.15, 0.22 + i * 0.15, "bf")
    return _fig("0 0 190 180", body, "ill-small")


# ---------------------------------------------------------------- mobile capability diagrams (tab explorer)
def cap_static():
    body = ln("M30 30 H150 V210 H30 Z", 0.0, 0.25)
    body += pop('<circle cx="90" cy="176" r="18"/>', 0.25, 0.35, "tf") + ln("M80 176 L87 183 L100 169", 0.32, 0.42, "b")
    body += ln("M48 56 H132 M48 74 H120 M48 92 H128", 0.2, 0.35)
    for r in range(4):
        for c in range(5):
            x, y = 190 + c * 30, 50 + r * 38
            bad = (r, c) == (2, 3)
            a = round(0.35 + (r * 5 + c) * 0.02, 3)
            body += pop(f'<rect x="{x}" y="{y}" width="22" height="28" rx="3"/>', a, round(a + 0.05, 3), "bf" if bad else "pf")
            body += ln(f"M{x} {y} H{x + 22} V{y + 28} H{x} Z", a, round(a + 0.06, 3), "b" if bad else "")
    body += ln("M150 120 H182", 0.3, 0.38, "dash")
    return _fig("0 0 360 240", body, "cap")


def cap_runtime():
    body = ""
    for i, x in enumerate((60, 210)):
        a = i * 0.2
        body += ln(f"M{x + 10} 30 H{x + 80} a10 10 0 0 1 10 10 V200 a10 10 0 0 1 -10 10 H{x + 10} a10 10 0 0 1 -10 -10 V40 a10 10 0 0 1 10 -10 Z", a, a + 0.3)
        body += ln(f"M{x + 12} 52 H{x + 78} V170 H{x + 12} Z", a + 0.2, a + 0.35, "b" if i == 0 else "")
        body += pop(f'<rect x="{x + 30}" y="90" width="30" height="30" rx="6"/>', a + 0.35, a + 0.45, "tf")
    body += ln("M108 64 L120 76 M120 64 L108 76", 0.55, 0.65, "b")
    body += ln("M256 72 h12 v-6 a6 6 0 0 0 -12 0 v6 m-2 0 h16 v12 h-16 z", 0.6, 0.75)
    body += ln("M150 120 H200", 0.75, 0.9, "dash")
    return _fig("0 0 360 240", body, "cap")


def cap_attribution():
    body = ""
    for i, (x, y) in enumerate(((100, 90), (260, 90), (180, 180))):
        a = i * 0.15
        body += pop(f'<circle cx="{x}" cy="{y}" r="44"/>', a, a + 0.12, "tf" if i == 1 else "pf")
        body += ring(x, y, 44, a, a + 0.2, "b" if i == 1 else "")
    body += ln("M180 36 V120 M130 150 L150 135 M230 150 L210 135", 0.5, 0.7, "dash")
    body += pop('<circle cx="260" cy="90" r="8"/>', 0.75, 0.85, "bf")
    body += ln("M306 36 L276 76", 0.8, 0.92, "b")
    return _fig("0 0 360 240", body, "cap")


def cap_compare():
    body = ln("M40 30 H160 V210 H40 Z", 0.0, 0.2) + ln("M200 30 H320 V210 H200 Z", 0.1, 0.3)
    body += pop('<rect x="44" y="142" width="272" height="24" rx="6"/>', 0.72, 0.8, "tf")
    for r in range(5):
        y = 56 + r * 32
        a = round(0.3 + r * 0.08, 3)
        diff = r == 3
        c = "b" if diff else ""
        body += ln(f"M58 {y} H142", a, round(a + 0.06, 3), c)
        body += ln(f"M218 {y} H{262 if diff else 302}", a, round(a + 0.06, 3), c)
        mid = (f"M172 {y - 6} L188 {y + 6} M188 {y - 6} L172 {y + 6}" if diff else f"M172 {y - 4} H188 M172 {y + 4} H188")
        body += ln(mid, round(a + 0.04, 3), round(a + 0.1, 3), c)
    return _fig("0 0 360 240", body, "cap")


def cap_proof():
    hot = {(1, 6), (1, 7), (2, 7)}
    body = ""
    for r in range(5):
        for c in range(12):
            x, y = 36 + c * 24, 40 + r * 24
            a = round(0.02 + (r * 12 + c) * 0.006, 3)
            if (r, c) in hot:
                body += pop(f'<rect x="{x}" y="{y}" width="18" height="18" rx="3"/>', round(a + 0.3, 3), round(a + 0.36, 3), "bf")
            body += ln(f"M{x} {y} H{x + 18} V{y + 18} H{x} Z", a, round(a + 0.05, 3), "b" if (r, c) in hot else "")
    body += ln("M168 172 V194 H218 V172", 0.7, 0.8, "b") + ln("M193 194 V212", 0.78, 0.84, "b")
    body += pop('<circle cx="193" cy="220" r="7"/>', 0.84, 0.92, "bf")
    return _fig("0 0 360 240", body, "cap")


CAPS = [cap_static, cap_runtime, cap_attribution, cap_compare, cap_proof]


def routing():
    xs = [60, 180, 300]
    body = pop('<circle cx="180" cy="22" r="14"/>', 0.0, 0.2, "bf")
    for i, x in enumerate(xs):
        a = round(0.2 + i * 0.15, 3)
        body += ln(f"M180 36 C180 60, {x} 50, {x} 86", a, round(a + 0.25, 3), "b dash")
        body += pop(f'<circle cx="{x}" cy="90" r="6"/>', round(a + 0.22, 3), round(a + 0.3, 3), "bf")
        body += f'<circle class="flow-dot" r="4" data-curve="180,36,180,60,{x},50,{x},86" data-off="{i / 3:.2f}"/>'
    return _fig("0 0 360 100", body, "routing ill-flow", scene="art flow")


def phone_scan():
    """Mobile hero: a wrapped build on a test device; a scan beam sweeps it; findings flow to the evidence store."""
    body = (
        '<rect class="ph-body" x="150" y="20" width="170" height="340" rx="28"/>'
        '<rect class="ph-screen" x="164" y="50" width="142" height="282" rx="10"/>'
        '<rect class="ph-notch" x="210" y="32" width="50" height="8" rx="4"/>'
        '<rect class="ph-layer" x="174" y="62" width="122" height="258" rx="8"/>'
        '<rect class="ph-block" x="188" y="80" width="94" height="44" rx="6"/>'
        '<rect class="ph-bar" x="188" y="140" width="94" height="8" rx="4"/>'
        '<rect class="ph-bar" x="188" y="158" width="70" height="8" rx="4"/>'
        '<rect class="ph-bar" x="188" y="176" width="82" height="8" rx="4"/>'
        '<rect class="ph-block" x="188" y="200" width="44" height="44" rx="6"/>'
        '<rect class="ph-block" x="238" y="200" width="44" height="44" rx="6"/>'
        '<rect class="ph-bar" x="188" y="262" width="94" height="8" rx="4"/>'
        '<rect class="ph-beam" x="168" y="56" width="134" height="3" rx="1.5"/>'
        '<path class="ph-link" d="M320 120 C370 120, 380 80, 430 80"/>'
        '<path class="ph-link" d="M320 190 C370 190, 380 190, 430 190"/>'
        '<path class="ph-link" d="M320 260 C370 260, 380 300, 430 300"/>'
        '<rect class="ph-store" x="430" y="56" width="60" height="48" rx="8"/>'
        '<rect class="ph-store" x="430" y="166" width="60" height="48" rx="8"/>'
        '<rect class="ph-store" x="430" y="276" width="60" height="48" rx="8"/>'
        '<path class="ph-tick" d="M448 80 l7 7 l13 -14 M448 190 l7 7 l13 -14 M448 300 l7 7 l13 -14"/>'
        '<path class="ph-dev" d="M40 150 h70 v80 h-70 z M58 176 h34 M58 192 h26 M58 208 h30"/>'
        '<path class="ph-link" d="M110 190 H150"/>'
        '<circle class="flow-dot" r="4" data-curve="320,120,370,120,380,80,430,80"/>'
        '<circle class="flow-dot" r="4" data-curve="320,190,370,190,380,190,430,190" data-off="0.33"/>'
        '<circle class="flow-dot" r="4" data-curve="320,260,370,260,380,300,430,300" data-off="0.66"/>'
    )
    return (f'<figure class="art phone" data-scene="phone" aria-hidden="true"><svg viewBox="0 0 520 380" fill="none" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</svg></figure>')


def ring_svg(icons):
    """About: four platform checks on a loop; each engagement goes round and feeds the next."""
    nodes = ""
    for i, name in enumerate(icons):
        a = i / 4 * 6.2832 - 1.5708
        x, y = 150 + 110 * math.cos(a), 150 + 110 * math.sin(a)
        nodes += (f'<g class="ring-node" transform="translate({x:.1f} {y:.1f})"><circle r="30"/>'
                  f'<g transform="translate(-14 -14) scale(0.5833)">{icon_paths(name)}</g></g>')
    return (f'<svg class="ring-svg" viewBox="0 0 300 300" fill="none" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            f'<circle class="ring-track" cx="150" cy="150" r="110"/>{nodes}<circle class="ring-dot" r="7" cx="150" cy="40"/></svg>')


def icon_paths(name):
    return "".join(f'<path d="{d}"/>' for d in ICONS[name].split("|"))
