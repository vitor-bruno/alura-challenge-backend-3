from django.contrib import admin
from transactions.models import Transacao, Arquivo

class Arquivos(admin.ModelAdmin):
    list_display = ('id', 'arquivo','data_upload', 'data_transacoes', 'usuario')
    list_display_links = ('id', 'arquivo')
    search_fields = ('arquivo',)
    list_per_page = 20

admin.site.register(Arquivo, Arquivos)