from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
#from django.conf import settings    # nao importar diretamente
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, localtime
from django.views.decorators.csrf import csrf_exempt

from ipware import get_client_ip

from datetime import date, timedelta, datetime
import pytz
import calendar
import time
import logging
import os
import json

import face_recognition # lembrar de instalar

import unidecode # lembrar de instalar
import string

from .models import *
from .forms import *


# Logger
logger = logging.getLogger(__name__)


def getFaceEcoding(image):
    print(image.name)
    if image.name is None:
        return {
            "invalid_image": True
        }
    print(os.path.join(settings.MEDIA_ROOT, image.name))
    source_image = face_recognition.load_image_file(os.path.join(settings.MEDIA_ROOT, image.name))
    print(len(source_image))
    if len(source_image) < 1:
        return {
            "invalid_image": True
        }
    else:
        encodings = face_recognition.face_encodings(source_image)
        if len(encodings) is 1:
            return {
                "invalid_image": False,
                "face_encoding": str(encodings[0].tolist()).replace(" ", "").replace("[", "").replace("]", ""),
                "encoding_distance_to_zero": 0
            }
        else:
            return {
                "invalid_image": True
            }


def normalizarNome(nome):
    nome_normalizado = unidecode.unidecode(nome).lower().replace(" ", "") # remove acentos e cedilha, colocar tudo em lower case e remove espacos
    for character in string.punctuation:
        nome_normalizado = nome_normalizado.replace(character, "") # remove pontuacoes, como apostrofos, tracos e etc.
    return nome_normalizado

def gerarNomesNormalizados(): # metodo para apeas gerar o nome normalizado para pessoas já cadastradas no momento da introducao desse conceito
    pessoas = Pessoa.objects.all()
    for pessoa in pessoas:
        pessoa.nome_normalizado = normalizarNome(pessoa.nome)
        pessoa.save()

# Adiciona IP do request ao fim de mensagens a serem utilizadas como log.
# Uso: logger.info(adicionarIp("Mensagem", request))
def adicionarIp(mensagem, request):
    client_ip = get_client_ip(request)
    ip_str = "[%s] " % (str(client_ip[0]) if client_ip is not None else "IP Desconhecido")
    return ip_str + mensagem

# Create your views here.

@login_required
def index(request):
    return render(request, "index.html", {})

def userLogin(request):
    if request.method == "POST":
        login_form = LogInForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data["username"], password=login_form.cleaned_data["password"])
            print(request)
            if user and user.is_active:
                login(request, user)

                logger.info(adicionarIp("Usuário %s autenticado." % (str(user.pk)), request))
                return redirect("index")
            else:
                logger.warning(adicionarIp("Tentativa de autenticação com dados inválidos (combinação inexistente ou usuário inativo).", request))
                return HttpResponse("Dados de autenticação inválidos.")
        else:
            logger.info(adicionarIp("Tentativa de autenticação com formulário inválido.", request))
            return HttpResponse("Dados de autenticação inválidos.")
    else:
        #logger.info(adicionarIp("Tentativa de autenticação por método HTTP inválido (%s). Redirecionando para página de log-in." % (request.method), request))
        return render(request, "login.html", {"form": LogInForm()})

@csrf_exempt
def userLoginMobile(request):
    if request.method == "POST":  
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        print(request.POST.get('username'))
        if user and user.is_active:
                login(request, user)

                #logger.info(adicionarIp("Usuário %s autenticado." % (str(user.pk)), request))
                return HttpResponse(status=200)
        else:
            #logger.warning(adicionarIp("Tentativa de autenticação com dados inválidos (combinação inexistente ou usuário inativo).", request))
            return HttpResponse(status=301)
    else:
        #logger.warning(adicionarIp("Tentativa de autenticação por método HTTP inválido (%s)." % (request.method), request))
        return HttpResponse(status=302)

@login_required
def userLogout(request):
    logger.info(adicionarIp("Usuário %s encerrou sua sessão." % (str(request.user.pk)), request))

    logout(request)

    return redirect("login")

@login_required
def desaparecidos(request):
    #form = BuscaPessoaForm()
    results = Pessoa.actives.all()
    return render(request, "desaparecidos.html", {
        #"form": form,
        "results": results,
    })

@login_required
def cadastrarDesaparecido(request):
    if request.method == "POST":
        form = PessoaForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.nome_normalizado = normalizarNome(instance.nome)
            print(instance.nome_normalizado)
            instance.save()
            #print(type(instance.photo))
            #print(instance.photo.name)
            #result = getFaceEcoding(instance.foto)
            #if result["invalid_image"] == False:
            #    instance.facial_encoding = result["face_encoding"]
            #    instance.encoding_distance_to_zero = result["encoding_distance_to_zero"]
            #    instance.save()
            #else:
            #    instance.delete()
            #    return HttpResponse("Imagem invalida. Por favor, tente outra.")

            logger.info(adicionarIp("Desaparecido %s cadastrado pelo usuário %s." % (str(instance.pk), str(request.user.pk)), request))

            return redirect("visualizarDesaparecido", pk = instance.pk)
    else:
        form = PessoaForm()
    return render(request, "cadastrar_pessoa_model_form.html", {
        "form": form
    })

