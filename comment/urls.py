from django.urls import path
from comment import views

urlpatterns = [
    # comment/
    path('', views.CommentView.as_view(), name="comment_post_view"),
    path('<comment_id>/', views.CommentView.as_view(), name="comment_put_delete_view"),
    path('<posttype_id>/<post_id>/', views.CommentView.as_view(), name="comment_get_view")
]
