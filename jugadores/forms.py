#from attr import fields
from django import forms
from .models import Jugador#, Members, document, Ajax, Csvupload
#from django.utils.translation import gettext_lazy as _
#from ckeditor.widgets import CKEditorWidget

class datosPersForm(forms.Form):
    class Meta:
        Model   = Jugador
        fields  = '__all__'

        