# src/scayflow/views.py
import calendar
from datetime import timezone
from itertools import count
import locale
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from scayflow.models import Cliente, Tramite, Proyecto, Pago
import json
from decimal import Decimal, InvalidOperation
from django.core.paginator import Paginator
from django.db.models import Sum, Count, Min, Max
from django.utils.dateformat import format as date_format
from django.db.models import Q
from django.utils import timezone
from django.db.models import Avg


@login_required
def dashboard(request):
    # Lista de los proyectos más recientes (limitado a 5 por ejemplo)
    proyectos = Proyecto.objects.all().order_by('-fecha_inicio')
    total_proyectos = Proyecto.objects.all().order_by('-fecha_inicio').count()

    # Conteos de trámites
    total_tramites = Tramite.objects.count()
    completados = Tramite.objects.filter(estatus__iexact='Completado').count()
    pendientes = Tramite.objects.exclude(estatus__iexact='Completado').count()
    
    activos = Tramite.objects.filter(estatus__iexact='Activo').count()
    tramites_activos = Tramite.objects.exclude(estatus__iexact='Activo').count()

    # Conteo agrupado por estado para gráfica
    estados = Tramite.objects.values('estatus').annotate(total=Count('estatus'))

    # Preparo listas para la gráfica (labels y datos)
    labels = [e['estatus'] for e in estados]
    cantidades = [e['total'] for e in estados]
    
    tramites_list = Tramite.objects.all().order_by('-fecha_inicio')
    
    eventos_calendario = []
    for tramite in tramites_list:
        if tramite.fecha_fin:
            eventos_calendario.append({
                "title": f"{tramite.nombre} ({tramite.proyecto})",
                "start": date_format(tramite.fecha_fin, 'Y-m-d'),
                "allDay": True,
            })

    return render(request, 'dashboard.html', {
        'proyectos': proyectos,
        'total_tramites': total_tramites,
        'completados': completados,
        'pendientes': pendientes,
        'activos' : activos,
        'estados': estados,
        'labels': labels,
        'cantidades': cantidades,
        'total_proyectos' : total_proyectos,
        'eventos_json': json.dumps(eventos_calendario),
        'ingresosTotales': getIngresosTotales(proyectos),
    })

#Vistas para proyectos
@login_required
def proyectos(request):
    proyectos_all = list(Proyecto.objects.all())  
    proyectos = Proyecto.objects.all().order_by('nombre') 
    # estados: lista con {'estatus': 'Activo', 'cantidad': 3}, etc.
    estados_raw_proy = proyectos.values('estado').annotate(cantidad=Count('estado'))

    # Separa los datos para las gráficas
    labels_estatus = [e['estado'] for e in estados_raw_proy]
    cantidades_estatus = [e['cantidad'] for e in estados_raw_proy]
     
    context = {'estadoProyectos': getEstadosProyectos(proyectos_all),
                 'ingresosProyectos': getIngresosProyectos(proyectos_all),
                 'evolucionDeIngresos': {},
                 'proyectosActivos': getProyectosActivos(proyectos_all),
                 'ingresosTotales': getIngresosTotales(proyectos_all),
                 'proyectosTotalesPorcentaje': getProyectosCompletadosPorcentaje(proyectos_all),
                 'totalCobrado': getTotalCobrado(proyectos_all),
                 'labels_estatus' : labels_estatus,
                 'cantidades_estatus' : cantidades_estatus
                }
    return render(request,'proyectos/proyectos.html', context)

def getEstadosProyectos (listaProyectos):    
    proyectosActivosContador = 0
    proyectosInactivosContador = 0
    for proyecto in listaProyectos:
        if proyecto.estado == 'Activo':
            proyectosActivosContador += 1
        if proyecto.estado == 'Inactivo':
            proyectosInactivosContador += 1
    data = {'proyectosActivos': proyectosActivosContador,
                   'proyectosInactivos': proyectosInactivosContador}
    return data

def getIngresosProyectos (listaProyectos):
    data = []
    for proyecto in listaProyectos:
        if proyecto.nombre != None and proyecto.total != None:
            data.append({
                'nombreDelProyecto': proyecto.nombre,
                'total': proyecto.total
            })    
    return data

