from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Niño, Apoderado, Evento, ListaUtiles, MensajeApoderado, SolicitudContacto
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils import timezone


################################################################
# NIÑOS
################################################################
@login_required
def pagina_administrador(request):
    return render(request, 'pagina_administrador.html')

@login_required
def gestionar_niños(request):
    niños = Niño.objects.all()
    apoderados = Apoderado.objects.all()
    return render(request, 'admin/nino/gestionar_ninos.html', {'niños': niños, 'apoderados': apoderados})


@login_required
@transaction.atomic
def agregar_niño(request):
    if request.method == 'POST':
        try:
            # Datos del niño
            nombre = request.POST['nombre']
            apellido_paterno = request.POST['apellido_paterno']
            apellido_materno = request.POST['apellido_materno']
            fecha_nacimiento = request.POST['fecha_nacimiento']
            rut = request.POST['rut']
            sexo = request.POST['sexo']

            # Datos del apoderado
            apoderado_nombre = request.POST['apoderado_nombre']
            apoderado_apellido_paterno = request.POST['apoderado_apellido_paterno']
            apoderado_apellido_materno = request.POST['apoderado_apellido_materno']
            apoderado_rut = request.POST['apoderado_rut']
            apoderado_telefono = request.POST['apoderado_telefono']

            # Generar correo y contraseña
            email = f"{apoderado_nombre[0].lower()}{apoderado_apellido_paterno.lower()}@jardin.cl"
            contraseña = f"{apoderado_nombre.lower()}.{apoderado_apellido_paterno.lower()}.123"

            # Verificar si el RUT del niño ya existe
            if Niño.objects.filter(rut=rut).exists():
                messages.error(request, f"El RUT {rut} ya está registrado. Por favor verifica los datos.")
                return redirect('gestionar_niños')

            # Verificar si el apoderado ya existe
            apoderado = Apoderado.objects.filter(rut=apoderado_rut).first()
            if not apoderado:
                # Crear el usuario del apoderado
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=contraseña,
                    first_name=apoderado_nombre,
                    last_name=apoderado_apellido_paterno,
                )

                # Crear apoderado asociado al usuario
                apoderado = Apoderado.objects.create(
                    user=user,
                    nombre=apoderado_nombre,
                    apellido_paterno=apoderado_apellido_paterno,
                    apellido_materno=apoderado_apellido_materno,
                    rut=apoderado_rut,
                    telefono=apoderado_telefono,
                    email=email,
                    contraseña=make_password(contraseña),
                )

            # Crear niño
            Niño.objects.create(
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                fecha_nacimiento=fecha_nacimiento,
                rut=rut,
                sexo=sexo,
                apoderado=apoderado
            )

            messages.success(request, f"Niño {nombre} agregado exitosamente. Apoderado: {apoderado.nombre}")
            return redirect('gestionar_niños')

        except Exception as e:
            messages.error(request, f"Hubo un error al agregar al niño: {str(e)}")
            return redirect('agregar_niño')

    return render(request, 'admin/nino/agregar_nino.html')


@login_required
def editar_niño(request, niño_id):
    niño = get_object_or_404(Niño, id=niño_id)
    apoderado = niño.apoderado  # Obtener el apoderado relacionado
    user = User.objects.filter(username=apoderado.email).first()  # Obtener el usuario si existe

    if request.method == 'POST':
        # Datos anteriores para comparar cambios
        apellidos_anteriores = (niño.apellido_paterno, niño.apellido_materno)

        # Actualizar datos del niño
        niño.nombre = request.POST['nombre']
        niño.apellido_paterno = request.POST['apellido_paterno']
        niño.apellido_materno = request.POST['apellido_materno']
        niño.fecha_nacimiento = request.POST['fecha_nacimiento']
        niño.rut = request.POST['rut']
        niño.sexo = request.POST['sexo']
        niño.save()

        # Actualizar el correo si cambian los apellidos
        if (niño.apellido_paterno, niño.apellido_materno) != apellidos_anteriores:
            nuevo_email = f"{niño.nombre[0].lower()}{niño.apellido_paterno.lower()}@jardin.cl"
            apoderado.email = nuevo_email  # Actualizar correo en el modelo Apoderado

            # Actualizar el usuario asociado en auth_user
            if user:
                user.username = nuevo_email
                user.email = nuevo_email
                user.save()

        apoderado.save()  # Guardar cambios en el apoderado

        messages.success(request, f"Niño {niño.nombre} actualizado exitosamente.")
        return redirect('gestionar_niños')  # Redirige a la lista de niños

    return render(request, 'admin/nino/editar_nino.html', {'niño': niño})


@login_required
def eliminar_niño(request, niño_id):
    # Obtén al niño que quieres eliminar
    niño = get_object_or_404(Niño, id=niño_id)
    apoderado = niño.apoderado  # Obtén el apoderado relacionado

    # Elimina al niño
    niño.delete()

    # Verifica si el apoderado tiene más niños asociados
    if not Niño.objects.filter(apoderado=apoderado).exists():
        # Si no tiene más niños, elimina el apoderado
        apoderado.user.delete()  # Eliminar el usuario asociado
        apoderado.delete()
    return redirect('gestionar_niños')  # Redirige a la gestión de niños

################################################################
# Apoderados
################################################################
@login_required
def gestionar_apoderados(request):
    apoderados = Apoderado.objects.all()
    return render(request, 'admin/apoderado/gestionar_apoderados.html', {'apoderados': apoderados})


