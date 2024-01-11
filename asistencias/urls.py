from django.urls import path
from . import views

urlpatterns = [
    path('', views.helloword),
    path('', views.helloword),
    path('jornadas/', views.jornadas, name='jornadas'),
    path('bloque/', views.jornadasBloque, name='jornadasBloque'),
    path('jornadas_create/', views.jornada_create, name='jornada_create'),
    path('asistencias/', views.asistencias, name='asistencias'),
    path('asistencias_detalle/<int:id>', views.asistencias_detalle, name='asistencias_detalle'),
    path('asistencias_detalle/mod_presente/<int:id>', views.modificar_presente, name='mod_presente'),
    path('asistencias_detalle/mod_presentet/<int:id>', views.modificar_presente_tarde, name='mod_presente_tarde'),
    path('asistencias_detalle/regJugador/<int:id>', views.registrarJugador, name='regJugador'), 
    path('asistencias_detalle/editJugador/<int:idAs>', views.editarJugador, name='editJugador'), 
    path('asistencias_detalle/modJugador/', views.modificarJugador, name='modJugador'), 
    path('bloque/modAsist/<int:id>', views.modificarJornada, name='modJornada'),
    path('bloque/elimAsist/<int:id>', views.eliminarJornada, name='elimJornada'),
    

    
]