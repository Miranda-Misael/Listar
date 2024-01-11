from django.db import models
from jugadores.models import Jugador, TipoSocio, TipoDivision
from django.contrib.auth.models import User

# Create your models here.

class TipoJor ( models.Model):
    descr =    models.CharField(max_length=15)
    def __str__(self): #no hacefalta en este caso declarar tipo -> str:
        return self.descr #super() #.__str__()


class Jornada ( models.Model):
    titulo =    models.CharField(max_length=200)
    tipoJor=    models.ForeignKey(TipoJor, on_delete=models.PROTECT)
    fechaJor = models.DateTimeField(null=True, blank=True)
    obs=        models.TextField()
    def __str__(self): #no hacefalta en este caso declarar tipo -> str:
        return self.titulo  + ' - ' + self.fechaJor.strftime("%d/%b/%Y")
#...una funcion dentro de la clase es un metodo 
#atrivutos campos
#ForeignKey vincula con otra tabla
#funcion on_delete=models.CASCADE determina que si se elimina un proyecto eliminara todas las tareas relacionadas


class Asistencia(models.Model):
    idJor=models.ForeignKey(Jornada, on_delete=models.CASCADE)
    idJug = models.ForeignKey(Jugador, on_delete=models.DO_NOTHING)
    #fechaDeJor
    # # como relaciono division?
    presente=models.BooleanField(default=False)
    tarde=models.BooleanField(default=False)
    fechaCompletado = models.DateTimeField(null=True, blank=True)
    # datecompleted=models.DateTimeField(null=True)#campo vacio inicial mente
    # campo vacio inicial,pero blank true me habielita a que sea opocional inicialmente para el administrador no pasre la base de datos
    # si creo una tarea pora defecto no todas son importantes
    #important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # metodo string q posibilita en el servidor ver otra descripcion
    def __str__(self):
       return self.idJor.titulo + '- día ' + self.idJor.fechaJor.strftime("%d/%b/%Y")
    
class AsistenciasTotal ( models.Model):
    idJor =    models.ForeignKey(Jornada, on_delete=models.CASCADE)
    tipoSoc=    models.ForeignKey(TipoSocio, on_delete=models.CASCADE)
    tipoDiv=    models.ForeignKey(TipoDivision, on_delete=models.CASCADE,null=True, blank=True)
    totalAsist =  models.IntegerField(default=0)
    
