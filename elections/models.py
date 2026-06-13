from django.db import models

class Campana(models.Model):
    nombre_campana = models.CharField(max_length=200)
    fecha_inicio = models.DateTimeField()
    fecha_cierre = models.DateTimeField()
    esta_activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_campana

class Plancha(models.Model):
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE, related_name='planchas')
    nombre = models.CharField(max_length=200)
    candidato_principal = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='planchas_logos/', null=True, blank=True)
    propuesta = models.TextField()
    votos_recibidos = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.candidato_principal})"

class Votante(models.Model):
    token_sesion = models.CharField(max_length=255)
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE, related_name='votantes')
    ya_voto = models.BooleanField(default=False)
    fecha_voto = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('token_sesion', 'campana')

    def __str__(self):
        return self.token_sesion

class AuditoriaVoto(models.Model):
    comprobante = models.CharField(max_length=255, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE, related_name='auditorias')

    def __str__(self):
        return self.comprobante

class SystemLog(models.Model):
    ACCION_CHOICES = [
        ('LOGIN', 'Inicio de sesión Admin'),
        ('LOGOUT', 'Cierre de sesión Admin'),
        ('CAMPANA_CREADA', 'Campaña Creada'),
        ('CAMPANA_EDITADA', 'Campaña Editada'),
        ('VOTO_EMITIDO', 'Voto Emitido'),
    ]
    accion = models.CharField(max_length=50, choices=ACCION_CHOICES)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.fecha.strftime('%Y-%m-%d %H:%M:%S')} - {self.accion}"
