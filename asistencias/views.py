from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import TipoJor, Jornada, Asistencia, AsistenciasTotal
from .forms import CreateNewJornada
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone
from jugadores.models import Jugador,TipoSocio, TipoDivision
from django.urls import reverse
from django.db.models import Count,Q #para jornadas asistentes
from django.db.models import Count, Case, When, Value, BooleanField,Sum
from collections import defaultdict

# Create your views here.


def helloword(request):
    return HttpResponse('Hello World Asistencias')


def tipoJors(request):
    tipoJors = TipoJor.objects.all()
    return render(request, 'as/tipoJors.html', {'tipoJors': tipoJors})

def jornadas(request):
    titulo = "Asistencias"
    club = "La canchita"
    jornadas = Jornada.objects.all().order_by('-id')
    asistencias_totals = []
    # Obtener todos los tipos de divisiones disponibles
    tipos_division = TipoDivision.objects.all()
    for jornada in jornadas:
        totals = defaultdict(int)
        # Obtener todos los jugadores para esta jornada
        jugadores = Jugador.objects.filter(tipoSocio__in=[1, 2, 3, 4])
        # Calcular los totales para cada tipoSocio y tipoDivision
        for jugador in jugadores:
            tipoSocio_id = jugador.tipoSocio.id
            tipoDiv_id = jugador.idDiv.id
            numAsistencias = Asistencia.objects.filter(idJor=jornada, presente=True, idJug=jugador).count()
            totals[(tipoSocio_id, tipoDiv_id)] += numAsistencias
        for tipoSocio_id in [1, 2, 3, 4]:
            for tipoDiv in tipos_division:
                tipoDiv_id = tipoDiv.id
                total = totals[(tipoSocio_id, tipoDiv_id)]
                AsistT, created = AsistenciasTotal.objects.get_or_create(
                    idJor=jornada,
                    tipoSoc=TipoSocio.objects.get(id=tipoSocio_id),
                    tipoDiv=tipoDiv
                )
                AsistT.totalAsist = total
                AsistT.save()
    asistencias_totals = AsistenciasTotal.objects.filter(tipoDiv=7).order_by('-idJor','tipoSoc')#filtra 8 por que me muestra la m12 y no la del mgr
    # totalizador por jornada
    return render(request, 'jornadas.html', {'asistencias_totals': asistencias_totals, 'jornadas': jornadas, 'titulo': titulo, 'club': club })

