# Generated by Django 4.2.23 on 2025-06-27 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_comment_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('subscriber', 'target')},
            },
        ),
        migrations.AddField(
            model_name='petuser',
            name='subscriptions',
            field=models.ManyToManyField(related_name='subscribers', through='core.Subscription', to=settings.AUTH_USER_MODEL, verbose_name='Подписки'),
        ),
    ]
