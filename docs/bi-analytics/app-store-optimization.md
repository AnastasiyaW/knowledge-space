---
title: App Store Optimization (ASO)
category: concepts
tags: [bi-analytics, aso, app-store, google-play, apple, keywords, ratings, mobile]
---

# App Store Optimization (ASO)

ASO is organic search optimization for app stores - the goal is to appear in top results for relevant keywords without paid ads. It covers keyword optimization, conversion rate optimization, ratings management, and competitor analysis across Google Play and Apple App Store.

## Key Facts

- ASO = organic search optimization for app stores
- Benchmark conversion rate (impressions -> installs): 25-35% for well-optimized apps
- App title has the highest keyword weight in both stores
- Getting featured by Apple/Google multiplies installs 10-100x
- A/B testing available: Google Play Store Listing Experiments, Apple Product Page Optimization
- Apps below 4.0 rating have significantly lower conversion

## Patterns

### Ranking Factors

**Keyword factors:**
- **App title** (highest weight) - include primary keyword
- **Subtitle** (iOS) / **Short description** (Android) - secondary keywords
- **Keyword field** (iOS only, 100 chars, comma-separated, not visible to users)
- **Description** (Android) - first 167 chars visible without "More"

**Performance factors:**
- Install volume (more installs = higher ranking)
- Conversion rate (impressions -> installs)
- Ratings and reviews (average + volume)
- Uninstall rate (negative signal)
- Engagement (sessions per user, retention)

### Keyword Research Process

1. Brainstorm seed keywords (product features, use cases, synonyms)
2. Analyze competitors' top keywords using ASO tools
3. Check search volume and difficulty for each keyword
4. Prioritize: high volume + low difficulty = best opportunity
5. Long-tail keywords: easier to rank but lower volume

**ASO tools:** AppFollow, AppTweak, Sensor Tower, MobileAction, AppMagic.

### Conversion Rate Optimization

Elements affecting install conversion (in order of impact):
1. **Icon** - first visual impression, must be recognizable at small size
2. **Screenshots** - first 2-3 visible without scrolling (most important visual element)
3. **Preview video** - auto-plays on iOS, show core value in first 3 seconds
4. **App name + subtitle** - conveys value proposition instantly
5. **Ratings** - apps below 4.0 have significantly lower conversion
6. **Reviews** - recent positive reviews matter more than old ones

A/B testing:
- **Google Play**: Store Listing Experiments (test 3 variants, auto winner selection)
- **App Store**: Product Page Optimization (test screenshots/icon)

### Google Play vs Apple App Store

| Feature | Google Play | Apple App Store |
|---------|------------|----------------|
| Review process | Automatic + manual for new apps | Manual for every update (1-3 days) |
| Install count | Displayed publicly (approximate) | Not public |
| Ratings | Persist across versions | Can reset per major version |
| A/B testing | Store Listing Experiments | Product Page Optimization |
| Developer analytics | Google Play Console | App Store Connect |
| Featured | Editorial outreach to quality apps | Submit via App Store Promotions |

### Ratings & Reviews Strategy

**When to prompt for rating:**
- After positive moments (level completion, successful task)
- Never on launch or after negative experience
- iOS: can only reset ratings on new major version
- Android: ratings persist across updates

**Review analysis:**
- Categorize: bugs, missing features, UX issues, praise
- Track sentiment over time (especially after updates)
- Map feature mentions to product roadmap
- Negative review spikes after update = rollback/hotfix signal
- Respond to negative reviews quickly (shows app is maintained)

### Getting Featured

Factors that help:
- Integration with platform features (iOS: widgets, Siri shortcuts, App Clips; Android: Google Assistant, instant apps)
- Technical quality (no crashes, fast load, guideline-compliant)
- Timing (submit request 6+ weeks before desired feature date)
- Platform-native design

### Competitor Analysis

Analyze competitors for:
- Keywords they rank for that you don't
- Rating trends (declining = your opportunity)
- Update frequency
- Screenshot presentation patterns
- User complaints in reviews = product gap opportunities

### Analytics Tools

**Free (built-in):**
- App Store Connect (Apple): impressions, page views, installs, crashes, revenue, retention
- Google Play Console: store listing stats, ratings, crashes, ANRs, revenue

**Paid third-party:**
- Sensor Tower: market intelligence, competitor analysis, download estimates
- AppTweak: ASO optimization, keyword tracking
- AppFollow: review management, sentiment analysis
- AppMagic: revenue estimates, market sizing

## Gotchas

- ASO is a continuous process, not a one-time optimization - competitors constantly change
- Keyword stuffing in title/description can trigger store review rejection
- Different regions may need different keyword strategies - localize ASO
- Category rank drives organic discovery but is harder to influence directly than search ranking
- Top Charts rankings (Free, Paid, Top Grossing) each use different metrics

## See Also

- [[funnel-analysis]] - install conversion funnel
- [[mobile-analytics-platforms]] - post-install analytics
- [[mobile-attribution-fraud]] - attribution from store to in-app
- [[product-metrics-framework]] - engagement metrics that affect ASO
