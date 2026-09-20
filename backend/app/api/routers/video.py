from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from app.pipeline.inference import process_video_stream

router = APIRouter()

@router.get("/")
def get_video_status():
    return {"status": "Video processing router is active."}

@router.websocket("/stream")
async def websocket_video_stream(websocket: WebSocket):
    """
    WebSocket endpoint for streaming video processing results.
    In a real scenario, this would connect to an RTSP stream.
    """
    await websocket.accept()
    try:
        # Pass the websocket to the inference pipeline to stream alerts/metadata
        await process_video_stream(websocket)
    except WebSocketDisconnect:
        print("Client disconnected from video stream")
    except Exception as e:
        print(f"Error in video stream: {e}")
        await websocket.close()
