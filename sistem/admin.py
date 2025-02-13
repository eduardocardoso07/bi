from django.contrib import admin
from .models import Usuario, Relatorios, Acesso, Coordenador, UsuarioRelatorios

class CoordenadorFilter(admin.SimpleListFilter):
    title = 'Coordenador'
    parameter_name = 'coordenador'

    def lookups(self, request, model_admin):
        coordenadores = Coordenador.objects.all()
        return [(coordenador.id, coordenador.nome) for coordenador in coordenadores]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(coordenador__id=self.value())
        return queryset

class UsuarioRelatoriosInline(admin.TabularInline):
    model = UsuarioRelatorios
    extra = 1

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'acesso', 'last_login', 'coordenador')
    fields = ('usuario', 'senha', 'acesso', 'onedrive_link', 'last_login', 'coordenador')
    list_filter = (CoordenadorFilter,)
    inlines = [UsuarioRelatoriosInline]

class RelatorioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'link', 'display_usuarios')

    def display_usuarios(self, obj):
        return ", ".join([usuario.usuario for usuario in obj.usuarios_relacionados.all()])  # Atualizado related_name
    display_usuarios.short_description = 'Usuários'

class AcessoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_hora', 'ip_address', 'get_coordenador')
    readonly_fields = ('data_hora', 'ip_address')
    list_filter = ('usuario__coordenador',)

    def get_coordenador(self, obj):
        return obj.usuario.coordenador
    get_coordenador.short_description = 'Coordenador'

class CoordenadorAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Relatorios, RelatorioAdmin)
admin.site.register(Acesso, AcessoAdmin)
admin.site.register(Coordenador, CoordenadorAdmin)
admin.site.register(UsuarioRelatorios)