def jornadasBloque(request):
    titulo = "Asistencias"
    club = "La canchita"
    #Diccionarios que totalizan socios por jornadas
    totalJug = defaultdict(int)
    totalPfe = defaultdict(int)
    totalMgr = defaultdict(int)
    totalPF = defaultdict(int)

    jornadas = Jornada.objects.all().order_by('-id')
    asistencias_totals = []
    # Obtener todos los tipos de divisiones disponibles
    tipos_division = TipoDivision.objects.all()
    for jornada in jornadas:
        totals = defaultdict(int)
        # Obtener todos los jugadores para esta jornada
        jugadores = Jugador.objects.filter(tipoSocio__in=[1, 2, 3, 4])
        # Calcular los totales para cada tipoSocio y tipoDivision
        for jugador in jugadores:
            tipoSocio_id = jugador.tipoSocio.id
            tipoDiv_id = jugador.idDiv.id
            numAsistencias = Asistencia.objects.filter(idJor=jornada, presente=True, idJug=jugador).count()
            totals[(tipoSocio_id, tipoDiv_id)] += numAsistencias
        #en estas sentencias de codigo totalizo en diccionarios a cada socio con un id que es la jornada
        numAsistSoc = AsistenciasTotal.objects.filter(idJor=jornada, tipoSoc=1).aggregate(Sum('totalAsist'))
        totalJug[(jornada.id)] =numAsistSoc["totalAsist__sum"]
        totalJug_dict = dict(totalJug)
        numAsistSoc = AsistenciasTotal.objects.filter(idJor=jornada, tipoSoc=2).aggregate(Sum('totalAsist'))
        totalPfe[(jornada.id)] =numAsistSoc["totalAsist__sum"]
        totalPfe_dict = dict(totalPfe)
        numAsistSoc = AsistenciasTotal.objects.filter(idJor=jornada, tipoSoc=3).aggregate(Sum('totalAsist'))
        totalMgr[(jornada.id)] =numAsistSoc["totalAsist__sum"]
        totalMgr_dict = dict(totalMgr)
        numAsistSoc = AsistenciasTotal.objects.filter(idJor=jornada, tipoSoc=4).aggregate(Sum('totalAsist'))
        totalPF[(jornada.id)] =numAsistSoc["totalAsist__sum"]
        totalPF_dict = dict(totalPF)
        # Actualizar o crear registros en AsistenciasTotal
        for tipoDiv in tipos_division:
            tipoDiv_id = tipoDiv.id
            for tipoSocio_id in [1, 2, 3, 4]:
                total = totals[(tipoSocio_id, tipoDiv_id)]
                AsistT, created = AsistenciasTotal.objects.get_or_create(
                    idJor=jornada,
                    tipoSoc=TipoSocio.objects.get(id=tipoSocio_id),
                    tipoDiv=tipoDiv
                )
                AsistT.totalAsist = total
                AsistT.save()
                asistencias_totals = AsistenciasTotal.objects.filter(tipoDiv__in=range(1, 10)).order_by('-idJor', 'tipoDiv', 'tipoSoc')
    return render(request, 'jornadasBloque.html', {'asistencias_totals': asistencias_totals, 'jornadas': jornadas, 'totalJug': totalJug_dict ,'totalPfe': totalPfe_dict ,'totalMgr': totalMgr_dict ,'totalPF': totalPF_dict , 'titulo': titulo, 'club': club})

def jornada_create(request):
    titulo="Asistencias"
    club="La canchita"
    totalJug = defaultdict(int)
    totalPfe = defaultdict(int)
    totalMgr = defaultdict(int)
    totalPF = defaultdict(int)
        
    if request.method == 'GET':
        return render(request, 'jornadas_create.html', {'form': CreateNewJornada ,'titulo': titulo ,'club':club})
    else:
        form = CreateNewJornada(request.POST)
        if form.is_valid():
            titulo              = form.cleaned_data['titulo']
            tipo_jor_instance   = form.cleaned_data['tipoJor']
            fecha_jor           = form.cleaned_data['fechaJor']
            obs                 = form.cleaned_data['obs']
            nueva_jornada       = Jornada(titulo=titulo, tipoJor=tipo_jor_instance, fechaJor=fecha_jor, obs=obs)
            nueva_jornada.save()
        jugadores = Jugador.objects.all()
        for jugador in jugadores:
            nueva_asistencia = Asistencia(idJor=nueva_jornada, idJug=jugador, user=request.user)
            nueva_asistencia.save()    

        tipoSocios = TipoSocio.objects.all()
        for tipoSoc in tipoSocios:
            nueva_asistT = AsistenciasTotal(idJor=nueva_jornada, tipoSoc=tipoSoc)
            nueva_asistT.save()    
        
        asistencias_totals = AsistenciasTotal.objects.filter(tipoDiv__in=range(1, 10)).order_by('-idJor', 'tipoDiv', 'tipoSoc')
