# Generated by Django 4.1.7 on 2023-04-12 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lojarelogiosapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='id_pedido',
            field=models.CharField(max_length=400, primary_key=True, serialize=False),
        ),
    ]
