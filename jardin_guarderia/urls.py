# jardin_guarderia/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jardin_app.urls')),  # Incluye las rutas de jardin_app
]
