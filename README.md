# IBVAP - Intelligent Border Video Analytics Platform

IBVAP is a computer-vision prototype for detecting objects and basic virtual-fence intrusions in video streams. It contains a FastAPI backend and a React/Vite frontend.

> **Prototype status:** This repository is a testing and demonstration prototype. It is not a production border-surveillance system and must not be used for operational decisions. The current version does not implement the complete IBVAP PRD.

## Current Prototype

The current version:

- Loads the YOLOv8n model from `backend/yolov8n.pt`.
- Reads the bundled sample video at `backend/test_vid/sample.mp4`.
- Resizes frames and performs CPU-based object detection.
- Applies one hard-coded polygon as a virtual fence.
- Sends annotated JPEG frames, detections, and intrusion alerts through a WebSocket.
- Displays the live stream and recent in-memory alerts in the React dashboard.

The current version does not yet support RTSP/ONVIF cameras, configurable zones, persistent alerts, evidence clips, user accounts, ANPR, face recognition, behavioral analytics, or offline edge operation.

## Project Structure

```text
backend/
	app/
		main.py                 FastAPI application and CORS configuration
		api/routers/video.py    HTTP status and WebSocket video routes
		pipeline/inference.py   Sample-video inference pipeline
	test_vid/                 Local demonstration video
	yolov8n.pt                YOLOv8n model weights
frontend/
	src/App.jsx               Live monitoring dashboard
	src/index.css             Global styling
Dockerfile                  Single-service production container
render.yaml                 Optional Render configuration for the Docker service
```

## Requirements

- Python 3.10 or newer
- Node.js 18 or newer
- npm
- A machine capable of running OpenCV and YOLO inference on CPU

## Run Locally

### Start the backend

From the repository root:

```bash
cd backend
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies and start FastAPI:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend runs at `http://localhost:8000`.

Useful endpoints:

- `GET /api/health` - health check
- `GET /api/video/` - video router status
- `WS /api/video/stream` - annotated sample-video stream

### Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The Vite development server normally runs at `http://localhost:5173`. In development, the frontend connects to `ws://localhost:8000/api/video/stream`.

## Deploy as One Render Web Service

The current deployment uses one Docker-based web service. The Dockerfile builds the React frontend, installs the Python backend, and runs FastAPI. FastAPI serves both the API and the built frontend from the same URL, including the WebSocket endpoint.

Manual Render deployment:

1. Push the repository to GitHub.
2. In Render, choose **New > Web Service**.
3. Select the repository and choose the `Docker` runtime.
4. Set the Dockerfile path to `./Dockerfile` if Render does not detect it automatically.
5. Set the Docker context to the repository root.
6. Select the Free plan for prototype testing and deploy.

The Docker image uses the Render-provided `PORT` value automatically. No frontend service or `VITE_API_URL` setting is required for production because the frontend connects to the same origin. The optional `render.yaml` describes the same Docker service if Blueprint deployment is used later.

Render's free service can sleep after inactivity, and CPU inference may be slow. The hosted prototype uses the bundled sample video; a cloud service cannot access a developer's local webcam or private CCTV network directly.

Render's free service can sleep after inactivity, and CPU inference may be slow. The hosted prototype uses the bundled sample video; a cloud service cannot access a developer's local webcam or private CCTV network directly.

## Environment Configuration

For local development, the frontend supports this build-time variable:

```text
VITE_API_URL=http://localhost:8000
```

In the single-service production deployment it is not needed because the frontend defaults to `window.location.origin`. Do not place camera credentials or other secrets in frontend environment variables.

## Known Limitations

- The input source is a local sample file, not a live camera integration.
- The virtual-fence polygon is fixed in source code.
- Alerts are held only in browser memory and disappear on refresh.
- No snapshots, video clips, database, audit log, or alert search are implemented.
- No authentication, authorization, user roles, or secure camera-credential storage are implemented.
- Inference currently runs on the server instead of an offline edge device.
- Accuracy, latency, bandwidth, and night-detection targets have not been validated against representative border footage.
- The free Render tier is suitable for testing only and is not an operational deployment target.

## Main Version Improvements

Before calling IBVAP production-ready, the main version needs to address the following areas:

1. Add RTSP and ONVIF camera onboarding with encrypted credential storage.
2. Move inference to an edge deployment with local operation during network outages.
3. Add a camera and zone management UI with editable polygon fences and per-zone thresholds.
4. Add persistent alert storage, evidence snapshots, short clips, search, filters, and retention policies.
5. Add object tracking with stable IDs, loitering, dwell-time, and night-time activity detection.
6. Add ANPR and optional face detection/watchlist integration with explicit privacy controls.
7. Add JWT authentication and role-based access control for administrators, operators, and viewers.
8. Add encrypted storage, TLS configuration, audit logging, rate limits, and secure secret management.
9. Reduce bandwidth by sending metadata by default and requesting evidence on demand.
10. Test accuracy, false-positive rate, alert latency, offline behavior, and edge-device performance using representative labeled footage.
11. Add automated backend and frontend tests, monitoring, health checks, and deployment rollback procedures.

## License and Operational Use

No production-use license, security review, or operational approval is implied by this repository. Complete legal, privacy, safety, and security reviews before connecting the system to real cameras or using its output.
