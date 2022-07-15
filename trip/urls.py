from django.urls import path
from . import views

# trip/
urlpatterns = [
    path('', views.TripView.as_view(), name="trip"), 
    path('<trip_id>/', views.TripDetailView.as_view(), name="trip_detail"), 
]