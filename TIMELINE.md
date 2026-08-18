# SAIV 10-Week Master Timeline (Week-by-Week)

A detailed 10-week roadmap for all 4 team members, aligning weekly deliverables, technical specifications, integration checkpoints, and test coverage to achieve full points (90 public + 40 hidden).

---

## High-Level Phase Overview

```
┌────────────────────────────────────────────────────────────────────────┐
│ Weeks 1–2: Foundation, Schema & Environment Setup                      │
├────────────────────────────────────────────────────────────────────────┤
│ Weeks 3–5: Core Module Implementation & Unit Development               │
├────────────────────────────────────────────────────────────────────────┤
│ Weeks 6–7: Cross-Module Integration & Passing 90/90 Public Tests       │
├────────────────────────────────────────────────────────────────────────┤
│ Weeks 8–9: Security Hardening, Anti-Spoofing & Hidden Test Prep        │
├────────────────────────────────────────────────────────────────────────┤
│ Week 10: Final System Polish, Performance Benchmarking & Demo Rehearsal│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🔹 Week 1: Environment Setup, Database Schema & Architecture Scaffolding

### 🎯 Weekly Goal
Establish the infrastructure, initialize repositories, define data contracts, and verify all base Docker containers and health endpoints.

| Module | Tasks & Technical Specifications |
|---|---|
| **Module 1**<br>*(Frontend)* | • Initialize Next.js 14 project with TypeScript and Tailwind CSS.<br>• Set up folder architecture (`/app`, `/components`, `/lib/api`, `/hooks`).<br>• Configure PWA skeleton (`manifest.json`, service worker registration).<br>• Create API client wrapper with Axios/Fetch and base interceptors for JWT injection. |
| **Module 2**<br>*(Backend)* | • Define SQLAlchemy 2.0 ORM models in `app/models/` for all 8 tables (`User`, `Course`, `Enrollment`, `Session`, `Device`, `CheckIn`, `RiskSignal`, `AuditLog`).<br>• Configure Alembic migrations and generate the initial migration script.<br>• Implement `GET /health` returning `{"status": "healthy", "service": "backend"}`.<br>• Set up Redis connection pool. |
| **Module 3**<br>*(Face Service)* | • Implement `GET /health` and `GET /` (listing all available endpoints).<br>• Set up base image loading and decoding pipeline (`decode_base64_image`) using Pillow and NumPy.<br>• Verify MediaPipe Face Detection initialization against sample test images in `sample_images/`. |
| **Module 4**<br>*(Dashboard)* | • Initialize Streamlit application structure (`app/main.py`, `/pages`).<br>• Configure PostgreSQL direct read connection and base Streamlit page layout.<br>• Verify Prometheus configuration (`prometheus.yml`) and Grafana connection. |

**🤝 Week 1 Integration Milestone:**
- Run `docker compose up -d postgres redis prometheus grafana`.
- Verify database migrations apply cleanly: `alembic upgrade head`.

---

## 🔹 Week 2: Core Authentication, Hashing & Base UI

### 🎯 Weekly Goal
Implement secure authentication (Bcrypt, JWT HS256, RBAC) and base frontend auth pages.

| Module | Tasks & Technical Specifications |
|---|---|
| **Module 1**<br>*(Frontend)* | • Build responsive **Registration Page** (Email, Password, Full Name, Role selector).<br>• Build **Login Page** with client-side field validation.<br>• Implement JWT token storage strategy (`accessToken` in memory/state, `refreshToken` in secure storage).<br>• Implement automatic token refresh interceptor on HTTP 401 responses. |
| **Module 2**<br>*(Backend)* | • Implement password hashing using `passlib[bcrypt]` (cost factor $\ge 10$).<br>• Implement `POST /api/v1/auth/register` (return `201 Created` with user JSON; reject weak passwords $< 8$ chars with `422`).<br>• Implement `POST /api/v1/auth/login` (issue 1-hour access token & 7-day refresh token).<br>• Implement `POST /api/v1/auth/refresh` and `POST /api/v1/auth/logout`.<br>• Create FastAPI dependency `get_current_user` with RBAC role hierarchy (`student`, `ta`, `instructor`, `admin`). |
| **Module 3**<br>*(Face Service)* | • Build face bounding box extraction and validation logic in `detect_face()`.<br>• Implement face quality scoring algorithm (checking face size relative to frame, bounding box aspect ratio, and detection confidence). |
| **Module 4**<br>*(Dashboard)* | • Build Instructor/TA Login page in Streamlit connecting to Backend `POST /api/v1/auth/login`.<br>• Persist session state (`st.session_state.token`) across dashboard page navigation. |

**🧪 Test Target:**
- Backend passes `pytest tests/public/test_api_functional.py -k TestAuthentication` (**5 pts**).
- Backend passes `pytest tests/public/test_security_basic.py -k TestAuthenticationSecurity` (**4 pts**).

---

## 🔹 Week 3: User Management, Consent Flow & Face Enrollment

### 🎯 Weekly Goal
Implement user profile management, explicit camera/location consent flows, and face enrollment hashing.

| Module | Tasks & Technical Specifications |
|---|---|
| **Module 1**<br>*(Frontend)* | • Build **User Profile & Consent Screen**.<br>• Implement explicit UI toggles for `camera_consent` and `geolocation_consent`.<br>• Integrate WebRTC camera stream (`navigator.mediaDevices.getUserMedia`) for face capture.<br>• Add camera capture canvas to convert live video frame to Base64 (stripping `data:image/...;base64,` header). |
| **Module 2**<br>*(Backend)* | • Implement `GET /api/v1/users/me` and `PUT /api/v1/users/me` (consent preference updates).<br>• Implement `POST /api/v1/users/me/face/enroll` proxying to Face Recognition service.<br>• Implement Admin user endpoints (`GET /api/v1/users/`, `GET /api/v1/users/{id}`, `PATCH /api/v1/users/{id}`).<br>• Implement testing admin hooks: `/api/v1/admin/users/{id}/activate` and `/api/v1/admin/users/{id}/deactivate`. |
| **Module 3**<br>*(Face Service)* | • Implement `POST /face/enroll`:
  - Validate `camera_consent == True` (return `400` if `False`).
  - Reject non-face / solid color images with `400` or `enrollment_successful=False`.
  - Crop normalized face region, resize to standard $64 \times 64$, and generate 64-char SHA-256 hex string.
  - Return `quality_score >= 0.5` for clear faces.<br>• Ensure zero raw images are written to disk. |
| **Module 4**<br>*(Dashboard)* | • Build **User & Student Directory View** in Streamlit (listing enrolled students, face enrollment status, active status). |

**🧪 Test Target:**
- Face Service passes `pytest tests/public/test_face_recognition.py -k TestFaceEnrollment` (**4 pts**).
- Backend passes `pytest tests/public/test_privacy_basic.py -k TestConsentManagement` (**3 pts**).

---

## 🔹 Week 4: Face Verification & Device Binding

### 🎯 Weekly Goal
Implement template verification in Module 3, Web Crypto device binding in Module 1, and device tracking in Module 2.

| Module | Tasks & Technical Specifications |
|---|---|
| **Module 1**<br>*(Frontend)* | • Implement Web Crypto API (`window.crypto.subtle`) for ECDSA (P-256) key-pair generation.<br>• Store private key in IndexedDB (non-exportable) and export public key in SPKI PEM format.<br>• Implement device fingerprint generation (browser properties, screen dimensions, canvas hash). |
| **Module 2**<br>*(Backend)* | • Implement `GET /api/v1/devices/my-devices` and device registration logic.<br>• Implement device trust evaluation (check for emulator/root flags in payload).<br>• Enforce RBAC security checks across all routes (student blocked from instructor endpoints). |
| **Module 3**<br>*(Face Service)* | • Implement `POST /face/verify` and alias `POST /face/match`:
  - Decode incoming image and detect face.
  - Compute current face template hash.
  - Compare with `reference_template_hash`: return `match_score >= 0.70` for same person, `< 0.70` for different person.
  - Set `match_passed = (match_score >= 0.70)`. |
| **Module 4**<br>*(Dashboard)* | • Build **Device Inventory View** showing student registered devices, platform stats, and trust levels. |

**🧪 Test Target:**
- Face Service passes `pytest tests/public/test_face_recognition.py -k TestFaceMatching` (**4 pts**).
- Backend passes `pytest tests/public/test_api_functional.py -k TestDeviceManagement` (**2 pts**).
- Backend passes `pytest tests/public/test_security_basic.py -k TestAuthorizationControls` (**4 pts**).

---

## 🔹 Week 5: Courses, Sessions & Geofencing Engine

### 🎯 Weekly Goal
Implement course/session management, Haversine geofence verification, and session status lifecycles.

| Module | Tasks & Technical Specifications |
|---|---|
| **Module 1**<br>*(Frontend)* | • Integrate HTML5 Geolocation API (`navigator.geolocation.getCurrentPosition`).<br>• Capture `latitude`, `longitude`, and `accuracy` with fallback handling when location permission is denied.<br>• Build **Active Sessions Screen** displaying ongoing lectures for enrolled courses. |
| **Module 2**<br>*(Backend)* | • Implement Course endpoints (`GET /api/v1/courses/`, `GET /api/v1/courses/{id}`).<br>• Implement Session endpoints (`POST /api/v1/sessions/`, `GET /api/v1/sessions/active`, `GET /api/v1/sessions/{id}`).<br>• Implement Haversine distance formula to compute distance (meters) between check-in coordinates and session venue coordinates.<br>• Implement admin test helpers: `PATCH /api/v1/admin/sessions/{id}/status` and `POST /api/v1/admin/enrollments/`. |
| **Module 3**<br>*(Face Service)* | • Begin MediaPipe Face Mesh integration for 3D landmark extraction (468 landmarks).<br>• Extract landmark index 1 (`nose_tip`) to measure z-depth ($|z| > 0.03$ for real 3D faces). |
| **Module 4**<br>*(Dashboard)* | • Build **Session Management View**:
  - Create new sessions with venue GPS coordinates & geofence radius (meters).
  - Open, close, and activate sessions in real time. |

**🧪 Test Target:**
- Backend passes `pytest tests/public/test_api_functional.py -k "TestCourseManagement or TestSessionManagement"` (**8 pts**).

---

## 🔹 Week 6: Liveness Detection, Risk Engine & Check-in Pipeline

### 🎯 Weekly Goal
Complete the multi-signal risk assessment engine, 3D liveness detection, and check-in submission pipeline.

| Module | Tasks & Technical Specifications |
|---|---|
| **Module 1**<br>*(Frontend)* | • Build **Interactive Check-in Wizard**:
  1. Select Active Session.
  2. Complete Liveness Challenge (Blink or Steady Face prompt).
  3. Obtain GPS Coordinates.
  4. Submit payload to `POST /api/v1/checkins/`.
  5. Display check-in confirmation (Approved vs Flagged with risk level). |
| **Module 2**<br>*(Backend)* | • Implement `POST /api/v1/checkins/`:
  - Validate session is active and user is enrolled.
  - Enforce single check-in constraint `(session_id, student_id)` — return `400` on duplicate.
  - Call Face Recognition service internally via `httpx` async client.
  - Compute distance and determine status (`approved` if `risk_score < threshold`, else `flagged`).
  - Write immutable audit entry to `audit_logs`.<br>• Implement `GET /api/v1/checkins/my-checkins` and `GET /api/v1/checkins/session/{id}`. |
| **Module 3**<br>*(Face Service)* | • Implement `POST /liveness/check` (Bonus feature):
  - Analyze 3D depth cue (`nose_tip_z`), face mesh completeness, and texture/color consistency.
  - Output `liveness_score` and `liveness_passed = (liveness_score >= 0.60)`.<br>• Implement `POST /risk/assess`:
  - Combine Liveness (25%), Face Match (25%), Device (20%), VPN/Network (15%), Geolocation (15%).
  - Map `risk_score` to `LOW` ($<0.3$), `MEDIUM` ($0.3-0.5$), `HIGH` ($0.5-0.7$), `CRITICAL` ($\ge 0.7$).
  - Return actionable recommendation strings for high-risk signals. |
| **Module 4**<br>*(Dashboard)* | • Build **Live Session Attendance Monitor**:
  - Live table of student check-ins with color-coded risk badges.
  - Filter by status (`approved`, `flagged`, `rejected`).
  - Action buttons for instructors to manually review and approve/reject flagged check-ins. |

**🧪 Test Target:**
- Face Service passes `pytest tests/public/test_face_recognition.py -k TestRiskAssessment` (**3 pts**).
- Backend passes `pytest tests/public/test_api_functional.py -k TestCheckInWorkflow` (**8 pts**).

---

## 🔹 Week 7: Full Integration & 90-Point Public Test Gate

### 🎯 Weekly Goal
Connect all services, verify rate limiting, ensure frontend/dashboard API contracts match, and achieve 100% on the Public Test Suite.

| Module | Tasks & Technical Specifications |
|---|---|
| **Module 1**<br>*(Frontend)* | • Validate contract compliance against `test_frontend_dashboard.py`.<br>• Implement user error banners for rate limiting (`429 Too Many Requests`) and out-of-bounds geofence warnings. |
| **Module 2**<br>*(Backend)* | • Implement Redis rate-limiting middleware (sliding window / fixed window counter):
  - Login: 60/hr per IP.
  - Check-in: 10/min per User.
  - Registration: 10/hr per IP.<br>• Implement Statistics endpoints (`/api/v1/stats/overview`, `/api/v1/stats/sessions/{id}`, `/api/v1/stats/courses/{id}`, `/api/v1/stats/students/{id}`).<br>• Implement `GET /api/v1/audit/` (Admin only). |
| **Module 3**<br>*(Face Service)* | • Verify response hygiene: confirm no Base64 strings or image buffers exist in any response payload.<br>• Benchmark latency on `/face/verify` and `/liveness/check` (target $< 300\text{ms}$). |
| **Module 4**<br>*(Dashboard)* | • Connect Overview Page to Backend `/api/v1/stats/*` endpoints.<br>• Implement **Audit Log Explorer** with filter controls (action, user ID, timestamp range).<br>• Implement **Gradebook CSV Export** matching LMS schema. |

**🏆 Week 7 Major Milestone:**
Execute full public test suite from root:
```bash
pytest tests/public/ -v
```
👉 **Score Target: 90.0 / 90.0 points (100% Letter Grade A)**.

---

## 🔹 Week 8: Anti-Spoofing, Replay Protection & Hidden Test Prep

### 🎯 Weekly Goal
Harden security against the 40 points of Hidden Tests (GPS spoofing, replay attacks, VPN detection, 2D photo spoofing).

| Module | Tasks & Technical Specifications |
|---|---|
| **Module 1**<br>*(Frontend)* | • Implement dynamic timestamp and challenge nonce signing in check-in payload.<br>• Add offline check-in queue using `localforage` for caching check-ins when network drops, with auto-sync on reconnect. |
| **Module 2**<br>*(Backend)* | • Implement Replay Attack Prevention (reject duplicate nonce/timestamp older than 2 minutes).<br>• Implement GPS Spoofing detection:
  - Flag impossible travel speed ($> 1000\text{ km/h}$ between consecutive check-ins).
  - Flag suspiciously perfect accuracy ($0.0\text{m}$) or unrealistic altitude/speed data.<br>• Implement bulk user creation endpoint: `POST /api/v1/admin/users/bulk` (for stress test setup). |
| **Module 3**<br>*(Face Service)* | • Implement **Advanced Anti-Spoofing Heuristics**:
  - Detect 2D paper photos / printed paper attacks (flat mesh $z \approx 0$).
  - Detect screen replay / moiré patterns through frequency domain texture analysis.<br>• Implement Blink EAR (Eye Aspect Ratio) challenge-response:
    $$\text{EAR} = \frac{\|p_2 - p_6\| + \|p_3 - p_5\|}{2 \|p_1 - p_4\|}$$
    Trigger liveness pass when eye blinks during challenge window. |
| **Module 4**<br>*(Dashboard)* | • Build **Risk Signal Deep Dive Modal** showing signal breakdown (Liveness, Match, Device, VPN, Geo) for flagged check-ins.<br>• Query Prometheus for risk score distribution histograms. |

---

## 🔹 Week 9: Privacy Auditing, Stress Testing & Performance Optimization

### 🎯 Weekly Goal
Pass privacy audits (30-day data retention, zero raw images in DB/disk) and stress tests (20+ concurrent check-ins, p95 latency $< 2\text{s}$).

| Module | Tasks & Technical Specifications |
|---|---|
| **Module 1**<br>*(Frontend)* | • Implement PWA Service Worker caching strategies.<br>• Audit responsive design across mobile (iOS Safari, Android Chrome) and tablet viewport sizes. |
| **Module 2**<br>*(Backend)* | • Implement **30-Day Data Retention Engine**:
  - Automatically calculate and store `scheduled_deletion_at = NOW() + INTERVAL '30 days'`.
  - Implement cleanup worker to purge expired records.<br>• Audit database queries with SQLAlchemy:
  - Add eager loading (`joinedload`/`selectinload`) to eliminate $N+1$ query issues on check-in listings.<br>• Verify database connection pooling (`pool_size=10, max_overflow=20`). |
| **Module 3**<br>*(Face Service)* | • Implement explicit memory hygiene (`gc.collect()`, `del` image arrays) to prevent memory leaks under sustained load.<br>• Benchmark concurrent face verification under ThreadPool execution. |
| **Module 4**<br>*(Dashboard)* | • Embed real-time Prometheus PromQL metrics cards:
  - `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))`
  - `sum(rate(checkin_success_total[5m])) / sum(rate(checkin_attempts_total[5m])) * 100`<br>• Test large CSV exports (1000+ records) with Pandas. |

**🧪 Test Target:**
- Pass `pytest tests/public/test_performance.py` (**5 pts**).
- Pass `pytest tests/public/test_privacy_basic.py` (**8 pts**).

---

## 🔹 Week 10: Final Polish, Full Docker Validation & Demo Rehearsal

### 🎯 Weekly Goal
Validate cold-boot full Docker Compose setup, polish UI/UX, prepare presentation materials and final report.

| Module | Tasks & Technical Specifications |
|---|---|
| **Module 1**<br>*(Frontend)* | • Final UI styling polish, loading skeletons, smooth micro-interactions, and error toast feedback.<br>• Test camera permissions and GPS consent on live physical mobile devices. |
| **Module 2**<br>*(Backend)* | • Final security audit: verify all passwords hashed with Bcrypt, verify audit logs are immutable (no `updated_at`), verify all admin endpoints protected. |
| **Module 3**<br>*(Face Service)* | • Final model parameter calibration on sample image suite (`sample_images/`). |
| **Module 4**<br>*(Dashboard)* | • Polish Streamlit UI layout and verify Grafana dashboard provisioning (`module4-observability/grafana/provisioning`). |
| **Entire Team** | • **Full Docker Compose Cold Boot Test**:
  ```bash
  docker compose down -v
  docker compose up --build -d
  docker compose ps
  pytest tests/public/ -v
  ```
  • Conduct live demo rehearsal: Instructor opens session $\rightarrow$ Student checks in on mobile with face & GPS $\rightarrow$ Instructor views live approval on dashboard $\rightarrow$ Gradebook CSV exported. |

---

## 📊 Summary Checkpoint Table

| Milestone | Target Week | Target Public Score | Key Deliverables |
|---|:---:|:---:|---|
| **M1: Foundation** | Week 1–2 | 15 / 90 pts | Docker infra up, DB models migrated, Auth endpoints working |
| **M2: Core Features** | Week 3–5 | 50 / 90 pts | Face enroll/verify passing, Course/Session CRUD, Consent flow |
| **M3: Public Test Gate** | Week 6–7 | **90 / 90 pts** | Full integration, check-in flow, rate limiting, stats endpoints |
| **M4: Hidden Test Prep** | Week 8–9 | **130 / 130 pts** | Anti-spoofing, GPS replay defense, privacy audit, stress testing |
| **M5: Final Demo** | Week 10 | Complete | Full Docker cold boot, final report, live capstone presentation |
