from import_export import resources
from .models import Jugador

class datosPersResource (resources.ModelResource):
    class Meta:
        model=Jugador

