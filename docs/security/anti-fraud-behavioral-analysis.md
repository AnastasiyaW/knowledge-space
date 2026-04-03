---
title: Anti-Fraud Behavioral Analysis
category: concepts
tags: [security, anti-fraud, behavioral-analysis, keystroke-dynamics, payment-fraud]
---

# Anti-Fraud Behavioral Analysis

Behavioral signals used by anti-fraud systems: mouse movement patterns, keystroke dynamics, session timing analysis, payment fraud detection (velocity checks, BIN analysis, 3D Secure), and social rating signals.

## Key Facts
- Mouse movement curves follow Bezier-like paths for humans; bots use linear interpolation
- Keystroke dynamics (dwell time, flight time) can identify individual users without credentials
- Velocity checks detect fraud patterns: multiple cards from same device, geographic impossibility
- BIN (first 6-8 digits) reveals issuing bank, card type, country, and consumer/commercial status
- 3D Secure shifts fraud liability from merchant to card issuer
- Anti-fraud scoring combines hundreds of signals - anomaly in any dimension raises risk

## Mouse Movement Patterns
- **Speed and acceleration**: bots move at constant speed; humans have micro-corrections
- **Click precision**: humans slightly miss targets; bots click exact coordinates
- **Movement curves**: human paths are Bezier-like; bots use linear interpolation
- **Idle patterns**: natural pauses vs complete absence of movement
- **Scroll behavior**: speed, direction changes, momentum

## Keystroke Dynamics (Biometrics)
Unique per-user typing patterns:
- **Dwell time** - how long each key is held
- **Flight time** - time between key release and next key press
- **Typing speed** - WPM and consistency
- **Error patterns** - backspace frequency, common corrections
- **Digraph/trigraph timings** - time between specific letter pairs

These biometrics build profiles over time and can identify users even without login credentials.

## Session Timing Analysis
- Time between page loads
- Time spent on forms before submission (too fast = bot, too slow = manual fraud)
- Navigation patterns (reading content vs jumping straight to checkout)
- Session duration and return patterns

## Payment Fraud Detection

### BIN (Bank Identification Number) Analysis
First 6-8 digits reveal:
- Issuing bank and country
- Card type: credit, debit, prepaid, virtual
- Card brand and level (standard/gold/platinum)
- Consumer vs commercial

Anti-fraud uses: verify billing country matches BIN country, detect virtual/prepaid cards (higher fraud risk), velocity checks per BIN range.

### Velocity Checks
- Number of transactions per card in time window
- Number of different cards from same device/IP
- Transaction amount patterns (small test charges before large)
- Geographic velocity (transactions from distant locations in impossible time)

### AVS (Address Verification System)
Compare billing address with issuer records: street number and ZIP code matching, country matching between billing and BIN.

### 3D Secure (3DS)
- Cardholder authenticates via bank's portal (Verified by Visa, Mastercard SecureCode)
- Shifts fraud liability from merchant to issuer
- 3DS2: risk-based authentication - frictionless flow for low-risk transactions

### Virtual/Prepaid Card Indicators
- Prepaid cards lack billing address verification
- Virtual cards often generated in bulk
- Known BIN ranges for prepaid/virtual products
- Limited transaction history for risk assessment

## Social Rating Signals
- Account age and activity patterns
- Social media profile consistency
- Email domain (free vs corporate)
- Phone number validation (VoIP vs carrier, number age)
- Behavioral consistency with claimed identity

## Gotchas
- Mouse/keystroke analysis can be defeated by sophisticated replay tools that inject human-like noise
- Velocity checks must account for legitimate scenarios (corporate cards with multiple users, shared IPs)
- VPN/proxy users are not necessarily fraudulent - overly aggressive IP scoring creates false positives
- 3DS friction reduces conversion rates - merchants balance security vs revenue loss
- Behavioral biometrics raise privacy concerns under GDPR (biometric data is special category)

## See Also
- [[browser-and-device-fingerprinting]] - device-level fingerprint signals
- [[tls-fingerprinting-and-network-identifiers]] - IP and network analysis
- [[deepfake-and-document-forensics]] - document forgery detection
- [[compliance-and-regulations]] - GDPR implications for behavioral tracking
