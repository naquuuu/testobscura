// Request form enhancement (WEBSITE-SPEC §7). The form also works without JS: native
// validation plus a POST to /api/request that answers with a 303 to the success page.
(function () {
  "use strict";
  var form = document.getElementById("request-form");
  if (!form) return;

  var msg = {
    required: form.dataset.errRequired,
    email: form.dataset.errEmail,
    consent: form.dataset.errConsent,
    format: form.dataset.errFormat,
    messageLen: form.dataset.errMessageLen,
    phone: form.dataset.errPhone
  };
  var TOPICS = ["awareness", "code", "mobile", "partner", "briefing", "other"];
  var NAME_RE = /^[\p{L}\p{M} .'\-]{2,100}$/u;
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  form.setAttribute("novalidate", "");
  form.elements.ts.value = String(Date.now());

  // Preselect topic from ?topic= (unknown values ignored) and show the platform field only for mobile.
  var q = new URLSearchParams(location.search).get("topic");
  if (q && TOPICS.indexOf(q) !== -1) form.elements.topic.value = q;
  var platformField = form.querySelector('[data-field="platform"]');
  function syncPlatform() { platformField.hidden = form.elements.topic.value !== "mobile"; }
  form.addEventListener("change", function (e) { if (e.target.name === "topic") syncPlatform(); });
  syncPlatform();

  function val(name) {
    var el = form.elements[name];
    return el && typeof el.value === "string" ? el.value.trim() : "";
  }

  function check() {
    var errors = {};
    if (TOPICS.indexOf(val("topic")) === -1) errors.topic = msg.required;
    var name = val("name");
    if (!name) errors.name = msg.required; else if (!NAME_RE.test(name)) errors.name = msg.format;
    var email = val("email");
    if (!email) errors.email = msg.required; else if (email.length > 254 || !EMAIL_RE.test(email)) errors.email = msg.email;
    var org = val("organization");
    if (!org) errors.organization = msg.required; else if (org.length < 2 || org.length > 150) errors.organization = msg.format;
    if (val("role").length > 100) errors.role = msg.format;
    var phone = val("phone");
    if (phone) {
      var digits = phone.replace(/\D/g, "").length;
      if (!/^[0-9 +\-]+$/.test(phone) || digits < 8 || digits > 15) errors.phone = msg.phone;
    }
    var message = val("message");
    if (!message) errors.message = msg.required; else if (message.length < 20 || message.length > 2000) errors.message = msg.messageLen;
    if (!form.querySelector('input[name="reply_language"]:checked')) errors.reply_language = msg.required;
    if (!form.elements.consent.checked) errors.consent = msg.consent;
    return errors;
  }

  function show(errors) {
    var first = null;
    form.querySelectorAll("[data-field]").forEach(function (wrap) {
      var name = wrap.getAttribute("data-field");
      var err = document.getElementById("err-" + name);
      var control = wrap.querySelector("input, select, textarea");
      if (errors[name]) {
        err.textContent = errors[name];
        err.hidden = false;
        if (control) control.setAttribute("aria-invalid", "true");
        if (!first) first = control;
      } else {
        err.textContent = "";
        err.hidden = true;
        if (control) control.removeAttribute("aria-invalid");
      }
    });
    return first;
  }

  var formError = document.getElementById("form-error");
  var success = document.getElementById("form-success");
  var live = document.getElementById("form-live");
  var button = form.querySelector('button[type="submit"]');

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    formError.hidden = true;
    var first = show(check());
    if (first) { first.focus(); return; }
    button.disabled = true;
    fetch(form.action, {
      method: "POST",
      body: new FormData(form),
      headers: { "Accept": "application/json" },
      credentials: "same-origin"
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (data) {
        if (res.ok && data.ok) {
          form.hidden = true;
          success.hidden = false;
          success.focus();
          live.textContent = success.textContent;
          return;
        }
        if (data.errors) {
          var mapped = {};
          Object.keys(data.errors).forEach(function (k) { mapped[k] = msg[data.errors[k]] || msg.format; });
          var f = show(mapped);
          if (f) { f.focus(); return; }
        }
        throw new Error("send failed");
      });
    }).catch(function () {
      formError.hidden = false;
      live.textContent = formError.textContent;
    }).then(function () { button.disabled = false; });
  });
})();
