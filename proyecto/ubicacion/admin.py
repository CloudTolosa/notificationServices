from django.contrib import admin
import nested_admin
from .models import *
# Register your models here.

class BarrioInline(nested_admin.NestedStackedInline):
    model = Barrio
    sortable_field_name = "nombre"
    extra = 0

class LocalidadInline(nested_admin.NestedStackedInline):
    model = Localidad
    sortable_field_name = "nombre"
    inlines = [BarrioInline]
    extra = 0

class CiudadAdmin(nested_admin.NestedModelAdmin):
    inlines = [LocalidadInline]

#admin.site.register(Barrio)
admin.site.register(Localidad)
admin.site.register(Ciudad, CiudadAdmin)