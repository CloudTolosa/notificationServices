from django.contrib import admin
from servicios.models import UserProfile, Barrio
from django.contrib import admin, sites

admin.site.register(UserProfile)
admin.site.register(Barrio)

class LocalizacionAdminSite(admin.AdminSite):
    site_header = 'Localización'

mi_seccion_admin_site = LocalizacionAdminSite(name='miadmin')
mi_seccion_admin_site.register(Barrio)