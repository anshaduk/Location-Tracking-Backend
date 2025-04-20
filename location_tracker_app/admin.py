# from django.contrib import admin
# from django.contrib.gis.admin import GISModelAdmin
# from location_tracker_app.models import UserLocation


# @admin.register(UserLocation)
# class UserLocationAdmin(GISModelAdmin):
#     list_display = ('user','timestamp','is_active')
#     list_filter = ('user','is_active')
#     search_fields = ('user__username',)


from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from location_tracker_app.models import UserLocation

@admin.register(UserLocation)
class UserLocationAdmin(LeafletGeoAdmin):
    list_display = ('user', 'timestamp', 'is_active')
    settings_overrides = {
        'DEFAULT_CENTER': (37.75, -122.4),
        'DEFAULT_ZOOM': 12,
        'MAX_ZOOM': 20,
    }