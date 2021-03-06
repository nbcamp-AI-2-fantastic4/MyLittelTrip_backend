from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('place/', include('place.urls')),
    path('comment/', include('comment.urls')),
    path('like/', include('like.urls')),
    path('review/', include('review.urls')),
    path('user/', include("user.urls")), 
    path('trip/', include("trip.urls")), 
    path('recommend/', include("recommend.urls")), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
