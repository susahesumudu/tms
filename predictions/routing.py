from django.urls import path
from .consumers import NotificationConsumer
from predictions.routing import websocket_urlpatterns

websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi()),
]
