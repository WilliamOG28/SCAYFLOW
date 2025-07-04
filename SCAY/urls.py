"""SCAY URL Configuration"""
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Proyectos.urls')),  # Include the URLs from the Proyectos app
]
