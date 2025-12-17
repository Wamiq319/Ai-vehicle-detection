from django.urls import path
from .consumers import LiveDetectionConsumer

websocket_urlpatterns = [
    path("ws/live-detection/", LiveDetectionConsumer.as_asgi()),
]
