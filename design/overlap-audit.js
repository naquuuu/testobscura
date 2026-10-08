// Layout overlap audit. Paste into the console of any page on the local server (or run via the
// browser tool). Loads every page in iframes at several widths, with all motion scenes frozen at
// their final state (?seek=all:1), and reports:
//   text  - two different text runs whose line boxes intersect
//   box   - two bordered/filled boxes that intersect without one containing the other
//   spill - text that sticks out of its card/panel/button
//   hscroll - page wider than the viewport
async function overlapAudit(pages, widths) {
  const out = [];
  const area = (a, b) => Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)) *
                        Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
  for (const w of widths) for (const path of pages) {
    const f = document.createElement("iframe");
    f.style.cssText = `position:fixed;left:0;top:0;width:${w}px;height:900px;border:0;visibility:hidden`;
    document.body.appendChild(f);
    await new Promise(r => { f.onload = r; f.src = path + (path.includes("?") ? "&" : "?") + "seek=all:1"; });
    await new Promise(r => setTimeout(r, 120));
    const d = f.contentDocument, win = f.contentWindow;
    const visible = el => {
      for (let e = el; e && e !== d.body; e = e.parentElement) {
        const cs = win.getComputedStyle(e);
        if (cs.display === "none" || cs.visibility === "hidden" || e.hidden || e.classList.contains("sr-only") ||
            e.classList.contains("hp") || e.classList.contains("skip") || e.classList.contains("mcta") ||
            e.classList.contains("msheet-panel")) return false;
      }
      return true;
    };
    // text runs
    const runs = [];
    const walker = d.createTreeWalker(d.body, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      if (!n.nodeValue.trim() || !visible(n.parentElement)) continue;
      const r = d.createRange(); r.selectNodeContents(n);
      for (const rect of r.getClientRects()) if (rect.width > 1 && rect.height > 1) runs.push({ el: n.parentElement, rect, txt: n.nodeValue.trim().slice(0, 30) });
    }
    for (let i = 0; i < runs.length; i++) for (let j = i + 1; j < runs.length; j++) {
      const a = runs[i], b = runs[j];
      if (a.el === b.el) continue;
      if (area(a.rect, b.rect) > 6) out.push({ w, path, kind: "text", a: a.txt, b: b.txt });
    }
    // boxes
    const boxes = Array.from(d.querySelectorAll("main *, header *, footer *")).filter(el => {
      if (!visible(el)) return false;
      const cs = win.getComputedStyle(el);
      const filled = cs.backgroundColor !== "rgba(0, 0, 0, 0)" || parseFloat(cs.borderTopWidth) > 0 || parseFloat(cs.borderLeftWidth) > 0;
      const r = el.getBoundingClientRect();
      return filled && r.width > 4 && r.height > 4 && cs.position !== "fixed";
    });
    for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
      const A = boxes[i], B = boxes[j];
      if (A.contains(B) || B.contains(A)) continue;
      const ra = A.getBoundingClientRect(), rb = B.getBoundingClientRect();
      if (area(ra, rb) > 6) out.push({ w, path, kind: "box", a: A.className || A.tagName, b: B.className || B.tagName });
    }
    // spill: text outside its nearest card-like container
    for (const run of runs) {
      const box = run.el.closest(".card, .panel, .btn, .chip, .lane, .mail, .manifest, .steps li, .compare, .path-report, .stack-result, .form-success, .form-error, .pill span");
      if (!box) continue;
      const b = box.getBoundingClientRect();
      if (run.rect.right > b.right + 1 || run.rect.left < b.left - 1 || run.rect.bottom > b.bottom + 1 || run.rect.top < b.top - 1)
        out.push({ w, path, kind: "spill", a: run.txt, b: box.className });
    }
    if (d.documentElement.scrollWidth > w + 1) out.push({ w, path, kind: "hscroll", a: d.documentElement.scrollWidth + "px", b: "" });
    f.remove();
  }
  return out;
}
