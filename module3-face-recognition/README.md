# Module 3: Face Recognition & Risk Service

**SAIV (Secure Attendance & Identity Verification) Capstone Project**  
*NTU Computer Science — Port: `8001`*

---

## 📌 1. Overview & Role in SAIV

Module 3 is the biometric identity verification and security risk evaluation microservice. It is called internally over HTTP REST by **Module 2 (Backend API)** during student onboarding and class check-in events.

### Core Capabilities
1. **Biometric Face Enrollment (`POST /face/enroll`)**: Detects facial presence, validates image quality, and generates a privacy-preserving 64-character biometric template hash stored in the PostgreSQL database.
2. **Face Verification (`POST /face/verify`)**: Compares incoming check-in selfies against enrolled reference hashes using Locality-Sensitive Hashing (SimHash) and continuous similarity scoring.
3. **Liveness & Anti-Spoofing (`POST /liveness/check`)**: Distinguishes real human faces from 2D printed photos and screen displays using 3D depth cue analysis (`nose_tip_z`), texture analysis, and active challenges (Blink EAR, Head Turn/Tilt).
4. **Multi-Signal Risk Assessment (`POST /risk/assess`)**: Fuses multiple security signals (Liveness, Match, Device Attestation, Network/VPN, Geolocation) into a unified risk score ($0.0 - 1.0$) with actionable recommendations.

---

## 🏗️ 2. Architectural Design & Pipeline

```
                       ┌────────────────────────────────────────┐
                       │  Incoming Base64 Request Payload       │
                       └───────────────────┬────────────────────┘
                                           │
                                           ▼
                       ┌────────────────────────────────────────┐
                       │ 1. Decode & In-Memory Preprocessing    │
                       │    • Strip Data URI header if present  │
                       │    • Decode to RGB NumPy Array (H,W,3) │
                       │    • Validate min dimensions (64x64)   │
                       └───────────────────┬────────────────────┘
                                           │
                                           ▼
                       ┌────────────────────────────────────────┐
                       │ 2. Face Detection & Quality Gate       │
                       │    • MediaPipe BlazeFace (confidence)  │
                       │    • Early exit if no face (HTTP 400)  │
                       │    • Compute quality score (Sharpness, │
                       │      lighting, frame coverage ratio)   │
                       └───────────────────┬────────────────────┘
                                           │
                                           ▼
                       ┌────────────────────────────────────────┐
                       │ 3. 3D Landmark Mesh & Pose Alignment   │
                       │    • MediaPipe Face Mesh (468 pts)     │
                       │    • Zero-center on inter-pupil midpoint│
                       │    • Scale by inter-ocular distance    │
                       │    • Extract invariant feature vector  │
                       │      v ∈ ℝ^D (D = 128)                 │
                       └───────────────────┬────────────────────┘
                                           │
                                           ▼
                       ┌────────────────────────────────────────┐
                       │ 4. Locality Sensitive Hashing (SimHash)│
                       │    • Projection: p = W · v (256 planes)│
                       │    • Binarize: bit_i = (p_i >= 0)      │
                       │    • Pack to 32 bytes ➔ 64-char Hex    │
                       └───────────────────┬────────────────────┘
                                           │
              ┌────────────────────────────┴────────────────────────────┐
              ▼                                                         ▼
    【 POST /face/enroll 】                                   【 POST /face/verify 】
  • Store 64-char hash in DB                               • Compute current 256-bit hash
  • Return quality_score & details                         • XOR with reference ➔ Hamming Dist d_H
                                                           • match_score = max(0, 1 - d_H / 64)
                                                           • match_passed = (match_score >= 0.70)
```

---

## 🔑 3. The SimHash Locality-Sensitive Hashing (LSH) Strategy

### Why not standard SHA-256?
Standard SHA-256 has the **Avalanche Effect** (1-bit difference produces a completely different hash). Biometric images naturally vary between selfies due to lighting, slight angle, and expressions. Two photos of the same person will never produce the exact same raw byte hash.

### How 256-bit SimHash bridges the gap:
1. **Feature Vector Extraction**: 468 landmarks from MediaPipe are centered and scaled by inter-ocular distance to create a scale- and translation-invariant geometric vector $\vec{v} \in \mathbb{R}^D$.
2. **Random Hyperplane Projection**: Project $\vec{v}$ onto 256 fixed hyperplanes $W \in \mathbb{R}^{256 \times D}$: $\vec{p} = W \vec{v}$.
3. **Binarization**: Each hyperplane creates 1 bit: $b_i = 1$ if $p_i \ge 0$ else $0$.
4. **Format Match**: 256 bits = 32 bytes = **exactly 64 hexadecimal characters**, matching the database `VARCHAR(64)` and test suite requirements perfectly!
5. **Hamming Distance Comparison**:
   $$\text{match\_score} = 1.0 - \frac{\text{HammingDistance}(\text{hash}_1, \text{hash}_2)}{64}$$
   * Same person: small Hamming distance $\rightarrow \text{match\_score} \ge 0.70$ (PASS).
   * Different person: large Hamming distance $\rightarrow \text{match\_score} < 0.50$ (FAIL).

