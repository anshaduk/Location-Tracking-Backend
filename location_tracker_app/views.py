from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from location_tracker_app.models import UserLocation
from location_tracker_app.serializers import UserSerializer,UserLocationSerializer
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


class UserListView(APIView):
    def get(self,requet):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)
    

class UserLocationUpdateView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            latitude = float(request.data.get('latitude'))
            longitude = float(request.data.get('longitude'))

            point = Point(longitude,latitude)

            user_loaction, created = UserLocation.objects.update_or_create(
                user=request.user,
                is_active=True,
                defaults={'point': point}
            ) 

            serializer = UserLocationSerializer(user_loaction)

            ##Broadcast to Websocket##
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "location_updates",
                {
                    "type": "location_update",
                    "message": serializer.data
                }
            )

            return Response(serializer.data,status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        
        except (ValueError,TypeError) as e:
            return Response({"error":f"Invalid location data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        


class ActiveLocationsView(APIView):
    def get(self,request):
        locations = UserLocation.objects.filter(is_active=True)
        serializer = UserLocationSerializer(locations,many=True)
        return Response(serializer.data)
    

class LocationHistoryView(APIView):
    def get(self,request,user_id):
        try:
            limit = int(request.query_params.get('limit',100))

            locations = UserLocation.objects.filter(user_id=user_id).order_by('-timestamp')[:limit]
            serializer = UserLocationSerializer(locations,many=True)
            return Response(serializer.data)
        
        except User.DoesNotExist:
            return Response({"error":"User not found"},status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error":"Invalid parameters"},status=status.HTTP_400_BAD_REQUEST)

