/* obscur4.online motion engine. Graphics move; text never does (owner direction, DECISIONS D9).
   Each scene is render(root, v) - a pure function of time (ms) or scroll progress (plus layout), so any frame can
   be reproduced with ?seek=name:value. No-JS and reduced-motion visitors get complete static drawings. */
(function () {
  "use strict";
  var d = document, html = d.documentElement;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  html.classList.add("js");
  if (!reduce) html.classList.add("m");

  function clamp(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }
  function seg(p, a, b) { return clamp((p - a) / (b - a)); }
  function ease(t) { return 1 - Math.pow(1 - t, 3); }
  function easeIO(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function set(el, name, v) { if (el) el.style.setProperty(name, typeof v === "number" ? v.toFixed(4) : v); }
  function all(root, sel) { return Array.prototype.slice.call(root.querySelectorAll(sel)); }
  function attr(el, k, v) { if (el) el.setAttribute(k, v); }
  function rng(seed) {
    return function () {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  var seek = {};
  (new URLSearchParams(location.search).get("seek") || "").split(",").forEach(function (pair) {
    var kv = pair.split(":");
    if (kv.length === 2 && !isNaN(+kv[1])) seek[kv[0]] = +kv[1];
  });
  if (Object.keys(seek).length) html.classList.add("seek");
  function seekFor(name) { return seek.hasOwnProperty(name) ? seek[name] : (seek.hasOwnProperty("all") ? seek.all : null); }

  // ---------------------------------------------------------------- shared renderers
  function drawParts(root, q) {
    all(root, "[data-a]").forEach(function (el) {
      set(el, "--k", ease(seg(q, +el.getAttribute("data-a"), +el.getAttribute("data-b"))));
    });
  }
  function bezier(c, u) {
    var v = 1 - u;
    return [v * v * v * c[0] + 3 * v * v * u * c[2] + 3 * v * u * u * c[4] + u * u * u * c[6],
            v * v * v * c[1] + 3 * v * v * u * c[3] + 3 * v * u * u * c[5] + u * u * u * c[7]];
  }
  function flowDots(root, ms) {
    all(root, ".flow-dot").forEach(function (dot) {
      var off = +(dot.getAttribute("data-off") || 0), u = ((ms / 2600) + off) % 1, p;
      if (dot.hasAttribute("data-curve")) p = bezier(dot.getAttribute("data-curve").split(",").map(Number), easeIO(u));
      else {
        var f = dot.getAttribute("data-from").split(",").map(Number), t = dot.getAttribute("data-to").split(",").map(Number);
        p = [lerp(f[0], t[0], easeIO(u)), lerp(f[1], t[1], easeIO(u))];
      }
      attr(dot, "cx", p[0].toFixed(1)); attr(dot, "cy", p[1].toFixed(1));
      set(dot, "--k", Math.sin(u * Math.PI));
    });
  }

  var SCENES = {
    // Drawings: lines draw and shapes pop, in mechanical steps, once, when the figure enters the viewport.
    art: { mode: "once", dur: 2200, render: function (root, p) { drawParts(root, p); } },
    // Continuous flows (dots along connectors).
    flow: { mode: "loop", render: function (root, ms) { flowDots(root, ms); } },
    // Hero kicker: a dotted leader runs out in steps.
    kicker: { mode: "once", dur: 1100, render: function (root, p) { set(root.querySelector(".dots"), "--k", easeIO(p)); } },

    // Home hero: a message moves through an organization; some people report it (blue).
    net: { mode: "loop", init: function (root) {
      var pts = root.getAttribute("data-pts").split(";").map(function (s) { return s.split(",").map(Number); });
      var adj = pts.map(function () { return []; });
      root.getAttribute("data-edges").split(";").forEach(function (s) {
        var e = s.split(",").map(Number); adj[e[0]].push(e[1]); adj[e[1]].push(e[0]);
      });
      var r = rng(11), walk = [0], rep = [false];
      for (var h = 1; h < 600; h++) {
        var cur = walk[h - 1], prev = h > 1 ? walk[h - 2] : -1;
        var nb = adj[cur].filter(function (x) { return x !== prev; });
        if (!nb.length) nb = adj[cur];
        walk.push(nb[Math.floor(r() * nb.length)]); rep.push(r() < 0.38);
      }
      var edges = {};
      all(root, ".net-e").forEach(function (el) { edges[el.getAttribute("data-e")] = el; });
      root._net = { pts: pts, walk: walk, rep: rep, nodes: all(root, ".net-n"), msg: root.querySelector(".net-msg"), edges: edges, lit: [] };
    }, render: function (root, ms) {
      var N = root._net, HOP = 1100, hop = Math.floor(ms / HOP) % (N.walk.length - 8), f = easeIO((ms % HOP) / HOP);
      var a = N.pts[N.walk[hop]], b = N.pts[N.walk[hop + 1]];
      attr(N.msg, "transform", "translate(" + lerp(a[0], b[0], f).toFixed(1) + " " + lerp(a[1], b[1], f).toFixed(1) + ")");
      var halo = {}, blue = {};
      for (var k = 0; k < 7 && hop - k >= 0; k++) {
        var node = N.walk[hop - k + 1], age = k + (1 - f);
        if (k === 0 && f < 0.85) continue;
        halo[node] = Math.max(halo[node] || 0, clamp(1 - age / 2.4));
        if (N.rep[hop - k + 1]) blue[node] = Math.max(blue[node] || 0, clamp(1 - age / 7));
      }
      N.nodes.forEach(function (g, i) { set(g, "--h", halo[i] || 0); set(g, "--r", blue[i] || 0); });
      N.lit.forEach(function (el) { set(el, "--e", 0); });
      N.lit = [];
      for (var q = 0; q < 4 && hop - q >= 0; q++) {
        var u = N.walk[hop - q], v = N.walk[hop - q + 1], key = Math.min(u, v) + "-" + Math.max(u, v), el = N.edges[key];
        if (el) { set(el, "--e", q === 0 ? 1 : clamp(1 - (q - 1 + f) / 3)); N.lit.push(el); }
      }
    } },

    // Home story: one graphic transforms through five steps as the reader scrolls (t in 0..5).
    story: { mode: "steps", map: function (raw, n, before) { return before ? raw : Math.min(5, raw + 0.85 + (raw >= n - 1 ? 0.15 : 0)); },
      render: function (root, t) {
      var svg = root.querySelector("[data-stage]"), card = svg.querySelector(".st-card");
      var cin = ease(seg(t, 0, 0.7)), cout = easeIO(seg(t, 2, 2.45));
      attr(card, "transform", "translate(280 175) scale(" + (lerp(0.92, 1, cin) * lerp(1, 0.12, cout)).toFixed(4) + ") translate(-280 -175)");
      set(card, "--o", cin * (1 - seg(t, 2.25, 2.45)));
      for (var i = 1; i <= 3; i++) {
        set(svg.querySelector(".m" + i), "--k", ease(seg(t, 0.95 + (i - 1) * 0.28, 1.2 + (i - 1) * 0.28)));
        set(svg.querySelector(".p" + i), "--k", ease(seg(t, 1.1 + (i - 1) * 0.28, 1.25 + (i - 1) * 0.28)));
      }
      var dot = svg.querySelector(".st-dot");
      set(dot, "--o", seg(t, 2.2, 2.35) * (1 - seg(t, 2.6, 2.75)));
      attr(dot, "cx", 280); attr(dot, "cy", 175);
      var reported = { 1: 1, 4: 1, 8: 1, 9: 1, 14: 1, 17: 1, 20: 1, 22: 1 };
      var group = easeIO(seg(t, 3, 3.7)), toReport = easeIO(seg(t, 4, 4.45));
      all(svg, ".st-p").forEach(function (g) {
        var i = +g.getAttribute("data-i"), r = +g.getAttribute("data-r"), c = +g.getAttribute("data-c");
        var x0 = 130 + c * 60, y0 = 100 + r * 52;
        var dist = Math.sqrt(Math.pow((x0 - 280) / 150, 2) + Math.pow((y0 - 178) / 80, 2)) / 1.42;
        var appear = ease(seg(t, 2.3 + dist * 0.45, 2.5 + dist * 0.45));
        var gi = i % 3, j = Math.floor(i / 3), x1 = 60 + gi * 160 + 36 + (j % 2) * 48, y1 = 160 + Math.floor(j / 2) * 36;
        var x = lerp(lerp(x0, x1, group), 280, toReport), y = lerp(lerp(y0, y1, group), 170, toReport);
        attr(g, "transform", "translate(" + x.toFixed(1) + " " + y.toFixed(1) + ") scale(" + (appear * lerp(1, 0.2, toReport)).toFixed(3) + ")");
        set(g, "--o", appear * (1 - seg(t, 4.2, 4.45)));
        set(g, "--b", reported[i] ? ease(seg(t, 2.65, 2.95)) : 0);
      });
      all(svg, ".st-group").forEach(function (g, gi) {
        set(g, "--k", ease(seg(t, 3.3 + gi * 0.1, 3.75 + gi * 0.1)) * (1 - seg(t, 4.05, 4.3)));
      });
      var rep = svg.querySelector(".st-report"), rin = ease(seg(t, 4.25, 4.7));
      attr(rep, "transform", "translate(0 " + lerp(18, 0, rin).toFixed(1) + ")");
      set(rep, "--o", rin);
      set(svg.querySelector(".st-seal"), "--k", ease(seg(t, 4.65, 4.9)));
      set(svg.querySelector(".st-tick"), "--k", ease(seg(t, 4.8, 5)));
      all(root, "[data-step]").forEach(function (li, n) { li.classList.toggle("is-active", n === Math.min(4, Math.floor(t))); });
    } },

    // Platform: the plate for the layer being read lifts and lights; a probe sits on it (t in 0..6).
    layerscroll: { mode: "steps", map: function (raw, n, before) { return before ? 0 : raw; }, render: function (root, t) {
      var svg = root.querySelector(".iso-svg"), plates = all(svg, ".plate");
      var cx = +svg.getAttribute("data-cx"), top = +svg.getAttribute("data-top"), gap = +svg.getAttribute("data-gap");
      var i = Math.max(0, Math.min(plates.length - 1, Math.round(t)));
      plates.forEach(function (pl, n) { pl.classList.toggle("is-active", n === i); });
      attr(svg.querySelector(".iso-probe"), "transform", "translate(" + cx + " " + (top + t * gap).toFixed(1) + ")");
      all(root, "[data-step]").forEach(function (li, n) { li.classList.toggle("is-active", n === i); });
    } },

    // Compact stack: a probe cycles through the layers, pausing at authorization; the list marker follows.
    teaser: { mode: "loop", render: function (root, ms) {
      var svg = root.querySelector(".iso-svg"); if (!svg) return;
      var plates = all(svg, ".plate"), cx = +svg.getAttribute("data-cx"), top = +svg.getAttribute("data-top"), gap = +svg.getAttribute("data-gap");
      var u = (ms % 9000) / 9000, s;
      if (u < 0.08) s = ease(u / 0.08);
      else if (u < 0.28) s = 1;
      else if (u < 0.85) s = 1 + 5 * easeIO((u - 0.28) / 0.57);
      else s = 6;
      var probe = svg.querySelector(".iso-probe");
      attr(probe, "transform", "translate(" + cx + " " + (top + s * gap).toFixed(1) + ")");
      set(probe, "--o", u > 0.93 ? 1 - (u - 0.93) / 0.07 : 1);
      var at = Math.round(s);
      plates.forEach(function (pl, n) { pl.classList.toggle("is-active", n === at); pl.classList.toggle("is-checked", n === 1 && u > 0.14); });
      all(root, ".teaser-list li").forEach(function (li, n) { li.classList.toggle("is-active", n === at); });
    } },

    // Awareness timeline: a dot carries the programme along the track; each station's icon draws when reached.
    timeline: { mode: "scroll", render: function (root, p) {
      var pp = easeIO(seg(p, 0.05, 0.8));
      set(root, "--p", pp);
      set(root, "--dot", 1 - seg(pp, 0.94, 1));
      all(root, ".tl-station").forEach(function (st, i) {
        var reached = seg(pp, i / 4 - 0.06, i / 4 + 0.02);
        st.classList.toggle("is-reached", reached > 0.5);
        drawParts(st, reached);
      });
    } },

    // Mobile comparison: the differing cell is outlined and the cause bar is drawn (text stays still).
    compare: { mode: "scroll", render: function (root, p) {
      set(root.querySelector(".is-diff"), "--f", ease(seg(p, 0.3, 0.55)));
      set(root.querySelector(".is-out"), "--f", ease(seg(p, 0.5, 0.7)));
      set(root.querySelector(".verdict"), "--k", ease(seg(p, 0.65, 0.9)));
    } },

    // Evidence manifest: each file is checked off in the order it is produced.
    bundle: { mode: "once", dur: 3000, render: function (root, p) {
      all(root, ".files li").forEach(function (li, i) { set(li, "--k", ease(seg(p, 0.08 + i * 0.12, 0.18 + i * 0.12))); });
      set(root.querySelector(".files"), "--p", ease(seg(p, 0.05, 0.95)));
    } },

    // Mobile hero: a scan beam sweeps the app; the protection layer pulses; findings flow out.
    phone: { mode: "loop", render: function (root, ms) {
      var u = (ms % 4200) / 4200;
      set(root, "--scan", easeIO(u < 0.5 ? u * 2 : 2 - u * 2));
      set(root, "--pulse", 0.5 + 0.5 * Math.sin(ms / 700));
      flowDots(root, ms);
    } },

    // Ring loop (About): a dot circles four checks; the legend marker follows.
    ring: { mode: "loop", render: function (root, ms) {
      var u = (ms % 8000) / 8000, n = 4, idx = Math.floor(u * n), f = easeIO((u * n) % 1);
      var a = ((idx + f) / n) * Math.PI * 2 - Math.PI / 2, R = 110, dot = root.querySelector(".ring-dot");
      attr(dot, "cx", (150 + R * Math.cos(a)).toFixed(1)); attr(dot, "cy", (150 + R * Math.sin(a)).toFixed(1));
      var at = f > 0.92 ? (idx + 1) % n : idx;
      all(root, ".ring-node").forEach(function (nd, i) { nd.classList.toggle("is-active", i === at); });
      all(root, ".ring-list li").forEach(function (li, i) { li.classList.toggle("is-active", i === at); });
    } },

    // Contact journey: a request travels down three stages; the stage marker follows.
    journey: { mode: "loop", render: function (root, ms) {
      var u = (ms % 7200) / 7200, n = 3, pos = u * n, idx = Math.min(n - 1, Math.floor(pos));
      set(root.querySelector(".journey-rail"), "--p", clamp(easeIO(clamp(pos / (n - 0.4)))));
      all(root, ".journey li").forEach(function (li, i) { li.classList.toggle("is-active", i === idx); li.classList.toggle("is-done", i < idx); });
    } }
  };

  // ---------------------------------------------------------------- scene runner
  function progressOf(el) {
    var r = el.getBoundingClientRect(), vh = window.innerHeight;
    return clamp((vh * 0.9 - r.top) / (r.height * 0.7 + vh * 0.35));
  }
  // Steps progress: 0 at the first step's centre crossing mid-screen, n-1 at the last one's.
  function stepsRaw(root) {
    var items = all(root, "[data-step]"), n = items.length;
    if (!n) return { raw: 0, before: true, n: 1 };
    var mid = window.innerHeight * 0.55;
    var c = items.map(function (el) { var r = el.getBoundingClientRect(); return r.top + r.height / 2; });
    if (mid < c[0]) return { raw: clamp(1 - (c[0] - mid) / (window.innerHeight * 0.5)) * 0.85, before: true, n: n };
    for (var i = 0; i < n - 1; i++) if (mid < c[i + 1]) return { raw: i + (mid - c[i]) / (c[i + 1] - c[i]), before: false, n: n };
    return { raw: n - 1, before: false, n: n };
  }

  function watch(el, cb, threshold) {
    if (!("IntersectionObserver" in window)) { cb(true); return; }
    new IntersectionObserver(function (es) { es.forEach(function (e) { cb(e.isIntersecting); }); }, { threshold: threshold || 0 }).observe(el);
  }

  function initScenes() {
    var scroll = [], loops = [];
    all(d, "[data-scene]").forEach(function (root) {
      root.getAttribute("data-scene").split(" ").forEach(function (name) {
        var sc = SCENES[name]; if (!sc) return;
        if (name === "art" && root.closest("[data-tabs]")) return;  // the tab explorer plays its own drawings
        if (sc.init) sc.init(root);
        var fixed = seekFor(name);
        if (fixed !== null) { sc.render(root, sc.mode === "loop" ? fixed * 1000 : fixed); return; }
        if (sc.mode === "steps") { scroll.push({ root: root, sc: sc, last: -99, cur: null }); return; }
        if (reduce) return;
        if (sc.mode === "scroll") scroll.push({ root: root, sc: sc, last: -99, cur: null });
        else if (sc.mode === "loop") loops.push({ root: root, sc: sc, on: false, t0: 0, acc: 0 });
        else {
          sc.render(root, 0);
          var started = false;
          watch(root, function (vis) {
            if (!vis || started) return; started = true;
            var t0 = performance.now() + 150;
            (function tick(now) { var p = clamp((now - t0) / sc.dur); sc.render(root, p); if (p < 1) requestAnimationFrame(tick); })(t0);
          }, 0.3);
        }
      });
      root.classList.add("is-init");
    });

    loops.forEach(function (L) { watch(L.root, function (vis) { L.on = vis; if (!vis) L.t0 = 0; }, 0.05); });
    if (loops.length) (function frame(now) {
      loops.forEach(function (L) {
        if (!L.on) return;
        if (!L.t0) L.t0 = now - L.acc;
        L.acc = now - L.t0;
        L.sc.render(L.root, L.acc);
      });
      requestAnimationFrame(frame);
    })(performance.now());

    // Scroll-driven scenes follow the scroll position with exponential smoothing, so wheel notches and
    // trackpad flicks become one continuous movement (time constant TAU ms).
    var TAU = 140, running = false, lastT = 0;
    function target(s) {
      if (s.sc.mode === "steps") {
        var st = stepsRaw(s.root), v = Math.max(0, s.sc.map(st.raw, st.n, st.before));
        return reduce ? Math.round(v) : v;
      }
      return progressOf(s.root);
    }
    function frame(now) {
      var dt = lastT ? Math.min(64, now - lastT) : 16, a = 1 - Math.exp(-dt / TAU), busy = false;
      lastT = now;
      scroll.forEach(function (s) {
        var t = target(s);
        if (s.cur === null || reduce) s.cur = t;
        else s.cur += (t - s.cur) * a;
        if (Math.abs(t - s.cur) < 0.0004) s.cur = t; else busy = true;
        if (Math.abs(s.cur - s.last) > 0.0002) { s.sc.render(s.root, s.cur); s.last = s.cur; }
      });
      if (busy) requestAnimationFrame(frame); else { running = false; lastT = 0; }
    }
    function onScroll() { if (!running) { running = true; requestAnimationFrame(frame); } }
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", function () { scroll.forEach(function (s) { s.last = -99; }); onScroll(); });
  }

  // ---------------------------------------------------------------- tabs (capability explorer)
  function initTabs() {
    all(d, "[data-tabs]").forEach(function (box) {
      var tabs = all(box, '[role="tab"]'), panels = all(box, '[role="tabpanel"]'), cur = 0, timer = null, paused = false;
      function play(panel) {
        var art = panel.querySelector('[data-scene~="art"]');
        if (!art || reduce) return;
        var t0 = performance.now();
        (function tick(now) { var q = clamp((now - t0) / 1600); drawParts(art, q); if (q < 1) requestAnimationFrame(tick); })(t0);
      }
      function restart() {
        if (reduce || paused) return;
        box.classList.remove("is-running"); void box.offsetWidth; box.classList.add("is-running");
        clearTimeout(timer);
        timer = setTimeout(function () { show((cur + 1) % tabs.length); }, 6500);
      }
      function show(i, focus) {
        cur = i;
        tabs.forEach(function (t, n) { t.setAttribute("aria-selected", n === i ? "true" : "false"); t.tabIndex = n === i ? 0 : -1; });
        panels.forEach(function (p, n) {
          p.hidden = n !== i;
          var art = p.querySelector('[data-scene~="art"]');
          if (art && n !== i && !reduce) drawParts(art, 0);
          if (n === i) play(p);
        });
        if (focus) tabs[i].focus();
        restart();
      }
      function stop() { paused = true; clearTimeout(timer); box.classList.add("is-paused"); }
      tabs.forEach(function (t, i) {
        t.addEventListener("click", function () { stop(); show(i); });
        t.addEventListener("keydown", function (e) {
          if (e.key === "ArrowRight" || e.key === "ArrowDown") { e.preventDefault(); stop(); show((cur + 1) % tabs.length, true); }
          if (e.key === "ArrowLeft" || e.key === "ArrowUp") { e.preventDefault(); stop(); show((cur - 1 + tabs.length) % tabs.length, true); }
        });
      });
      box.classList.add("tabs-on");
      panels.forEach(function (p, n) { p.hidden = n !== 0; });
      tabs.forEach(function (t, n) { t.setAttribute("aria-selected", n === 0 ? "true" : "false"); t.tabIndex = n === 0 ? 0 : -1; });
      watch(box, function (vis) { if (vis && !box._started) { box._started = true; show(0); } }, 0.3);
    });
  }

  // ---------------------------------------------------------------- header, nav, sheet, sticky CTA
  function initChrome() {
    var header = d.querySelector("[data-header]"), nav = d.querySelector("[data-nav]"), ind = nav && nav.querySelector(".nav-ind");
    var sheet = d.querySelector("[data-sheet]"), mcta = d.querySelector("[data-mcta]"), closingBand = d.querySelector(".closing");
    function frame() {
      var y = window.scrollY, max = d.documentElement.scrollHeight - window.innerHeight;
      if (header) { header.classList.toggle("is-scrolled", y > 8); set(header, "--sp", max > 0 ? clamp(y / max) : 0); }
      if (mcta) {
        var nearEnd = closingBand && closingBand.getBoundingClientRect().top < window.innerHeight;
        mcta.classList.toggle("is-on", y > window.innerHeight * 0.6 && !nearEnd && !(sheet && sheet.open));
      }
    }
    var q = false;
    window.addEventListener("scroll", function () { if (!q) { q = true; requestAnimationFrame(function () { q = false; frame(); }); } }, { passive: true });
    frame();
    if (nav && ind) {
      var current = nav.querySelector('a[aria-current="page"]');
      var place = function (a) {
        if (!a) { set(ind, "--o", 0); return; }
        set(ind, "--x", (a.offsetLeft + 11) + "px"); set(ind, "--w", (a.offsetWidth - 22) + "px"); set(ind, "--o", 1);
      };
      place(current);
      requestAnimationFrame(function () { requestAnimationFrame(function () { nav.classList.add("nav-ready"); }); });
      all(nav, "a").forEach(function (a) { a.addEventListener("mouseenter", function () { place(a); }); a.addEventListener("focus", function () { place(a); }); });
      nav.addEventListener("mouseleave", function () { place(current); });
      window.addEventListener("resize", function () { place(current); });
    }
    if (sheet) {
      sheet.addEventListener("toggle", function () { html.classList.toggle("sheet-open", sheet.open); frame(); });
      d.addEventListener("keydown", function (e) { if (e.key === "Escape" && sheet.open) { sheet.open = false; sheet.querySelector("summary").focus(); } });
      all(sheet, "a").forEach(function (a) { a.addEventListener("click", function () { sheet.open = false; }); });
    }
  }

  function boot() {
    var y = +new URLSearchParams(location.search).get("y");  // verification only: ?y=1200 scrolls before scenes start
    if (y) window.scrollTo(0, y);
    initChrome(); initTabs(); initScenes();
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", boot); else boot();
  window.__seek = function (name, v) { all(d, '[data-scene~="' + name + '"]').forEach(function (r) { SCENES[name].render(r, v); }); };
})();
