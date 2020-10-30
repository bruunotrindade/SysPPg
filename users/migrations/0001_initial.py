# Generated by Django 3.0.8 on 2020-10-30 05:41

from django.db import migrations, models
import users.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cpf', models.CharField(error_messages={'unique': 'Já existe um usuário com este CPF'}, max_length=15, unique=True, verbose_name='CPF')),
                ('email', models.EmailField(error_messages={'unique': 'Já existe um usuário com este email'}, max_length=254, unique=True, verbose_name='Email')),
                ('full_name', models.CharField(max_length=255, verbose_name='Nome Completo')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Membro da Equipe')),
                ('is_active', models.BooleanField(default=True, help_text='Desative para tirar o acesso do usuário', verbose_name='Ativo')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
            managers=[
                ('objects', users.managers.UserManager()),
            ],
        ),
    ]