
from django.contrib import admin
from django.urls import path
from . import views

# review/
urlpatterns = [
    path('', views.ReviewView.as_view(), name='review_view'),
    path('<review_id>/', views.ReviewDetailView.as_view(), name='review_detail_view'),
]
