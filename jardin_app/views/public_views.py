from django.shortcuts import render
from ..models import Evento

def pagina_principal(request):
    eventos = Evento.objects.all()
    return render(request, 'pagina_principal.html', {'eventos': eventos})
