---
title: Deepfake and Document Forensics
category: concepts
tags: [security, deepfake, forensics, image-analysis, anti-fraud, document-forgery]
---

# Deepfake and Document Forensics

Detection and analysis of forged content: deepfake video/audio technology and detection methods, document forgery techniques and verification, image forensics (ELA, perceptual hashing, clone detection), and email spoofing analysis.

## Key Facts
- Modern voice cloning achieves ~99% fidelity from minutes of sample audio
- Error Level Analysis (ELA) detects manipulated image regions via JPEG compression artifact differences
- Perceptual hashing produces similar hashes for similar images (unlike cryptographic hashing)
- Email SPF/DKIM/DMARC together prevent spoofing - check all three for verification
- EXIF metadata survives most editing but is stripped by social media platforms
- Real-time deepfake tools for video calls now exist commercially

## Deepfake Technology

### Components
1. **Face synthesis** - AI models trained on target's face (hundreds to thousands of photos)
2. **Voice synthesis** - voice cloning from audio samples (~99% fidelity from minutes of audio)
3. **Lip sync** - matching generated speech to facial movements

### Detection Methods
- **Blink analysis** - early deepfakes did not simulate natural blinking
- **Facial boundary artifacts** - seams where face overlay meets background
- **Audio-visual sync** - subtle mouth/speech mismatches
- **Frequency analysis** - GAN-generated images have detectable frequency domain patterns
- **Metadata analysis** - generated videos lack expected camera metadata

## Document Forgery

### Types of Forged Documents
- Identity documents (passports, driver's licenses)
- Financial documents (bank statements, tax returns, invoices)
- Corporate documents (employment letters, articles of incorporation)
- KYC verification selfies with documents

### Verification Methods
- **EXIF metadata** - creation date, software used, device info
- **Template matching** - comparing against known genuine document templates
- **Database cross-reference** - checking document numbers against official databases
- **UV/hologram checks** - physical verification for printed documents

## Image Forensics

### Error Level Analysis (ELA)
Detects manipulated regions by analyzing JPEG compression artifacts:
- Re-save image at known quality level
- Compare with original pixel by pixel
- Manipulated regions show different compression levels (brighter in ELA output)

### Perceptual Hashing
- Images reduced to compact hash values
- Similar images produce similar hashes
- Used for: detecting known fraudulent documents, matching against databases
- Enables scanning billions of images without human review

### Additional Techniques
- **Clone detection** - finding copy-pasted regions within an image
- **Lighting/shadow analysis** - inconsistent light sources reveal compositing
- **Noise analysis** - different cameras/sensors produce different noise patterns
- **EXIF data extraction** - camera model, GPS, date, editing software

## Email Forensics

### Header Analysis
```sql
Received: chain   - traces routing path from sender to recipient
X-Originating-IP  - may reveal sender's real IP
Message-ID         - domain should match sender
Return-Path        - vs From: mismatches indicate spoofing
```

### Spoofing Detection
- Check SPF record alignment (envelope sender vs header From)
- Verify DKIM cryptographic signature
- Evaluate DMARC policy
- Analyze header chain consistency
- Check for BEC (Business Email Compromise) indicators

## Google Anti-Fraud Signals
Google's unified trust model across services:
- Phone number: carrier type (VoIP vs mobile), number age, reuse patterns
- Device fingerprint and IP reputation at registration
- Behavioral patterns post-registration (human vs bot activity)
- Account age and activity history

### Common Abuse Patterns
- Account selling (value increases with age, phone verification, service eligibility)
- Cloud hosting abuse ($1 trial credits for compute resources)
- AdSense fraud (fake impressions/clicks)
- Maps fake businesses (SEO/reputation manipulation)

## Gotchas
- AI-generated content detection is an arms race - detection methods have increasing false negative rates
- ELA only works on JPEG (lossy compression artifacts) - not applicable to PNG/BMP
- EXIF data can be trivially modified or removed - absence of EXIF is not proof of forgery
- Perceptual hashing can be defeated by sufficient image transformation
- Email SPF pass only verifies the envelope sender domain, not the header From displayed to user
- Video call deepfakes are detectable by asking the person to perform unexpected actions (turn sideways, cover face partially)

## See Also
- [[osint-and-reconnaissance]] - metadata extraction, evidence gathering
- [[anti-fraud-behavioral-analysis]] - behavioral fraud signals
- [[browser-and-device-fingerprinting]] - device identification
- [[compliance-and-regulations]] - data protection in investigations
