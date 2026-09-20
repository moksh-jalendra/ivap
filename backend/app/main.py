from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from app.api.routers import video

FRONTEND_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"

app = FastAPI(
    title="IBVAP Backend API",
    description="Backend for the Intelligent Border Video Analytics Platform",
    version="1.0.0"
)

# Configure CORS for Vercel/localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video.router, prefix="/api/video", tags=["Video"])

assets_dir = FRONTEND_DIST / "assets"
if assets_dir.is_dir():
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "IBVAP Backend is running"}


@app.get("/", include_in_schema=False)
def frontend_index():
    index_file = FRONTEND_DIST / "index.html"
    if index_file.is_file():
        return FileResponse(index_file)
    return JSONResponse({"status": "ok", "message": "IBVAP API is running"})


@app.get("/{path:path}", include_in_schema=False)
def frontend_route(path: str):
    requested_file = FRONTEND_DIST / path
    if requested_file.is_file() and FRONTEND_DIST in requested_file.parents:
        return FileResponse(requested_file)

    index_file = FRONTEND_DIST / "index.html"
    if index_file.is_file():
        return FileResponse(index_file)
    return JSONResponse({"detail": "Not found"}, status_code=404)
