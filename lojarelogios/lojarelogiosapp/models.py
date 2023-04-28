from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Carrinho(models.Model):
    id_carrinho = models.AutoField(primary_key=True)
    fk_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField(null=True)
    frete = models.FloatField(null=True, default=0.00)

    def __str__(self):
        return "Carrinho do usuário " + str(self.fk_usuario)

# Essa model, basicamente gera um pedido baseado no retrato do carrinho ao clicarmos em 'comprar'. Ela se atualiza baseado no estado do pagamaento gerado pela API de Payment Gateway
class Pedido(models.Model):

    STATUS_OPTIONS = [
        ('pendente', 'pendente'),
        ('aceito', 'aceito'),
        ('despachado', 'despachado')
    ]
    # Esse aqui é o ID encontrado na página de pedidos do stripe
    id_pedido = models.AutoField(primary_key=True)
    fk_carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, editable=False)
    nome = models.CharField(max_length=50, null=True)
    sobrenome = models.CharField(max_length=50, null=True)
    total = models.FloatField(default=0.00)
    data_pedido = models.DateTimeField(auto_now_add=False, default=timezone.now)
    telefone_1 = models.CharField(max_length=25, null=True)
    telefone_2 = models.CharField(max_length=25, null=True)
    estado = models.CharField(max_length=25, null=True)
    cidade = models.CharField(max_length=50, null=True)
    bairro = models.CharField(max_length=150, null=True)
    rua = models.CharField(max_length=150, null=True)
    numero_rua = models.CharField(max_length=150, null=True)
    complemento = models.CharField(null=True, max_length=150)
    cep = models.CharField(max_length=20, null=True)
    status = models.CharField(choices=STATUS_OPTIONS, default=STATUS_OPTIONS[0][1], max_length=25)
    # Quando o produto estiver com status = 'despachado', o administrador insere um link com o código de despache nos correios
    link_rastreamento = models.URLField(null=True)

    def __str__(self):
        return str(self.id_pedido)


# Esta model deve ser cadastrado antes no stripe, depois na página de admin
class Produto(models.Model):
    id_produto = models.AutoField(primary_key=True)
    # Posso acessar o carrinho tanto usando o carrinho.produto_set quanto com o produto.fk_carrinho
    fk_carrinho = models.ManyToManyField(Carrinho, editable=False)
    fk_pedido = models.ManyToManyField(Pedido, editable=False)
    titulo = models.CharField(max_length=25)
    descricao = models.CharField(max_length=150)
    preco = models.FloatField(default=0.00)
    quantidade = models.IntegerField(default=1)

    # Imagens
    imagem_capa = models.FileField(upload_to="lojarelogiosapp/static/lojarelogiosapp/uploads/", null=True)
    imagem_2 = models.FileField(upload_to="lojarelogiosapp/static/lojarelogiosapp/uploads/", null=True)
    imagem_3 = models.FileField(upload_to="lojarelogiosapp/static/lojarelogiosapp/uploads/", null=True)

    # stripe_id é o id do objeto de preço do produto no stripe. O produto primeiro é cadastrado no stripe, depois cadastrado no banco de dados do site
    # Só com o stripe isso aqi
    # stripe_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.titulo
    
class password_token(models.Model):
    id_token = models.SlugField(max_length=50, primary_key=True)
    data_cr = models.DateTimeField(auto_now_add=False, default=timezone.now)

    # Trocando display name na admin page
    class Meta:
        verbose_name = "Token de senha"
        verbose_name_plural = "Tokens de senha"

    def __str__(self):
        return str(self.id_token)
