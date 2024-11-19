from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        nueva_contrasena = request.POST['password']
        if len(nueva_contrasena) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
            return render(request, 'auth_session/cambiar_contrasena.html')

        usuario = request.user
        usuario.set_password(nueva_contrasena)
        usuario.save()
        messages.success(request, 'Contraseña actualizada con éxito.')
        return redirect('iniciar_sesion')
    return render(request, 'auth_session/cambiar_contrasena.html')


@csrf_exempt
def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('pagina_administrador')
            else:
                return redirect('pagina_apoderado')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'auth_session/iniciar_sesion.html')