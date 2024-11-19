from django.contrib import admin

from .models import SolicitudContacto, MensajeApoderado, Apoderado, Niño, Evento

admin.site.register(SolicitudContacto)
admin.site.register(MensajeApoderado)
admin.site.register(Apoderado)
admin.site.register(Niño)
admin.site.register(Evento)