from arrendados.models import Usuario, Propiedad, Usuario_Tiene_Tipo_Usuario, Tipo_Usuario
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import StreamingHttpResponse
from django.db import IntegrityError


#---------------------------------- USUARIOS ---------------------------------------------------
@csrf_exempt
def usuarios(request):
#-----Consulta a todos los usuarios a localhost:8000/usuarios/
    if request.method == 'GET':
        usuarios = Usuario.objects.all()
        usuarios = serializers.serialize("json",usuarios)
        return HttpResponse(usuarios, content_type='application/json')

    


@csrf_exempt
def usuario(request,id="0"):
#-----Consulta a un usuario especificando ID a localhost:8000/usuario/idusuario/
    if request.method == 'GET':
        usuario = Usuario.objects.filter(pk=id)
        usuario = serializers.serialize("json",usuario)
        return HttpResponse(usuario, content_type='application/json')

        print usuario

#-----Agrega un nuevo usuario mandandole los parametros por ajax a localhost:8000/usuario
    if request.method == 'POST':

        try:
            json_data = json.loads(request.body)

            nombre = json_data['nombre']
            fecha_nacimiento = json_data['fecha_nacimiento']
            email = json_data['email']
            password = json_data['password']
            telefono = json_data['telefono']
            direccion = json_data['direccion']
            tipo_usuario = json_data['tipo_usuario']


            datos_usuario = Usuario(nombre=nombre,fecha_nacimiento=fecha_nacimiento,email=email,password=password,telefono=telefono,direccion=direccion)
            datos_usuario.save() 

            tipo_usuario1 = Tipo_Usuario.objects.get(pk=tipo_usuario)

            datos_tipo = Usuario_Tiene_Tipo_Usuario(Usuario_idUsuario=datos_usuario, Tipo_Usuario_idTipo=tipo_usuario1)
            datos_tipo.save()

            if datos_usuario.id is None or datos_tipo.id is None:
                unsuccessful={'unsuccessful':'Hubo un problema al agregar un Usuario'}
                successful_json = json.dumps(unsuccesful)
                return HttpResponse(unsuccessful, content_type='application/json', status=400)
            else:
                successful ={'success':'Usuario agregado correctamente','id':datos_usuario.id}
                successful_json = json.dumps(successful)
                return HttpResponse(successful_json, content_type='application/json', status=201)
        
        except IntegrityError as c:
            error ={'error':c.args[1]}
            error_json = json.dumps(error)

            return HttpResponse(error_json, content_type='application/json', status=400)

        
        
        
        
    





#--------------------------------PROPIEDADES-----------------------------------------------

@csrf_exempt
def propiedades(request):
#-----Consulta a todas las propiedades a localhost:8000/propiedades/
    if request.method == 'GET':
        propiedades = Propiedad.objects.all()
        propiedades = serializers.serialize("json",propiedades)
        return HttpResponse(propiedades, content_type='application/json') 
        
@csrf_exempt        
def propiedad(request,id="0"):
#-----Consulta a una propiedad especificando ID a localhost:8000/propiedad/idpropiedad/

    if request.method == 'GET':
        propiedad = Propiedad.objects.filter(pk=id)
        propiedad = serializers.serialize("json",propiedad)
        return HttpResponse(propiedad, content_type='application/json')

    
    if request.method == "POST":
        direccion = request.POST.get('direccion')
        cantidad_disponible = request.POST.get('cantidad_disponible')
        cantidad = request.POST.get('cantidad')
        latitud = request.POST.get('latitud')
        longitud = request.POST.get('longitud')
        ciudad = request.POST.get('ciudad')    # Valdivia ->1    Osorno ->2 y asi... 
        tipo_propiedad = request.POST.get(tipo_propiedad)




    
    
    