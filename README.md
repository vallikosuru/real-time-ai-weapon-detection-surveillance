# Real-Time AI-Based Weapon Detection and Surveillance System with WhatsApp Alerting

## 📌 Overview

This project is a real-time AI-based weapon detection and surveillance
system developed using Python, Deep Learning, and Computer Vision.

The system uses a combination of deep learning models to analyze
real-time video input and identify potential weapons. When a potential
weapon is detected, the system generates an alert and automatically
sends a WhatsApp notification.

The project combines AI-based image analysis, real-time video
processing, alert generation, and notification services into an
end-to-end surveillance solution.

---

## 🚀 Key Features

- Real-time video surveillance
- AI-based weapon detection
- Multi-model deep learning approach
- Image and video processing
- Weapon classification and confidence scoring
- Automated alert generation
- WhatsApp alert notifications
- Alarm notification
- Firebase integration
- Incident recording and management
- Real-time monitoring

---

## 🧠 AI & Deep Learning

The system uses multiple deep learning models as part of the
weapon detection pipeline.

One of the models used in the project is **ResNet-50**, which is
utilized for deep learning-based image analysis and classification.

The multi-model approach is designed to improve the reliability of
weapon detection and classification in surveillance scenarios.

---

## 🔄 System Workflow

```text
        Camera / Video Input
                │
                ▼
       Real-Time Video Processing
                │
                ▼
        Preprocessing / Frames
                │
                ▼
       Multiple AI/ML Models
                │
                ▼
        Weapon Detection
                │
                ▼
     Confidence / Classification
                │
          ┌─────┴─────┐
          │           │
       No Weapon    Weapon Detected
          │           │
          ▼           ▼
       Continue    Generate Alert
                      │
              ┌───────┴────────┐
              │                │
              ▼                ▼
        Alarm / Record     WhatsApp Alert
                               │
                               ▼
                         Notification
