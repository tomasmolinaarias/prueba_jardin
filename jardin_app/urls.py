from django.urls import path
from jardin_app.views.public_views import pagina_principal
from jardin_app.views.auth_views import iniciar_sesion, cambiar_contrasena
from jardin_app.views.admin_views import (
    pagina_administrador,
    gestionar_niños,
    agregar_niño,
    editar_niño,
    eliminar_niño,
    gestionar_apoderados,
    gestionar_eventos,
    gestionar_utiles,
    ver_mensajes,  # Lista de mensajes
    ver_mensajes,  # Detalle de un mensaje específico
    responder_mensaje,
    editar_apoderado,
    eliminar_apoderado,
    agregar_evento,
    editar_evento,
    eliminar_evento,
    agregar_util,
    editar_util,
    eliminar_util,
    ver_solicitudes_contacto,
    marcar_como_visto,
    ver_mensaje
)
from jardin_app.views.contact_views import formulario_contacto, contacto_exitoso
from jardin_app.views.apoderado_views import (
    pagina_apoderado, ver_eventos_apoderado, ver_lista_utiles_apoderado, ver_mensajes_apoderado, enviar_mensaje)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Página principal
    path('', pagina_principal, name='pagina_principal'),

    # Iniciar sesión
    path('login/', iniciar_sesion, name='iniciar_sesion'),

    # Formulario de contacto
    path('contacto/', formulario_contacto, name='formulario_contacto'),
    path('contacto-exitoso/', contacto_exitoso, name='contacto_exitoso'),

    # Panel del administrador
    path('dashboard/admin', pagina_administrador, name='pagina_administrador'),

    # Panel del apoderado
    path('dashboard/apoderado/', pagina_apoderado, name='pagina_apoderado'),

    # Cambiar contraseña
    path('cambiar-contraseña/', cambiar_contrasena, name='cambiar_contrasena'),

    # Cerrar sesión
    path('logout/', LogoutView.as_view(), name='logout'),

    # ----------------------------------------------------------------
    #                        Gestión ADMIN
    # ----------------------------------------------------------------
    ################################################################
    # niño
    ################################################################
    path('dashboard/admin/niños/', gestionar_niños, name='gestionar_niños'),
    path('dashboard/admin/niños/agregar/', agregar_niño, name='agregar_niño'),
    path('dashboard/admin/niños/editar/<int:niño_id>/',
         editar_niño, name='editar_niño'),
    path('dashboard/admin/niños/eliminar/<int:niño_id>/',
         eliminar_niño, name='eliminar_niño'),

    ################################################################
    # apoderado
    ################################################################
    path('dashboard/admin/apoderados/',
         gestionar_apoderados, name='gestionar_apoderados'),
    path('dashboard/admin/apoderados/editar/<int:apoderado_id>/',
         editar_apoderado, name='editar_apoderado'),
    path('dashboard/admin/apoderados/eliminar/<int:apoderado_id>/',
         eliminar_apoderado, name='eliminar_apoderado'),

    ################################################################
    # eventos
    ################################################################
    path('dashboard/admin/eventos/', gestionar_eventos, name='gestionar_eventos'),
    path('dashboard/admin/eventos/agregar/',
         agregar_evento, name='agregar_evento'),
    path('dashboard/admin/eventos/editar/<int:evento_id>/',
         editar_evento, name='editar_evento'),
    path('dashboard/admin/eventos/eliminar/<int:evento_id>/',
         eliminar_evento, name='eliminar_evento'),

    ################################################################
    # mensajes
    ################################################################
     path('dashboard/admin/mensajes/', ver_mensajes, name='ver_mensajes'),  # Lista de mensajes
     path('dashboard/admin/mensajes/<int:mensaje_id>/', ver_mensaje, name='ver_mensaje'),  # Detalle de un mensaje específicoer un mensaje
     path('dashboard/admin/mensajes/<int:mensaje_id>/responder/',
          responder_mensaje, name='responder_mensaje'),

    ################################################################
    # útiles
    ################################################################

    path('dashboard/admin/utiles/', gestionar_utiles, name='gestionar_utiles'),
    path('dashboard/admin/utiles/agregar/', agregar_util, name='agregar_util'),
    path('dashboard/admin/utiles/editar/<int:util_id>/',
         editar_util, name='editar_util'),
    path('dashboard/admin/utiles/eliminar/<int:util_id>/',
         eliminar_util, name='eliminar_util'),
    ################################################################
    # contacto
    ################################################################
    path('dashboard/admin/solicitudes/', ver_solicitudes_contacto,
         name='ver_solicitudes_contacto'),
    path('dashboard/admin/solicitudes/<int:solicitud_id>/marcar/',
         marcar_como_visto, name='marcar_como_visto'),
    # ----------------------------------------------------------------
    #                        apoderado
    # ----------------------------------------------------------------

    path('dashboard/apoderado/', pagina_apoderado, name='pagina_apoderado'),
    path('dashboard/apoderado/eventos/',
         ver_eventos_apoderado, name='ver_eventos_apoderado'),
    path('dashboard/apoderado/utiles/', ver_lista_utiles_apoderado,
         name='ver_lista_utiles_apoderado'),
    path('dashboard/apoderado/mensajes/',
         ver_mensajes_apoderado, name='ver_mensajes_apoderado'),
    path('dashboard/apoderado/mensajes/enviar/',
         enviar_mensaje, name='enviar_mensaje'),


]
