# obscur4.online website

Static bilingual site, graphics-led with motion (DECISIONS D9-D14). Bahasa Indonesia is the default at `/`, English sits under `/en/` (this reverses D12, English-only). Copy lives in `content.py` and `content_platform.py` as (Bahasa Indonesia, English) tuples, graphics in `illustrations.py`, motion in `assets/motion.js`. No framework and no npm dependencies. A Python script generates plain HTML into `public/`, and one Cloudflare Pages Function handles the request form.

```
website/
  content.py            page copy, (ID, EN) tuples; both languages are built  <- edit copy here
  content_platform.py   Platform page copy, (ID, EN) tuples
  illustrations.py      animated SVG graphics
  build.py              generator + quality gates
  release.json          release flags (contact email, sign-offs, attested claims)
  assets/               site.css, site.js, favicon.svg
  functions/api/request.js   Cloudflare Pages Function for POST /api/request
  public/               build output = what gets deployed (regenerated on every build)
```

## Build and view locally

```bash
python build.py
```

```bash
python -m http.server 8000 -d public
```

Open http://localhost:8000 (Bahasa Indonesia) or http://localhost:8000/en/ (English). Use a local server rather than opening the files directly, because links are root-relative. Locally the form shows its "not sent" message, since `/api/request` only exists on Cloudflare.

**Production vs release.** `python build.py` makes the production site but keeps it out of search engines (noindex) until the release gates pass.

**Old notes (preview mode):**
- `python build.py` produces a **preview** build:
  - a yellow "Preview" bar on every page;
  - pending items (HOLD) highlighted;
  - `noindex` on every page, `robots.txt` disallowing everything, and an `X-Robots-Tag: noindex` header.
- `python build.py --release` refuses to build until every release gate passes:
  - no HOLD left in `content.py`;
  - `contact_email` set;
  - legal sign-off and native-speaker review recorded;
  - claims C1-C11 attested (WEBSITE-SPEC §9).

## Deploy on Cloudflare Pages (for whoever holds the obscur4.online zone)

Create the Pages project in **the same Cloudflare account that holds the domain**, so the custom domain hooks up automatically.

**Option A: Wrangler CLI (simplest; includes the form function)**

Run these from the `website/` folder:

```bash
python build.py
```

```bash
npx wrangler pages deploy public --project-name obscur4
```

Wrangler picks up `functions/` automatically when it runs from this folder. Do **not** use the dashboard's drag-and-drop upload: it deploys `public/` without the form function.

**Option B: Git integration**
1. Push the repo.
2. In Pages, connect it with:
   - Root directory: `website`
   - Build command: `python build.py`
   - Build output directory: `public`
3. If the build image has no Python, commit the prebuilt `public/` and leave the build command empty.

**After the first deploy**
1. **Stay on the `*.pages.dev` URL while the site is a preview build.** Attach `obscur4.online` under Pages → Custom domains only when the release build passes. If it is attached earlier, the preview build still sends `noindex` and shows the Preview bar, so nothing is indexed.
2. **Form delivery.** Set `FORM_WEBHOOK_URL` (plus an optional `FORM_WEBHOOK_TOKEN`) under Pages → Settings → Variables and Secrets.
   - The function POSTs each submission as JSON to that URL.
   - Until it is set, the form answers "not sent", so no request is silently lost.
   - **Where that URL stores data is a data-residency decision for counsel** (DECISIONS D7, in-Indonesia hosting assumed). Do not point it at an arbitrary SaaS without that sign-off.
3. **Rate limiting.** Add a rule under Security → WAF → Rate limiting rules for path `/api/request`. The target is 5 requests per IP per hour; use the closest period your plan allows.
4. **Headers.** `public/_headers` sets the CSP, HSTS and the other security headers (BUILD-BRIEF §11). Keep "Always Use HTTPS" on for the zone.
5. **Check after deploy:**
   - every page loads in ID and EN;
   - the language switcher lands on the counterpart page;
   - `/.well-known/security.txt` is served;
   - an unknown path shows the 404 page;
   - one test form submission reaches the webhook (or shows "not sent" if it is not configured).

## Quality gates run on every build

Hero headline ≤ 12 words and subline ≤ 25. Banned wording, competitor and chat-product names, prices, and citation residue are rejected (BUILD-BRIEF §8). Release builds also enforce the HOLD, contact, legal, review and attestation gates.

## Not included yet (by design)
- **Analytics:** the spec calls for self-hosted, cookieless analytics in a Jakarta region (BUILD-BRIEF §6). Nothing is wired in, so there are no third-party requests.
- **Open Graph image:** a text-only card per locale is specified. Pages currently use `twitter:card=summary` without an image.
- **Copy:** all Bahasa Indonesia copy still needs native-speaker review before release, including the new Secure development page and the Platform page, whose Indonesian side was written later.
- **Old English URLs:** the English-only preview served English at the root. `_redirects` sends those paths (for example `/awareness-phishing/`) to their `/en/` pages.

## Motion and verification
- Only graphics animate; text is static. Visitors with "reduce motion" switched on see complete, still drawings.
- Freeze any animation for review: `?seek=all:1`, or e.g. `?seek=story:2.5` (home scroll story) or `?seek=net:4` (seconds into the hero loop).
- `design/shoot.py` captures stills with headless Chrome using a throwaway profile. In Git Bash, run it with `MSYS_NO_PATHCONV=1` so URL paths are not rewritten.
- `design/overlap-audit.js` checks every page for overlapping text and boxes and for horizontal scroll.

## Before launch
- Create the mailbox **hello@obscur4.online**; Cloudflare Email Routing can forward it.
- Set `FORM_WEBHOOK_URL` for the request form.
- When counsel has signed off and claims C1-C12 are attested, update `release.json` and run `python build.py --release`.
