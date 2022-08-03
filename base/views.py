from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json

#---------------#
### USER CRUD ###
#---------------#

@csrf_exempt
def postUser(request): #POST
    if request.method == "POST":
    # ------------------------ #
        name, gmail, password = request.POST['name'],request.POST['gmail'], request.POST['password']

        user = User.objects.create_user(name,gmail,password)
        UserData.objects.create(
                user = user,
                telefono = " ",
                tarjeta = " ",
                )

        return HttpResponse(
                json.dumps({'message':'/POST/USER/REGISTER 200'}, indent=3),
                content_type='application/json'
                )

    # ------------------------ #
    else:
        return HttpResponse(
                    json.dumps({'message':'/POST/USER/REGISTER 404 INCORRECT REQUEST METHOD'}, indent=3),
                    content_type='application/json'
                    )

@csrf_exempt
def loginUser(request): #POST
    if request.method == "POST":
    # ------------------------ #
        name, password = request.POST['name'], request.POST['password']

        if request.user.is_authenticated:
            return HttpResponse(
                    json.dumps({'message':'Already Authenticated'}, indent=3),
                    content_type='application/json'
                    )

        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(
                    json.dumps({'message':'/POST/USER/LOGIN 200'}, indent=3),
                    content_type='application/json'
                    )
        else:
            return HttpResponse(
                    json.dumps({'message':'/POST/USER/LOGIN 404 INCORRECT USER DATA'}, indent=3),
                    content_type='application/json'
                    )

    # ------------------------ #
    else:
        return HttpResponse(
                    json.dumps({'message':'/POST/USER/LOGIN INCORRECT REQUEST METHOD'}, indent=3),
                    content_type='application/json'
                    )

@csrf_exempt
def logoutUser(request): #POST
    if request.method == "POST":
    # ------------------------ #

        logout(request)
        userl = request.user
        return HttpResponse(
                json.dumps({'message':'/POST/USER/LOGOUT 200'}, indent=3),
                content_type='application/json'
                )

    # ------------------------ #
    else:
        return HttpResponse(
                json.dumps({'message':'/POST/USER/LOGOUT INCORRECT REQUEST METHOD'}, indent=3),
                content_type='application/json'
                )

def profileUser(request): #GET
    if request.user.is_authenticated:
        user = request.user
        user_data = UserData.objects.get(user_id=user.id)
        jsonUser = {
                'id': user.id,
                'Username': user.username,
                'Correo': user.email,
                'Nombre': user.first_name,
                'Apellido': user.last_name,
                'Telefono': user_data.telefono,
                'Tarjeta': user_data.tarjeta
                }

        return HttpResponse(
                json.dumps(jsonUser, indent=3),
                content_type='application/json'
                )

    else:
        return HttpResponse(
                json.dumps({'message':'/POST/USER/PUT 404 NO USER AUTHENTICATED'}, indent=3),
                content_type='application/json'
                )

@csrf_exempt
def putUser(request): # PUT
    if request.method == "POST":
    # ------------------------ #

        if request.user.is_authenticated:
            user = request.user 
            user_data = UserData.objects.get(user_id=user.id)

            user.username = request.POST["uname"]
            user.email = request.POST["gmail"]
            user.first_name = request.POST["fname"]
            user.last_name = request.POST["lname"]
            user_data.telefono = request.POST["telefono"]
            user_data.tarjeta = request.POST["tarjeta"]

            user.save()
            user_data.save()

            return HttpResponse(
                    json.dumps({'message':'/POST/USER/PUT 200'}, indent=3),
                    content_type='application/json'
                    )

        else:
            return HttpResponse(
                json.dumps({'message':'/POST/USER/PUT 404 NO USER AUTHENTICATED'}, indent=3),
                content_type='application/json'
                )

    # ------------------------ #
    else:
        return HttpResponse(
                    json.dumps({'message':'/POST/USER/PUT INCORRECT REQUEST METHOD'}, indent=3),
                    content_type='application/json'
                    )

#-----------------------#
### PUBLICATIONS CRUD ###
#-----------------------#

def getPublications(request): #GET
    publications = Publication.objects.all()
    publications = [x for x in publications if x.estado == 'Activo']
    jsonPublications = []
    for x in publications:
        jsonPublications.append({
                'id': x.id,
                'Nombre': x.nombre,
                'Usuario': x.user.username,
                'UserID': x.user.id,
                'Descripcion': x.descripcion,
                'Puntuacion': x.puntuacion,
                'Estado': x.estado,
                'Precio': x.precio,
                'FechaCreacion': str(x.created)
                })

    return HttpResponse(
            json.dumps(jsonPublications, indent=3),
            content_type='application/json'
            )

@csrf_exempt
def postPublicationDetail(request): #POST
    if request.method == "POST":
    # ------------------------ #
        name, description, punctuation, status, price = request.POST['nombre'], request.POST['descripcion'], request.POST['puntuacion'], request.POST['estado'], request.POST['precio']

        if request.user.is_authenticated:
            Publication.objects.create(
                    user = request.user,
                    nombre = name,
                    descripcion = description,
                    puntuacion = punctuation,
                    estado = status,
                    precio = price
                    )

            return HttpResponse(
                    json.dumps({'message':'/POST/PUBLICATION/REGISTER 200'}, indent=3),
                    content_type='application/json'
                    )
        else:
            return HttpResponse(
                    json.dumps({'message':'/POST/PUBLICATION/REGISTER 404 NO USER AUTHENTICATED'}, indent=3),
                    content_type='application/json'
                    )

    # ------------------------ #
    else:
        return HttpResponse(
                    json.dumps({'message':'/POST/PUBLICATION/REGISTER INCORRECT REQUEST METHOD'}, indent=3),
                    content_type='application/json'
                    )

