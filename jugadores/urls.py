from django.urls import path
from . import views


urlpatterns = [
path('importExcel/', views.importExcel, name='importExcel'),
path('datosPersonales/', views.datosPersonales, name='datosPersonales'),#apunta al html 
path('datosPersTable/', views.datosPersTable, name='datosPersTable'),#apunta a la lista que se generara de datos personales en un datatable
path('eliminarJugador/<int:id>', views.eliminarJugador, name='eliminarJugador'),
]

