
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.oaauth.urls')),
    path('absent/', include('apps.absent.urls')),
    path('inform/', include('apps.inform.urls')),
    path('staff/', include('apps.staff.urls')),
]