@login_required
def editarDesaparecido(request, pk):
    if request.method == "POST":
        instance = Pessoa.actives.get(pk=pk)
        form = PessoaForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save()
            instance.nome_normalizado = normalizarNome(instance.nome)
            print(instance.nome_normalizado)
            instance.save()
            #result = getFaceEcoding(instance.foto)
            #if result["invalid_image"] == False:
            #    instance.facial_features = result["face_encoding"]
            #    instance.encoding_distance_to_zero = result["encoding_distance_to_zero"]
            #    instance.save()
            #else:
            #    return HttpResponse("Imagem invalida. Por favor, tente outra.")

            logger.info(adicionarIp("Desaparecido %s editado pelo usuário %s." % (str(instance.pk), str(request.user.pk)), request))

            return redirect("editarDesaparecido", pk = instance.pk)
    else:
        instance = Pessoa.actives.get(pk=pk)
        form = PessoaForm(instance = instance)
    return render(request, "editar_pessoa_model_form.html", {
        "form": form,
    })

@login_required
def visualizarDesaparecido(request, pk):
    pessoa = Pessoa.actives.get(pk=pk)

    logger.info(adicionarIp("Desaparecido %s visualizado pelo usuário %s." % (str(pessoa.pk), str(request.user.pk)), request))

    return render(request, "desaparecido.html", {"pessoa": pessoa})

@login_required
def removerDesaparecido(request, pk):
    pessoa = get_object_or_404(Pessoa, pk=pk)
    pessoa.is_active=False
    pessoa.save()

    logger.info(adicionarIp("Desaparecido %s removido/desativado pelo usuário %s." % (str(pessoa.pk), str(request.user.pk)), request))

    return redirect("desaparecidos")

@login_required
def buscarDesaparecidoWeb(request):
    if request.method == "POST":
        atributos_esperados = [
            "nome", "idade_aparente", "faixa_altura", "cor_pele", "cor_olhos", "cor_cabelos", "sexo",
            "nome_pai", "nome_mae", "possui_tatuagem", "possui_cicatriz", "possui_deficiencia",
            "sofreu_amputacao", "tipo_fisico"
        ]
        atributos_numericos = ["idade", "altura"]
        atributos_booleanos = ["possui_tatuagem", "possui_cicatriz", "possui_deficiencia", "sofreu_amputacao"]

        form = PessoaBuscaForm(request.POST)

        if form.is_valid():
            contador_de_parametros = 0
            resultadoBusca = Pessoa.actives
            for atributo in atributos_esperados:
                if atributo in form.cleaned_data:
                    if form.cleaned_data[atributo] == "" or form.cleaned_data[atributo] is None:
                        continue
                    contador_de_parametros += 1
                    if atributo in atributos_numericos or atributo in atributos_booleanos:
                        kwargs = {'{0}'.format(atributo): form.cleaned_data[atributo]}
                        resultadoBusca = resultadoBusca.filter(**kwargs)
                    else:
                        if atributo == "nome":
                            atributo = "nome_normalizado"
                            form.cleaned_data[atributo] = normalizarNome(form.cleaned_data["nome"])
                            print(form.cleaned_data[atributo])
                        kwargs = {'{0}__{1}'.format(atributo, 'icontains'): form.cleaned_data[atributo]}
                        resultadoBusca = resultadoBusca.filter(**kwargs)
            results = []


            logger.info(adicionarIp("Busca por desaparecido realizada pelo usuário %s com os parâmetros: %s" % (str(request.user.pk), str(form.cleaned_data)), request))

            if contador_de_parametros == 0:
                return render(request, "erro_busca.html", {})
                #return HttpResponse("Por favor, informe algum valor para busca.")

            print(resultadoBusca.query)
            for resultado in resultadoBusca:
                results.append(resultado)
            return render(request, "resultados_desaparecido.html", {"form": form, "results": results})
        else:
            return HttpResponse("Formulario Invalido.")



    else:
        form = PessoaBuscaForm()
        return render(request, "busca_desaparecido.html", {"form": form})