@login_required
def editar_apoderado(request, apoderado_id):
    apoderado = get_object_or_404(Apoderado, id=apoderado_id)

    if request.method == 'POST':
        apoderado.nombre = request.POST['nombre']
        apoderado.apellido_paterno = request.POST['apellido_paterno']
        apoderado.apellido_materno = request.POST['apellido_materno']
        apoderado.rut = request.POST['rut']
        apoderado.telefono = request.POST['telefono']
        apoderado.save()
        messages.success(request, f"Apoderado {apoderado.nombre} actualizado exitosamente.")
        return redirect('gestionar_apoderados')

    return render(request, 'admin/apoderado/editar_apoderado.html', {'apoderado': apoderado})


@login_required
def eliminar_apoderado(request, apoderado_id):
    apoderado = get_object_or_404(Apoderado, id=apoderado_id)
    apoderado.user.delete()  # Eliminar usuario asociado
    apoderado.delete()
    messages.success(request, f"Apoderado {apoderado.nombre} eliminado exitosamente.")
    return redirect('gestionar_apoderados')

################################################################
# Eventos
################################################################
@login_required
def gestionar_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'admin/eventos/gestionar_eventos.html', {'eventos': eventos})


@login_required
def agregar_evento(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        fecha = request.POST['fecha']
        hora = request.POST['hora']
        lugar = request.POST['lugar']

        Evento.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            fecha=fecha,
            hora=hora,
            lugar=lugar
        )
        messages.success(request, 'Evento creado exitosamente.')
        return redirect('gestionar_eventos')

    return render(request, 'admin/eventos/agregar_evento.html')


@login_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if request.method == 'POST':
        evento.nombre = request.POST['nombre']
        evento.descripcion = request.POST['descripcion']
        evento.fecha = request.POST['fecha']
        evento.hora = request.POST['hora']
        evento.lugar = request.POST['lugar']
        evento.save()

        messages.success(request, 'Evento actualizado exitosamente.')
        return redirect('gestionar_eventos')

    return render(request, 'admin/eventos/editar_evento.html', {'evento': evento})


@login_required
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    evento.delete()
    messages.success(request, 'Evento eliminado exitosamente.')
    return redirect('gestionar_eventos')

################################################################
# Útiles
################################################################
@login_required
def gestionar_utiles(request):
    utiles = ListaUtiles.objects.all()
    return render(request, 'admin/utiles/gestionar_utiles.html', {'utiles': utiles})


@login_required
def agregar_util(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        cantidad = request.POST['cantidad']
        descripcion = request.POST['descripcion']
        
        ListaUtiles.objects.create(nombre=nombre, cantidad=cantidad, descripcion=descripcion)
        messages.success(request, f"El útil '{nombre}' ha sido agregado exitosamente.")
        return redirect('gestionar_utiles')
    return render(request, 'admin/utiles/agregar_util.html')


@login_required
def editar_util(request, util_id):
    util = get_object_or_404(ListaUtiles, id=util_id)
    if request.method == 'POST':
        util.nombre = request.POST['nombre']
        util.cantidad = request.POST['cantidad']
        util.descripcion = request.POST['descripcion']
        util.save()
        messages.success(request, f"El útil '{util.nombre}' ha sido actualizado exitosamente.")
        return redirect('gestionar_utiles')
    return render(request, 'admin/utiles/editar_util.html', {'util': util})


@login_required
def eliminar_util(request, util_id):
    util = get_object_or_404(ListaUtiles, id=util_id)
    util.delete()
    messages.success(request, f"El útil '{util.nombre}' ha sido eliminado exitosamente.")
    return redirect('gestionar_utiles')

################################################################
# Mensajes
################################################################
@login_required
def ver_mensajes(request):
    mensajes = MensajeApoderado.objects.all()
    return render(request, 'admin/mensajes/ver_mensajes.html', {'mensajes': mensajes})


@login_required
def responder_mensaje(request, mensaje_id):
    mensaje = get_object_or_404(MensajeApoderado, id=mensaje_id)

    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        mensaje.respuesta = respuesta
        mensaje.estado = 'Resuelto'
        mensaje.fecha_respuesta = timezone.now()
        mensaje.save()
        messages.success(request, 'Mensaje respondido correctamente.')
        return redirect('ver_mensaje', mensaje_id=mensaje.id)

    return render(request, 'admin/mensajes/responder_mensaje.html', {'mensaje': mensaje})

@login_required
def ver_mensaje(request, mensaje_id):
    mensaje = get_object_or_404(MensajeApoderado, id=mensaje_id)
    return render(request, 'admin/mensajes/ver_mensaje.html', {'mensaje': mensaje})


################################################################
# Contacto
################################################################
@login_required
def ver_solicitudes_contacto(request):
    pendientes = SolicitudContacto.objects.filter(estado="Pendiente")
    vistas = SolicitudContacto.objects.filter(estado="Visto")
    return render(request, 'admin/contacto/ver_solicitudes.html', {
        'pendientes': pendientes,
        'vistas': vistas
    })


@login_required
def marcar_como_visto(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudContacto, id=solicitud_id)
    solicitud.estado = "Visto"
    solicitud.save()
    messages.success(request, f"La solicitud de {solicitud.nombre} ha sido marcada como vista.")
    return redirect('ver_solicitudes_contacto')
