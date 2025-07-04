from django.shortcuts import render
from django.http import HttpResponse

def base(request):
    return render(request, 'base.html')


#Vistas para proyectos
def proyectos(request):
    return render(request,'proyectos/proyectos.html')
def nuevo_proyecto(request):
    return render(request,'proyectos/nuevo_proyecto.html')
def lista_proyectos(request):
    return render(request,'proyectos/lista_proyectos.html')
def detalles(request):
    return render(request,'proyectos/nuevo_proyecto.html')


#Vistas para clientes
def clientes(request):
    return render(request,'clientes/clientes.html')
def nuevo_cliente(request):
    return render(request,'clientes/nuevo_cliente.html')
def lista_clientes(request):
    return render(request,'clientes/lista_clientes.html')

#Vistas para tramites
#def tramites(request):
    #return render(request,'tramites/tramites.html')
def nuevo_tramite(request):
    return render(request,'tramites/nuevo_tramite.html')
def lista_tramites(request):
    return render(request,'tramites/lista_tramites.html')