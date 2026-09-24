/* Shared EU PostHog project 208594. Megamind separates each business by website host. */
(() => {
  const host = location.hostname.replace(/^www\./, '');
  if (!['marsadesk.com', 'lodgehelm.com', 'sahemstrategy.com'].includes(host)) return;
  const showNotice = () => {
    const footers = document.querySelectorAll('footer');
    const places = footers.length ? footers : [document.body];
    for (const footer of places) {
      if (footer.querySelector('[data-site-analytics-notice]')) continue;
      const note = document.createElement('p');
      note.dataset.siteAnalyticsNotice = '1';
      note.style.cssText = 'padding:12px 16px;text-align:center;font-size:12px;opacity:.75';
      const link = document.createElement('a');
      link.href = '/analytics-privacy.html';
      link.textContent = 'Site analytics and how to turn it off';
      note.append(link);
      footer.append(note);
    }
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', showNotice, { once: true });
  else showNotice();
  window.addEventListener('load', () => setTimeout(showNotice, 1000), { once: true });
  try { if (localStorage.getItem('site_analytics_off') === '1') return; } catch { return; }
  if (navigator.doNotTrack === '1' || navigator.globalPrivacyControl === true) return;

  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split('.');2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement('script')).type='text/javascript',p.crossOrigin='anonymous',p.async=!0,p.src=s.api_host.replace('.i.posthog.com','-assets.i.posthog.com')+'/static/array.js',(r=t.getElementsByTagName('script')[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a='posthog',u.people=u.people||[],u.toString=function(t){var e='posthog';return'posthog'!==a&&(e+='.'+a),t||(e+=' (stub)'),e},u.people.toString=function(){return u.toString(1)+'.people (stub)'},o='init capture'.split(' '),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
  posthog.init('phc_xpgg4xbpp4mCYL2nVT7QUjYBCR34sckhqjiSYbpiDYy5', {
    api_host: 'https://eu.i.posthog.com',
    person_profiles: 'identified_only',
    capture_pageview: true,
    autocapture: false,
    disable_session_recording: true,
    respect_dnt: true,
    persistence: 'sessionStorage',
  });

  document.addEventListener('click', event => {
    const target = event.target instanceof Element ? event.target.closest('a[href],button') : null;
    if (!target) return;
    const detail = { page: location.pathname, kind: target.tagName.toLowerCase() };
    if (target instanceof HTMLAnchorElement) {
      const href = target.getAttribute('href') || '';
      if (href.startsWith('mailto:')) detail.destination = 'email';
      else if (href.startsWith('tel:')) detail.destination = 'phone';
      else if (href && !href.startsWith('javascript:')) {
        try {
          const url = new URL(href, location.href);
          detail.destination = url.hostname === location.hostname ? url.pathname : url.hostname;
        } catch { /* An invalid link does not block navigation. */ }
      }
    }
    if (window.posthog?.__loaded) posthog.capture('site_click', detail);
  }, { capture: true });
})();
