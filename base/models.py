import uuid
from django.db import models
from django.utils.translation import gettext as _

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UndergraduateCourse(BaseModel):
    name = models.CharField(_('Nome'), max_length=40, unique=True)

    class Meta:
        verbose_name = _('Curso de Graduação')
        verbose_name_plural = _('Cursos de Graduação')

    def __str__(self):
        return f'{self.name}'

CENTERS = (
    ('CCET', 'Centro de Ciências Exatas e Tecnológicas'),
    ('CCJSA', 'Centro de Ciências Jurídicas e Sociais Aplicadas'),
    ('CCSD', 'Centro de Ciências da Saúde e do Desporto'),
    ('CELA', 'Centro de Educação, Letras e Artes'),
    ('CFCH', 'Centro de Filosofia e Ciências Humanas'),
    ('CCBN', 'Centro de Ciências Biológicas e da Natureza'),
    ('CEL', 'Centro de Educação'),
    ('CMULTI', 'Centro Multidisciplinar'),
)

class PostGraduationProgram(BaseModel):
    name = models.CharField(_('Nome'), max_length=40, unique=True)
    center = models.CharField(_('Centro'), max_length=6, choices=CENTERS)

    class Meta:
        verbose_name = _('Programa de Pós-graduação')
        verbose_name_plural = _('Programas de Pós-graduação')

    def __str__(self):
        return f'[{self.center}] {self.name}'

class Modality(BaseModel):
    name = models.CharField(_('Nome'), max_length=30, unique=True)
    center = models.CharField(_('Centro'), max_length=6, choices=CENTERS)

    class Meta:
        verbose_name = _('Modalidade de Vaga')
        verbose_name_plural = _('Modalidades de Vaga')

    def __str__(self):
        return f'[{self.center}] {self.name}'

class Step(BaseModel):
    name = models.CharField(_('Nome'), max_length=20, unique=True)

    class Meta:
        verbose_name = _('Tipo de Etapa')
        verbose_name_plural = _('Tipos de Etapa')

    def __str__(self):
        return f'{self.name}'
