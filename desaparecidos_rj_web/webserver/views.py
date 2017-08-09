from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, localtime

from datetime import date, timedelta, datetime
import pytz
import calendar
import time

import os
import json

import face_recognition

from .models import *
from .forms import *	


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


# Create your views here.

@login_required
def index(request):
    return render(request, "index.html", {})

def userLogin(request):
    if request.method == "POST":
        login_form = LogInForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data["username"], password=login_form.cleaned_data["password"])
            if user and user.is_active:
                login(request, user)
                return redirect("index")
            else:
                return HttpResponse("Dados de autenticacao invalidos.")
        else:
            return HttpResponse("Dados de autenticacao invalidos.")
    else:
        return render(request, "login.html", {"form": LogInForm()})

@login_required
def userLogout(request):
    logout(request)
    return redirect("login")

@login_required
def desaparecidos(request):
    #form = BuscaPessoaForm()
    results = Pessoa.objects.all()
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
            return redirect("visualizarDesaparecido", pk = instance.pk)
    else:
        form = PessoaForm()
    return render(request, "cadastrar_pessoa_model_form.html", {
        "form": form
    })

@login_required
def editarDesaparecido(request, pk):
    if request.method == "POST":
        instance = Pessoa.objects.get(pk=pk)
        form = PessoaForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save()
            #result = getFaceEcoding(instance.foto)
            #if result["invalid_image"] == False:
            #    instance.facial_features = result["face_encoding"]
            #    instance.encoding_distance_to_zero = result["encoding_distance_to_zero"]
            #    instance.save()
            #else:
            #    return HttpResponse("Imagem invalida. Por favor, tente outra.")
            return redirect("editarDesaparecido", pk = instance.pk)
    else:
        instance = Pessoa.objects.get(pk=pk)
        form = PessoaForm(instance = instance)
    return render(request, "editar_pessoa_model_form.html", {
        "form": form,
    })

@login_required
def visualizarDesaparecido(request, pk):
    pessoa = Pessoa.objects.get(pk=pk)
    return render(request, "desaparecido.html", {"pessoa": pessoa})

@login_required
def removerDesaparecido(request, pk):
    pessoa = get_object_or_404(Pessoa, pk=pk)
    pessoa.delete()
    return redirect("desaparecidos")


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
            resultadoBusca = Pessoa.objects
            for atributo in atributos_esperados:
                if atributo in form.cleaned_data:
                    if form.cleaned_data[atributo] == "" or form.cleaned_data[atributo] is None:
                        continue
                    contador_de_parametros += 1
                    if atributo in atributos_numericos or atributo in atributos_booleanos:
                        kwargs = {'{0}'.format(atributo): form.cleaned_data[atributo]}
                        resultadoBusca = resultadoBusca.filter(**kwargs)
                    else:
                        kwargs = {'{0}__{1}'.format(atributo, 'icontains'): form.cleaned_data[atributo]}
                        resultadoBusca = resultadoBusca.filter(**kwargs)
            results = []

            if contador_de_parametros == 0:
                return HttpResponse("Por favor, informe algum valor para busca.")

            print(resultadoBusca.query)
            for resultado in resultadoBusca:
                results.append(resultado)
            return render(request, "resultados_desaparecido.html", {"form": form, "results": results})
        else:
            return HttpResponse("Formulario Invalido.")



    else:
        form = PessoaBuscaForm()
        return render(request, "busca_desaparecido.html", {"form": form})



def buscarDesaparecido(request):
    dadosBusca = request.GET.get("dados")
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
    resultadoBusca = Pessoa.objects
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
            kwargs = {'{0}__{1}'.format(atributo, 'icontains'): dadosBusca[atributo]}
            #print(kwargs)
            resultadoBusca = resultadoBusca.filter(**kwargs)
            #print(resultadoBusca.query)

    resultadoFinal = {
        "desaparecidos": []
    }

    if contador_de_parametros == 0:
        return HttpResponse(json.dumps(resultadoFinal))

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
    return HttpResponse(json.dumps(resultadoFinal))

@login_required
def usuarios(request):
    results = User.objects.all()
    return render(request, "usuarios.html", {
        #"form": form,
        "results": results,
    })

@login_required
def cadastrarUsuario(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            usuario.set_password(usuario.password) # to hash the password
            usuario.save()

            return redirect("visualizarUsuario", pk = usuario.pk)
    else:
        form = UserForm()
    return render(request, "cadastrar_usuario_model_form.html", {
        "form": form
    })

@login_required
def editarUsuario(request, pk):
    if request.method == "POST":
        instance = User.objects.get(pk=pk)
        form = UserForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
            return redirect("editarUsuario", pk = instance.pk)
    else:
        instance = User.objects.get(pk=pk)
        form = UserForm(instance = instance)
    return render(request, "editar_usuario_model_form.html", {
        "form": form,
    })

@login_required
def visualizarUsuario(request, pk):
    usuario = User.objects.get(pk=pk)
    return render(request, "usuario.html", {"usuario": usuario})

@login_required
def removerUsuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    usuario.delete()
    return redirect("usuarios")
