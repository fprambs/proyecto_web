from arrendados.models import Usuario, Propiedad, Usuario_Tiene_Tipo_Usuario, Tipo_Usuario, Tipo_Propiedad, Ciudad
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import StreamingHttpResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def Users(request):
    #Obtengo a todos los usuarios de la BD
    if request.method == 'GET':
        # Obtengo como objeto la lista de todos los usuarios de la BD
        usuarios = Usuario.objects.all()
        #Hago una conversion a formato JSON
        usuarios = serializers.serialize("json",usuarios)
        #Entrego una respuesta de formato JSON
        return HttpResponse(usuarios, content_type='application/json')
    #Agrego un nuevo registro de tipo Usuario a la BD
    if request.method == 'POST':
        try:
            #Obtengo la data del body de la peticion que viene en formato JSON
            json_data = json.loads(request.body)
            #Guardo en variables cada uno de los atributos
            nombre = json_data['nombre']
            fecha_nacimiento = json_data['fecha_nacimiento']
            email = json_data['email']
            password = json_data['password']
            telefono = json_data['telefono']
            direccion = json_data['direccion']
            tipo_usuario = json_data['tipo_usuario']
            check_offer = json_data['check_offer']


            #Hago un INSERT a la BD en la tabla Usuarios
            datos_usuario = Usuario(nombre=nombre,fecha_nacimiento=fecha_nacimiento,email=email,password=password,telefono=telefono,direccion=direccion, check_offer=check_offer)
            datos_usuario.save() 

            #Guardo un objeto de de tipo : Tipo_Usuario donde la id sea el tipo del usuario
            tipo_usuario1 = Tipo_Usuario.objects.get(id=tipo_usuario)

            #Hago un INSERT a la BD en la tabla Usuario_Tiene_Tipo_Usuario para formar la relacion
            datos_tipo = Usuario_Tiene_Tipo_Usuario(Usuario_idUsuario=datos_usuario, Tipo_Usuario_idTipo=tipo_usuario1)
            datos_tipo.save()

            #Verificamos que la id del Usuario o la id del Usuario_Tiene_Tipo_Usuario sea Valida
            #Si es Vacia, hubo un problema y respondimos en formato JSON
            if datos_usuario.id is None or datos_tipo.id is None:
                unsuccessful={'unsuccessful':'Hubo un problema al agregar un Usuario'}
                successful_json = json.dumps(unsuccesful)
                return HttpResponse(unsuccessful, content_type='application/json', status=400)
            #Si son correctas es que los datos fueron agregados exitosamente
            else:
                successful ={'success':'Usuario agregado correctamente','id':datos_usuario.id}
                successful_json = json.dumps(successful)
                return HttpResponse(successful_json, content_type='application/json', status=201)
        
        #Manejo de error para el Email unico
        except IntegrityError as c:
            error ={'error':c.args[1]}
            error_json = json.dumps(error)

            return HttpResponse(error_json, content_type='application/json', status=400)




@csrf_exempt        
def User(request,id="0"):
    if request.method == 'GET':
        usuario = Usuario.objects.filter(id=id)
        usuario = serializers.serialize("json",usuario)
        return HttpResponse(usuario, content_type='application/json')

    if request.method == 'PUT':
        try:
            usuario = Usuario.objects.get(id=id)
            json_data = json.loads(request.body)
            nombre = json_data['nombre']
            fecha_nacimiento = json_data['fecha_nacimiento']
            email = json_data['email']
            password = json_data['password']
            telefono = json_data['telefono']
            direccion = json_data['direccion']
            tipo_usuario = json_data['tipo_usuario']
            check_offer= json_data['check_offer']
            #Obtengo  los datos a modificar y los guardo nuevamente
            datos_usuario = Usuario(id=id, nombre=nombre,fecha_nacimiento=fecha_nacimiento,email=email,password=password,telefono=telefono,direccion=direccion, check_offer=check_offer)
            datos_usuario.save() 

            #Obtengo la id de la relacion segun la id del usuario
            usuario_relacion = Usuario_Tiene_Tipo_Usuario.objects.get(Usuario_idUsuario=id)

            #Obtengo la id del tipo de usuario segun la id del usuario
            tipo_usuario1 = Tipo_Usuario.objects.get(id=tipo_usuario)

            #Modifico la tabla Usuario_Tiene_Tipo_Usuario segun los datos nuevos
            datos_tipo = Usuario_Tiene_Tipo_Usuario(id=usuario_relacion.id, Usuario_idUsuario=datos_usuario, Tipo_Usuario_idTipo=tipo_usuario1)
            datos_tipo.save()

            response ={'response': 'Se cambiaron correctamente los registros', 'code': '200', 'status': 'OK'}
            successful_json = json.dumps(response)
            return HttpResponse(successful_json, content_type='application/json', status=200)


        except Exception as c:
            print c
            response ={'response': 'No se cambiaron los registros', 'code': '500', 'status': 'ERROR'}
            successful_json = json.dumps(response)
            return HttpResponse(successful_json, content_type='application/json', status=200)

    if request.method == 'DELETE':
        try:
            usuario = Usuario.objects.get(id=id)
            usuario.delete()
            
            if usuario.id is None:
                response ={'response': 'El usuario de id: ' + str(id) + ' ha sido eliminado correctamente', 'code': '200', 'status': 'OK'}
                successful_json = json.dumps(response)
                return HttpResponse(successful_json, content_type='application/json', status=200)

        except ObjectDoesNotExist as c:
                response ={'response': 'El usuario de id: ' + str(id) + ' no existe', 'code': '500', 'status': 'ERROR'}
                successful_json = json.dumps(response)
                return HttpResponse(successful_json, content_type='application/json', status=500)





