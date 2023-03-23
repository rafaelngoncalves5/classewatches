from datetime import timezone
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Produto
from django.contrib.auth.models import User
from django.contrib.auth import logout

# Create your views here.
def index(request):
    return render(request, 'lojarelogiosapp/index.html')

def products(request):
    return render(request, 'lojarelogiosapp/products.html', {'produtos': Produto.objects.all()})

# Usuário
def register(request):
    if request.method == 'POST':
              primeiro_nome = request.POST['primeiro_nome']
              ultimo_nome = request.POST['ultimo_nome']
              usuario = request.POST['usuario']
              email = request.POST['email']
              senha = request.POST['senha']

              try:
                     new_user = User.objects.create_user(f"{usuario}", f"{email}", f"{senha}")
                     new_user.first_name = primeiro_nome
                     new_user.last_name = ultimo_nome
                     new_user.date_joined = timezone.now()
                     #new_user.get_username
                     new_user.save()
                     return redirect(reverse('lojarelogiosapp:index'))


              except IntegrityError:
                     # Tratar isso aqui na fase de testes
                     return render(request, 'lojarelogiosapp/user/register.html', {'erro_msg': 'Erro de integridade, tente de novo com um usuário e/ou email diferente(s)!'})

    return render(request, 'lojarelogiosapp/user/register.html')

def login(request):
    return render(request, 'lojarelogiosapp/user/login.html')

def logout(request):
    return render(request, 'lojarelogiosapp/user/register.html')
