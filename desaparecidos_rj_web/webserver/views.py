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
            result = getFaceEcoding(instance.foto)
            if result["invalid_image"] == False:
                instance.facial_encoding = result["face_encoding"]
                instance.encoding_distance_to_zero = result["encoding_distance_to_zero"]
                instance.save()
            else:
                instance.delete()
                return HttpResponse("Imagem invalida. Por favor, tente outra.")
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
            result = getFaceEcoding(instance.foto)
            if result["invalid_image"] == False:
                instance.facial_features = result["face_encoding"]
                instance.encoding_distance_to_zero = result["encoding_distance_to_zero"]
                instance.save()
            else:
                return HttpResponse("Imagem invalida. Por favor, tente outra.")
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
    return render(request, "index.html", {"pessoa": pessoa})

@login_required
def removerDesaparecido(request, pk):
    pessoa = get_object_or_404(Pessoa, pk=pk)
    pessoa.delete()
    return redirect("desaparecidos")

@login_required
def usuarios(request):
    pass

@login_required
def cadastrarUsuario(request):
    pass

@login_required
def editarUsuario(request, pk):
    pass

@login_required
def visualizarUsuario(request, pk):
    pass

@login_required
def removerUsuario(request, pk):
    pass
