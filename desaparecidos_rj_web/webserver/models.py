from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pessoa(models.Model):
	FAIXA_IDADE = (
		("ate_18_anos", "Até 18 anos"),
		("de_19_ate_30_anos", "De 19 até 30 anos"),
		("de_31_ate_45_anos", "De 31 até 45 anos"),
		("de_46_ate_65_anos", "De 46 até 65 anos"),
		("acima_de_65_anos", "Acima de 65 anos"),
	)	

	FAIXA_ALTURA = (
		("anao", "Anão"),
		("ate_160", "Até 1,60 m"),
		("de_160_ate_170", "De 1,60 até 1,70 m"),
		("de_170_ate_180", "De 1,70 até 1,80 m"),
		("acima_de_180", "Acima de 1,80 m"),
	)

	SEXO = (
		("masculino", "Masculino"),
		("feminino", "Feminino"),
	)	

	COR_PELE = (
		("albino", "Albino"),
		("amarela", "Amarela"),
		("branca", "Branca"),
		("negra", "Negra"),
		("parda", "Parda"),
		("vermelha", "Vermelha"),
	)

	COR_OLHOS = (
		("azuis", "Azuis"),
		("castanhos_claros", "Castanhos Claros"),
		("castanhos_escuros", "Castanhos Escuros"),
		("cinzentos", "Cinzentos"),
		("castanhos", "Castanhos"),
		("desiguais_na_cor", "Desiguais na Cor"),
		("pretos", "Pretos"),
		("verdes", "Verdes"),
		("violetas", "Violetas"),
	)

	COR_CABELOS = (
		("aco", "Aço"),
		("branco", "Branco"),
		("castanho_claro", "Castanho Claro"),
		("castanho_escuro", "Castanho Escuro"),
		("com_mexas_ou_faixas", "Com Mexas ou Faixas"),
		("louro", "Louro"),
		("preto", "Preto"),
		("ruivo", "Ruivo")
	)

	TIPO_FISICO = (
		("magro", "Magro"),
		("normal", "Normal"),
		("gordo", "Gordo"),
		("forte", "Forte"),
	)

	nome = models.CharField(max_length = 254, blank=True, null=True)
	idade = models.IntegerField(blank=True, null=True)
	idade_aparente = models.CharField(max_length = 100, choices = FAIXA_IDADE, blank=True, null=True)
	altura = models.IntegerField(blank=True, null=True)
	faixa_altura = models.CharField(max_length = 100, choices = FAIXA_ALTURA, blank=True, null=True)
	cor_pele = models.CharField(max_length = 100, choices = COR_PELE, blank=True, null=True)
	cor_olhos = models.CharField(max_length = 100, choices = COR_OLHOS, blank=True, null=True)
	cor_cabelos = models.CharField(max_length = 100, choices = COR_CABELOS, blank=True, null=True)
	sexo = models.CharField(max_length = 100, choices = SEXO, blank=True, null=True)
	nome_pai = models.CharField(max_length = 254, blank=True, null=True)
	nome_mae = models.CharField(max_length = 254, blank=True, null=True)
	foto = models.ImageField(upload_to = "fotos/", blank = True, null = True)
	facial_encoding = models.TextField(blank = True, null = True)
	encoding_distance_to_zero = models.FloatField(blank = True, null = True)
	data_nascimento = models.DateTimeField(blank=True, null=True)
	data_desaparecimento = models.DateTimeField(blank=True, null=True)
	local_desaparecimento = models.CharField(max_length = 254, blank=True, null=True)
	cartazete = models.ImageField(upload_to = "cartazetes/",blank = True, null = True)
	nome_no_cartazete = models.CharField(max_length = 254, blank=True, null=True)
	comentario_desaparecimento = models.TextField(blank = True, null = True)
	possui_tatuagem = models.NullBooleanField(blank=True, null=True)
	possui_cicatriz = models.NullBooleanField(blank=True, null=True)
	possui_deficiencia = models.NullBooleanField(blank=True, null=True)
	sofreu_amputacao = models.NullBooleanField(blank=True, null=True)
	esta_desaparecido = models.NullBooleanField(default=True, null=True)
	tipo_fisico = models.CharField(max_length = 254, choices = TIPO_FISICO, blank=True, null=True)

	rg = models.CharField(max_length = 9, blank=True, null=True)
	emissor_rg = models.CharField(max_length = 15, blank=True, null=True)
	cpf = models.CharField(max_length = 11, blank=True, null=True)
	cnh = models.CharField(max_length = 11, blank=True, null=True)

	#def __str__(self):
	#	return self.nome + " " + self.rg
