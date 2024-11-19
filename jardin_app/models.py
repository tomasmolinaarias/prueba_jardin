from django.db import models
from django.contrib.auth.models import User

class Apoderado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100, default="Desconocido")
    apellido_materno = models.CharField(max_length=100, default="Desconocido")
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno} - {self.rut}"


class Niño(models.Model):
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100, default="Desconocido")  # Valor por defecto
    apellido_materno = models.CharField(max_length=100, default="Desconocido")  # Valor por defecto
    fecha_nacimiento = models.DateField()
    rut = models.CharField(max_length=12, unique=True)
    sexo = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Crear automáticamente el usuario del apoderado si no existe
        if not User.objects.filter(username=self.apoderado.email).exists():
            clave = f"{self.nombre[0].lower()}{self.apellido_paterno.lower()}123"
            User.objects.create_user(
                username=self.apoderado.email,
                email=self.apoderado.email,
                password=clave,
                first_name=self.apoderado.nombre,
                last_name=self.apoderado.apellido_paterno
            )
    
class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
# Modelo para solicitudes de contacto de usuarios no registrados
class SolicitudContacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=[('Pendiente', 'Pendiente'), ('Visto', 'Visto')], default='Pendiente')

    def __str__(self):
        return f"Solicitud de {self.nombre} - {self.email}"

class ListaUtiles(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del útil (e.g., lápiz, goma)
    cantidad = models.IntegerField(default=1)  # Cantidad sugerida
    descripcion = models.TextField(blank=True, null=True)  # Descripción opcional
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def __str__(self):
        return f"{self.nombre} - {self.cantidad} unidades"

# Modelo para mensajes de apoderados al administrador
class MensajeApoderado(models.Model):
    apoderado = models.ForeignKey('Apoderado', on_delete=models.CASCADE)
    mensaje = models.TextField()
    respuesta = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=10, choices=[('Pendiente', 'Pendiente'), ('Resuelto', 'Resuelto')], default='Pendiente')
    fecha_envio = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Mensaje de {self.apoderado.nombre} - {self.estado}"
    
