from django.contrib import admin
from .models import TipoJor,Jornada,Asistencia,AsistenciasTotal
# Register your models here.

#class asistAdmin (admin.ModelAdmin):
#    readonly_fields=("created",)#esta tupla que crea permite qur se vean todos los camps en el admin

admin.site.register(TipoJor)
admin.site.register(Jornada)
admin.site.register(Asistencia)#,  asistAdmin )
admin.site.register(AsistenciasTotal)