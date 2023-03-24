from django.db import models

# Create your models here.
class Produto(models.Model):
    id_produto = models.AutoField(primary_key=True)
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
    
