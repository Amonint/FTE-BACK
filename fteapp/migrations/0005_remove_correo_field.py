# Generated by Django 5.2.1 on 2025-06-16 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fteapp', '0004_rename_correo_usuario_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
