from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Evento, ListaUtiles, MensajeApoderado

@login_required
def pagina_apoderado(request):
    """Panel principal del apoderado."""
    return render(request, 'apoderado/pagina_apoderado.html')

@login_required
def ver_eventos_apoderado(request):
    """Muestra los eventos relacionados."""
    eventos = Evento.objects.all()
    return render(request, 'apoderado/eventos.html', {'eventos': eventos})

@login_required
def ver_lista_utiles_apoderado(request):
    """Muestra la lista de útiles."""
    utiles = ListaUtiles.objects.all()
    return render(request, 'apoderado/utiles.html', {'utiles': utiles})

@login_required
def ver_mensajes_apoderado(request):
    """Muestra los mensajes enviados por el apoderado."""
    mensajes = MensajeApoderado.objects.filter(apoderado=request.user.apoderado)
    return render(request, 'apoderado/mensajes.html', {'mensajes': mensajes})

@login_required
def enviar_mensaje(request):
    """Permite al apoderado enviar un mensaje al administrador."""
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje')
        apoderado = request.user.apoderado
        MensajeApoderado.objects.create(apoderado=apoderado, mensaje=mensaje)
        return redirect('ver_mensajes_apoderado')
    return render(request, 'apoderado/enviar_mensaje.html')
