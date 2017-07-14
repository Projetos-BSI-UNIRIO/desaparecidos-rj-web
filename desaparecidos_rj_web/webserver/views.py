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

def buscarDesaparecido(request):
    dadosBusca = request.GET.get("dados")
    if len(dadosBusca) == 0:
        return HttpResponse("JSON vazio ou mal formatado recebido.")

    atributos_esperados = [
        "nome", "idade", "altura", "cor_pele", "cor_olhos", "cor_cabelos", "sexo", 
        "nome_pai", "nome_mae", "data_nascimento", "data_desaparecimento", 
        "local_desaparecimento", "nome_no_cartazete", "comentario_desaparecimento",
        "possui_tatuagem", "possui_cicatriz", "possui_deficiencia", "sofreu_amputacao", "tipo_fisico"
    ]

    atributos_numericos = ["idade", "altura"]
    atributos_booleanos = ["possui_tatuagem", "possui_cicatriz", "possui_deficiencia", "sofreu_amputacao"]

    dadosBusca = json.loads(dadosBusca)
    resultadoBusca = Pessoa.objects
    for atributo in dadosBusca:
        #print(atributo)
        if atributo not in atributos_esperados:
            return HttpResponse("Parametro invalido encontrado.")
        if dadosBusca[atributo] == "":
            continue
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
    for resultado in resultadoBusca:
        um_desaparecido = {
            "nome": resultado.nome, 
            "idade": resultado.idade, 
            "altura": resultado.altura, 
            "cor_pele": resultado.cor_pele, 
            "cor_olhos": resultado.cor_olhos, 
            "cor_cabelos": resultado.cor_cabelos, 
            "sexo": resultado.sexo, 
            "nome_pai": resultado.nome_pai, 
            "nome_mae": resultado.nome_mae, 
            "data_nascimento": resultado.data_nascimento, 
            "data_desaparecimento": resultado.data_desaparecimento, 
            "local_desaparecimento": resultado.local_desaparecimento, 
            "nome_no_cartazete": resultado.nome_no_cartazete, 
            "comentario_desaparecimento": resultado.comentario_desaparecimento,
            "possui_tatuagem": resultado.possui_tatuagem, 
            "possui_cicatriz": resultado.possui_cicatriz, 
            "possui_deficiencia": resultado.possui_deficiencia, 
            "sofreu_amputacao": resultado.sofreu_amputacao, 
            "tipo_fisico": resultado.tipo_fisico
        }

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
