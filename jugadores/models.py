from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class TipoDivision (models.Model):
    descrp = models.CharField(max_length=3, null=True, blank=True)

# Create your models here. que va heredar los modelos de my site
class TipoSocio (models.Model):
    descrp = models.CharField(max_length=30)
    def __str__(self):  # no hacefalta en este caso declarar tipo -> str:
        return self.descrp  # super() #.__str__()




class Jugador (models.Model):
    apodo = models.CharField(max_length=30)
    idDiv = models.ForeignKey(TipoDivision,null=True, on_delete=models.PROTECT)
    DU = models.IntegerField(null=True)#, unique=True)
    entrena = models.BooleanField(null=True, default=True)
    ImagenCampo = models.CharField(max_length=200,null=True, blank=True)
    tipoSocio = models.ForeignKey(TipoSocio,null=True, on_delete=models.PROTECT)
    Fichaje = models.BooleanField(null=True,default=False) 
    fechaAct = models.DateTimeField(null=True, blank=True)
    email = models.CharField(max_length=100 ,null=True, blank=True)
    nombre = models.CharField(max_length=30,null=True, blank=True)
    apellido = models.CharField(max_length=30 ,null=True, blank=True)
    fechaNaci = models.DateTimeField(null=True, blank=True)
    colegio = models.CharField(max_length=30,null=True, blank=True)
    domicilio = models.CharField(max_length=30,null=True, blank=True)
    barrio = models.CharField(max_length=30, null=True, blank=True)
    imgOS = models.CharField(max_length=200, null=True, blank=True)
    imgDU = models.CharField(max_length=200,null=True, blank=True )
    hnosOtraDiv = models.CharField(max_length=30,null=True, blank=True)
    antecedMed = models.TextField(max_length=200,null=True, blank=True)
    pracOtroDep = models.CharField(max_length=30,null=True, blank=True)
    celJug = models.CharField(max_length=20,null=True, blank=True)
    nombPadre = models.CharField(max_length=30,null=True, blank=True)
    telPadre = models.CharField(max_length=20,null=True, blank=True)
    nombMadre = models.CharField(max_length=30,null=True, blank=True)
    telMadre = models.CharField(max_length=20,null=True, blank=True)
    nombTutor = models.CharField(max_length=30,null=True, blank=True)
    telTutor =models.CharField(max_length=20,null=True, blank=True)
    Puesto = models.IntegerField(default=0,null=True, blank=True)
    PuestAlt = models.IntegerField(default=0,null=True, blank=True)
    puestElejJug = models.IntegerField(default=0,null=True, blank=True)
    dniValidado = models.BooleanField(null=True, default=False)
    def __str__(self):  # no hacefalta en este caso declarar tipo -> str:
        return self.apodo  # super() #.__str__()
        # ...una funcion dentro de la clase es un metodo
        # atrivutos campos


