# Generated by Django 4.1.7 on 2023-04-18 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lojarelogiosapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='bairro',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='cidade',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='numero_rua',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='rua',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='telefone_1',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='telefone_2',
            field=models.CharField(max_length=25, null=True),
        ),
    ]