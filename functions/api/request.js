// Cloudflare Pages Function: POST /api/request (WEBSITE-SPEC §7, BUILD-BRIEF §4).
//
// Validates the request form server-side and forwards it to FORM_WEBHOOK_URL.
// There is deliberately no default destination: where form data lands is a data-residency
// decision for counsel (DECISIONS D7). Until FORM_WEBHOOK_URL is set, the endpoint answers
// 503 and the page shows its "not sent" message, so no request is silently lost.
//
// Environment variables (Pages > Settings > Variables and Secrets):
//   FORM_WEBHOOK_URL    https endpoint that receives the JSON payload (required to accept submissions)
//   FORM_WEBHOOK_TOKEN  optional bearer token sent as Authorization header
//   SITE_ORIGIN         optional extra allowed origin, e.g. https://obscur4.online
//
// Rate limiting: add a Cloudflare rate-limiting rule on /api/request (BUILD-BRIEF target: 5 per IP per hour).
// Logging: never log field values (BUILD-BRIEF §4).

const TOPICS = ["awareness", "code", "mobile", "partner", "briefing", "other"];
const ORG_TYPES = ["", "bank", "fintech", "insurer", "payment", "consultancy", "other"];
const PLATFORMS = ["", "ios", "android", "both", "unsure"];
const NAME_RE = /^[\p{L}\p{M} .'\-]{2,100}$/u;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const SENT = { id: "/contact/sent/", en: "/contact/sent/" };
const BACK = { id: "/contact/", en: "/contact/" };
const FAIL = {
  id: "Permintaan Anda belum terkirim. Silakan kembali dan coba lagi nanti.",
  en: "Your request was not sent. Please go back and try again later.",
};

function validate(f) {
  const e = {};
  const s = (k) => (typeof f[k] === "string" ? f[k].trim() : "");
  if (!TOPICS.includes(s("topic"))) e.topic = "required";
  if (!s("name")) e.name = "required"; else if (!NAME_RE.test(s("name"))) e.name = "format";
  if (!s("email")) e.email = "required"; else if (s("email").length > 254 || !EMAIL_RE.test(s("email"))) e.email = "email";
  if (!s("organization")) e.organization = "required"; else if (s("organization").length < 2 || s("organization").length > 150) e.organization = "format";
  if (s("role").length > 100) e.role = "format";
  if (!ORG_TYPES.includes(s("org_type"))) e.org_type = "format";
  if (s("phone")) {
    const digits = s("phone").replace(/\D/g, "").length;
    if (!/^[0-9 +\-]+$/.test(s("phone")) || digits < 8 || digits > 15) e.phone = "phone";
  }
  if (!PLATFORMS.includes(s("platform"))) e.platform = "format";
  if (!s("message")) e.message = "required"; else if (s("message").length < 20 || s("message").length > 2000) e.message = "messageLen";
  if (!["id", "en"].includes(s("reply_language"))) e.reply_language = "required";
  if (s("consent") !== "yes") e.consent = "consent";
  return e;
}

function originAllowed(request, env) {
  const self = new URL(request.url).origin;
  const allowed = [self, env.SITE_ORIGIN].filter(Boolean);
  const origin = request.headers.get("Origin");
  if (origin) return allowed.includes(origin);
  const referer = request.headers.get("Referer");
  if (!referer) return false;
  try { return allowed.includes(new URL(referer).origin); } catch { return false; }
}

function respond(request, lang, ok, status, errors) {
  const wantsJson = (request.headers.get("Accept") || "").includes("application/json");
  if (wantsJson) {
    return new Response(JSON.stringify(ok ? { ok: true } : { ok: false, errors: errors || undefined }), {
      status, headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" },
    });
  }
  if (ok) return new Response(null, { status: 303, headers: { Location: SENT[lang] } });
  const body = `<!doctype html><html lang="${lang}"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">` +
    `<meta name="robots" content="noindex"><title>obscur4</title><p>${FAIL[lang]}</p><p><a href="${BACK[lang]}">&larr;</a></p></html>`;
  return new Response(body, { status, headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" } });
}

export async function onRequestPost({ request, env }) {
  let fields = {};
  try {
    const data = await request.formData();
    for (const [k, v] of data.entries()) if (typeof v === "string") fields[k] = v;
  } catch {
    return respond(request, "id", false, 400);
  }
  const lang = fields.lang === "en" ? "en" : "id";

  if (!originAllowed(request, env)) return respond(request, lang, false, 403);
  // Honeypot filled, or submitted faster than 3 s after page load (ts set by the page script; absent without JS).
  const ts = Number(fields.ts);
  if ((fields.website || "").length > 0 || (ts && Date.now() - ts < 3000)) return respond(request, lang, false, 400);

  const errors = validate(fields);
  if (Object.keys(errors).length) return respond(request, lang, false, 422, errors);

  if (!env.FORM_WEBHOOK_URL) {
    console.log(JSON.stringify({ event: "request_form", status: "not_configured" }));
    return respond(request, lang, false, 503);
  }

  const payload = {
    received_at: new Date().toISOString(),
    page_language: lang,
    topic: fields.topic.trim(),
    name: fields.name.trim(),
    email: fields.email.trim(),
    organization: fields.organization.trim(),
    role: (fields.role || "").trim(),
    org_type: fields.org_type || "",
    phone: (fields.phone || "").trim(),
    platform: fields.topic === "mobile" ? fields.platform || "" : "",
    message: fields.message.trim(),
    reply_language: fields.reply_language,
    consent: true,
  };
  try {
    const headers = { "Content-Type": "application/json" };
    if (env.FORM_WEBHOOK_TOKEN) headers.Authorization = `Bearer ${env.FORM_WEBHOOK_TOKEN}`;
    const res = await fetch(env.FORM_WEBHOOK_URL, { method: "POST", headers, body: JSON.stringify(payload) });
    if (!res.ok) throw new Error(`webhook ${res.status}`);
  } catch (err) {
    console.log(JSON.stringify({ event: "request_form", status: "delivery_failed", error: String(err.message || err).slice(0, 80) }));
    return respond(request, lang, false, 502);
  }
  console.log(JSON.stringify({ event: "request_form", status: "delivered", topic: payload.topic }));
  return respond(request, lang, true, 200);
}
