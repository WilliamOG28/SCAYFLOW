from django.shortcuts import render
from django.http import HttpResponse

def base(request):
    return render(request, 'base.html')

#Vistas para proyectos
def proyectos(request):
    return render(request,'proyectos/proyectos.html')
def nuevo(request):
    return render(request,'proyectos/nuevo_proyecto.html')
def gestionar(request):
    return render(request,'proyectos/gestion_proyecto.html')
def detalles(request):
    return render(request,'proyectos/nuevo_proyecto.html')
# Create your views here.
