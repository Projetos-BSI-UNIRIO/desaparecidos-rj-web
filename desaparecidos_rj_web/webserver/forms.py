from django import forms

from .models import *


class LogInForm(forms.Form):
	username = forms.CharField(label='Usuario', max_length=100, required=True)
	password = forms.CharField(widget=forms.PasswordInput(), label='Senha', required=True)

class PessoaForm(forms.ModelForm):
	class Meta:
		model = Pessoa
		fields = [
			"nome", "idade", "altura", "cor_pele", "cor_olhos", "cor_cabelos", "sexo", 
			"nome_pai", "nome_mae", "foto", "data_nascimento", "data_desaparecimento", 
			"local_desaparecimento", "cartazete", "nome_no_cartazete", "comentario_desaparecimento",
			"possui_tatuagem", "possui_cicatriz", "possui_deficiencia", "sofreu_amputacao", "tipo_fisico"
		]