#        se podria hacer una functionque devuelva este diccionario
        jornadas = Jornada.objects.all().order_by('-id')
        for jornada in jornadas:    
            numAsistSoc = AsistenciasTotal.objects.filter(idJor=jornada, tipoSoc=1).aggregate(Sum('totalAsist'))
            totalJug[(jornada.id)] =numAsistSoc["totalAsist__sum"]
            totalJug_dict = dict(totalJug)
            numAsistSoc = AsistenciasTotal.objects.filter(idJor=jornada, tipoSoc=2).aggregate(Sum('totalAsist'))
            totalPfe[(jornada.id)] =numAsistSoc["totalAsist__sum"]
            totalPfe_dict = dict(totalPfe)
            numAsistSoc = AsistenciasTotal.objects.filter(idJor=jornada, tipoSoc=3).aggregate(Sum('totalAsist'))
            totalMgr[(jornada.id)] =numAsistSoc["totalAsist__sum"]
            totalMgr_dict = dict(totalMgr)
            numAsistSoc = AsistenciasTotal.objects.filter(idJor=jornada, tipoSoc=4).aggregate(Sum('totalAsist'))
            totalPF[(jornada.id)] =numAsistSoc["totalAsist__sum"]
            totalPF_dict = dict(totalPF)
        return render(request, 'jornadasBloque.html', {'asistencias_totals': asistencias_totals, 'jornadas': jornadas, 'totalJug': totalJug_dict ,'totalPfe': totalPfe_dict ,'totalMgr': totalMgr_dict ,'totalPF': totalPF_dict , 'titulo': titulo, 'club': club})

def asistencias(request):
    asistencias = Asistencia.objects.all()
    return render(request, 'asistencias.html', {'asistencias': asistencias})

def asistencias_detalle(request, id): # recibo id jornada
    titulo="Tomar Asistencia"
    club="La canchita"
    asistencias_presentes = Asistencia.objects.filter(idJor=id, presente=True, idJug__tipoSocio__id=1 ).count()#envio el totalde presentes
    jornada= get_object_or_404(Jornada,id=id) #de esta manera si solicito una jornada inexistente me devuelve la pagina404
    #asistencias=Asistencia.objects.all()    #2  --- aca me tre todas las tareas 
    #asistencias=Asistencia.objects.filter(idJor=id).order_by('idJug__apodo')
    tipos_socio = TipoSocio.objects.all()# para cargar combo socio
    # ... rest of your view logic
    asistencias = Asistencia.objects.filter(idJor=id, idJug__idDiv__id=7).order_by('idJug__tipoSocio__descrp', 'idJug__apodo')#pero necesito solo las relacionadas a este project
    return render (request, 'asistencias_detalle.html', {'jornada':jornada, 'asistencias':asistencias,'titulo': titulo ,'club':club,'asistencias_presentes': asistencias_presentes,'tipos_socio': tipos_socio})

def modificar_presente(request, id):# recibo id asistencia
    asistencia = Asistencia.objects.get(id=id)
    # Cambiar el valor de 'presente' al contrario
    asistencia.presente = not asistencia.presente
    asistencia.save()
    jornada = Jornada.objects.get(id=asistencia.idJor.id)
    #asistencias=Asistencia.objects.filter(idJor=asistencia.idJor.id)
    asistencias=Asistencia.objects.filter(idJor=asistencia.idJor.id, idJug__idDiv__id=7).order_by('idJug__tipoSocio__descrp', 'idJug__apodo')#pero necesito solo las relacionadas a este project
    asistencias_presentes = Asistencia.objects.filter(idJor=asistencia.idJor.id, presente=True, idJug__tipoSocio__id=1 ).count() #envio el totalde presentes
    return render (request, 'asistencias_detalle.html', {'jornada':jornada, 'asistencias':asistencias,'asistencias_presentes': asistencias_presentes})

def modificar_presente_tarde(request, id):# recibo id asistencia
    asistencia = Asistencia.objects.get(id=id)
    # Cambiar el valor de 'presente' al contrario
    asistencia.presente = not asistencia.presente
    asistencia.tarde = not asistencia.tarde
    asistencia.save()
    jornada = Jornada.objects.get(id=asistencia.idJor.id)
    #asistencias=Asistencia.objects.filter(idJor=asistencia.idJor.id)
    asistencias=Asistencia.objects.filter(idJor=asistencia.idJor.id, idJug__idDiv__id=7).order_by('idJug__tipoSocio__descrp', 'idJug__apodo')#pero necesito solo las relacionadas a este project
    asistencias_presentes = Asistencia.objects.filter(idJor=asistencia.idJor.id, presente=True, idJug__tipoSocio__id=1 ).count() #envio el totalde presentes
    return render (request, 'asistencias_detalle.html', {'jornada':jornada, 'asistencias':asistencias,'asistencias_presentes': asistencias_presentes})

