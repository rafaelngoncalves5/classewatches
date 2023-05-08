# Generated by Django 4.1.7 on 2023-05-08 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id_carrinho', models.AutoField(primary_key=True, serialize=False)),
                ('total', models.FloatField(null=True)),
                ('frete', models.FloatField(default=0.0, null=True)),
                ('fk_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='password_token',
            fields=[
                ('id_token', models.SlugField(primary_key=True, serialize=False)),
                ('data_cr', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Token de senha',
                'verbose_name_plural': 'Tokens de senha',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id_pedido', models.CharField(max_length=900, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=50, null=True)),
                ('sobrenome', models.CharField(max_length=50, null=True)),
                ('total', models.FloatField(default=0.0)),
                ('data_pedido', models.DateTimeField(default=django.utils.timezone.now)),
                ('telefone_1', models.CharField(max_length=25, null=True)),
                ('telefone_2', models.CharField(max_length=25, null=True)),
                ('estado', models.CharField(max_length=25, null=True)),
                ('cidade', models.CharField(max_length=50, null=True)),
                ('bairro', models.CharField(max_length=150, null=True)),
                ('rua', models.CharField(max_length=150, null=True)),
                ('numero_rua', models.CharField(max_length=150, null=True)),
                ('numero_casa', models.CharField(max_length=150, null=True)),
                ('complemento', models.CharField(max_length=150, null=True)),
                ('cep', models.CharField(max_length=20, null=True)),
                ('status', models.CharField(choices=[('pendente', 'pendente'), ('aceito', 'aceito'), ('despachado', 'despachado')], default='pendente', max_length=25)),
                ('link_rastreamento', models.URLField(null=True)),
                ('fk_carrinho', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='lojarelogiosapp.carrinho')),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id_produto', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=25)),
                ('descricao', models.CharField(max_length=150)),
                ('preco', models.FloatField(default=0.0)),
                ('quantidade', models.IntegerField(default=1)),
                ('imagem_capa', models.FileField(null=True, upload_to='lojarelogiosapp/static/lojarelogiosapp/uploads/')),
                ('imagem_2', models.FileField(null=True, upload_to='lojarelogiosapp/static/lojarelogiosapp/uploads/')),
                ('imagem_3', models.FileField(null=True, upload_to='lojarelogiosapp/static/lojarelogiosapp/uploads/')),
                ('fk_carrinho', models.ManyToManyField(editable=False, to='lojarelogiosapp.carrinho')),
                ('fk_pedido', models.ManyToManyField(editable=False, to='lojarelogiosapp.pedido')),
            ],
        ),
    ]
