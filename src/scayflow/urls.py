"""
URL configuration for scayflow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    #Urls para proyectos
    path('proyectos', views.proyectos, name='proyectos'),
    path('proyectos/nuevo', views.nuevo_proyecto, name='nuevo_proyecto'),
    path('proyectos/lista', views.lista_proyectos, name='lista_proyectos'),
    path('proyectos/detalles', views.detalles, name='detalles'),

    #Urls para clientes
    path('clientes', views.clientes, name='clientes'),
    path('clientes/nuevo', views.nuevo_cliente, name='nuevo_cliente'),
    path('clientes/lista', views.lista_clientes, name='lista_clientes'),
    path('clientes/editar', views.editar_cliente, name='editar_cliente'),

     #Urls para tramites
    #path('tramites', views.tramites, name='tramites'),
    path('tramites/nuevo', views.nuevo_tramite, name='nuevo_tramite'),
    path('tramites/lista', views.lista_tramites, name='lista_tramites'),

    #Urls para pagos
    path('pagos/pagos', views.pagos, name='pagos'),
    path('pagos/nuevo_pago', views.nuevo_pago, name='nuevo_pago'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)