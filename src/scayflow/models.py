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
        db_table = 'clientes'  # <--- Aquí le dices a Django que use esa tabla

class Proyecto(models.Model):
    proyecto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    tipo_proyecto = models.CharField(max_length=100)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)  # FK
    estado = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.TextField()
    sector = models.CharField(max_length=100)
    costo_base = models.DecimalField(max_digits=10, decimal_places=2)
    tarifa_porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    tarifa_monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        editable=False,   # <- esto es clave
    )
    total = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True, editable=False
    )
    nota = models.TextField(blank=True, null=True)

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
    total_tramite = models.DecimalField(max_digits=12, decimal_places=2)
    duracion_estimada = models.CharField(max_length=50)
    tiempo_resolucion = models.CharField(max_length=50)
    dependencia = models.CharField(max_length=255)
    responsable_dependecnia = models.CharField(max_length=255)
    estatus = models.CharField(max_length=50)
    documentos_requeridos = models.TextField()
    observaciones = models.TextField()
    fecha_ultima_actualizacion = models.DateField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'tramites'