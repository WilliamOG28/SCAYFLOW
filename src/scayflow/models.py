from decimal import Decimal
from django.db import models
from django.core.validators import RegexValidator

class Cliente(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{10}$', message="El teléfono debe contener exactamente 10 dígitos.")]
    )
    direccion = models.CharField(max_length=255)
    empresa = models.CharField(max_length=255, blank=True, null=True)
    persona_contacto = models.CharField(max_length=255, blank=True, null=True)
    tipo = models.CharField(max_length=100)
    rfc = models.CharField(
        max_length=13,
        validators=[RegexValidator(
            regex=r'^[A-ZÑ&]{4}\d{6}[A-Z0-9]{3}$',
            message="El RFC no tiene el formato correcto"
        )]
    )
    notas = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'clientes'

class Proyecto(models.Model):
    proyecto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    tipo_proyecto = models.CharField(max_length=100)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    estado = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    descripcion = models.TextField()
    sector = models.CharField(max_length=100)
    costo_base = models.DecimalField(max_digits=10, decimal_places=2)
    tarifa_porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    tarifa_monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, editable=False)
    iva_monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, editable=False)
    total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, editable=False)
    nota = models.TextField(blank=True, null=True)
    @property
    def total_pagado(self):
        return sum(p.monto for p in self.pagos.all())

    @property
    def saldo_pendiente(self):
        return (self.total or 0) - self.total_pagado

    @property
    def gasto_total(self):
        return sum(
            t.total_tramite for t in self.tramites.all() 
            if t.es_gasto and t.total_tramite is not None
        ) or 0

    @property
    def utilidad_total(self):
        return self.total - self.gasto_total
    
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'proyectos'

class Tramite(models.Model):
    tramite_id = models.AutoField(primary_key=True)
    proyecto = models.ForeignKey(Proyecto, related_name='tramites', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    costo_base = models.DecimalField(max_digits=10, decimal_places=2)
    tarifa_porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    tarifa_monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, editable=False)
    iva_monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, editable=False)
    total_tramite = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, editable=False)
    duracion_estimada = models.IntegerField()
    tiempo_resolucion = models.IntegerField()
    dependencia = models.CharField(max_length=255)
    responsable_dependencia = models.CharField(max_length=255)
    estatus = models.CharField(max_length=50)
    documentos_requeridos = models.TextField()
    observaciones = models.TextField()
    fecha_ultima_actualizacion = models.DateField(null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    es_gasto = models.BooleanField(null=False, blank=False)    

    @property
    def total_pagado(self):
        return sum(p.monto or Decimal('0.00') for p in self.pagos.all())

    @property
    def saldo_pendiente(self):
        return (self.total_tramite or 0) - self.total_pagado
    
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'tramites'

class Pago(models.Model):
    pago_id = models.AutoField(primary_key=True)
    proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE, null=True, blank=True, related_name='pagos')
    tramite = models.ForeignKey('Tramite', on_delete=models.CASCADE, null=True, blank=True, related_name='pagos')
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha = models.DateField()
    metodo_pago = models.CharField(max_length=100)
    comprobante = models.FileField(upload_to='comprobantes/', blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    def __str__(self):
        if self.proyecto:
            return f"Pago de ${self.monto} a Proyecto {self.proyecto.nombre}"
        elif self.tramite:
            return f"Pago de ${self.monto} a Trámite {self.tramite.nombre}"
        else:
            return f"Pago de ${self.monto}"
    class Meta:
        db_table = 'pagos'