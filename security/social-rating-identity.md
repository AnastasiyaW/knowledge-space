---
title: Social Rating and Digital Identity
category: identification
tags: [social-rating, identity, reputation, account-age, digital-identity]
---

# Social Rating and Digital Identity

## Key Facts

- Social rating is a unique user identifier based on accumulated online activity history - resistant to quick changes unlike device/network identifiers
- Components: email account age, purchase history, service account longevity, review/rating history, linked social accounts
- Older accounts (5+ years) with consistent activity patterns are significantly more trusted by [[anti-fraud-systems]]
- Account age is verifiable via registration timestamps, first purchase records, email creation dates
- Social graph analysis: connections between accounts, mutual friends, shared payment methods reveal real vs synthetic identities
- [[browser-fingerprinting]] and [[network-identifiers]] can be spoofed in minutes; social rating takes months/years to build legitimately
- Leaked email databases (e.g., from 2015 breaches) contain old accounts that may still be active on services like Amazon, eBay

## Patterns

```python
# Social rating signal aggregation
def compute_social_score(user_data: dict) -> float:
    """
    Compute trust score based on digital identity signals.
    Higher score = more trusted identity.
    """
    score = 0.0

    # Email age (major factor)
    email_age_years = user_data.get('email_age_days', 0) / 365
    if email_age_years > 5:
        score += 30
    elif email_age_years > 2:
        score += 20
    elif email_age_years > 0.5:
        score += 10

    # Purchase history
    if user_data.get('purchase_count', 0) > 10:
        score += 20
    elif user_data.get('purchase_count', 0) > 3:
        score += 10

    # Linked accounts (Google, Facebook, etc.)
    score += min(user_data.get('linked_accounts', 0) * 5, 15)

    # Phone verification
    if user_data.get('phone_verified'):
        score += 15

    # Review/rating history
    if user_data.get('reviews_written', 0) > 5:
        score += 10

    return min(score, 100)
```

```
# Identity verification hierarchy (weakest to strongest):
1. Email exists                    - trivial to create
2. Email verified                  - slightly harder
3. Phone verified                  - requires SIM/VoIP
4. Account age > 6 months          - requires time investment
5. Purchase history exists         - requires financial activity
6. Multiple linked social accounts - requires social graph
7. Government ID verified          - KYC requirement
8. Biometric verification          - hardest to fake
```

## Gotchas

- Manipulating system clock on a clean VM to a past date can trick some websites into setting older cookies - simple but effective against basic timestamp checks
- Old leaked databases are freely available on forums - attackers use these to recover abandoned accounts with high social rating
- Account recovery with leaked email may be technically legal (you registered the email) but ethically and legally grey depending on subsequent use
- Social rating is most valuable for marketplace platforms (Amazon, eBay) where seller/buyer reputation directly affects trust
- Some platforms detect sudden changes in activity patterns on dormant accounts as suspicious

## See Also

- [NIST SP 800-63A Digital Identity Guidelines - Enrollment and Identity Proofing](https://pages.nist.gov/800-63-3/sp800-63a.html)
- [OWASP Identity Verification](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
