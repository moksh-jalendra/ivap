from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import video

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

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "IBVAP Backend is running"}
