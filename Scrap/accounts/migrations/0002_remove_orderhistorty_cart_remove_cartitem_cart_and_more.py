# Generated by Django 5.1.2 on 2024-12-12 11:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vehicle', '0002_brand_name_en'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderhistorty',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='customersellershistorty',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='customersellershistorty',
            name='sellers',
        ),
        migrations.RemoveField(
            model_name='orderhistorty',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='product',
            name='car',
        ),
        migrations.RemoveField(
            model_name='product',
            name='seller',
        ),
        migrations.AddField(
            model_name='profilecustomer',
            name='registration_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profileseller',
            name='brands',
            field=models.ManyToManyField(to='Vehicle.brand'),
        ),
        migrations.AddField(
            model_name='profileseller',
            name='registration_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
        migrations.DeleteModel(
            name='CustomerSellersHistorty',
        ),
        migrations.DeleteModel(
            name='OrderHistorty',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]