# Generated by Django 5.1.5 on 2025-03-15 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_customer_password'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Admin',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Feedback',
        ),
        migrations.DeleteModel(
            name='Food',
        ),
        migrations.DeleteModel(
            name='Login',
        ),
        migrations.DeleteModel(
            name='Menu',
        ),
        migrations.DeleteModel(
            name='Offer',
        ),
        migrations.DeleteModel(
            name='Report',
        ),
        migrations.DeleteModel(
            name='Restaurant',
        ),
        migrations.DeleteModel(
            name='Sales',
        ),
    ]
