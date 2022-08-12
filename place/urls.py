
from django.contrib import admin
from django.urls import path, include
from . import views

# place/
urlpatterns = [
    path('', views.PlaceViewAll.as_view(),name='place_view'),
    path('<place_id>/', views.PlaceViewAll.as_view()),
    path('detail/<place_id>/', views.PlaceViewDetail.as_view(),name='place_detailview')
    
]
