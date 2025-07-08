# src/scayflow/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Cliente, Tramite, Proyecto
import json
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

#Vistas para proyectos
@login_required
def proyectos(request):
    return render(request,'proyectos/proyectos.html')

@login_required
def nuevo_proyecto(request):
    if request.method == 'POST':
        # Recoge campos del proyecto
        fecha_fin_proyecto = request.POST.get('fecha_fin')
        if not fecha_fin_proyecto:
            fecha_fin_proyecto = None

        proyecto = Proyecto.objects.create(
            nombre=request.POST.get('nombre'),
            tipo_proyecto=request.POST.get('tipo_proyecto'),
            cliente_id=request.POST.get('cliente_id'),
            estado='1',
            fecha_inicio=request.POST.get('fecha_inicio'),
            fecha_fin=request.POST.get('fecha_fin') or None,
            descripcion=request.POST.get('descripcion'),
            sector=request.POST.get('sector'),
            costo_base=request.POST.get('costo_base'),
            tarifa_porcentaje=request.POST.get('tarifa_porcentaje'),
            nota=request.POST.get('nota')
        )
        # Tramites
        tramites = json.loads(request.POST.get('tramites_json', '[]'))
        for t in tramites:
            fecha_fin_tramite = t.get('fecha_fin', None)
            if not fecha_fin_tramite:
                fecha_fin_tramite = None
            Tramite.objects.create(
                proyecto=proyecto,
                nombre=t['nombre'],
                descripcion=t['descripcion'],
                costo_base=t['costo_base'],
                tarifa_porcentaje=t['tarifa_porcentaje'],
                duracion_estimada=t['duracion_estimada'],
                tiempo_resolucion=t.get('tiempo_resolucion', ''),
                dependencia=t.get('dependencia', ''),
                responsable_dependencia=t.get('responsable_dependencia', ''),
                estatus=t.get('estatus', ''),
                documentos_requeridos=t.get('documentos_requeridos', ''),
                observaciones=t.get('observaciones', ''),
                fecha_ultima_actualizacion=None,  # Siempre null
                fecha_inicio=t.get('fecha_inicio', None),
                fecha_fin=fecha_fin_tramite,      # Puede ser null
            )
        return redirect('lista_proyectos')
    else:
        clientes = Cliente.objects.all()
        return render(request, 'proyectos/nuevo_proyecto.html', {'clientes': clientes})
@login_required
def lista_proyectos(request):
    return render(request,'proyectos/lista_proyectos.html')
@login_required
def detalles(request):
    return render(request,'proyectos/nuevo_proyecto.html')


#Vistas para clientes
@login_required
def clientes(request):
    return render(request,'clientes/clientes.html')
@login_required
def nuevo_cliente(request):
    if request.method == 'POST':
        Cliente.objects.create(
            nombre=request.POST.get('nombre', ''),
            email=request.POST.get('email', ''),
            telefono=request.POST.get('telefono', ''),
            direccion=request.POST.get('direccion', ''),
            empresa=request.POST.get('empresa', ''),
            persona_contacto=request.POST.get('persona_contacto', ''),
            tipo=request.POST.get('tipo', ''),
            rfc=request.POST.get('rfc', ''),
            notas=request.POST.get('notas', ''),
        )
        return redirect('lista_clientes')  # Ajusta al nombre correcto en tu urls.py
    return render(request, 'clientes/nuevo_cliente.html')
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})
@login_required
def editar_cliente(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        cliente = get_object_or_404(Cliente, cliente_id=cliente_id)

        # Actualiza los campos
        cliente.nombre = request.POST.get('nombre', cliente.nombre)
        cliente.email = request.POST.get('email', cliente.email)
        cliente.telefono = request.POST.get('telefono', cliente.telefono)
        cliente.empresa = request.POST.get('empresa', cliente.empresa)
        cliente.tipo = request.POST.get('tipo', cliente.tipo)
        cliente.rfc = request.POST.get('rfc', cliente.rfc)
        # Si tienes más campos, agrégalos aquí

        try:
            cliente.save()
            messages.success(request, "Cliente actualizado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al actualizar: {e}")

        # Redirecciona de vuelta a la lista de clientes
        return redirect('lista_clientes')
    else:
        messages.error(request, "Acceso no permitido.")
        return redirect('lista_clientes')

#Vistas para tramites
#def tramites(request):
    #return render(request,'tramites/tramites.html')
@login_required
def nuevo_tramite(request):
    return render(request,'tramites/nuevo_tramite.html')
@login_required
def lista_tramites(request):
    return render(request,'tramites/lista_tramites.html')