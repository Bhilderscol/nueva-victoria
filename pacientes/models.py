from django.db import models
from django.urls import reverse

def foto_upload_to(instance, filename):
    # guardar por expediente
    return f"pacientes/{instance.expediente or 'pendiente'}/{filename}"

class Paciente(models.Model):
    expediente = models.CharField(max_length=20, unique=True, blank=True)
    nombre_completo = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    tipo_adiccion = models.CharField(max_length=100, blank=True)

    responsable_nombre = models.CharField(max_length=200, blank=True)
    responsable_telefono = models.CharField(max_length=30, blank=True)
    responsable_direccion = models.CharField(max_length=255, blank=True)

    fecha_ingreso = models.DateField(null=True, blank=True)
    fecha_egreso_probable = models.DateField(null=True, blank=True)

    costo_semana = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_laboratorios = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_traslado = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    foto_perfil = models.ImageField(upload_to=foto_upload_to, null=True, blank=True)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        return f"{self.expediente or 'NV-?'} - {self.nombre_completo}"

    def get_absolute_url(self):
        return reverse("pacientes_detalle", args=[self.pk])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.expediente and self.pk:
            self.expediente = f"NV-{self.pk:06d}"
            type(self).objects.filter(pk=self.pk).update(expediente=self.expediente)