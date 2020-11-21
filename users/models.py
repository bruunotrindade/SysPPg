from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from datetime import datetime
from .managers import UserManager
from base.models import BaseModel, UndergraduateCourse
from django.utils.translation import gettext as _

MARITAL_STATUS = (
    ('S', 'Solteiro(a)'),
    ('C', 'Casado(a)'),
    ('D', 'Divorciado(a)'),
    ('V', 'Viúvo(a)')
)

SEX = (
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outro')
)

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    cpf = models.CharField(
        _('CPF'),
        unique=True,
        error_messages={'unique': _("Já existe um usuário com este CPF")},
        max_length=15
    )
    email = models.EmailField(
        _('Email'),
        unique=True,
        error_messages={'unique': _("Já existe um usuário com este email")},
    )
    full_name = models.CharField(_('Nome Completo'), max_length=255)
    address = models.CharField(_('Endereço Residencial'), max_length=90, null=True)
    phone_number = models.CharField(_('Telefone'), max_length=20, null=True)
    marital_status = models.CharField(_('Estado Civil'), max_length=1, choices=MARITAL_STATUS, null=True)
    sex = models.CharField(_('Sexo'), max_length=1, choices=SEX, null=True)
    date_of_birth = models.DateField(_('Data de nascimento'), null=True)
    is_staff = models.BooleanField(_('Membro da Equipe'), default=False)
    is_active = models.BooleanField(
        _('Ativo'), default=True, help_text=_('Desative para tirar o acesso do usuário')
    )

    objects = UserManager()

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['full_name', 'email']

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')

    def __str__(self):
        return f'{self.email} {self.full_name[:30]}'

class UserCourse(BaseModel):
    completion_date = models.DateField(_('Data de conclusão'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    course = models.ForeignKey(UndergraduateCourse, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Graduação de Usuário')
        verbose_name_plural = _('Graduações de Usuário')

    def __str__(self):
        return f'{self.name}'

NOTIFICATION_STATUS = (
    ('N', 'Não lida'),
    ('L', 'Lida')
)

class Notification(BaseModel):
    content = models.CharField(_('Conteúdo'), max_length=80)
    status = models.CharField(_('Status'), max_length=1, choices=NOTIFICATION_STATUS)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")

    class Meta:
        verbose_name = _('Notificação')
        verbose_name_plural = _('Notificações')

    def __str__(self):
        return f'{self.name}'
