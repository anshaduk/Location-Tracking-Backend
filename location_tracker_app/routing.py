from django.urls import re_path
from location_tracker_app.consumers import LocationConsumer


websocket_urlpatterns = [
    re_path(r'ws/locations/$',LocationConsumer.as_asgi()),
]