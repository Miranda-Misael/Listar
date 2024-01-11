from django import forms
from .models import TipoJor
from datetime import date

class CreateNewJornada(forms.Form):
    fechaJor =  forms.DateField(label ="Elejir Fecha", 
                                widget=forms.DateInput(attrs={'type': 'date'}), initial= date.today()  )
    # Establecer la fecha actual como valor inicial
    tipoJor =   forms.ModelChoiceField(label ="Tipo de Jornada",
                                       queryset = TipoJor.objects.all())
    titulo =    forms.CharField(#label="Lugar - Nombre de Jornada", 
                                max_length=200, initial="Lugar - Nombre de Jornada",
                                widget = forms.TextInput(attrs={'class':'input'})) 
    obs =       forms.CharField(label='Observación', 
                                widget=forms.Textarea(attrs={'class':'input'})) 

    