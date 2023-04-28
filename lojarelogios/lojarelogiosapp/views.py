import json
import time
from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import Produto, Carrinho, Pedido, password_token
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views import View
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template import loader
from uuid import uuid4
import requests
from datetime import datetime

# SDK do Mercado Pago
import mercadopago
# Adicione as credenciais
sdk = mercadopago.SDK("TEST-6033284383326765-042517-f71f881b0fdb00736ff2f02a4c8360ac-472353305")

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

            # Pegando só os 5 primeiro pedidos
            pedidos_recentes = pedidos.order_by("-data_pedido")[0:4]

            context = {
                 'user': user,
                 'pedidos': pedidos_recentes,
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
    
    if request.user.is_authenticated:
         return redirect('lojarelogiosapp:index_user')

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

'''
def payment_view(request):
     carrinho = Carrinho.objects.get(fk_usuario = request.user.id)

     total = 0
     for produto in carrinho.produto_set.all():
      total += produto.preco

      context = {
           'carrinho': carrinho,
           'total': total
           }
     return render(request, 'lojarelogiosapp/payment/index.html', context)'''

# Varíavel global para armazenar a checkout_session
session = object
msg = ''

def shipment_view(request):
     if request.method == "POST":
          carrinho = Carrinho.objects.get(fk_usuario = request.user.id)

          total = 0
          for produto in carrinho.produto_set.all():
               total += produto.preco

          context = {
               'total': total,
               'carrinho': carrinho
          }
     
          return render(request, 'lojarelogiosapp/payment/shipment.html', context)
     return HttpResponseNotFound()

def checkout_view(request):
    carrinho = Carrinho.objects.get(fk_usuario = request.user.id)
    produtos_comprados = []

    # Primeiro a gente verifica se todos os produtos no carrinho estão disponíveis
    for produto in carrinho.produto_set.all():
         if produto.quantidade >= 1:
            pass
         else:
            user = request.user

            old_total = 0

            for produto in carrinho.produto_set.all():
                  old_total += produto.preco
                  # Removendo os produtos indisponíveis
                  produto.fk_carrinho.remove(carrinho)

            context = {'erro_msg': 'Produto indisponível. Tente mais tarde!', 
                       'produtos': Produto.objects.all(), 
                       'carrinho': carrinho,
                       'total': old_total,
                       'available': check_available(request, Produto.objects.all())                       
                       }

            return render(request, 'lojarelogiosapp/products/index.html', context)
            
    if request.method == 'POST':
         line_items_list = []
         total = 0

         for produto in carrinho.produto_set.all():
            total += produto.preco
            line_items_list.append({
                 'title': produto.titulo,
                 'quantity': 1,
                 'unit_price': produto.preco,
                 'picture_url': produto.imagem_capa.url
            })

            '''line_items_list.append({
                 'price': produto.stripe_id,
                 'quantity': 1,
                 })'''
         # print(line_items_list)
         # Stripe e pagamento
         stripe.api_key = settings.STRIPE_SECRET_KEY
         domain = "http://localhost:8000/lojarelogiosapp"
         
         '''if settings.DEBUG:
                 domain = "http://127.0.0.1:8000/lojarelogiosapp"
                 checkout_session = stripe.checkout.Session.create(
                      payment_method_types=['card', 'boleto'],
                      line_items=line_items_list,
                      mode='payment',
                      success_url=domain + '/payment/success',
                      cancel_url=domain + '/payment/cancel',
                      #billing_address_collection ='required',
                      phone_number_collection = {"enabled": True},
                      shipping_address_collection = {'allowed_countries': ['BR']},
                      )'''
         # Alterando a session com a checkout_session        
         global session
         #session = checkout_session

         url = "https://api.mercadopago.com/checkout/preferences?access_token={}".format("TEST-6033284383326765-042517-f71f881b0fdb00736ff2f02a4c8360ac-472353305")

         # Cria um item na preferência
         preference_data = {
               "items": line_items_list,
               "back_urls": {
                    'success': domain + '/payment/success',
                    'pending': domain + '/payment/success',
                    'failure': domain + '/payment/cancel', 
               },
               "shipments": {
                    "receiver_address": {
                         "zip_code": request.POST['cep'],
                         "street_name": request.POST['rua'],
                         "city_name": request.POST['cidade'],
                         "state_name": request.POST['estado'],
                         "street_number": request.POST['numero_rua'],
                         "apartment": request.POST['numero_casa'],
                         "floor": request.POST['complemento']
                    }
               }
               }
         
         response = requests.post(url, json = preference_data)
         parsed_res = json.loads(response.text)

         session = preference_data
          
         '''if response:
              print(parsed_res['id'])
         else:
              print('Response Failed! ' + str(response.text))
              print(line_items_list)'''
         
         # Dados de usuário
         user = request.user
         nome = request.POST['nome']
         sobrenome = request.POST['sobrenome']
         # Colhendo os dados relevantes ao pedido
         # id_pedido = checkout_session.id
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
         numero_casa = request.POST['numero_casa']

         # Instanciando um pedido
         new_pedido = Pedido.objects.create(
               id_pedido = parsed_res['id'],
               fk_carrinho=fk_carrinho,
               nome=nome,
               sobrenome=sobrenome,
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
               numero_casa=numero_casa,
               complemento=complemento
              )
         
         context = {
              'pref_id': parsed_res['id'],
              'carrinho': carrinho,
              'total': total,
              'address': new_pedido
              }
         
         for produto in carrinho.produto_set.all():
          new_pedido.produto_set.add(produto)
          produtos_comprados.append(produto.titulo)

          # Por fim, envie um email ao administrador com os dados do pedido e com a url para acompanhar situação do pagamento no stripe
          global msg
          msg = str(f"Um novo pedido foi feito pelo usuário {user.username} de nome {nome} {sobrenome}, com o ID de usuário {user.id}.\n\n Dados do pedido: \n\n - ID do pedido: {parsed_res['id']}\n - Email: {user.email}\n - Data: {data_pedido}\n - Total: {total}\n - Produtos comprados: {produtos_comprados} \n\n\nTelefones de contato:\n\n - Telefone 1: {telefone_1}\n - Telefone 2: {telefone_2}\n \n\nEndereço de entrega:\n\n - Estado: {estado}\n - Cidade: {cidade}\n - Bairro: {bairro}\n - Rua: {rua}\n - Número da rua: {numero_rua}\n - Número da casa: {numero_casa} \n - Complemento: {complemento}. \n\n\nLembre-se, você pode ver os dados do pedido pesquisando na sua página do mercado pago, através do ID do pedido, apenas acessando sua página de pedidos ou transações do mercado pago, ou através da aba de pedidos da administração da sua loja virtual!")

         # return redirect(checkout_session.url)
         # Passando o template com o pref_id da response
         return render(request, 'lojarelogiosapp/payment/checkout.html', context)
    else:
          return HttpResponseNotFound()

def success_view(request):
     carrinho = Carrinho.objects.get(fk_usuario = request.user.id)

     # Só salva o pedido no BD, se der certo a transação
     # npedido.save()

     # Reduzindo a quantidade de produtos no banco de dados e adicionando os produtos do carrinho no pedido
     for produto in carrinho.produto_set.all():
          current_product = Produto.objects.get(pk=produto.id_produto)
          current_product.quantidade -= 1
          current_product.save()

     # Limpando o carrinho pós compra
     for produto in carrinho.produto_set.all():
          # 1 - Pego o produto
          current_product = Produto.objects.get(pk = produto.id_produto)
          # 2 - Removo a instância
          current_product.fk_carrinho.remove(carrinho)
      
     local_msg = msg
     send_mail(
          "NOVO PEDIDO NA LOJA VIRTUAL!",
          local_msg,
          "rafaelngoncalves5@outlook.com",
          ["rafaelngoncalves5@outlook.com"],
          fail_silently=False,
          )

     return render(request, 'lojarelogiosapp/payment/success.html')

def cancel_view(request):
     #pedido = Pedido.objects.get(pk = session.id)
     #pedido.delete()
     
     return render(request, 'lojarelogiosapp/payment/cancel.html')

user_mail = ''

# Método que troca senha
def switch_password(request):
     # Antes de qualquer coisa: remova TODOS os tokens antigos
     if password_token:
          for token in password_token.objects.all():
               token.delete()

     if request.user.is_authenticated:
           logout(request)
     if request.method == 'POST':
          user_email = request.POST['email']

          # Checando se existe esse email, no BD
          if User.objects.filter(email = user_email).exists():
               try:
                    # Vou intanciar um token novo que vai ser um slug
                    rand_token = uuid4()
                    new_token = password_token.objects.create(id_token=rand_token)
                    # Depois eu verifico se existe o token e se sim, eu dou acesso à url de troca (confirm-pass) e redireciono
                    current_token = get_object_or_404(password_token, pk=new_token.id_token)
                    
                    link = f"Este token é válido por 5 minutos! \nhttp://localhost:8000/lojarelogiosapp/user/switch-pass/{current_token.id_token}/confirm-pass"
                    send_mail(
                         "Link para troca de senha",
                         link,
                         "rafaelngoncalves5@outlook.com",
                         ["rafaelngoncalves5@outlook.com"],
                         fail_silently=False,
                         )
                    
                    success_msg = 'Favor verificar email para troca de senhas enviado para {}!'.format(user_email)
                    
                    global user_mail
                    user_mail = user_email

                    # Retorno uma msg de sucesso!
                    return render(request, 'lojarelogiosapp/user/switch-pass.html', {'success_msg': success_msg})

               except (KeyError, password_token.DoesNotExist):
                    erro_msg = 'Ops, algo de errado ocorreu, por favor, entre em contato com a administração!'
                    return render(request, 'lojarelogiosapp/user/switch-pass.html', {'erro_msg': erro_msg})
 
          else:
               erro_msg = 'Email não cadastrado no site!'
               return render(request, 'lojarelogiosapp/user/switch-pass.html', {'erro_msg': erro_msg})
      
     return render(request, 'lojarelogiosapp/user/switch-pass.html')

def confirm_pass(request, pk):
      try:
           pk_token = get_object_or_404(password_token, pk=pk)
           user = User.objects.get(email=user_mail)
           if request.method == 'POST':
                # Altera a senha antiga, com a nova:
                senha = request.POST['senha']
                user.set_password(senha)
                user.save()
                
                # Eu excluo o token, para que não haja reutilização
                current_token = password_token.objects.get(pk=pk_token.id_token)
                current_token.delete()
                success_msg = "Senha trocada com sucesso!"
                return render(request, 'lojarelogiosapp/user/login.html', {'success_msg': success_msg})

      except(KeyError, password_token.DoesNotExist):
           erro_msg = 'Ops, algo de errado ocorreu, por favor, entre em contato com a administração!'
           return render(request, 'lojarelogiosapp/user/switch-pass.html', {'erro_msg': erro_msg})

      return render(request, 'lojarelogiosapp/user/confirm-pass.html', {'pk': pk})