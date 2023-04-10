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
from django.views import View
import stripe
from django.conf import settings
from django.http import JsonResponse

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
    
    # 1 - Colhendo dados de formulário
    user = request.user
    
    carrinho = Carrinho.objects.get(fk_usuario = request.user.id)
    total = 0
    for produto in carrinho.produto_set.all():
      total += produto.preco
      
      # 2.1 - Colhendo os dados relevantes ao pagamento
      payment_method = request.POST['payment_method']
      card_name = request.POST['card-name']
      card_number = request.POST['card-number']
      expiration = request.POST['expiration']
      cvv = request.POST['cvv']

      # 2.2 - Colhendo os dados relevantes ao pedido
      fk_carrinho = carrinho
      data_pedido = timezone.now()
      cep = request.POST['cep']
      telefone_1 = request.POST['telefone_1']
      telefone_2 = request.POST['telefone_2']
      endereco_entrega_1 = request.POST['endereco_entrega_1']
      endereco_entrega_2 = request.POST['endereco_entrega_2']

      # 3 - Instanciando um pedido
      # ...

      # 4 - Stripe e pagamento
      stripe.api_key = settings.STRIPE_SECRET_KEY

      domain = "http://localhost:8000/lojarelogiosapp"
      
      if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
            checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': 'price_1MvTqtKY6ADNgA35HYRCtT87',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=domain + '/payment/success',
            cancel_url=domain + '/payment/cancel',
        )
      context = {
            'carrinho': carrinho,
            'total': total,
            'checkout_id': checkout_session.id,
            }
      return redirect(checkout_session.url)
    
def success_view(request):
     return render(request, 'lojarelogiosapp/payment/success.html')

def cancel_view(request):
     return render(request, 'lojarelogiosapp/payment/cancel.html')