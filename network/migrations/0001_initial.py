# Generated by Django 5.0.3 on 2024-03-15 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=128, verbose_name='название продукта')),
                ('model', models.CharField(max_length=128, verbose_name='модель')),
                ('release_date', models.DateField(verbose_name='дата выхода на рынок')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='NetworkObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_type', models.CharField(choices=[('factory', 'завод'), ('retail', 'розничная сеть'), ('entrepreneur', 'ИП')], max_length=12, verbose_name='тип объекта')),
                ('name', models.CharField(max_length=128, verbose_name='название')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('country', models.CharField(max_length=128, verbose_name='страна')),
                ('city', models.CharField(max_length=128, verbose_name='город')),
                ('street', models.CharField(max_length=128, verbose_name='улица')),
                ('bld', models.CharField(max_length=10, verbose_name='номер дома')),
                ('debt', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='задолженность перед поставщиком')),
                ('hierarchy', models.IntegerField(verbose_name='уровень иерархии')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='network.networkobject')),
                ('products', models.ManyToManyField(to='network.product')),
            ],
            options={
                'verbose_name': 'объект сети',
                'verbose_name_plural': 'объекты сети',
                'ordering': ('id',),
            },
        ),
    ]
