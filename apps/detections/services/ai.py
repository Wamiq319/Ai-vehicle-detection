import random
from django.utils import timezone
from apps.detections.models import Detection
from apps.tolls.models import TollRate


def process_video_and_create_detections(video_file) -> int:
    """
    Stub AI processor. For now, create a few random detections.
    Returns number of detections created.
    """
    vehicle_types = ["truck", "car", "bolan"]
    created = 0
    for _ in range(random.randint(2, 6)):
        v = random.choice(vehicle_types)
        try:
            rate = TollRate.objects.get(vehicle_type=v).rate
        except TollRate.DoesNotExist:
            rate = 0
        Detection.objects.create(
            vehicle_type=v,
            toll_rate=rate,
            detected_at=timezone.now(),
        )
        created += 1
    return created

