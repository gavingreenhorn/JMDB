# Generated by Django 2.2.16 on 2023-03-05 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth_yamdb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmationcode',
            name='username',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='code', to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]