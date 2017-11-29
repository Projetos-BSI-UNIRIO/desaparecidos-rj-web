from django import forms

from .models import *


class LogInForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label='Senha', required=True)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        labels = {
            "username": "Usuário", 
            "email": "E-mail",
            "password": "Senha"
        }

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = [
            "nome", "idade_aparente", "faixa_altura", "cor_pele", "cor_olhos", "cor_cabelos", "sexo", 
            "nome_pai", "nome_mae", "foto", "data_nascimento", "data_desaparecimento", 
            "local_desaparecimento", "cartazete", "nome_no_cartazete", "comentario_desaparecimento",
            "possui_tatuagem", "possui_cicatriz", "possui_deficiencia", "sofreu_amputacao", "tipo_fisico"
        ]
        labels = {
            "nome": "Nome", 
            "idade_aparente": "Idade Aparente",
            "faixa_altura": "Faixa Altura", 
            "cor_pele": "Cor da Pele", 
            "cor_olhos": "Cor dos Olhos", 
            "cor_cabelos": "Cor do Cabelo", 
            "sexo": "Sexo", 
            "nome_pai": "Nome do Pai", 
            "nome_mae": "Nome da Mãe", 
            "possui_tatuagem": "Possui Tatuagem?", 
            "possui_cicatriz": "Possui Cicatriz?", 
            "possui_deficiencia": "Possui Deficiencia?", 
            "sofreu_amputacao": "Sofreu Amputacao?", 
            "tipo_fisico": "Tipo Fisico",
            "data_desaparecimento": "Data de Desaparecimento", 
            "local_desaparecimento": "Local de Desaparecimento",
            "comentario_desaparecimento": "Comentário sobre o desaparecimento"
        }

class PessoaBuscaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = [
            "nome", "idade_aparente", "faixa_altura", "cor_pele", "cor_olhos", "cor_cabelos", "sexo",
            "nome_pai", "nome_mae", "possui_tatuagem", "possui_cicatriz", "possui_deficiencia", 
            "sofreu_amputacao", "tipo_fisico"
        ]
        labels = {
            "nome": "Nome", 
            "idade_aparente": "Idade Aparente",
            "faixa_altura": "Faixa Altura", 
            "cor_pele": "Cor da Pele", 
            "cor_olhos": "Cor dos Olhos", 
            "cor_cabelos": "Cor do Cabelo", 
            "sexo": "Sexo", 
            "nome_pai": "Nome do Pai", 
            "nome_mae": "Nome da Mãe", 
            "possui_tatuagem": "Possui Tatuagem?", 
            "possui_cicatriz": "Possui Cicatriz?", 
            "possui_deficiencia": "Possui Deficiencia?", 
            "sofreu_amputacao": "Sofreu Amputacao?", 
            "tipo_fisico": "Tipo Fisico"
        }
