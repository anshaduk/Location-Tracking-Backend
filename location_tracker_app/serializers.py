from rest_framework import serializers
from django.contrib.auth.models import User
from location_tracker_app.models import UserLocation
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']


class UserLocationSerializer(GeoFeatureModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)


    class Meta:
        model = UserLocation
        geo_field = 'point'
        fields = ['id','user','username','point','timestamp','is_active']
        read_only_fields = ['timestamp']