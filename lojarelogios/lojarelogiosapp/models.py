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

class Produto(models.Model):
    id_produto = models.AutoField(primary_key=True)
    # Posso acessar o carrinho tanto usando o carrinho.produto_set quanto com o produto.fk_carrinho
    fk_carrinho = models.ManyToManyField(Carrinho, editable=False)
    titulo = models.CharField(max_length=50)
    descricao = models.CharField(max_length=150)
    preco = models.FloatField(default=0.00)
    quantidade = models.IntegerField(default=1)

    # Imagens
    imagem_capa = models.FileField(upload_to="lojarelogiosapp/static/lojarelogiosapp/uploads/", null=True)
    imagem_2 = models.FileField(upload_to="lojarelogiosapp/static/lojarelogiosapp/uploads/", null=True)
    imagem_3 = models.FileField(upload_to="lojarelogiosapp/static/lojarelogiosapp/uploads/", null=True)

    def __str__(self):
        return self.titulo

# Essa model, basicamente gera um pedido baseado no retrato do carrinho ao clicarmos em 'comprar'. Ela se atualiza baseado no estado do pagamaento gerado pela API de Payment Gateway
class Pedido(models.Model):

    STATUS_OPTIONS = [
        ('pendente', 'pendente'),
        ('aceito', 'aceito'),
        ('despachado', 'despachado')
    ]

    id_pedido = models.AutoField(primary_key=True)
    fk_carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=False, default=timezone.now)
    telefone_1 = models.IntegerField()
    telefone_2 = models.IntegerField(null=True)
    endereco_entrega_1 = models.CharField(max_length=150)
    endereco_entrega_2 = models.CharField(max_length=150, null=True)
    status = models.CharField(choices=STATUS_OPTIONS, default=STATUS_OPTIONS[0][1], max_length=25)
    # Quando o produto estiver com status = 'despachado', o administrador insere um link com o código de despache nos correios
    link_rastreamento = models.CharField(max_length=999, null=True)

    def __str__(self):
        return self.id_pedido
