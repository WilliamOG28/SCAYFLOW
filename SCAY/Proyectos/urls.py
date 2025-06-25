from django.urls import path
from . import views

urlpatterns = [
    #Url principal
    path('', views.base, name='base'),

    #Url para proyectos
    path('proyectos', views.proyectos, name='proyectos'),
    path('proyectos/nuevo', views.nuevo, name='nuevo'),
    path('proyectos/gestionar', views.gestionar, name='gestionar'),
    path('proyectos/detalles', views.detalles, name='detalles'),
    ]