---
title: Image Forensics for Anti-Fraud
category: fraud-prevention
tags: [image-forensics, document-verification, ocr, manipulation-detection, anti-fraud]
---

# Image Forensics for Anti-Fraud

## Key Facts

- Image forensics in anti-fraud verifies authenticity of submitted documents (IDs, receipts, bank statements)
- Key techniques: Error Level Analysis (ELA), metadata examination, copy-move detection, splicing detection
- Error Level Analysis highlights areas with different JPEG compression levels - manipulated regions show inconsistent compression
- EXIF metadata contains camera model, GPS coordinates, timestamps - absence or inconsistency indicates manipulation
- Document template matching compares submitted documents against known genuine templates for layout/font/positioning anomalies
- [[deepfake-detection]] focuses on faces/video; image forensics covers broader document and photo manipulation
- [[anti-fraud-systems]] combine image forensics with [[social-rating-identity]] checks for multi-layered verification

## Patterns

```python
# Error Level Analysis (ELA) for manipulation detection
from PIL import Image, ImageChops
import numpy as np

def error_level_analysis(image_path: str, quality: int = 95) -> np.ndarray:
    """
    Save image at known quality, compare with original.
    Manipulated areas show different error levels.
    """
    original = Image.open(image_path)
    # Re-save at known quality
    original.save('/tmp/ela_temp.jpg', 'JPEG', quality=quality)
    resaved = Image.open('/tmp/ela_temp.jpg')

    # Compute difference
    diff = ImageChops.difference(original, resaved)

    # Amplify differences for visualization
    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    scale = 255.0 / max_diff if max_diff != 0 else 1

    ela_image = diff.point(lambda x: x * scale)
    return np.array(ela_image)
    # Uniform brightness = authentic
    # Bright spots in specific regions = likely manipulated
```

```python
# EXIF metadata extraction for fraud detection
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def extract_exif(image_path: str) -> dict:
    """Extract and analyze EXIF metadata for fraud signals"""
    img = Image.open(image_path)
    exif_data = img._getexif()
    if not exif_data:
        return {'warning': 'No EXIF data - possible screenshot or manipulation'}

    parsed = {}
    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)
        parsed[tag] = value

    # Fraud signals
    signals = []
    if 'Software' in parsed:
        if any(s in str(parsed['Software']).lower()
               for s in ['photoshop', 'gimp', 'paint']):
            signals.append('Editing software detected')

    if 'DateTime' not in parsed:
        signals.append('No timestamp - unusual for camera photos')

    return {'metadata': parsed, 'fraud_signals': signals}
```

```python
# Copy-move forgery detection (basic)
import cv2
import numpy as np

def detect_copy_move(image_path: str) -> list:
    """Detect duplicated regions using ORB features"""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    orb = cv2.ORB_create(nfeatures=5000)
    kp, des = orb.detectAndCompute(img, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    matches = bf.knnMatch(des, des, k=2)

    suspicious = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            pt1 = kp[m.queryIdx].pt
            pt2 = kp[m.trainIdx].pt
            dist = np.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)
            if dist > 50:  # Not self-match
                suspicious.append((pt1, pt2, m.distance))

    return suspicious  # Non-empty = potential copy-move forgery
```

## Gotchas

- Screenshots of documents strip all EXIF metadata - absence of metadata is not proof of manipulation, but it is a warning sign
- JPEG re-compression introduces artifacts even without manipulation - ELA must account for expected compression patterns
- Modern AI image generators (DALL-E, Midjourney, Stable Diffusion) create images without typical camera artifacts - standard forensic techniques may not detect them
- Printed-and-re-scanned documents lose digital manipulation traces - physical document inspection remains necessary for high-value verification
- Social media platforms strip EXIF and re-compress images on upload - analyzing downloaded social media images for EXIF is unreliable

## See Also

- [FotoForensics - online ELA tool](https://fotoforensics.com/)
- [NIST Digital Forensics](https://www.nist.gov/digital-forensics)
- [CWE-345 Insufficient Verification of Data Authenticity](https://cwe.mitre.org/data/definitions/345.html)