def registrarJugador(request, id): #envio id jornada
    apodo = request.POST['txtApodo']
    idDiv = TipoDivision.objects.get(id=7)
    tipo_socio_id = request.POST['tipoSocio']  # valor seleccionado del campo de selección nuevo jugador
    tipoSocio = TipoSocio.objects.get(id=tipo_socio_id)
    #tipoSocio = TipoSocio.objects.get(id=2)
    jugadorNuevo = Jugador.objects.create(apodo=apodo, idDiv=idDiv,tipoSocio=tipoSocio )#,
    jornada = Jornada.objects.get(id=id)
    nueva_asistencia = Asistencia(idJor=jornada, idJug=jugadorNuevo, presente=True, user=request.user)
    nueva_asistencia.save()    
    asistencias_presentes = Asistencia.objects.filter(idJor=id, presente=True, idJug__tipoSocio__id=1 ).count() #envio el totalde presentes
    asistencias=Asistencia.objects.filter(idJor=id, idJug__idDiv__id=7).order_by('idJug__tipoSocio__descrp', 'idJug__apodo')#pero necesito solo las relacionadas a este project
    return render (request, 'asistencias_detalle.html', {'jornada':jornada, 'asistencias':asistencias,'asistencias_presentes': asistencias_presentes})
      
def editarJugador(request,idAs):
        asistencia=Asistencia.objects.get(id=idAs)
        jugador = Jugador.objects.get(id=asistencia.idJug.id)
        tipos_socio = TipoSocio.objects.all()
        Divisiones = TipoDivision.objects.all()
        return render(request , "editarJugador.html",{'jugador':jugador,'asistencia':asistencia,'tipos_socio':tipos_socio,'tipos_Div':Divisiones } )

def modificarJugador(request):
    apodo = request.POST['txtApodo']
    div = request.POST['txtdiv']
    idJu = request.POST['txtId']
    IdAs = request.POST['txtIdAs']
    entrena = request.POST.get('txtEntrena') == 'True'
    print(request.POST.get('txtEntrena'))
    jugador = Jugador.objects.get(id=idJu)
    jugador.apodo=apodo
    jugador.div=div
    jugador.entrena=entrena
    jugador.save()
    asistencia = Asistencia.objects.get(id=IdAs)
    jornada = Jornada.objects.get(id=asistencia.idJor.id)
    asistencias=Asistencia.objects.filter(idJor=asistencia.idJor.id)
    return render (request, 'asistencias_detalle.html', {'jornada':jornada, 'asistencias':asistencias})