@csrf_exempt
def buscarDesaparecido(request):
    dadosBusca = request.POST.get("dados")
    if len(dadosBusca) == 0:
        return HttpResponse("JSON vazio ou mal formatado recebido.")

    atributos_esperados = [
        "nome", "idade_aparente", "faixa_altura", "cor_pele", "cor_olhos", "cor_cabelos", "sexo",
        "nome_pai", "nome_mae", "possui_tatuagem", "possui_cicatriz", "possui_deficiencia",
        "sofreu_amputacao", "tipo_fisico"
    ]

    atributos_numericos = ["idade", "altura"]
    atributos_booleanos = ["possui_tatuagem", "possui_cicatriz", "possui_deficiencia", "sofreu_amputacao"]

    dadosBusca = json.loads(dadosBusca)
    contador_de_parametros = 0
    resultadoBusca = Pessoa.actives
    for atributo in dadosBusca:
        #print(atributo)
        if atributo not in atributos_esperados:
            return HttpResponse("Parametro invalido encontrado.")
        if dadosBusca[atributo] == "":
            continue
        contador_de_parametros += 1
        if atributo in atributos_numericos or atributo in atributos_booleanos:
            kwargs = {'{0}'.format(atributo): dadosBusca[atributo]}
            #print(kwargs)
            resultadoBusca = resultadoBusca.filter(**kwargs)
            #print(resultadoBusca.query)
        else:
            valor_a_ser_buscado = dadosBusca[atributo]
            if atributo == "nome":
                atributo = "nome_normalizado"
                valor_a_ser_buscado = normalizarNome(dadosBusca["nome"])
                print(valor_a_ser_buscado)
            kwargs = {'{0}__{1}'.format(atributo, 'icontains'): valor_a_ser_buscado}
            #print(kwargs)
            resultadoBusca = resultadoBusca.filter(**kwargs)
            #print(resultadoBusca.query)

    resultadoFinal = {
        "desaparecidos": []
    }

    if contador_de_parametros == 0:
        response = HttpResponse(json.dumps(resultadoFinal))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
        return response

    for resultado in resultadoBusca:
        um_desaparecido = {
            "nome": resultado.nome,
            "idade": resultado.idade,
            "idade_aparente": resultado.idade_aparente,
            "altura": resultado.altura,
            "faixa_altura": resultado.faixa_altura,
            "cor_pele": resultado.cor_pele,
            "cor_olhos": resultado.cor_olhos,
            "cor_cabelos": resultado.cor_cabelos,
            "sexo": resultado.sexo,
            "nome_pai": resultado.nome_pai,
            "nome_mae": resultado.nome_mae,
            "data_nascimento": str(resultado.data_nascimento),
            "data_desaparecimento": str(resultado.data_desaparecimento),
            "local_desaparecimento": resultado.local_desaparecimento,
            "nome_no_cartazete": resultado.nome_no_cartazete,
            #"comentario_desaparecimento": resultado.comentario_desaparecimento,
            "possui_tatuagem": resultado.possui_tatuagem,
            "possui_cicatriz": resultado.possui_cicatriz,
            "possui_deficiencia": resultado.possui_deficiencia,
            "sofreu_amputacao": resultado.sofreu_amputacao,
            "tipo_fisico": resultado.tipo_fisico,
            "foto": resultado.foto.url if resultado.foto.name else "",
            "cartazete": resultado.cartazete.url if resultado.cartazete.name else ""
        }

        """if resultado.foto.name:
            um_desaparecido["foto"] = resultado.foto.url
        if resultado.cartazete.name:
            um_desaparecido["cartazete"] = resultado.cartazete.url"""

        resultadoFinal["desaparecidos"].append(um_desaparecido)

    response = HttpResponse(json.dumps(resultadoFinal))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"

    print(request.META)
    print("\n-----\n")
    print(response.has_header("Access-Control-Allow-Origin"))

    #return HttpResponse(json.dumps(resultadoFinal))
    return response

@login_required
def usuarios(request):
    results = Usuario.actives.all()
    return render(request, "usuarios.html", {
        #"form": form,
        "results": results,
    })

def cadastrarUsuario(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            usuario.set_password(usuario.password) # to hash the password
            usuario.save()

            logger.info(adicionarIp("Usuário %s cadastrado pelo usuário %s." % (str(usuario.pk), str(request.user.pk)), request))

            return redirect("visualizarUsuario", pk = usuario.pk)
    else:
        form = UserForm()
    return render(request, "cadastrar_usuario_model_form.html", {
        "form": form
    })

@login_required
def editarUsuario(request, pk):
    if request.method == "POST":
        usuario = User.objects.get(pk=pk)
        form = UserForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save()
            usuario.set_password(usuario.password)
            usuario.save()

            logger.info(adicionarIp("Usuário %s editado pelo usuário %s." % (str(usuario.pk), str(request.user.pk)), request))

            return redirect("editarUsuario", pk = usuario.pk)
    else:
        usuario = Usuario.actives.get(pk=pk)
        form = UserForm(instance = usuario)
    return render(request, "editar_usuario_model_form.html", {
        "form": form,
    })

@login_required
def visualizarUsuario(request, pk):
    usuario = Usuario.actives.get(pk=pk)

    logger.info(adicionarIp("Usuário %s visualizado pelo usuário %s." % (str(usuario.pk), str(request.user.pk)), request))

    return render(request, "usuario.html", {"usuario": usuario})

@login_required
def removerUsuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    usuario.is_active = False
    usuario.save()

    logger.info(adicionarIp("Usuário %s removido/desativado pelo usuário %s." % (str(usuario.pk), str(request.user.pk)), request))

    return redirect("usuarios")