def getProyectosActivos (listaProyectos):
    proyectosActivosContador = 0
    for proyecto in listaProyectos:
        if proyecto.estado == 'Activo':
            proyectosActivosContador += 1
    return proyectosActivosContador

def getIngresosTotales (listaProyectos):
    ingresosTotales = 0
    for proyecto in listaProyectos:
        if proyecto.total != None:
            ingresosTotales += proyecto.total
    return ingresosTotales

def getTotalCobrado (listaProyectos):
    totalCobrado = 0
    for proyecto in listaProyectos:
        if proyecto.total_pagado == None:
            pass
        else:
            totalCobrado =+ proyecto.total_pagado

def getProyectosCompletadosPorcentaje (listaProyectos):
    proyectosActivosContador = 0
    proyectosTotalesContador = 0
    for proyecto in listaProyectos:
        if proyecto.estado == 'Activo':
            proyectosActivosContador += 1
        proyectosTotalesContador += 1
    if proyectosTotalesContador == 0  or proyectosActivosContador == 0:
        return 0
    porcentaje = (proyectosActivosContador / proyectosTotalesContador)
    return round(porcentaje, 0)

from decimal import Decimal

def safe_decimal(value, default=Decimal('0.00')):
    if value is None or value == '':
        return default
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError):
        return default
    
@login_required
def nuevo_proyecto(request):
    if request.method == 'POST':
        try:
            # Create project with safe decimal conversion
            proyecto = Proyecto.objects.create(
                nombre=request.POST.get('nombre'),
                tipo_proyecto=request.POST.get('tipo_proyecto'),
                cliente_id=request.POST.get('cliente_id'),
                estado=request.POST.get('estado'),
                fecha_inicio=request.POST.get('fecha_inicio'),
                fecha_fin=request.POST.get('fecha_fin') or None,
                descripcion=request.POST.get('descripcion'),
                sector=request.POST.get('sector'),
                costo_base=safe_decimal(request.POST.get('costo_base')),
                tarifa_porcentaje=request.POST.get('tarifa_porcentaje'),
                nota=request.POST.get('nota'),
            )

            # Create procedures
            tramites = json.loads(request.POST.get('tramites_json', '[]'))
            for t in tramites:
                costo_base = safe_decimal(t.get('costo_base'))
                tarifa_porcentaje = safe_decimal(t.get('tarifa_porcentaje'))
                
                # Cálculos
                tarifa_monto = costo_base * (tarifa_porcentaje / Decimal('100'))
                subtotal = costo_base + tarifa_monto
                iva_monto = subtotal * Decimal('0.16')
                total_tramite = subtotal + iva_monto
                
                Tramite.objects.create(
                    proyecto=proyecto,
                    nombre=t.get('nombre', ''),
                    descripcion=t.get('descripcion', ''),
                    costo_base=safe_decimal(t.get('costo_base')),
                    tarifa_porcentaje=safe_decimal(t.get('tarifa_porcentaje')),
                    duracion_estimada=t.get('duracion_estimada', 0),
                    tiempo_resolucion=t.get('tiempo_resolucion', ''),
                    dependencia=t.get('dependencia', ''),
                    responsable_dependencia=t.get('responsable_dependencia', ''),
                    estatus='Activo',
                    documentos_requeridos=t.get('documentos_requeridos', ''),
                    observaciones=t.get('observaciones', ''),
                    fecha_ultima_actualizacion=None,
                    fecha_inicio=t.get('fecha_inicio', None),
                    fecha_fin=t.get('fecha_fin', None),
                    es_gasto=t.get('es_gasto', False),
                    tarifa_monto=tarifa_monto,
                    iva_monto=iva_monto,
                    total_tramite=total_tramite,
                )

            # Calculate totals without refresh_from_db if it's causing issues
            proyecto.total = (
                (proyecto.costo_base or Decimal('0')) + 
                (proyecto.tarifa_monto or Decimal('0')) + 
                (proyecto.iva_monto or Decimal('0'))
            )
            proyecto.save(update_fields=['total'])

            return redirect('lista_proyectos')
            
        except Exception as e:
            # Log the error and return a user-friendly message
            print(f"Error creating project: {str(e)}")
            messages.error(request, "Error creating project. Please check your input values.")
            clientes = Cliente.objects.all()
            return render(request, 'proyectos/nuevo_proyecto.html', {'clientes': clientes})
            
    else:
        clientes = Cliente.objects.all()
        return render(request, 'proyectos/nuevo_proyecto.html', {'clientes': clientes})
    
