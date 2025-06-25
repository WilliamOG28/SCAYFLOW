from django.urls import path
from . import views

urlpatterns = [
    #Url principal
    path('', views.base, name='base'),

    #Urls para proyectos
    path('proyectos', views.proyectos, name='proyectos'),
    path('proyectos/nuevo', views.nuevo_proyecto, name='nuevo_proyecto'),
    path('proyectos/lista', views.lista_proyectos, name='lista_proyectos'),
    path('proyectos/detalles', views.detalles, name='detalles'),

    #Urls para clientes
    path('clientes', views.clientes, name='clientes'),
    path('clientes/nuevo', views.nuevo_cliente, name='nuevo_cliente'),
    path('clientes/lista', views.lista_clientes, name='lista_clientes'),
    ]