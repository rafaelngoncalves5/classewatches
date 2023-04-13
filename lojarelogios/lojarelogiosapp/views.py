import time
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
from django.core.mail import send_mail
from django.template import loader

# Create your views here.
def check_available(request, produtos):
     total = 0
     for produto in produtos:
      total += produto.quantidade

     if total <= 0:
      return False
     else:
      return True     

def index_view(request):
    return render(request, 'lojarelogiosapp/index.html', {'user': request.user})

def privacy_view(request):
     return render(request, 'lojarelogiosapp/privacy.html')

def products_view(request):
    if request.user.is_authenticated:
         user = request.user

         produtos = Produto.objects.all()
            
         carrinho = Carrinho.objects.get(fk_usuario=user.id)
         total = 0
         for produto in carrinho.produto_set.all():
              total += produto.preco

         context = {'produtos': produtos,
                     'carrinho': carrinho,
                     'total': total,
                     'available': check_available(request, produtos)
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
                       'total': total,
                       'available': check_available(request, Produto.objects.all())
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
                  'total': total,
                  'available': check_available(request, Produto.objects.all())
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
            pedidos = Pedido.objects.filter(fk_carrinho = carrinho)
            
            # Boa área para adicionar WEBHOOKS do stripe
            # ...

            context = {
                 'user': user,
                 'pedidos': pedidos,
                 #'primeiro_produto': primeiro_produto,
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
    carrinho = Carrinho.objects.get(fk_usuario = request.user.id)
    
    # Primeiro a gente verifica se todos os produtos no carrinho estão disponíveis
    for produto in carrinho.produto_set.all():
         if produto.quantidade >= 1:
            pass
         else:
            user = request.user

            total = 0

            for produto in carrinho.produto_set.all():
                  total += produto.preco
                  # Removendo os produtos indisponíveis
                  produto.fk_carrinho.remove(carrinho)

            context = {'erro_msg': 'Produto indisponível. Tente mais tarde!', 
                       'produtos': Produto.objects.all(), 
                       'carrinho': carrinho,
                       'total': total,
                        'available': check_available(request, Produto.objects.all())                       
                       }

            return render(request, 'lojarelogiosapp/products/index.html', context)
            
    try:
         line_items_list = []
         total = 0
         for produto in carrinho.produto_set.all():
            line_items_list.append({
                 'price': produto.stripe_id,
                 'quantity': 1,
                 }),
            total += produto.preco
            
            # Stripe e pagamento
            stripe.api_key = settings.STRIPE_SECRET_KEY
            domain = "http://localhost:8000/lojarelogiosapp"
            
            if settings.DEBUG:
                 domain = "http://127.0.0.1:8000/lojarelogiosapp"
                 checkout_session = stripe.checkout.Session.create(
                      payment_method_types=['card'],
                      line_items=line_items_list,
                      mode='payment',
                      success_url=domain + '/payment/success',
                      cancel_url=domain + '/payment/cancel',
                      )
                 
            # Dados de usuário
            user = request.user
            nome = request.POST['nome']
            sobrenome = request.POST['sobrenome']
            
            # Colhendo os dados relevantes ao pedido
            id_pedido = checkout_session.id
            fk_carrinho = carrinho
            data_pedido = timezone.now()
            telefone_1 = request.POST['telefone_1']
            telefone_2 = request.POST['telefone_2']
            estado = request.POST['estado']
            cidade = request.POST['cidade']
            bairro = request.POST['bairro']
            rua = request.POST['rua']
            numero_rua = request.POST['numero_rua']
            complemento = request.POST['complemento']
            cep = request.POST['cep']
            
            # Instanciando um pedido
            new_pedido = Pedido.objects.create(
                 id_pedido=id_pedido,
                 fk_carrinho=fk_carrinho,
                 total=total,
                 data_pedido=data_pedido, 
                 telefone_1=telefone_1,
                 telefone_2=telefone_2,
                 cep=cep,
                 estado=estado,
                 cidade=cidade,
                 bairro=bairro,
                 rua=rua,
                 numero_rua=numero_rua,
                 complemento=complemento
                 )
            
            # Reduzindo a quantidade de produtos no banco de dados e adicionando os produtos do carrinho no pedido
            for produto in carrinho.produto_set.all():
                 new_pedido.produto_set.add(produto)
                 
                 current_product = Produto.objects.get(pk=produto.id_produto)
                 current_product.quantidade -= 1
                 current_product.save()
                 
            produtos_comprados = []
                 
            for produto in carrinho.produto_set.all():
                  produtos_comprados.append(produto.titulo)
                      
                  # Por fim, envie um email ao administrador com os dados do pedido e com a url para acompanhar situação do pagamento no stripe
                  msg = f"Um novo pedido foi feito pelo usuário {user.username} de nome {nome} {sobrenome}, com o ID {user.id}.\n\n\n Dados do pedido: \n\n - ID do pedido: {checkout_session.stripe_id}\n - Email: {user.email}\n - Data: {data_pedido}\n - Status: {checkout_session.status}\n - Total: {total} {checkout_session.currency}\n - Produtos comprados: {produtos_comprados} \n\n\nTelefones de contato:\n\n - Telefone 1: {telefone_1}\n - Telefone 2: {telefone_2}\n \n\nEndereço de entrega:\n\n - Estado: {estado}\n - Cidade: {cidade}\n - Bairro: {bairro}\n - Rua: {rua}\n - Número da rua: {numero_rua}\n - Complemento: {complemento}. \n\n\nLembre-se, você pode ver os dados do pedido pesquisando na sua página do stripe, através do ID do pedido, apenas acessando sua página de pedidos do stripe, ou através da aba de pedidos da administração da sua loja virtual!"
                      
                  send_mail(
                        "NOVO PEDIDO NA LOJA VIRTUAL!",
                        msg,
                        "rafaelngoncalves5@outlook.com",
                        ["rafaelngoncalves5@outlook.com"],
                        fail_silently=False,
                        )
                      
                  # Limpando o carrinho pós compra
                  for produto in carrinho.produto_set.all():
                        # 1 - Pego o produto
                        current_product = Produto.objects.get(pk = produto.id_produto)
                        # 2 - Removo a instância
                        current_product.fk_carrinho.remove(carrinho)
                                 
            return redirect(checkout_session.url)
    except:
         pass
    
def success_view(request):     
     return render(request, 'lojarelogiosapp/payment/success.html')

def cancel_view(request):
     return render(request, 'lojarelogiosapp/payment/cancel.html')