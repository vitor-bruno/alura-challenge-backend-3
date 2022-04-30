from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('importacoes', views.importacoes, name='imports'),
    path('usuarios', views.usuarios, name='usuarios'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('deletar/<int:usuario_id>', views.deleta_usuario, name='deleta_usuario'),
    path('editar/<int:usuario_id>', views.edita_usuario, name='edita_usuario'),
    path('atualizar_usuario', views.atualiza_usuario, name='atualiza_usuario')
]