---

## 🛡️ 4. Anti-Spoofing & Liveness Detection

| Challenge Mode | Method | Detection Target | Pass Criteria |
|---|---|---|---|
| **Passive (Single-Frame)** | 3D Depth Protrusion ($z$-coordinate of Nose Tip L1 vs Ears/Cheeks L234/L454) | 2D Paper photos, flat screen replays | $|z| > 0.03$ (Proves 3D face structure) |
| **Eye Blink (`blink`)** | Eye Aspect Ratio (EAR) across eye contour landmarks | Replay videos, static photos | $\text{EAR} < 0.20$ during blink |
| **Head Turn (`head_turn`)** | Yaw ratio of nose tip relative to left vs right eye corners | Photo spoofing | $\text{Ratio} < 0.6$ (Left) or $> 1.6$ (Right) |
| **Head Tilt (`head_tilt`)** | Roll angle $\theta = \arctan2(\Delta y, \Delta x)$ of eye axis | Photo spoofing | $|\theta| > 15^\circ$ |

---

## 📂 5. Folder Structure & Separation of Concerns

```text
module3-face-recognition/
├── Dockerfile                      # Container build definition (Debian + OpenCV deps)
├── requirements.txt                # FastAPI, MediaPipe, OpenCV, NumPy, Pillow, Redis, OTEL
├── README.md                       # This architecture & roadmap documentation
└── app/
    ├── __init__.py
    ├── main.py                     # FastAPI entrypoint, CORS, route definitions, health checks
    ├── models.py                   # Pydantic request & response schemas (DTOs)
    │
    ├── core/                       # Computer Vision & Math Engine
    │   ├── __init__.py
    │   ├── image_utils.py          # Base64 decoding, PIL conversion, quality & blurriness scoring
    │   ├── detector.py             # Cached singleton MediaPipe FaceDetection & FaceMesh
    │   └── simhash.py              # Landmark vectorization, 256-bit LSH, Hamming distance
    │
    └── services/                   # Business Logic & Risk Analysis
        ├── __init__.py
        ├── liveness_service.py     # 3D Depth analysis & active challenges (blink, head pose)
        └── risk_service.py         # Multi-signal weighted risk fusion, IP/VPN heuristics
```

---

## 📡 6. API Endpoints Specification

| Method | Endpoint | Description | Public Test Points |
|---|---|---|---|
| `GET` | `/health` | Health check (`{"status": "healthy", "service": "saiv-face-recognition"}`) | 1 pt |
| `GET` | `/` | API endpoint directory listing | 1 pt |
| `POST` | `/face/enroll` | Enroll face, validate consent, return 64-char hash & quality score | 4 pts |
| `POST` | `/face/verify` | Verify check-in selfie against enrolled template hash | 4 pts |
| `POST` | `/face/match` | Alias for `/face/verify` (backward compatibility) | Shared |
| `POST` | `/risk/assess` | Multi-signal risk calculation (Liveness, Match, Device, VPN, Geo) | 3 pts |
| `POST` | `/liveness/check`| 3D depth cue and active challenge liveness evaluation | Bonus (3 pts) |

---

## 🚀 7. Step-by-Step Implementation Roadmap

- [ ] **Milestone 1: Health & Root Endpoints** (`app/main.py`) — *2 pts*
- [ ] **Milestone 2: Image Decoding & Quality Assessment** (`app/core/image_utils.py`)
- [ ] **Milestone 3: MediaPipe Detector & Face Mesh Manager** (`app/core/detector.py`)
- [ ] **Milestone 4: Landmark Vectorization & 256-bit SimHash** (`app/core/simhash.py`)
- [ ] **Milestone 5: Face Enrollment Endpoint** (`POST /face/enroll`) — *4 pts*
- [ ] **Milestone 6: Face Verification Endpoint** (`POST /face/verify`) — *4 pts*
- [ ] **Milestone 7: Privacy & Memory Sanitation** (`test_privacy_basic.py`) — *2 pts*
- [ ] **Milestone 8: Multi-Signal Risk Assessment Engine** (`POST /risk/assess`) — *3 pts*
- [ ] **Milestone 9: 3D Depth & Active Liveness Challenges** (`POST /liveness/check`) — *Bonus & Hidden Tests*

---

## 🧪 8. How to Test Standalone

1. **Start the Service**:
   ```bash
   source .venv/bin/activate
   cd module3-face-recognition
   uvicorn app.main:app --reload --port 8001
   ```

2. **Run Public Test Suite (15 Public Points)**:
   ```bash
   pytest tests/public/test_face_recognition.py -v
   ```

3. **Interactive Swagger Docs**:
   Open `http://localhost:8001/docs` in any web browser.
