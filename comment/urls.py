from django.urls import path
from comment import views

urlpatterns = [
    # comment/
    path('', views.CommentView.as_view()),
    path('<comment_id>/', views.CommentView.as_view()),
    path('<posttype_id>/<post_id>/', views.CommentView.as_view())
]
