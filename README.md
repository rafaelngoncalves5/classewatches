# Loja de Relógios

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![SASS](https://img.shields.io/badge/SASS-hotpink.svg?style=for-the-badge&logo=SASS&logoColor=white)

<br />

![banner](https://github.com/rafaelngoncalves5/classewatches/assets/62622905/65dc882e-1010-4aed-a1fd-fe371c266e32)

## Introdução

Projeto do tipo E-Commerce, fortemente centralizado na página de administração do **Django**

## Gateway de pagamento

O pagamento é mediado utilizando o checkout pro do **mercado pago**

![mercadopago](https://github.com/rafaelngoncalves5/classewatches/assets/62622905/0095ed46-92b9-4e8b-89a5-88ff721e3bf7)


Foram feitos testes usando a SDK pra Python do [stripe](https://stripe.com/docs) também:

![stripe](https://github.com/rafaelngoncalves5/classewatches/assets/62622905/86486b37-b318-45a7-a226-fd8b4714d2cd)

## Hospedagem

A hospedagem do projeto foi feita na **Heroku**

usando o [Whitenoise](https://whitenoise.readthedocs.io/) para fazer o gerenciamento de arquivos estáticos, em um Dyno básico com um add-on para utilização com **PostgreSQL** da **Amazon AWS**

![deploy](https://github.com/rafaelngoncalves5/classewatches/assets/62622905/e244191c-1987-4166-90d1-623429395c10)

<br />

__Para rodar o app, é necessário rodarmos o collectstatic toda vez que alterarmos arquivos estáticos__

## Documentação

### A documentação completa encontra-se na pasta [docs](https://github.com/rafaelngoncalves5/loja-relogios/tree/master/docs)

- O projeto utilizou a técnica de prototipagem no estilo **wireframes**, os quais foram feitos com o uso do [figma](https://www.figma.com/). O protótipo no figma pode ser encontrado nesse [link](https://www.figma.com/file/x50yDDgJO1vNL9x0uMe7ZK/E-commerce?node-id=0-1&t=FXz16bZ9s8brMhMe-0)

### As models foram baseadas no seguinte diagrama:

<br />

![DER](https://github.com/rafaelngoncalves5/classewatches/assets/62622905/c5f9bad4-506e-41cb-9507-e0694f94acf1)

Feito com ajuda do [diagrams.net](https://www.diagrams.net/)

### O projeto seguiu os seguintes Requisitos Funcionais:

<br />

![RFs](https://github.com/rafaelngoncalves5/classewatches/assets/62622905/a93cc58a-32ce-4378-9328-aa282367f89e)

Os requisitos foram trabalhados aqui no GitHub, e podem ser encontrados nas abas [projects](https://github.com/rafaelngoncalves5/loja-relogios/projects?query=is%3Aopen) e [issues](https://github.com/rafaelngoncalves5/loja-relogios/issues)
