from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('importacoes', views.importacoes, name='imports'),
    path('importacoes/detalhes/<int:importacao_id>', views.detalha_transacoes, name='detalha_transacoes')
]