from django.shortcuts import render, redirect
from ..models import SolicitudContacto

def formulario_contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        SolicitudContacto.objects.create(nombre=nombre, email=email, mensaje=mensaje)
        return redirect('contacto_exitoso')
    return render(request, 'contacto/contacto.html')

def contacto_exitoso(request):
    return render(request, 'contacto/contacto_exitoso.html')
