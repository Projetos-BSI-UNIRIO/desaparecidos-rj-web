from django.db import models

# Create your models here.
class Pessoa(models.Model):
	SEXO = (
		("masculino", "Masculino"),
		("feminino", "Feminino"),
		("indeterminado", "Indeterminado")
	)

	COR_PELE = (
		("branca", "Branca"),
		("preta", "Preta"),
		("parda", "Parda"),
		("amarela", "Amarela"),
	)

	COR_OLHOS = (
		("castanhos", "Castanhos"),
		("azuis", "Azuis"),
		("verdes", "Verdes")
	)

	COR_CABELOS = (
		("preto", "Castanhos"),
		("loiro", "Loiros"),
		("ruivo", "Ruivos")
	)

	nome = models.CharField(max_length = 254, blank=True, null=True)
	idade = models.IntegerField(blank=True, null=True)
	altura = models.IntegerField(blank=True, null=True)
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
	possui_tatuagem = models.BooleanField(blank=True)
	possui_cicatriz = models.BooleanField(blank=True)
	possui_deficiencia = models.BooleanField(blank=True)
	sofreu_amputacao = models.BooleanField(blank=True)
	esta_desaparecido = models.BooleanField(default=True)
	tipo_fisico = models.CharField(max_length = 254, blank=True, null=True)

	rg = models.CharField(max_length = 9, blank=True, null=True)
	emissor_rg = models.CharField(max_length = 15, blank=True, null=True)
	cpf = models.CharField(max_length = 11, blank=True, null=True)
	cnh = models.CharField(max_length = 11, blank=True, null=True)

	#def __str__(self):
	#	return self.nome + " " + self.rg
