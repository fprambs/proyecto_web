from __future__ import unicode_literals

from django.db import models


class Usuario(models.Model):
    nombre = models.CharField(max_length=80)
    fecha_nacimiento = models.DateField()
    email= models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=15)
    telefono = models.IntegerField(blank=True, null= True)
    direccion = models.CharField(max_length=80, null=True, blank=True)
    check_offer = models.NullBooleanField(null= True, default=False)


class Tipo_Usuario(models.Model):
    tipo = models.CharField(max_length=45)

class Usuario_Tiene_Tipo_Usuario(models.Model):
    Usuario_idUsuario = models.ForeignKey(Usuario)
    Tipo_Usuario_idTipo = models.ForeignKey(Tipo_Usuario)

class Region(models.Model):
    region = models.CharField(max_length=30)

class Comuna(models.Model):
    comuna = models.CharField(max_length=30)
    Region_idRegion = models.ForeignKey(Region)

class Ciudad(models.Model):
    ciudad = models.CharField(max_length=30)
    Comuna_idComuna = models.ForeignKey(Comuna)


class Tipo_Propiedad(models.Model):
    tipo = models.CharField(max_length=30)


class Propiedad(models.Model):
    direccion = models.CharField(max_length=80)
    cantidad_disponible = models.IntegerField()
    cantidad = models.IntegerField()
    latitud = models.CharField(max_length=40)
    longitud = models.CharField(max_length=40)
    Ciudad_idCiudad = models.ForeignKey(Ciudad)
    Tipo_Propiedad_idTipo_Propiedad = models.ForeignKey(Tipo_Propiedad)

class Foto(models.Model):
    ruta = models.CharField(max_length=200)
    Propiedad_idPropiedad= models.ForeignKey(Propiedad)


class Usuario_Ocupa_Propiedad(models.Model):
     Usuario_idUsuario = models.ForeignKey(Usuario)
     Propiedad_idPropiedad = models.ForeignKey(Propiedad)
     fecha_inicio = models.DateTimeField(primary_key=True)
     fecha_termino = models.DateTimeField()
    
class Usuario_Arrienda_Propiedad(models.Model):
     Usuario_idUsuario = models.ForeignKey(Usuario)
     Propiedad_idPropiedad = models.ForeignKey(Propiedad)
     fecha_inicio = models.DateTimeField(primary_key=True)
     fecha_termino = models.DateTimeField()


class Usuario_Califica_Usuario(models.Model):
    Usuario_idUsuario = models.ForeignKey(Usuario,related_name='usuario1')
    Usuario_idUsuario1 = models.ForeignKey(Usuario, related_name='usuario2')
    fecha = models.DateField()
    calificacion = models.IntegerField()

class Usuario_Califica_Propiedad(models.Model):
    fecha = models.DateField()
    calificacion = models.IntegerField()
    comentario = models.CharField(max_length=500,null=True)
    Usuario_idUsuario = models.ForeignKey(Usuario)
    Propiedad_idPropiedad = models.ForeignKey(Propiedad)



 
    

