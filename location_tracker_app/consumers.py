import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point  # ✅ Required for spatial data
from location_tracker_app.models import UserLocation
from location_tracker_app.serializers import UserLocationSerializer

class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = None
        await self.accept()

    async def disconnect(self, close_code):
        if self.user:
            pass

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            user_id = text_data_json.get('user_id')
            latitude = text_data_json.get('latitude')
            longitude = text_data_json.get('longitude')

            if user_id and latitude and longitude:
                user = User.objects.get(id=user_id)
                point = Point(float(longitude), float(latitude))  # Cast to float

                user_location, created = UserLocation.objects.update_or_create(
                    user=user,
                    is_active=True,
                    defaults={'point': point}
                )

                serializer = UserLocationSerializer(user_location)

                await self.send(text_data=json.dumps({
                    'message': serializer.data
                }))
        except Exception as e:
            print(f"Error processing message: {e}")

    async def location_update(self, event):
        await self.send(text_data=json.dumps(event["message"]))
