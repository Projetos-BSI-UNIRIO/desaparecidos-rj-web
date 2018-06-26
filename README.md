# Aplicação Desaparecidos-RJ (Web)

## Introdução ##

O Sistema de Gerenciamento de Desaparecidos (nome provisório), idealizado no âmbito do projeto Desaparecidos-RJ (nome provisório), é um sistema sendo desenvolvido por um grupo de voluntários da Universidade Federal do Estado do Rio de Janeiro (UNIRIO) em colaboração com a Delegacia de Descoberta de Paradeiros (DDPA) da Polícia Civil do Estado do Rio de Janeiro.

Esse sistema é composto de duas aplicações, uma web e uma móvel, que, quando combinadas, permitem aos usuários do aplicativo móvel pesquisar por pessoas desaparecidas com base em dados de descrição física. Assim, através do uso dessa nova ferramenta, assistentes sociais, enfermeiras, policiais e outros agentes públicos terão uma chance de descobrirem mais facilmente a identidade de pessoas sem identificação, o que poderá colaborar para um aumento no número de casos de desaparecimento solucionados.

## Funcionamento ##

O sistema web, presente neste repositório, é desenvolvido em Python 3, utilizando o framework Django (versão 1.1). Apresenta opções para cadastro e busca de pessoas desaparecidas e usuários, provendo busca apenas para desaparecidos, que, assim, como no caso do aplicativo móvel, é baseada em características físicas. A principal função da aplicação web é permitir aos policiais e funcionários da DDPA cadastrar pessoas desaparecidas e manter e gerenciar esses dados.

O aplicativo móvel, por sua vez, é desenvolvido em Javascript/Typescript, utilizando o framework Ionic, o que permite que sejam suportadas as plataformas Android e iOS. É o componente que ficará nas mãos daqueles que lidam com pessoas sem identificação, ou seja, assistentes sociais, funcionários de serviços de saúde, policiais, dentre outros. 

A comunicação entre essas duas partes é feito através de uma API simples, constituída de um método, que permite ao aplicativo móvel efetuar buscas no webserver.

![planning_1_crop_small](https://user-images.githubusercontent.com/6119173/35132273-8b8ec8e4-fcb1-11e7-8910-70e5e126680e.png)

## Instalação ##

Para “executar” a aplicação web no Ubuntu Linux (16.04), basta instalar o Python 3 (já presente em algumas distribuições Linux) e a Dlib e suas dependências. Também é sugerida a instalação das dependências em um ambiente virtual. Assim, o passo-a-passo é executar no terminal:

    wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
    
    bash Miniconda2-latest-Linux-x86_64.sh
    
    conda create -n desaparecidosrjweb python=3.6
    
    source activate desaparecidosrjweb
    
    pip install django
    
    pip install unidecode
    
    # Esta linha demorará a ser concluída.
    pip install face_recognition

Para testar a aplicação fora de produção, basta executar, dentro do ambiente virtual, a seguinte linha e acessar, através de um navegador web, a URL “http://localhost:8000”:

    python manage.py runserver

Para servir a aplicação utilizando o Apache, um tutorial que pode ajudar é:

https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-14-04

## Informação Adicional ##

Software em desenvolvimento por equipe voluntária da Universidade Federal do Estado do Rio de Janeiro (UNIRIO), sob orientação das professoras Geiza M. H. Silva e Renata M. Araújo. 

Desenvolvido utilizando:
- Python 3.x
- Django 1.1
