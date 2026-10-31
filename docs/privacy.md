---
title: Privacy Policy
---

# Privacy Policy

**Last updated:** 24 October 2026

## What we collect

When you subscribe to updates, we store:

- Your email address
- Timestamp of subscription
- IP address (for consent verification)

Outside the optional analytics described below, we do not collect names, payment information, or other personal data.

## Why we collect it

To send you occasional email updates when new articles are published on happyin.space.

## How we store it

Your data is stored on Cloudflare's infrastructure (D1 database), encrypted at rest.

## Your rights

- **Unsubscribe** at any time via the link in every email, or by contacting us
- **Request deletion** of your data by contacting us
- **Request export** of your data by contacting us

## Contact

For any privacy-related questions: [GitHub Issues](https://github.com/AnastasiyaW/knowledge-space/issues) or the [Telegram channel](https://t.me/happyin_space). More ways are on the [contact page](contact.md). Please do not post personal data in a public issue; ask for a private channel instead.

## Anonymous usage counts

We count how the site is used; we do not build profiles of visitors.

- **Page views** come from Cloudflare Web Analytics, which sets no cookies and does not fingerprint visitors. We read its daily totals by page, referring site, country and device type.
- **Return counter.** To learn whether people come back, your browser keeps a small record in its local storage: the date of your first visit, the date of your last visit, and how many different days you have visited. The record itself stays on your device. Once per day of your visits, the page requests one tiny file whose name says only one of:
    - a new visit;
    - back after 1, 2-7, 8-30 or 31+ days;
    - the same, from a browser that has visited on 5 or more different days.
- **Star buttons.** Clicking a "Star" button requests one tiny file that names only where the button was: the top bar, the end of an article, or the notice after copying code. The page also requests one when that notice is shown, so we can see which placement helps.
- **Crawlers and AI assistants.** We read aggregate request statistics grouped by user agent, for example how often an AI assistant fetched an article on someone's behalf. These statistics contain no IP addresses.

These requests carry no cookie, no identifier and no page address. Like every request to this site, they reach Cloudflare's network with your IP address and your browser's standard headers. Our counts use the file name, the day and whether a browser sent the request; the counts hold no IP addresses.

The record expires 13 months after your first visit, and later visits do not extend it. Clearing this site's data resets it.

The return counter and the star-button counts are off when any of these apply:

- your browser sends Global Privacy Control or Do Not Track;
- the browser is run by automation software;
- the browser does not let the site store data;
- you turn it off below.

Page views in Web Analytics and the aggregate request statistics still apply. Safari deletes a site's storage after 7 days of browsing without any interaction with that site, so a Safari visitor who comes back after such a gap is counted as new.

<p class="ks-counter-switch"><span data-ks-counter-state>This switch needs JavaScript.</span> <button type="button" class="md-button" data-ks-counter-toggle>Turn it off</button></p>

## Google Analytics and Google advertising

When the site owner has configured them, pages load Google Analytics 4 and, on article pages, Google AdSense ads. Google's [How Google uses information from sites or apps that use our services](https://policies.google.com/technologies/partner-sites) explains what Google does with that data; [How Google uses cookies in advertising](https://policies.google.com/technologies/ads) describes its advertising cookies.

**Consent Mode.** Both use Google Consent Mode v2, set before any Google script loads:

- **In the EEA, the UK and Switzerland**, analytics and advertising storage are off by default (`analytics_storage`, `ad_storage`, `ad_user_data` and `ad_personalization` denied). You see a prompt, and Google Analytics cookies are used only if you choose **Allow**. Until then Google may still receive signals without cookies or advertising identifiers (for example, that a page was viewed). Consent to personalised advertising in these countries is collected by Google's certified consent message, shown by Google when ads are enabled; without it, ads there are not personalised.
- **Elsewhere**, these settings are on by default, and Google may set analytics and advertising cookies. You can turn them off at any time.
- **Global Privacy Control or Do Not Track** turns everything to denied: the Google Analytics tag is not loaded at all, and any ads are shown without cookie-based personalisation.

**Your choice.** The **Privacy choices** link in the footer of every page, and the button below, reopen the prompt. Choosing **Decline** sets all four Consent Mode signals to denied in this browser, stops our analytics events and removes this site's Google cookies (`_ga`, `_ga_*`, `__gads`, `__gpi`, `__eoi`). Your choice is kept in this browser's local storage under `ks_consent_v2`. To decide where the prompt is needed, the page asks this site's `/api/consent-region`, which answers only "prompt needed: yes or no" from the country Cloudflare derives from your IP address; the country is not stored.

**What we measure.** Aggregate use of the knowledge base: page and article views, search use and result opens, code copies, GitHub-star clicks and successful newsletter subscriptions, each with the site section and, for buttons, where the button was. We do **not** send search terms, prompts, email addresses, feedback text, URL query strings or advertising identifiers in these events, and Google signals and ad personalisation are turned off for our analytics.

**Advertising.** Ads, when shown, come from Google AdSense and appear only on article pages (never on the home page, this page, or the about and contact pages). Google and its partners may use cookies to serve ads based on your visits to this and other sites; you can manage personalised advertising in [Google's My Ad Center](https://myadcenter.google.com/). Ads are marked "Advertisement" and do not influence what articles say.

<p class="ks-counter-switch"><span data-ks-analytics-state>This switch needs JavaScript.</span> <button type="button" class="md-button" data-ks-analytics-preferences hidden>Privacy choices</button></p>

## Feedback reports

The GET search API (`/api/search?q=...`) records a query as a private gap report when the deployed article index has no matching result. The authenticated diffusion.love MCP service can also report its searches with no results. These reports share the retention and private research queue described below, with channels `search` and `mcp-search`, but their limits differ: public search and explicit feedback each allow 30 reports per IP address per day (separate allowances), while the authenticated MCP service allows 3,000 per day. All report sources together share a 3,000-report daily cap. A failed search does not create a gap. Use public topics only: do not submit personal data, private code or secrets as a search query. Search replies explicitly say whether a gap was recorded; storage failures are reported as errors.

Anyone, including an AI assistant working for you, can send a report to `/api/feedback`: a topic that is missing, an article that is outdated or wrong, or an article that helped. We store what the report says (kind, topic, article, detail, an optional link and an optional client name such as "claude-code"), the time, whether it came as a POST or a GET, the family of the sending software read from its User-Agent (for example "curl" or "claude-user"; the full User-Agent is not kept), and a one-day pseudonym: a hash of the IP address, the date and a secret, which lets us limit how many reports one sender makes per day and cannot be turned back into the address. The IP address itself is not stored. Reports are read only by the owner's research pipeline and are never published on the site; a report's status page shows only its number, kind, date and outcome, and once it is handled the title we gave it and a link to the result, and the list of wanted topics shows titles the owner writes, never the words of a report; an article written in response cites its own sources, not the report. Reports older than 12 months are deleted automatically when the next report arrives. Do not put personal data in a report. To have a report removed sooner, open a [GitHub Issue](https://github.com/AnastasiyaW/knowledge-space/issues) with its text and date.

## Other services the pages load

Pages load fonts from Google Fonts, the 3D graph library from jsDelivr (home page only), and star counts from GitHub's API. Each of those services receives your IP address and browser headers, as with any web request. When Google Analytics or ads are enabled, Google also receives the requests described above under its own privacy terms.

## Cookies

- **Google Analytics** (`_ga`, `_ga_*`, up to 2 years) and **Google advertising** cookies (`__gads`, `__gpi`, `__eoi` on this domain, and Google's own cookies on Google domains), only as described under Consent Mode above: after your consent in the EEA, the UK and Switzerland; by default elsewhere, until you decline.
- **Cloudflare** may set essential cookies for security.
- **Local storage**, not cookies: the return counter, your consent choice, and whether the newsletter prompt was dismissed.
