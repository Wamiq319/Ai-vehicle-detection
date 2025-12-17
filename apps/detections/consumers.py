import json
import os
import cv2
import base64
import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from ultralytics import YOLO
from channels.db import database_sync_to_async
from django.utils import timezone
from apps.tolls.models import TollRate
from .models import Detection

class LiveDetectionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        # Clean up video file if it exists
        if hasattr(self, 'video_path') and os.path.exists(self.video_path):
            os.remove(self.video_path)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        video_url = data.get('video_url')

        if video_url:
            self.video_path = os.path.join(settings.MEDIA_ROOT, os.path.basename(video_url))
            await self.process_video()

    async def process_video(self):
        # Load the trained model
        model_path = os.path.join(settings.BASE_DIR, "apps", "detections/services", "Model.pt")
        model = YOLO(model_path)

        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        charged_ids = set()
        all_boxes = {}
        frame_number = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            timestamp = round(frame_number / fps, 2)
            
            # Run detection
            results = model.track(frame, persist=True, tracker="bytetrack.yaml", conf=0.5, classes=[0, 1, 2, 3, 4, 5])
            
            boxes_data = []
            if results[0].boxes is not None and results[0].boxes.id is not None:
                # Save detections to DB and collect box data
                for box, track_id, cls in zip(results[0].boxes.xyxy, results[0].boxes.id, results[0].boxes.cls):
                    vid = int(track_id)
                    cname = model.names[int(cls)].lower()
                    if vid not in charged_ids:
                        charged_ids.add(vid)
                        await self.save_detection(cname)
                    
                    x1, y1, x2, y2 = box
                    boxes_data.append({
                        "x1": float(x1),
                        "y1": float(y1),
                        "x2": float(x2),
                        "y2": float(y2),
                        "label": cname
                    })
            
            if boxes_data:
                all_boxes[str(timestamp)] = boxes_data

            frame_number += 1

        cap.release()
        
        # Send a single message with all bounding box data
        video_url = os.path.basename(self.video_path)
        await self.send(text_data=json.dumps({
            'status': 'complete',
            'video_url': f'/media/{video_url}',
            'box_data': all_boxes
        }))

        # The video file is kept for the frontend to play, so we don't remove it here.
        # It should be cleaned up later, perhaps by a separate management command or user action.


    @database_sync_to_async
    def save_detection(self, vehicle_type):
        if vehicle_type in ["car", "threewheel", "bus", "truck", "motorbike", "van"]:
            try:
                toll_rate = TollRate.objects.get(vehicle_type=vehicle_type).rate
            except TollRate.DoesNotExist:
                toll_rate = 0.00

            Detection.objects.create(
                vehicle_type=vehicle_type,
                toll_rate=toll_rate,
                detected_at=timezone.now()
            )
