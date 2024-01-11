from django.shortcuts import render
from .resources import datosPersResource
from tablib import Dataset
from .models import Jugador,TipoDivision, TipoSocio
import openpyxl
from django.http.response import JsonResponse
from django.utils.text import Truncator

# Create your views here.

def importExcel(request):
    if request.method == 'POST':
        jugador_resource = datosPersResource()
        dataset = Dataset()
        newJugadores = request.FILES["my_file"]
        # imported_data=dataset.load(newJugadores.read(), format='xlsx'  )

        workbook = openpyxl.load_workbook(newJugadores, data_only=True)
        sheet = workbook.active

        for data in sheet.iter_rows(min_row=2, values_only=True):
            du_value = data[2]  # DU es la tercera columna (índice 2)

            if du_value is not None:#  Compruebo si el valor DU no está 
                jugador, created = Jugador.objects.get_or_create(DU=du_value, defaults={
                    'apodo': data[0],
                    'idDiv':  TipoDivision.objects.get(id=data[1]),  # Asigna una instancia válida de TipoDivision
                    'DU': data[2],
                    'entrena': True,  # data[3],
                    'ImagenCampo': data[4],
                    'tipoSocio': TipoSocio.objects.get(id=data[5]), # Asigna una instancia válida de TipoSocio
                    'Fichaje': data[6],
                    'fechaAct': data[7],
                    'email': data[8],
                    'nombre': data[9],
                    'apellido': data[10],
                    'fechaNaci': data[11],
                    'colegio': Truncator(data[12]).chars(30),
#                     data['nombre'] = Truncator(data['nombre']).chars(30)
                    'domicilio':Truncator(data[13]).chars(30),
                    'barrio': data[14],
                    'imgOS': data[15],
                    'imgDU': data[16],
                    'hnosOtraDiv': data[17],
                    'antecedMed': data[18],
                    'pracOtroDep': data[19],
                    'celJug': data[20],
                    'nombPadre': Truncator(data[21]).chars(30),
                    'telPadre': data[22],
                    'nombMadre': Truncator(data[23]).chars(30),
                    'telMadre': data[24],
                    'nombTutor': data[25],
                    'telTutor': data[26],
                })
                if not created:
                    # Actualizar campos si el jugador ya existía
                    jugador.apodo= data[0]
                    jugador.idDiv = TipoDivision.objects.get(id=data[1])  # Asigna una instancia válida de TipoDivision
                    jugador.entrena= True
                    jugador.ImagenCampo= data[4]
                    jugador.tipoSocio = TipoSocio.objects.get(id=data[5]) # Asigna una instancia válida de TipoSocio
                    jugador.Fichaje= data[6]
                    jugador.fechaAct= data[7]
                    jugador.email= data[8]
                    jugador.nombre= data[9]
                    jugador.apellido= data[10]
                    jugador.fechaNaci= data[11]
                    jugador.colegio= Truncator(data[12]).chars(30)
                    jugador.domicilio= Truncator(data[13]).chars(30)
                    jugador.barrio= data[14]
                    jugador.imgOS= data[15]
                    jugador.imgDU= data[16]
                    jugador.hnosOtraDiv= data[17]
                    jugador.antecedMed= data[18]
                    jugador.pracOtroDep= data[19]
                    jugador.celJug= data[20]
                    jugador.nombPadre= Truncator(data[21]).chars(30)
                    jugador.telPadre= data[22]
                    jugador.nombMadre= Truncator(data[23]).chars(30)
                    jugador.telMadre= data[24]
                    jugador.nombTutor= data[25]
                    jugador.telTutor= data[26]
                    jugador.save()    
                    #value = Jugador(**jugador)
                    #value.save()

    return render(request, 'ImportJugadores.html')

def datosPersonales(request):
    titulo=" - Datos Personales"
    return render(request,"datosPersonales.html",{'titulo': titulo})

def datosPersTable(_request):
    jugadores = list(Jugador.objects.values())
    data = {'jugadores': jugadores}
    return JsonResponse(data)

def eliminarJugador_Anterior_no_estaria_en_uso (request, id):
    jugador = Jugador.objects.get(id=id)
    jugador.delete()
    # js messages.success(request, '¡Curso eliminado!')
    titulo=" - Datos Personales"
    return render(request,"datosPersonales.html",{'titulo': titulo})

def eliminarJugador(request, id):
    try:
        jugador = Jugador.objects.get(id=id)
        jugador.delete()
        return JsonResponse({'success': True})
    except Jugador.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Jugador no encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})