@csrf_exempt
def putPublicationDetail(request, pk): # PUT
    if request.method == "POST":
    # ------------------------ #

        if request.user.is_authenticated:

            try:
                publicationDetail = Publication.objects.get(id=pk)

                if request.user == publicationDetail.user:
                    x = publicationDetail                
                    x.nombre = request.POST['Nombre']
                    x.descripcion = request.POST['Descripcion']
                    x.puntuacion = request.POST['Puntuacion']
                    x.estado = request.POST['Estado']
                    x.precio = request.POST['Precio']
                    x.save()

                    jsonPublicationDetail = {
                            'id': x.id,
                            'Nombre': x.nombre,
                            'Usuario': x.user.username,
                            'Descripcion': x.descripcion,
                            'Puntuacion': x.puntuacion,
                            'Estado': x.estado,
                            'Precio': x.precio,
                            'FechaCreacion': str(x.created)
                            }

                    return HttpResponse(
                        json.dumps(jsonPublicationDetail, indent=3),
                        content_type='application/json'
                        )

                else:
                    return HttpResponse(
                        json.dumps({'message':'/PUT/PUBLICATION 404 NO USER PERMISSIONS'}, indent=3),
                        content_type='application/json'
                        )

            except:
                return HttpResponse(
                        json.dumps({'message':'/PUT/PUBLICATION 404 UNREGISTERED PUBLICATION'}, indent=3),
                        content_type='application/json'
                        )
        else:
            return HttpResponse(
                json.dumps({'message':'/PUT/PUBLICATION 404 NO USER AUTHENTICATED'}, indent=3),
                content_type='application/json'
                )

    # ------------------------ #
    else:
        return HttpResponse(
                    json.dumps({'message':'/POST/PUBLICATION/PUT INCORRECT REQUEST METHOD'}, indent=3),
                    content_type='application/json'
                    )

@csrf_exempt
def delPublicationDetail(request, pk): # DELETE
    if request.method == "POST":
    # ------------------------ #

        if request.user.is_authenticated:

            try:
                publicationDetail = Publication.objects.get(id=pk)

                if request.user == publicationDetail.user:
                    publicationDetail.delete()

                    return HttpResponse(
                            json.dumps({'message':'/POST/PUBLICATION/DELETE 200'}, indent=3),
                            content_type='application/json'
                            )
                else:
                    return HttpResponse(
                            json.dumps({'message':'/POST/PUBLICATION/DELETE 404 NO USER PERMISSIONS'}, indent=3),
                            content_type='application/json'
                            )

            except:
                return HttpResponse(
                        json.dumps({'message':'/POST/PUBLICATION/DELETE 404 UNREGISTERED PUBLICATION'}, indent=3),
                        content_type='application/json'
                        )

        else:
            return HttpResponse(
                json.dumps({'message':'/POST/PUBLICATION/DELETE 404 NO USER AUTHENTICATED'}, indent=3),
                content_type='application/json'
                )
    # ------------------------ #
    else:
        return HttpResponse(
                    json.dumps({'message':'/POST/PUBLICATION/DELETE INCORRECT REQUEST METHOD'}, indent=3),
                    content_type='application/json'
                    )

def getPublicationUser(request, pk): # GET
    try:
        user = User.objects.get(id=pk)
        user_publications = Publication.objects.filter(user=user)
        jsonPublications = []
        for x in user_publications:
            jsonPublications.append({
                'id': x.id,
                'Nombre': x.nombre,
                'Usuario': x.user.username,
                'UserID': x.user.id,
                'Descripcion': x.descripcion,
                'Puntuacion': x.puntuacion,
                'Estado': x.estado,
                'Precio': x.precio,
                'FechaCreacion': str(x.created)
                })

        return HttpResponse(
                json.dumps(jsonPublications, indent=3),
                content_type='application/json'
                )
    except:
        return HttpResponse(
                json.dumps({'message':'/GET/PUBLICATION/USER 404 NO USER REGISTERED'}, indent=3),
                content_type='application/json'
                )

#-----------------------#
### REPORTES CRUD ###
#-----------------------#

@csrf_exempt
def postReportDetail(request):
    if request.method == "POST":
    # ------------------------ #
        publication, razon_r, estado_r = request.POST['publicacionid'], request.POST['razon'], request.POST['estado']

        if request.user.is_authenticated:

            publication = Publication.objects.get(id=publication)
            Reportes.objects.create(
                    user = request.user,
                    publicacion = publication,
                    razon = razon_r,
                    estado = estado_r
                    )

            return HttpResponse(
                    json.dumps({'message':'/POST/REPORT/REGISTER 200'}, indent=3),
                    content_type='application/json'
                    )

        else:
            return HttpResponse(
                    json.dumps({'message':'/POST/REPORT/REGISTER 404 NO USER AUTHENTICATED'}, indent=3),
                    content_type='application/json'
                    )

    # ------------------------ #
    else:
        return HttpResponse(
                    json.dumps({'message':'/POST/REPORT/REGISTER INCORRECT REQUEST METHOD'}, indent=3),
                    content_type='application/json'
                    )