def modificarJornada (request,id):
    titulo="Asistencias"
    club="La canchita"
    totalJug = defaultdict(int)
    totalPfe = defaultdict(int)
    totalMgr = defaultdict(int)
    totalPF = defaultdict(int)

    jornada = get_object_or_404(Jornada, pk=id)#, user=request.user)
    if request.method == 'GET':
        form = CreateNewJornada(initial={'fechaJor': jornada.fechaJor, 'tipoJor': jornada.tipoJor, 'titulo': jornada.titulo, 'obs': jornada.obs})
        return render(request, 'jornadasModificar.html', {'form': form ,'titulo': titulo ,'club':club})
    else:
        form = CreateNewJornada(request.POST)
        if form.is_valid():
            # Actualizar los campos de la instancia de Jornada
            jornada.fechaJor = form.cleaned_data['fechaJor']
            jornada.tipoJor = form.cleaned_data['tipoJor']
            jornada.titulo = form.cleaned_data['titulo']
            jornada.obs = form.cleaned_data['obs']
            jornada.save()

            # Resto de la lógica después de guardar el formulario
            jornadas = Jornada.objects.all()
            asistencias_totals = AsistenciasTotal.objects.filter(tipoDiv__in=range(1, 10)).order_by('-idJor', 'tipoDiv', 'tipoSoc')
            #        se podria hacer una functionque devuelva este diccionario
            jornadas = Jornada.objects.all().order_by('-id')
            for jornada in jornadas:    
                numAsistSoc = AsistenciasTotal.objects.filter(idJor=jornada, tipoSoc=1).aggregate(Sum('totalAsist'))
                totalJug[(jornada.id)] =numAsistSoc["totalAsist__sum"]
                totalJug_dict = dict(totalJug)
                numAsistSoc = AsistenciasTotal.objects.filter(idJor=jornada, tipoSoc=2).aggregate(Sum('totalAsist'))
                totalPfe[(jornada.id)] =numAsistSoc["totalAsist__sum"]
                totalPfe_dict = dict(totalPfe)
                numAsistSoc = AsistenciasTotal.objects.filter(idJor=jornada, tipoSoc=3).aggregate(Sum('totalAsist'))
                totalMgr[(jornada.id)] =numAsistSoc["totalAsist__sum"]
                totalMgr_dict = dict(totalMgr)
                numAsistSoc = AsistenciasTotal.objects.filter(idJor=jornada, tipoSoc=4).aggregate(Sum('totalAsist'))
                totalPF[(jornada.id)] =numAsistSoc["totalAsist__sum"]
                totalPF_dict = dict(totalPF)
            return render(request, 'jornadasBloque.html', {'asistencias_totals': asistencias_totals, 'jornadas': jornadas, 'totalJug': totalJug_dict ,'totalPfe': totalPfe_dict ,'totalMgr': totalMgr_dict ,'totalPF': totalPF_dict , 'titulo': titulo, 'club': club})
        else:
            # Manejar el caso en que el formulario no es válido
            return render(request, 'jornadasModificar.html', {'form': form, 'titulo': titulo, 'club': club, 'error': 'Error Actualizando Asistencia'})



def eliminarJornada (request,id):
            titulo = "Asistencias"
            club = "La canchita"
            totalJug = defaultdict(int)
            totalPfe = defaultdict(int)
            totalMgr = defaultdict(int)
            totalPF = defaultdict(int)
            
            jornada=Jornada.objects.get(id=id)
            jornada.delete()
            
            jornadas = Jornada.objects.all()
            asistencias_totals = AsistenciasTotal.objects.filter(tipoDiv__in=range(1, 10)).order_by('-idJor', 'tipoDiv', 'tipoSoc')
            #        se podria hacer una functionque devuelva este diccionario
            jornadas = Jornada.objects.all().order_by('-id')
            for jornada in jornadas:    
                numAsistSoc = AsistenciasTotal.objects.filter(idJor=jornada, tipoSoc=1).aggregate(Sum('totalAsist'))
                totalJug[(jornada.id)] =numAsistSoc["totalAsist__sum"]
                totalJug_dict = dict(totalJug)
                print(totalJug)
                numAsistSoc = AsistenciasTotal.objects.filter(idJor=jornada, tipoSoc=2).aggregate(Sum('totalAsist'))
                totalPfe[(jornada.id)] =numAsistSoc["totalAsist__sum"]
                totalPfe_dict = dict(totalPfe)
                print(totalPfe)
                numAsistSoc = AsistenciasTotal.objects.filter(idJor=jornada, tipoSoc=3).aggregate(Sum('totalAsist'))
                totalMgr[(jornada.id)] =numAsistSoc["totalAsist__sum"]
                totalMgr_dict = dict(totalMgr)
                print(totalMgr)
                numAsistSoc = AsistenciasTotal.objects.filter(idJor=jornada, tipoSoc=4).aggregate(Sum('totalAsist'))
                totalPF[(jornada.id)] =numAsistSoc["totalAsist__sum"]
                totalPF_dict = dict(totalPF)
                print(totalPF)
            return render(request, 'jornadasBloque.html', {'asistencias_totals': asistencias_totals, 'jornadas': jornadas, 'totalJug': totalJug_dict ,'totalPfe': totalPfe_dict ,'totalMgr': totalMgr_dict ,'totalPF': totalPF_dict , 'titulo': titulo, 'club': club})

   

        






