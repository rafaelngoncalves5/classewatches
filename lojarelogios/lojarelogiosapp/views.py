from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Produto, Carrinho
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views import generic

# Create your views here.
def index_view(request):
    return render(request, 'lojarelogiosapp/index.html', {'user': request.user})

def products_view(request):
    if request.user.is_authenticated:
         user = request.user
         return render(request, 'lojarelogiosapp/products/index.html', {'produtos': Produto.objects.all(), 'carrinho': Carrinho.objects.get(fk_usuario=user.id)})

    else:
      return render(request, 'lojarelogiosapp/products/index.html', {'produtos': Produto.objects.all()})

class DetailsView(generic.DetailView):
      # Envia como 'produto' para o template especificado
      model = Produto
      template_name = 'lojarelogiosapp/products/details.html'

def add_cart(request, id_produto):
      if request.user.is_authenticated:
            user = request.user

            product = Produto.objects.get(pk=id_produto)
            cart = Carrinho.objects.get(fk_usuario_id=request.user.id)

            # Numa relação many-to-many, aqui nós adicionamos os produtos ao clickarmos, no carrinho do user
            product.fk_carrinho.add(cart)

            return render(request, 'lojarelogiosapp/products/index.html', {'sucesso_msg': 'Produto adicionado ao carrinho com sucesso!', 'produtos': Produto.objects.all(), 'carrinho': Carrinho.objects.get(fk_usuario=user.id)})
      else:
            return redirect('lojarelogiosapp:login')

def remove_cart(request, id_produto):
      if request.user.is_authenticated:
            user = request.user

            product = Produto.objects.get(pk=id_produto)
            cart = Carrinho.objects.get(fk_usuario_id=request.user.id)

            product.fk_carrinho.remove(cart)

            return render(request, 'lojarelogiosapp/products/index.html', {'sucesso_msg': 'Produto removido do carrinho com sucesso!', 'produtos': Produto.objects.all(), 'carrinho': Carrinho.objects.get(fk_usuario=user.id)})
      else:
            return redirect('lojarelogiosapp:login')

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

              if User.objects.filter(email = email).exists():
                  return render(request, 'lojarelogiosapp/user/register.html', {'erro_msg': 'Endereço de email já cadastrado!'})

              try:
                  new_user = User.objects.create_user(f"{usuario}", f"{email}", f"{senha}")
                  new_user.first_name = primeiro_nome
                  new_user.last_name = ultimo_nome
                  new_user.date_joined = timezone.now()
                  new_user.save()

                  # Agora nós criamos um carrinho para esse usuário:
                  new_cart = Carrinho.objects.create(fk_usuario=new_user)
                  new_cart.save()
                  return render(request, 'lojarelogiosapp/index.html', {'sucesso_msg': "Usuário cadastrado com sucesso!"})
              
              except IntegrityError:
                  return render(request, 'lojarelogiosapp/user/register.html', {'erro_msg': 'Nome de usuário já cadastrado!'})
              

    return render(request, 'lojarelogiosapp/user/register.html')

def delete_user_view(request):
      current_user = request.user
      db_user = User.objects.get(id = current_user.id)
      db_user.delete()
      return redirect('lojarelogiosapp:index')

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