# detections/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from apps.tolls.models import TollRate
from .models import Detection
from .services.ai import process_video_and_create_detections

def upload_video(request):
    """Handles video uploads from the frontend"""
    if request.method == "POST":
        video_file = request.FILES.get("video_file")
        if not video_file:
            messages.error(request, "Please upload a video file.")
            return redirect("detections:upload_video")

        # 👉 Call AI stub to generate detections for now
        created = process_video_and_create_detections(video_file)
        messages.success(request, f"Video uploaded. {created} detections recorded.")
        return redirect("reports:reports")

    # Build simple rates context for the UI
    rates_qs = TollRate.objects.all()
    rates = {
        "truck": next((r.rate for r in rates_qs if r.vehicle_type == "truck"), 0),
        "car": next((r.rate for r in rates_qs if r.vehicle_type == "car"), 0),
        "bolan": next((r.rate for r in rates_qs if r.vehicle_type == "bolan"), 0),
    }

    return render(request, "dashbaord/admin/video_detect.html", {"rates": rates})


def save_detection(request):
    """
    API endpoint — AI system calls this with detected vehicle.
    Example payload: { "vehicle_type": "car" }
    """
    if request.method == "POST":
        vehicle_type = request.POST.get("vehicle_type")

        if vehicle_type not in ["truck", "car", "bolan"]:
            return JsonResponse({"error": "Invalid vehicle type"}, status=400)

        try:
            toll_rate = TollRate.objects.get(vehicle_type=vehicle_type).rate
        except TollRate.DoesNotExist:
            toll_rate = 0.00

        Detection.objects.create(
            vehicle_type=vehicle_type,
            toll_rate=toll_rate,
            detected_at=timezone.now()
        )

        return JsonResponse({
            "status": "success",
            "vehicle": vehicle_type,
            "toll": str(toll_rate)
        })

    return JsonResponse({"error": "Only POST allowed"}, status=405)


