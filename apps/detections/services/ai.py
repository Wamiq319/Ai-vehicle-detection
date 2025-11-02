
import os
import uuid
from django.conf import settings
from django.utils import timezone
from ultralytics import YOLO
from apps.tolls.models import TollRate
from ..models import Detection

def process_video_and_create_detections(video_file):
    
    # Generate a unique filename to avoid conflicts
    unique_filename = f"{uuid.uuid4()}.mp4"
    video_path = os.path.join(settings.MEDIA_ROOT, unique_filename)

    # Create the directory if it doesn't exist
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    # Save the uploaded video to the temporary path
    with open(video_path, "wb+") as destination:
        for chunk in video_file.chunks():
            destination.write(chunk)

    # Load the trained model
    model_path = os.path.join(settings.BASE_DIR, "apps", "detections/services", "Model.pt")
    model = YOLO(model_path)

    charged_ids = set()
    detection_count = 0

    # Track video
    for result in model.track(
        source=video_path,
        tracker="bytetrack.yaml",
        stream=True,
        conf=0.5,
        classes=[0, 1, 2, 3, 4, 5]  # Adjust classes as per your model
    ):
        if result.boxes is not None and result.boxes.id is not None:
            for box, track_id, cls in zip(result.boxes.xyxy, result.boxes.id, result.boxes.cls):
                vid = int(track_id)
                cname = model.names[int(cls)].lower()

                if vid not in charged_ids:
                    charged_ids.add(vid)
                    
                    # Map detected class to vehicle type
                    if cname in ["truck", "car", "bolan"]:
                        try:
                            toll_rate = TollRate.objects.get(vehicle_type=cname).rate
                        except TollRate.DoesNotExist:
                            toll_rate = 0.00

                        Detection.objects.create(
                            vehicle_type=cname,
                            toll_rate=toll_rate,
                            detected_at=timezone.now()
                        )
                        detection_count += 1

    # Clean up the temporary video file
    os.remove(video_path)

    return detection_count
