from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'login/$', views.userLogin, name='login'),
    url(r'logout/$', views.userLogout, name='logout'),
    url(r'loginmobile/$', views.userLoginMobile, name='loginMobile'),

    url(r'desaparecidos/$', views.desaparecidos, name='desaparecidos'),
    url(r'desaparecidos/cadastrar/$', views.cadastrarDesaparecido, name='cadastrarDesaparecido'),
    url(r'desaparecidos/editar/(?P<pk>\d+)/$', views.editarDesaparecido, name='editarDesaparecido'),
    url(r'desaparecidos/visualizar/(?P<pk>\d+)/$', views.visualizarDesaparecido, name='visualizarDesaparecido'),
    url(r'desaparecidos/remover/(?P<pk>\d+)/$', views.removerDesaparecido, name='removerDesaparecido'),
    url(r'desaparecidos/buscarDesaparecido/$', views.buscarDesaparecido, name='buscarDesaparecido'),
    url(r'desaparecidos/buscarDesaparecidoWeb/$', views.buscarDesaparecidoWeb, name='buscarDesaparecidoWeb'),
    url(r'desaparecidos/getFaceEcoding/$', views.getFaceEcoding, name='getFaceEcoding'),
    url(r'desaparecidos/gerarCartaz/(?P<pk>\d+)/$', views.gerarCartaz, name='gerarCartaz'),
    url(r'desaparecidos/editarNomeCartazete/(?P<request>[^/]+)/(?P<pk>\d+)/$', views.editarNomeCartazete, name='editarNomeCartazete'),

    url(r'usuarios/$', views.usuarios, name='usuarios'),
    url(r'usuarios/cadastrar/$', views.cadastrarUsuario, name='cadastrarUsuario'),
    url(r'usuarios/editar/(?P<pk>\d+)/$', views.editarUsuario, name='editarUsuario'),
    url(r'usuarios/visualizar/(?P<pk>\d+)/$', views.visualizarUsuario, name='visualizarUsuario'),
    url(r'usuarios/remover/(?P<pk>\d+)/$', views.removerUsuario, name='removerUsuario'),
]
