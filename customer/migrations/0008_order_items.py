# Generated by Django 5.1.5 on 2025-03-15 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_order_cus_id'),
        ('restaurant', '0004_alter_restaurant_rest_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='orders', to='restaurant.food'),
        ),
    ]