@login_required
def lista_proyectos(request):
    proyectos_list = Proyecto.objects.all().order_by('-fecha_inicio')

    paginator = Paginator(proyectos_list, 5)
    page_number = request.GET.get('page')
    proyectos = paginator.get_page(page_number)

    return render(request, 'proyectos/lista_proyectos.html', {'proyectos': proyectos})
@login_required
def proyecto_detalles(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    
    tramites = proyecto.tramites.all()
    pagos = proyecto.pagos.all()
    
    context = {
        'proyecto': proyecto,
        'tramites': tramites,
        'pagos': pagos,
    }
    return render(request, 'proyectos/detalles.html', context)
@login_required
def editar_proyecto(request):
    if request.method == 'POST':
        proyecto_id = request.POST.get('proyecto_id')
        proyecto = get_object_or_404(Proyecto, pk=proyecto_id)

        try:
            # Helper function for safe decimal conversion
            def get_decimal(value, default='0.00'):
                try:
                    return Decimal(str(value)) if value else Decimal(default)
                except (InvalidOperation, TypeError):
                    return Decimal(default)

            # Update fields with proper decimal handling
            proyecto.nombre = request.POST.get('nombre')
            proyecto.estado = request.POST.get('estado')
            proyecto.tipo_proyecto = request.POST.get('tipo_proyecto')
            proyecto.fecha_inicio = request.POST.get('fecha_inicio')
            proyecto.fecha_fin = request.POST.get('fecha_fin') or None
            proyecto.descripcion = request.POST.get('descripcion')
            proyecto.sector = request.POST.get('sector')
            proyecto.nota = request.POST.get('nota')
            
            # Decimal fields with proper handling
            proyecto.costo_base = get_decimal(request.POST.get('costo_base'))
            proyecto.tarifa_porcentaje = get_decimal(request.POST.get('tarifa_porcentaje'))

            # Recalculate derived fields
            proyecto.tarifa_monto = (proyecto.costo_base * proyecto.tarifa_porcentaje) / Decimal(100)
            proyecto.iva_monto = (proyecto.costo_base + proyecto.tarifa_monto) * Decimal('0.16')
            proyecto.total = proyecto.costo_base + proyecto.tarifa_monto + proyecto.iva_monto

            proyecto.save()
            return redirect('lista_proyectos')

        except Exception as e:
            # Handle any errors gracefully
            print(f"Error updating project: {str(e)}")
            # You might want to add a message to the user here
            return redirect('editar_proyecto', proyecto_id=proyecto_id)

@login_required
def eliminar_proyecto(request):
    proyecto_id = request.POST.get('proyecto_id')
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    proyecto.delete()
    return redirect('lista_proyectos')
        
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
    buscar = request.GET.get('buscar-cliente')

    if buscar:
        clientes_list = Cliente.objects.filter(
            Q(nombre__icontains=buscar)
        ).order_by('nombre')
    else:
        clientes_list = Cliente.objects.all().order_by('nombre')

    paginator = Paginator(clientes_list, 10)
    page_number = request.GET.get('page')
    clientes = paginator.get_page(page_number)

    return render(request, 'clientes/lista_clientes.html', {
        'clientes': clientes,
        'buscar': buscar,  # Para mantener el valor en el input
    })
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
        cliente.persona_contacto = request.POST.get('persona_contacto', cliente.persona_contacto)
        cliente.direccion = request.POST.get('direccion', cliente.direccion)
        cliente.notas = request.POST.get('notas', cliente.notas)

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

##################################################################################################
#Vistas para tramites
#def tramites(request):
    #return render(request,'tramites/tramites.html')
#def nuevo_tramite(request):
#    return render(request,'tramites/nuevo_tramite.html')
@login_required
def nuevo_tramite(request):
    proyectos = Proyecto.objects.all()

    if request.method == 'POST':
        proyecto_id = request.POST.get('proyecto')
        proyecto = get_object_or_404(Proyecto, pk=proyecto_id)

        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        costo_base = request.POST.get('costo_base')
        tarifa_porcentaje = request.POST.get('tarifa_porcentaje')
        duracion_estimada = request.POST.get('duracion_estimada')
        tiempo_resolucion = request.POST.get('tiempo_resolucion')
        dependencia = request.POST.get('dependencia')
        responsable_dependencia = request.POST.get('responsable_dependencia')
        estatus = request.POST.get('estatus')
        documentos_requeridos = request.POST.get('documentos_requeridos')
        observaciones = request.POST.get('observaciones')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin') or None
        es_gasto = 'es_gasto' in request.POST

        # Convierte los valores numéricos y fechas con seguridad
        try:
            costo_base = Decimal(costo_base)
        except:
            costo_base = Decimal(0)

        try:
            tarifa_porcentaje = Decimal(tarifa_porcentaje)
        except:
            tarifa_porcentaje = Decimal(0)

        try:
            duracion_estimada = int(duracion_estimada)
        except:
            duracion_estimada = 0

        try:
            tiempo_resolucion = int(tiempo_resolucion)
        except:
            tiempo_resolucion = 0

        # Calcula tarifas e IVA
        tarifa_monto = costo_base * tarifa_porcentaje / Decimal(100)
        iva_monto = (costo_base + tarifa_monto) * Decimal('0.16')
        total_tramite = costo_base + tarifa_monto + iva_monto

        tramite = Tramite.objects.create(
            proyecto=proyecto,
            nombre=nombre,
            descripcion=descripcion,
            costo_base=costo_base,
            tarifa_porcentaje=tarifa_porcentaje,
            duracion_estimada=duracion_estimada,
            tiempo_resolucion=tiempo_resolucion,
            dependencia=dependencia,
            responsable_dependencia=responsable_dependencia,
            estatus=estatus,
            documentos_requeridos=documentos_requeridos,
            observaciones=observaciones,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tarifa_monto=tarifa_monto,
            iva_monto=iva_monto,
            total_tramite=total_tramite,
            es_gasto=es_gasto
        )

        return redirect('lista_tramites')

    return render(request, 'tramites/nuevo_tramite.html', {'proyectos': proyectos})
@login_required
def lista_tramites(request):
    clientes = Cliente.objects.all().order_by('nombre')
    proyectos = Proyecto.objects.none()  # inicial vacío

    proyecto_id = request.GET.get('proyecto')
    cliente_id = request.GET.get('cliente') 
    estatus = request.GET.get('estatus')

    # Si se seleccionó un cliente, cargar sus proyectos para mostrar en select
    if cliente_id:
        proyectos = Proyecto.objects.filter(cliente_id=cliente_id).order_by('nombre')
    else:
        proyectos = Proyecto.objects.all().order_by('nombre')

    # Filtrar trámites por proyecto si se seleccionó
    if proyecto_id:
        tramites_list = Tramite.objects.filter(proyecto_id=proyecto_id).order_by('-fecha_inicio')
    elif cliente_id:
        tramites_list = Tramite.objects.filter(proyecto__cliente_id=cliente_id).order_by('-fecha_inicio')
    else:
        tramites_list = Tramite.objects.all().order_by('-fecha_inicio')
        
    if estatus:
        tramites_list = tramites_list.filter(estatus__iexact=estatus)

    paginator = Paginator(tramites_list, 5)
    page_number = request.GET.get('page')
    tramites = paginator.get_page(page_number)

    # KPIs
    total_tramites = tramites_list.count()
    activos = tramites_list.filter(estatus__iexact='Activo').count()
    completados = tramites_list.filter(estatus__iexact='Completado').count()
    monto_total = tramites_list.aggregate(Sum('total_tramite'))['total_tramite__sum'] or 0
    total_pagado = sum((t.total_pagado or Decimal('0.00')) for t in tramites_list)

    porcentaje_completado = round((completados / total_tramites) * 100, 2) if total_tramites else 0

    # estados: lista con {'estatus': 'Activo', 'cantidad': 3}, etc.
    estados_raw = tramites_list.values('estatus').annotate(cantidad=Count('estatus'))

    # Separa los datos para las gráficas
    labels_estatus = [e['estatus'] for e in estados_raw]
    cantidades_estatus = [e['cantidad'] for e in estados_raw]
    
    eventos_calendario = []
    for tramite in tramites_list:
        if tramite.fecha_fin:
            eventos_calendario.append({
                "title": f"{tramite.nombre} ({tramite.proyecto})",
                "start": date_format(tramite.fecha_fin, 'Y-m-d'),
                "allDay": True,
            })

    return render(request, 'tramites/lista_tramites.html', {
        'tramites': tramites,
        'clientes': clientes,
        'proyectos': proyectos,
        'cliente_seleccionado': cliente_id,
        'proyecto_seleccionado': proyecto_id,
        'total_tramites': total_tramites,
        'activos': activos,
        'completados': completados,
        'monto_total': monto_total,
        'total_pagado': total_pagado,
        'porcentaje_completado': porcentaje_completado,
        'estados': estados_raw,
        'labels_estatus': labels_estatus,
        'cantidades_estatus': cantidades_estatus,
        'estatus_seleccionado': estatus,
        'eventos_json': json.dumps(eventos_calendario),
    })

    
@login_required
def proyectos_por_cliente(request):
    cliente_id = request.GET.get('cliente_id')

    if cliente_id:
        proyectos_qs = Proyecto.objects.filter(cliente_id=cliente_id).order_by('nombre')
    else:
        proyectos_qs = Proyecto.objects.all().order_by('nombre')

    proyectos = list(proyectos_qs.values('proyecto_id', 'nombre'))
    return JsonResponse({'proyectos': proyectos})

@login_required
def editar_tramite(request):
    tramite_id = request.POST.get('tramite_id')
    tramite = get_object_or_404(Tramite, pk=tramite_id)

    tramite.nombre = request.POST.get('nombre')
    tramite.descripcion = request.POST.get('descripcion')
    tramite.costo_base = Decimal(request.POST.get('costo_base') or 0)
    tramite.tarifa_porcentaje = Decimal(request.POST.get('tarifa_porcentaje') or 0)
    tramite.tarifa_monto = tramite.costo_base * tramite.tarifa_porcentaje / Decimal(100)
    tramite.iva_monto = (tramite.costo_base + tramite.tarifa_monto) * Decimal('0.16')
    tramite.total_tramite = tramite.costo_base + tramite.tarifa_monto + tramite.iva_monto
    tramite.dependencia = request.POST.get('dependencia')
    tramite.responsable_dependencia = request.POST.get('responsable_dependencia')
    tramite.estatus = request.POST.get('estatus')
    tramite.es_gasto = 'es_gasto' in request.POST

    tramite.save()
    return redirect('lista_tramites')

@login_required
def eliminar_tramite(request):
    tramite_id = request.POST.get('tramite_id')
    tramite = get_object_or_404(Tramite, pk=tramite_id)
    tramite.delete()
    return redirect('lista_tramites')

##################################################################################################

##################################################################################################
#Vistas para pagos
@login_required
def pagos(request):
    
    try:
        locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')  # Linux/macOS
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Alternativa Linux/macOS
        except locale.Error:
            locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Windows

    pagos_list = Pago.objects.all().order_by('-fecha')
    total_pagos = Pago.objects.all().order_by('-fecha').count()
    
    hoy = timezone.now()
    mes_actual = hoy.month
    año_actual = hoy.year
    
    nombre_mes = calendar.month_name[mes_actual] 

    # Pagos solo del mes actual
    pagos_mes = Pago.objects.filter(
        fecha__year=año_actual,
        fecha__month=mes_actual
    ).order_by('-fecha')
    
    pagos_mes_count = pagos_mes.count()
    
    monto_promedio_pago = Pago.objects.aggregate(promedio=Avg('monto'))['promedio'] or 0

    #Pago max y min del mes
    pago_minimo = pagos_mes.aggregate(minimo=Min('monto'))['minimo'] or 0
    pago_maximo = pagos_mes.aggregate(maximo=Max('monto'))['maximo'] or 0
    
    eventos_calendario = []
    for pago in pagos_list:
        if pago.fecha:
            eventos_calendario.append({
                "title": f"{pago.tramite} ({pago.proyecto})",
                "start": date_format(pago.fecha, 'Y-m-d'),
                "allDay": True,
            })

    return render(request, 'pagos/pagos.html', {
        'total_pagos': total_pagos,
        'eventos_json': json.dumps(eventos_calendario),
        'pagos_mes' : pagos_mes_count,
        'nombre_mes' : nombre_mes,
        'monto_promedio_pago' : monto_promedio_pago,
        'pago_minimo' : pago_minimo,
        'pago_maximo' : pago_maximo
    })
@login_required
def lista_pagos(request):
    tramite_id = request.GET.get('tramite')
    tramites = Tramite.objects.select_related('proyecto').all()

    if tramite_id and tramite_id.strip() != "":
        pagos = Pago.objects.filter(tramite_id=tramite_id).order_by('-fecha')
    else:
        pagos = Pago.objects.all().order_by('-fecha')

    paginator = Paginator(pagos, 10)  # 10 pagos por página
    page_number = request.GET.get('page')
    pagos_paginados = paginator.get_page(page_number)

    context = {
        'pagos': pagos_paginados,
        'tramites': tramites,
        'tramite_id': tramite_id  # Para mantener la selección
    }
    return render(request, 'pagos/lista_pagos.html', context)

@login_required
def editar_pago(request):
    pago_id = request.POST.get('pago_id')
    pago = get_object_or_404(Pago, pk=pago_id)

    pago.monto = request.POST.get('monto')
    pago.fecha = request.POST.get('fecha')
    pago.metodo_pago = request.POST.get('metodo_pago')
    pago.notas = request.POST.get('notas')

    if 'comprobante' in request.FILES:
        pago.comprobante = request.FILES['comprobante']

    pago.save()
    return redirect('lista_pagos')
@login_required
def eliminar_pago(request):
    pago_id = request.POST.get('pago_id')
    pago = get_object_or_404(Pago, pk=pago_id)
    pago.delete()
    return redirect('lista_pagos')
@login_required
def nuevo_pago(request):
    proyectos = Proyecto.objects.all()
    proyecto_id = request.GET.get('proyecto_id') or request.POST.get('proyecto_id')
    proyecto = Proyecto.objects.filter(pk=proyecto_id).first() if proyecto_id else None
    tramites = proyecto.tramites.all() if proyecto else []

    error_msg = None

    if request.method == 'POST' and proyecto:
        monto = Decimal(request.POST.get('monto'))
        fecha = request.POST.get('fecha')
        metodo_pago = request.POST.get('metodo_pago')
        comprobante = request.FILES.get('comprobante') or request.POST.get('comprobante')
        nota = request.POST.get('nota')
        pago_tipo = request.POST.get('pago_tipo')
        tramite_id = request.POST.get('tramite_id')
        tramite = Tramite.objects.get(pk=tramite_id) if (pago_tipo == 'tramite' and tramite_id) else None

        # Validación: que no pague más de lo pendiente
        if pago_tipo == 'proyecto':
            pendiente = proyecto.saldo_pendiente
            if monto > pendiente:
                error_msg = f"No puedes abonar más de lo pendiente (${pendiente:.2f}) en el proyecto."
        elif pago_tipo == 'tramite' and tramite:
            pendiente = tramite.saldo_pendiente
            if monto > pendiente:
                error_msg = f"No puedes abonar más de lo pendiente (${pendiente:.2f}) en el trámite seleccionado."

        # Responde error si es AJAX
        if error_msg and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': error_msg})

        if not error_msg:
            Pago.objects.create(
                proyecto=proyecto if pago_tipo == 'proyecto' else None,
                tramite=tramite,
                monto=monto,
                fecha=fecha,
                metodo_pago=metodo_pago,
                comprobante=comprobante,
                notas=nota
            )

            # Refresca y recalcula los datos necesarios
            proyecto.refresh_from_db()
            tramites = proyecto.tramites.all()
            total_pagado = proyecto.total_pagado
            saldo = proyecto.saldo_pendiente
            porcentaje_pagado = porcentaje_pendiente = 0
            iva = getattr(proyecto, 'iva', 0) if proyecto else 0
            if proyecto.total:
                porcentaje_pagado = round(Decimal(proyecto.total_pagado) / Decimal(proyecto.total) * 100, 1) if proyecto.total > 0 else 0
                porcentaje_pendiente = round(Decimal(proyecto.saldo_pendiente) / Decimal(proyecto.total) * 100, 1) if proyecto.total > 0 else 0

            total_tramites = sum([t.total_tramite for t in tramites]) if tramites else 0
            total_pagado_tramites = sum([t.total_pagado for t in tramites]) if tramites else 0
            total_pendiente_tramites = sum([t.saldo_pendiente for t in tramites]) if tramites else 0
            n_tramites = len(tramites)
            porc_pagado = round((Decimal(total_pagado_tramites) / Decimal(total_tramites) * 100), 1) if total_tramites else 0
            porc_pendiente = round((Decimal(total_pendiente_tramites) / Decimal(total_tramites) * 100), 1) if total_tramites else 0

            # Si es AJAX, renderiza sólo el bloque parcial y responde
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('pagos/proyecto_info.html', {
                    'proyecto': proyecto,
                    'tramites': tramites,
                    'total_pagado': total_pagado,
                    'saldo': saldo,
                    'iva': iva,
                    'porcentaje_pagado': porcentaje_pagado,
                    'porcentaje_pendiente': porcentaje_pendiente,
                    'total_tramites': total_tramites,
                    'total_pagado_tramites': total_pagado_tramites,
                    'total_pendiente_tramites': total_pendiente_tramites,
                    'n_tramites': n_tramites,
                    'porc_pagado': porc_pagado,
                    'porc_pendiente': porc_pendiente,
                }, request=request)
                return JsonResponse({'success': True, 'html': html})

            # Si no es AJAX, redirige normal
            return redirect('nuevo_pago')

    total_pagado = proyecto.total_pagado if proyecto else 0
    saldo = proyecto.saldo_pendiente if proyecto else 0

    # ==== RESUMEN PROYECTO ====
    porcentaje_pagado = porcentaje_pendiente = 0
    iva = getattr(proyecto, 'iva', 0) if proyecto else 0
    if proyecto and proyecto.total:
        porcentaje_pagado = round(Decimal(proyecto.total_pagado) / Decimal(proyecto.total) * 100, 1) if proyecto.total > 0 else 0
        porcentaje_pendiente = round(Decimal(proyecto.saldo_pendiente) / Decimal(proyecto.total) * 100, 1) if proyecto.total > 0 else 0

    # ==== RESUMEN TRÁMITES ====
    total_tramites = sum(
        float(t.total_tramite) 
        for t in tramites or [] 
        if hasattr(t, 'total_tramite') and t.total_tramite is not None
    )    
    total_pagado_tramites = sum([t.total_pagado for t in tramites]) if tramites else 0
    total_pendiente_tramites = sum([t.saldo_pendiente for t in tramites]) if tramites else 0
    n_tramites = len(tramites)
    porc_pagado = round((Decimal(total_pagado_tramites) / Decimal(total_tramites) * 100), 1) if total_tramites else 0
    porc_pendiente = round((Decimal(total_pendiente_tramites) / Decimal(total_tramites) * 100), 1) if total_tramites else 0

    return render(request, 'pagos/nuevo_pago.html', {
        'proyectos': proyectos,
        'proyecto': proyecto,
        'tramites': tramites,
        'total_pagado': total_pagado,
        'saldo': saldo,
        'error_msg': error_msg,
        'iva': iva,
        # Para sección de proyecto
        'porcentaje_pagado': porcentaje_pagado,
        'porcentaje_pendiente': porcentaje_pendiente,
        # Para sección de trámites
        'total_tramites': total_tramites,
        'total_pagado_tramites': total_pagado_tramites,
        'total_pendiente_tramites': total_pendiente_tramites,
        'n_tramites': n_tramites,
        'porc_pagado': porc_pagado,
        'porc_pendiente': porc_pendiente,
    })