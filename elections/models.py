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
    token_sesion = models.CharField(max_length=255, unique=True)
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE, related_name='votantes')
    ya_voto = models.BooleanField(default=False)
    fecha_voto = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.token_sesion

class AuditoriaVoto(models.Model):
    comprobante = models.CharField(max_length=255, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE, related_name='auditorias')

    def __str__(self):
        return self.comprobante
