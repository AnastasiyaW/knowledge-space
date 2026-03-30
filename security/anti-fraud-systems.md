---
title: Anti-Fraud Systems
category: fraud-prevention
tags: [anti-fraud, antibot, fraud-detection, risk-scoring, ecommerce]
---

# Anti-Fraud Systems

## Key Facts

- Anti-fraud systems detect and prevent fraudulent transactions; anti-bot systems block automated activity - these are distinct systems often confused
- Major anti-fraud vendors: Sift, Forter, Riskified, IPQualityScore, FraudFusion, Kount, Signifyd
- Multi-layered identification: [[browser-fingerprinting]] + [[network-identifiers]] + [[behavioral-analysis]] + [[social-rating-identity]] + device identifiers
- Free tier API checks (e.g., IPQualityScore free plan) use limited data sources - only IP reputation and email reputation without premium blacklists, device fingerprinting, or extended fraud databases
- Paid tiers access premium blacklists, FraudFusion, AbuseShield, DarkData, BotKiller and other extended intelligence sources
- Fraud scoring is probabilistic - systems assign risk scores (0-100) rather than binary allow/deny
- [[geolocation-security]] mismatches between IP, timezone, and language are strong fraud signals

## Patterns

```python
# Risk score aggregation pattern
class FraudScorer:
    def __init__(self):
        self.signals = []

    def add_signal(self, name: str, score: float, weight: float):
        self.signals.append({
            'name': name,
            'score': score,  # 0.0 = safe, 1.0 = fraud
            'weight': weight
        })

    def compute_risk(self) -> float:
        total_weight = sum(s['weight'] for s in self.signals)
        weighted_sum = sum(s['score'] * s['weight'] for s in self.signals)
        return weighted_sum / total_weight if total_weight > 0 else 0.0

# Example signals
scorer = FraudScorer()
scorer.add_signal('ip_reputation', 0.3, weight=0.25)
scorer.add_signal('device_fingerprint_age', 0.8, weight=0.20)
scorer.add_signal('velocity_check', 0.1, weight=0.20)
scorer.add_signal('geo_mismatch', 0.9, weight=0.15)
scorer.add_signal('behavioral_score', 0.4, weight=0.20)
risk = scorer.compute_risk()  # Aggregate risk
```

```
# Typical fraud detection pipeline:
1. Network layer: IP reputation, ASN type (residential vs datacenter), proxy/VPN detection
2. Device layer: Browser fingerprint, OS identifiers, hardware identifiers
3. Behavioral layer: Mouse patterns, typing cadence, navigation flow
4. Identity layer: Email age, phone verification, social graph
5. Transaction layer: Velocity checks, amount patterns, merchant category
```

## Gotchas

- Checking your setup on free-tier anti-fraud APIs gives false confidence - paid tiers use entirely different data sources and may flag what free tier passes
- IP from hosting provider (datacenter) vs residential ISP is a strong signal - VPN users get flagged even if IP itself is clean
- Anti-fraud and anti-bot are different systems: anti-bot blocks automation (CAPTCHA, rate limits), anti-fraud evaluates transaction legitimacy
- Systems continuously evolve - a technique that bypasses detection today may be flagged within weeks
- Google's anti-fraud differs from its anti-bot: you can pass anti-bot (register without SMS) but still be flagged by anti-fraud later

## See Also

- [OWASP Automated Threats to Web Applications](https://owasp.org/www-project-automated-threats-to-web-applications/)
- [NIST SP 800-83 Guide to Malware Incident Prevention](https://csrc.nist.gov/publications/detail/sp/800-83/rev-1/final)
