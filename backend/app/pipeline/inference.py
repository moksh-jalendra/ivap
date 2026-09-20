import cv2
import asyncio
import base64
import numpy as np
import os
from fastapi import WebSocket

try:
    from ultralytics import YOLO
    model = YOLO("yolov8n.pt") 
    HAS_YOLO = True
except ImportError:
    HAS_YOLO = False
    print("Ultralytics not installed. Please run: pip install ultralytics")

ZONE_POLYGON = np.array([[100, 200], [540, 200], [600, 350], [40, 350]], np.int32)

async def process_video_stream(websocket: WebSocket):
    video_path = "test_vid/sample.mp4"
    
    # Try video file, fallback to webcam if missing
    if not os.path.exists(video_path):
        print(f"Warning: {video_path} not found. Trying webcam...")
        video_path = 0
        
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_path}")
        await websocket.send_json({"alerts": ["Error: Could not open video source. Please check camera or test_vid/sample.mp4"]})
        return

    frame_skip = 3 
    frame_count = 0
    consecutive_fails = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            consecutive_fails += 1
            if consecutive_fails > 10:
                print("Failed to read frames continuously. Ending stream.")
                break
                
            # If video ends, loop it back to the beginning
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            await asyncio.sleep(0.1) # CRITICAL: Yield to event loop!
            continue
            
        consecutive_fails = 0
        frame_count += 1
        
        if frame_count % frame_skip != 0:
            continue
            
        frame = cv2.resize(frame, (640, 360))
        
        detections = []
        alerts = []
        
        cv2.polylines(frame, [ZONE_POLYGON], isClosed=True, color=(0, 255, 255), thickness=2)
        
        if HAS_YOLO:
            results = model(frame, classes=[0, 1, 2, 3, 5, 7], verbose=False)
            
            for box in results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]
                
                bottom_center = ((x1 + x2) // 2, y2)
                inside = cv2.pointPolygonTest(ZONE_POLYGON, bottom_center, False) >= 0
                
                color = (0, 0, 255) if inside else (0, 255, 0)
                
                if inside:
                    alerts.append(f"INTRUSION: {cls_name.upper()} detected in restricted zone!")
                    
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{cls_name} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                detections.append({
                    "class": cls_name,
                    "confidence": conf,
                    "bbox": [x1, y1, x2, y2],
                    "intrusion": inside
                })
                
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        frame_b64 = base64.b64encode(buffer).decode('utf-8')
        
        try:
            await websocket.send_json({
                "image": frame_b64,
                "alerts": alerts,
                "detections": detections
            })
        except Exception as e:
            print("Client disconnected", e)
            break
            
        await asyncio.sleep(0.01)
        
    cap.release()
