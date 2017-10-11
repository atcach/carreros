from django.contrib import admin
from django.urls import reverse
from django.db.models import Q
from leaflet.admin import LeafletGeoAdmin
from .models import Seccion, Circuito, LugarVotacion, Mesa, Partido, Opcion, Eleccion, VotoMesaReportado
from django.http import HttpResponseRedirect
from django_admin_row_actions import AdminRowActionsMixin


class HasLatLongListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Tiene coordenadas'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'coordenadas'

    def lookups(self, request, model_admin):
        return (
            ('sí', 'sí'),
            ('no', 'no'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            isnull = value == 'no'
            queryset = queryset.filter(geom__isnull=isnull)
        return queryset


class TieneResultados(admin.SimpleListFilter):
    title = 'Tiene resultados'
    parameter_name = 'tiene_resultados'

    def lookups(self, request, model_admin):
        return (
            ('sí', 'sí'),
            ('no', 'no'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        print("==>> ",value)
        if value is not None:
            q = Q(votomesaoficial__votos__gt=0) | Q(votomesareportado__votos__gt=0)
            if value == "no":
                queryset = queryset.filter(~q)
            else:
                queryset = queryset.filter(q)

        return queryset


class TieneFiscal(admin.SimpleListFilter):
    title = 'Tiene fiscal'
    parameter_name = 'fiscal'
    lookup = 'asignacion__isnull'

    def lookups(self, request, model_admin):
        return (
            ('sí', 'sí'),
            ('no', 'no'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            isnull = value == 'no'
            queryset = queryset.filter(**{self.lookup: isnull})
        return queryset


class TieneFiscalGeneral(TieneFiscal):
    title = 'Tiene fiscal general'
    lookup = 'asignacion__isnull'


def mostrar_en_mapa(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ids = ",".join(selected)
    mapa_url = reverse('mapa')
    return HttpResponseRedirect(f'{mapa_url}?ids={ids}')

mostrar_en_mapa.short_description = "Mostrar seleccionadas en el mapa"


def mostrar_resultados_escuelas(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ids = ",".join(selected)
    mapa_url = reverse('resultados_escuelas')
    return HttpResponseRedirect(f'{mapa_url}?ids={ids}')

mostrar_resultados_escuelas.short_description = "Mostrar resultados de Escuelas seleccionadas"


def resultados_oficiales(modeladmin, request, queryset):

    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    name = modeladmin.model.__name__.lower()
    ids = "&".join(f'{name}={s}' for s in selected)
    mapa_url = reverse('resultados-mapa')
    return HttpResponseRedirect(f'{mapa_url}?{ids}')

resultados_oficiales.short_description = "Ver Resultados Oficiales"


class LugarVotacionAdmin(AdminRowActionsMixin, LeafletGeoAdmin):

    def sección(o):
        return o.circuito.seccion.numero

    list_display = ('nombre', 'direccion', 'ciudad', 'circuito', sección, 'mesas_desde_hasta', 'electores')
    list_display_links = ('nombre',)
    list_filter = (HasLatLongListFilter, TieneFiscalGeneral, 'circuito__seccion', 'circuito')
    search_fields = (
        'nombre', 'direccion', 'ciudad', 'barrio', 'mesas__numero'
    )
    show_full_result_count = False
    actions = [mostrar_en_mapa, resultados_oficiales]

    def get_row_actions(self, obj):
        row_actions = [
            {
                'label': 'Mesas',
                'url': reverse('admin:elecciones_mesa_changelist') + f'?lugar_votacion__id={obj.id}',
                'enabled': True,
            }
        ]
        if obj.asignacion_actual:
            url = reverse('admin:fiscales_asignacionfiscalgeneral_change', args=(obj.asignacion_actual.id,))
            label_asignacion = 'Editar asignación'

        else:
            url = reverse('admin:fiscales_asignacionfiscalgeneral_add') + f'?lugar_votacion={obj.id}'
            label_asignacion = 'Asignar fiscal general'

        row_actions.append({
            'label': f'{label_asignacion}',
            'url': url,
            'enabled': True
        })

        if obj.asignacion_actual and obj.asignacion_actual.fiscal:
            row_actions.append({
                'label': 'Fiscal',
                'url': reverse('admin:fiscales_fiscal_changelist') + f'?id={obj.asignacion_actual.fiscal.id}',
                'enabled': True
            })

        row_actions += super().get_row_actions(obj)
        return row_actions


def mostrar_resultados_mesas(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ids = ",".join(selected)
    mapa_url = reverse('resultados_mesas_ids')
    return HttpResponseRedirect(f'{mapa_url}?ids={ids}')

mostrar_resultados_mesas.short_description = "Mostrar resultados de Mesas seleccionadas"


class MesaAdmin(AdminRowActionsMixin, admin.ModelAdmin):
    actions = [resultados_oficiales]
    list_display = ('numero', 'lugar_votacion')
    list_filter = ('eleccion', TieneFiscal, TieneResultados, 'es_testigo', 'lugar_votacion__circuito__seccion', 'lugar_votacion__circuito')
    search_fields = (
        'numero', 'lugar_votacion__nombre', 'lugar_votacion__direccion',
        'lugar_votacion__ciudad', 'lugar_votacion__barrio',
    )

    def get_row_actions(self, obj):
        row_actions = [
            {
                'label': 'Escuela',
                'url': reverse('admin:elecciones_lugarvotacion_changelist') + f'?id={obj.lugar_votacion.id}',
                'enabled': True,
            },
            {
                'label': 'Resultados',
                'url': reverse('resultados-mapa') + f'?mesa={obj.id}',
                'enabled': obj.computados or obj.tiene_reporte,
            }
        ]
        if obj.asignacion_actual:
            url = reverse('admin:fiscales_asignacionfiscaldemesa_change', args=(obj.asignacion_actual.id,))
            label_asignacion = 'Editar asignación'

        else:
            url = reverse('admin:fiscales_asignacionfiscaldemesa_add') + f'?mesa={obj.id}'
            label_asignacion = 'Asignar fiscal'

        row_actions.append({
            'label': f'{label_asignacion}',
            'url': url,
            'enabled': True
        })

        row_actions += super().get_row_actions(obj)
        return row_actions



class PartidoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'nombre')
    list_display_links = list_display


class CircuitoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'seccion')
    list_display_links = list_display
    list_filter = ('seccion',)
    filter_horizontal = ('referentes',)
    search_fields = (
        'nombre', 'numero',
    )
    actions = ['asignar', resultados_oficiales]

    def asignar(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ids = ",".join(selected)
        url = reverse('asignar-referentes')
        return HttpResponseRedirect(f'{url}?ids={ids}')

    asignar.short_description = "Asignar referentes"

class SeccionAdmin(admin.ModelAdmin):
    actions = [resultados_oficiales]
    search_fields = (
        'nombre', 'numero',
    )


admin.site.register(Seccion, SeccionAdmin)
admin.site.register(Circuito, CircuitoAdmin)
admin.site.register(Partido, PartidoAdmin)
admin.site.register(LugarVotacion, LugarVotacionAdmin)
admin.site.register(Mesa, MesaAdmin)


for model in (Opcion, Eleccion, VotoMesaReportado):
    admin.site.register(model)


# Register your models here.