@csrf_exempt
def Properties(request):
    #Obtengo todas las propiedades de la BD
    if request.method == 'GET':
        #Obtengo como objeto la lista de todas las propiedades de la BD
        propiedades = Propiedad.objects.all()
        #Hago una conversion a formato JSON
        propiedades = serializers.serialize("json",propiedades)
        #Engtrego una respuesta en formato JSON
        return HttpResponse(propiedades, content_type='application/json', status=200) 
    #Agrego un nuevo registro de tipo propiedad a la BD
    if request.method == 'POST':

            #Obtengo la data del body de la peticion que viene en formato JSON
            json_data = json.loads(request.body)
            #Guardo en variables cada uno de los atributos
            direccion = json_data['direccion']
            cantidad_disponible = json_data['cantidad_disponible']
            cantidad = json_data['cantidad']
            latitud = json_data['latitud']
            longitud = json_data['longitud']
            Ciudad_idCiudad = json_data['Ciudad_idCiudad']
            Tipo_Propiedad_idTipo_Propiedad = json_data['Tipo_Propiedad_idTipo_Propiedad']
            #Obtengo el objeto del tipo de propiedad segun la id del tipo de propiedad
            tipo_propiedad = Tipo_Propiedad.objects.get(id=Tipo_Propiedad_idTipo_Propiedad)
            #Obtengo el objeto de la ciudad segun la id de la ciudad
            ciudad = Ciudad.objects.get(id=Ciudad_idCiudad)


            #Hago un INSERT a la BD en la tabla Propiedad
            datos_propiedad = Propiedad(direccion=direccion, cantidad_disponible=cantidad_disponible,cantidad=cantidad, latitud=latitud,longitud=longitud,Ciudad_idCiudad=ciudad,Tipo_Propiedad_idTipo_Propiedad = tipo_propiedad)
            datos_propiedad.save()

            #Verificamos que la id de la Propiedad 
            #Si es Vacia, hubo un problema y respondimos en formato JSON
            if datos_propiedad.id is None :
                unsuccessful={'unsuccessful':'Hubo un problema al agregar una propiedad'}
                successful_json = json.dumps(unsuccesful)
                return HttpResponse(unsuccessful, content_type='application/json', status=400)
            #Si son correctas es que los datos fueron agregados exitosamente
            else:
                successful ={'success':'Propiedad agregada correctamente','id':datos_propiedad.id}
                successful_json = json.dumps(successful)
                return HttpResponse(successful_json, content_type='application/json', status=201)


        
@csrf_exempt        
def Property(request,id="0"):

    if request.method == 'GET':
        propiedad = Propiedad.objects.filter(pk=id)
        propiedad = serializers.serialize("json",propiedad)
        return HttpResponse(propiedad, content_type='application/json')

    if request.method == 'PUT':
        try:
            usuario = Usuario.objects.get(id=id)
            json_data = json.loads(request.body)
            nombre = json_data['nombre']
            fecha_nacimiento = json_data['fecha_nacimiento']
            email = json_data['email']
            password = json_data['password']
            telefono = json_data['telefono']
            direccion = json_data['direccion']
            tipo_usuario = json_data['tipo_usuario']
            check_offer= json_data['check_offer']
            #Obtengo  los datos a modificar y los guardo nuevamente
            datos_usuario = Usuario(id=id, nombre=nombre,fecha_nacimiento=fecha_nacimiento,email=email,password=password,telefono=telefono,direccion=direccion, check_offer=check_offer)
            datos_usuario.save() 

            #Obtengo la id de la relacion segun la id del usuario
            usuario_relacion = Usuario_Tiene_Tipo_Usuario.objects.get(Usuario_idUsuario=id)

            #Obtengo la id del tipo de usuario segun la id del usuario
            tipo_usuario1 = Tipo_Usuario.objects.get(id=tipo_usuario)

            #Modifico la tabla Usuario_Tiene_Tipo_Usuario segun los datos nuevos
            datos_tipo = Usuario_Tiene_Tipo_Usuario(id=usuario_relacion.id, Usuario_idUsuario=datos_usuario, Tipo_Usuario_idTipo=tipo_usuario1)
            datos_tipo.save()

            response ={'response': 'Se cambiaron correctamente los registros', 'code': '200', 'status': 'OK'}
            successful_json = json.dumps(response)
            return HttpResponse(successful_json, content_type='application/json', status=200)


        except Exception as c:
            print c
            response ={'response': 'No se cambiaron los registros', 'code': '500', 'status': 'ERROR'}
            successful_json = json.dumps(response)
            return HttpResponse(successful_json, content_type='application/json', status=200)


    




    
    
    