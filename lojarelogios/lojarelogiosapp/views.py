from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Produto
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect

# Create your views here.
def index_view(request):
    return render(request, 'lojarelogiosapp/index.html', {'user': request.user})

def products_view(request):
    return render(request, 'lojarelogiosapp/products/index.html', {'produtos': Produto.objects.all()})

def details_view(request, id_produto):
      return render(request, 'lojarelogiosapp/products/details.html')

# Usuário
def index_user_view(request):
      if request.user.is_authenticated:
            return render(request, 'lojarelogiosapp/user/index.html', {'user': request.user})
      else:
            return HttpResponseRedirect(reverse('lojarelogiosapp:login'))

def register_view(request):
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
                     return render(request, 'lojarelogiosapp/user/register.html', {'erro_msg': 'Nome de usuário já cadastrado!'})

    return render(request, 'lojarelogiosapp/user/register.html')

def login_view(request):

    if request.method == 'POST':
          usuario = request.POST['usuario']
          senha = request.POST['senha']
          
          user = authenticate(request, username=usuario, password=senha)

          if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('lojarelogiosapp:products'))
          else:
                erro_msg = "Usuário e/ou senha incorretos!"
                return render(request, 'lojarelogiosapp/user/login.html', {'erro_msg': erro_msg})

    return render(request, 'lojarelogiosapp/user/login.html')

def logout_view(request):
    logout(request)
    return redirect('lojarelogiosapp:products')
