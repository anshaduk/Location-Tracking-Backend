from django.urls import path
from location_tracker_app import views


urlpatterns = [
    path('users/',views.UserListView.as_view(),name='user-list'),
    path('update-location/',views.UserLocationUpdateView.as_view(),name='update-location'),
    path('active-locations/',views.ActiveLocationsView.as_view(),name='active-locations'),
    path('location-history/<int:user_id>/',views.LocationHistoryView.as_view(),name='location-history'),
]