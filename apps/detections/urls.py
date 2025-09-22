# detections/urls.py
from django.urls import path
from . import views

app_name = "detections"

urlpatterns = [
    path("upload-video/", views.upload_video, name="upload_video"),
    path("save-detection/", views.save_detection, name="save_detection"),
]
