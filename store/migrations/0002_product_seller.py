# Generated by Django 5.0.3 on 2024-04-01 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='seller',
            field=models.CharField(max_length=200, null=True),
        ),
    ]