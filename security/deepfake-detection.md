---
title: Deepfake Detection and Image Forensics
category: fraud-prevention
tags: [deepfake, image-analysis, computer-vision, fraud-detection, forensics, ml]
---

# Deepfake Detection and Image Forensics

## Key Facts

- Image analysis is a fundamental component of modern [[anti-fraud-systems]] - verifying document authenticity, detecting manipulated photos
- Deepfake detection approaches: face detection consistency, temporal analysis (video), compression artifact analysis, noise pattern analysis
- Document verification: checking for editing artifacts in ID documents, comparing fonts and layouts against known templates
- Anti-fraud image analysis includes: ID document verification, selfie-to-document matching, image manipulation detection
- Face detection cascades (Haar cascades, MTCNN, RetinaFace) are the first step in both deepfake detection and identity verification
- [[behavioral-analysis]] complements image forensics - real-time liveness detection uses user interaction

## Patterns

```python
# Basic deepfake detection framework
import cv2
import numpy as np

def analyze_video_faces(video_path: str) -> dict:
    """Detect potential deepfake by analyzing face consistency"""
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    no_face_frames = 0
    face_sizes = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        if len(faces) == 0:
            no_face_frames += 1
        else:
            face_sizes.append(faces[0][2] * faces[0][3])  # width * height

    cap.release()
    no_face_pct = (no_face_frames / frame_count * 100) if frame_count > 0 else 0

    return {
        'total_frames': frame_count,
        'no_face_percentage': no_face_pct,
        'face_size_variance': np.var(face_sizes) if face_sizes else 0,
        'likely_deepfake': no_face_pct > 50 or np.var(face_sizes) > threshold,
    }
```

```python
# Image classification with pre-trained model
import tensorflow as tf
import numpy as np
import cv2

def classify_image(image_path: str) -> list:
    """Classify image content using MobileNetV2"""
    model = tf.keras.applications.MobileNetV2(
        weights='imagenet', include_top=True,
        input_shape=(224, 224, 3)
    )
    image = cv2.imread(image_path)
    image = cv2.resize(image, (224, 224))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)

    predictions = model.predict(image)
    decoded = tf.keras.applications.imagenet_utils.decode_predictions(
        predictions, top=5
    )[0]
    return [(label, float(score)) for _, label, score in decoded]
```

## Gotchas

- Haar cascades are fast but inaccurate for non-frontal faces - modern systems use MTCNN or RetinaFace for better detection
- High-quality deepfakes pass basic face detection - advanced detection requires analyzing compression artifacts, lighting inconsistencies, or training specialized classifiers
- Liveness detection (blink detection, head movement) can be bypassed by pre-recorded videos - multi-factor verification is essential
- EXIF metadata stripping removes camera/location info but does not remove manipulation artifacts from pixel data
- Generative AI images often have telltale signs in hands, teeth, hair boundaries, and text rendering - but quality improves rapidly

## See Also

- [NIST Face Recognition Vendor Test](https://pages.nist.gov/frvt/)
- [OWASP Image Upload Security](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [FaceForensics++ benchmark](https://github.com/ondyari/FaceForensics)
