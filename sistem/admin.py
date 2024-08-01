# admin.py
from django.contrib import admin
from .models import Usuario, Relatorio, Acesso

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'acesso', 'last_login')
    fields = ('usuario', 'senha', 'acesso', 'relatorios', 'onedrive_link', 'last_login')

class RelatorioAdmin(admin.ModelAdmin):
    list_display = ('relatorio', 'link', 'display_usuarios')

    def display_usuarios(self, obj):
         return ", ".join([usuario.usuario for usuario in obj.usuarios.all()])
    display_usuarios.short_description = 'Usuários'

class AcessoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_hora', 'ip_address')
    readonly_fields = ('data_hora', 'ip_address')

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Relatorio, RelatorioAdmin)
admin.site.register(Acesso, AcessoAdmin)
