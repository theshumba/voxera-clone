/* LodgeHelm site analytics — PostHog.
 *
 * THE ONLY LINE YOU EVER EDIT IS THE NEXT ONE.
 * Paste the Project API key from PostHog (Settings > Project > Project API key).
 * It starts with "phc_". It is a public key and is safe in this file.
 * Until it is set, this file does nothing at all.
 */
var LH_POSTHOG_KEY = "PASTE_KEY_HERE";
var LH_POSTHOG_HOST = "https://eu.i.posthog.com"; // EU cloud: data stays in Europe

(function () {
  if (!LH_POSTHOG_KEY || LH_POSTHOG_KEY.indexOf("phc_") !== 0) return;

  var s = document.createElement("script");
  s.async = true;
  s.src = LH_POSTHOG_HOST.replace(".i.posthog.com", "-assets.i.posthog.com") + "/static/array.js";
  s.onload = function () {
    // array.js installs the real posthog on window; init once it is there.
    window.posthog.init(LH_POSTHOG_KEY, {
      api_host: LH_POSTHOG_HOST,
      defaults: "2026-06-25",      // includes history_change pageviews — this site is client-routed
      person_profiles: "identified_only", // anonymous visitors still counted, no profile stored
    });
    wire();
  };
  document.head.appendChild(s);

  function cap(name, props) {
    try { window.posthog.capture(name, props || {}); } catch (e) {}
  }

  function wire() {
    // 1. The two CTAs that matter, wherever they appear on the page.
    document.addEventListener(
      "click",
      function (e) {
        var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
        if (!a) return;
        var href = a.getAttribute("href") || "";
        // Framer duplicates nav text across breakpoints, so read the first
        // text element rather than the whole link.
        var t = a.querySelector("p") || a;
        var label = (t.textContent || "").trim().slice(0, 60);
        if (href.indexOf("calendly.com") > -1) cap("book_a_call_clicked", { label: label, href: href });
        else if (href.indexOf("app.lodgehelm.com") > -1) cap("app_clicked", { label: label, href: href });
        else if (href.indexOf("plan-your-safari") > -1) cap("plan_safari_clicked", { label: label });
      },
      true
    );

    // 2. The enquiry form on /plan-your-safari/. The form's own script swaps
    //    #done / #err into view on success / failure, so watch for that rather
    //    than duplicating its submit logic.
    watch("done", "enquiry_submitted");
    watch("err", "enquiry_failed");
  }

  function watch(id, event) {
    var el = document.getElementById(id);
    if (!el) return;
    var fired = false;
    new MutationObserver(function () {
      if (fired || !el.classList.contains("show")) return;
      fired = true;
      cap(event);
    }).observe(el, { attributes: true, attributeFilter: ["class"] });
  }
})();

/* Note: visitors running an ad blocker are not counted. Fixing that needs a
 * reverse proxy on our own domain, which GitHub Pages cannot do. Real traffic
 * is therefore a little higher than the number PostHog shows. */
