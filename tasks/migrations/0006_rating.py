# Generated by Django 5.0.2 on 2024-06-26 15:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_otzyv_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(1, 'Нравится'), (-1, 'Не нравится')], verbose_name='Значение')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP Адрес')),
                ('otzyv', models.ForeignKey(help_text='Отзыв', on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='tasks.otzyv')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
