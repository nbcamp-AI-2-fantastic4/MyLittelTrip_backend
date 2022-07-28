from django.urls import path
from like import views

urlpatterns = [
    # like/
    path('', views.LikeView.as_view(), name="like_view"),
]
