from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Produto, Carrinho, Pedido
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views import generic
import braintree

# Create your views here.
def index_view(request):
    return render(request, 'lojarelogiosapp/index.html', {'user': request.user})

def privacy_view(request):
     return render(request, 'lojarelogiosapp/privacy.html')

def products_view(request):
    if request.user.is_authenticated:
         user = request.user

         carrinho = Carrinho.objects.get(fk_usuario=user.id)
         total = 0
         for produto in carrinho.produto_set.all():
              total += produto.preco

         context = {'produtos': Produto.objects.all(),
                     'carrinho': carrinho,
                     'total': total
                     }
         return render(request, 'lojarelogiosapp/products/index.html', context)

    else:
      return render(request, 'lojarelogiosapp/products/index.html', {'produtos': Produto.objects.all()})

def add_cart(request, id_produto):
      if request.user.is_authenticated:
            user = request.user

            product = Produto.objects.get(pk=id_produto)
            cart = Carrinho.objects.get(fk_usuario_id=request.user.id)

            # Numa relação many-to-many, aqui nós adicionamos os produtos ao clickarmos, no carrinho do user
            product.fk_carrinho.add(cart)

            carrinho = Carrinho.objects.get(fk_usuario=user.id)
            total = 0
            for produto in carrinho.produto_set.all():
                  total += produto.preco

            context = {'sucesso_msg': 'Produto adicionado ao carrinho com sucesso!', 
                       'produtos': Produto.objects.all(), 
                       'carrinho': Carrinho.objects.get(fk_usuario=user.id),
                       'total': total
                       }

            return render(request, 'lojarelogiosapp/products/index.html', context)
      else:
            return redirect('lojarelogiosapp:login')

def remove_cart(request, id_produto):
      if request.user.is_authenticated:
            user = request.user

            product = Produto.objects.get(pk=id_produto)
            cart = Carrinho.objects.get(fk_usuario_id=request.user.id)

            product.fk_carrinho.remove(cart)

            carrinho = Carrinho.objects.get(fk_usuario=user.id)
            total = 0
            for produto in carrinho.produto_set.all():
                  total += produto.preco

            context = {
                 'sucesso_msg': 'Produto removido do carrinho com sucesso!',
                  'produtos': Produto.objects.all(),
                  'carrinho': Carrinho.objects.get(fk_usuario=user.id),
                  'total': total
                  }

            return render(request, 'lojarelogiosapp/products/index.html', context)
      else:
            return redirect('lojarelogiosapp:login')

class DetailsView(generic.DetailView):
      # Envia como 'produto' para o template especificado
      model = Produto
      template_name = 'lojarelogiosapp/products/details.html'

      def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
             context = super().get_context_data(**kwargs)

             carrinho = Carrinho.objects.get(fk_usuario = self.request.user.id)
             context['carrinho'] = carrinho
             
             total = 0
             for produto in carrinho.produto_set.all():
                  total += produto.preco

             context['total'] = total
             return context
        else:
             context = super().get_context_data(**kwargs)
             return context

# Usuário
def index_user_view(request):
      if request.user.is_authenticated:
            user = request.user
            carrinho = Carrinho.objects.get(fk_usuario = user.id)
            context = {
                 'user': user,
                 'pedidos': Pedido.objects.filter(fk_carrinho = carrinho)
            }
            return render(request, 'lojarelogiosapp/user/index.html', context)
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

def payment_view(request):
     carrinho = Carrinho.objects.get(fk_usuario = request.user.id)

     total = 0
     for produto in carrinho.produto_set.all():
      total += produto.preco
      context = {
           'carrinho': carrinho,
           'total': total
           }
     return render(request, 'lojarelogiosapp/payment/index.html', context)

def checkout_view(request):
    
    user = request.user

    context = {}

    gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                braintree.Environment.Sandbox,
                merchant_id="wjn3nwnyk7jpdxbm",
                public_key="9br7xc3vm98kpfcj",
                private_key="8a106243762ffc29e20f7ee34f01155e"
            )
        )

    if request.method == 'GET':
         # Passando o client token pro front-end
         client_token = gateway.client_token.generate()

         context = {
              'client_token': client_token,
         }
         return render(request, 'lojarelogiosapp/payment/checkout.html', context)
     
    else:
         # Em caso de request 'POST' nós pegamos o carrinho do usuário e o total
         carrinho = Carrinho.objects.get(fk_usuario = request.user.id)

         total = 0
         for produto in carrinho.produto_set.all():
            total += produto.preco

            context = {
                 'carrinho': carrinho,
                 'total': total
            }

            # 1 - Aqui a gente primeiro procede com um pagamento
            # ...

            # 2 - Depois, nós instanciamos um novo pedido
            #fk_carrinho = carrinho
            #data_pedido = timezone.now()
            #cep = request.POST['cep']
            #telefone_1 = request.POST['telefone_1']
            #telefone_2 = request.POST['telefone_2']
            #endereco_entrega_1 = request.POST['endereco_entrega_1']
            #endereco_entrega_2 = request.POST['endereco_entrega_2']
            return render(request, 'lojarelogiosapp/payment/checkout.html')