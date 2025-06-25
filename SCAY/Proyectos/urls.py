from django.urls import path
from . import views

urlpatterns = [
    #Url principal
    path('', views.base, name='base'),

    #Url para proyectos
    path('proyectos', views.proyectos, name='proyectos'),
    path('proyectos/nuevo', views.nuevo, name='nuevo_proyecto'),
    path('proyectos/gestionar', views.gestionar, name='gestion_proyecto'),
    path('proyectos/detalles', views.detalles, name='detalles_proyecto'),
    ]