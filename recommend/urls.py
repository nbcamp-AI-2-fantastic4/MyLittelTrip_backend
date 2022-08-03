from django.urls import path
from . import views

# recommend/
urlpatterns = [
    path('', views.ParsingView.as_view()),
    path('schedule/', views.ScheduleView.as_view()),
]
