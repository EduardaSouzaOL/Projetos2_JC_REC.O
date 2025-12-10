from django.contrib import admin
from .models import Perfil, Interesse, AssinanteNewsletter

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cidade', 'estado', 'data_nascimento')
    search_fields = ('usuario__username', 'usuario__email', 'cidade')

@admin.register(Interesse)
class InteresseAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(AssinanteNewsletter)
class AssinanteNewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at')
    search_fields = ('email',)
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('unsubscribe_token', 'created_at')
    list_per_page = 50
    actions = ['marcar_como_ativo', 'marcar_como_inativo']

    def marcar_como_ativo(self, request, queryset):
        queryset.update(is_active=True)
    marcar_como_ativo.short_description = "Marcar selecionados como Ativos"

    def marcar_como_inativo(self, request, queryset):
        queryset.update(is_active=False)
    marcar_como_inativo.short_description = "Marcar selecionados como Inativos"