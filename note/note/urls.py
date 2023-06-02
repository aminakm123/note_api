from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/notes_api/', include('api.v1.notes_api.urls', namespace='notes_api')),
]
