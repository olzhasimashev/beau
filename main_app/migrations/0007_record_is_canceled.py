# Generated by Django 3.2.4 on 2023-04-22 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_customer_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='is_canceled',
            field=models.BooleanField(default=False),
        ),
    ]
