from django.db import models
from django.utils.translation import gettext as _

from base.models import BaseModel, Modality, Step
from users.models import User

NOTICE_STATUS_CHOICES = (
    ('P', 'Pendente'),
    ('A', 'Em andamento'),
    ('X', 'Cancelado'),
    ('C', 'Concluído'),
    ('D', 'Desativado')
)

class Notice(BaseModel):
    title = models.CharField(_('Título'), max_length=40)
    identifier = models.CharField(_('Identificador'), max_length=15)
    opening_date = models.DateField(_('Data de abertura'))
    closing_date = models.DateField(_('Data de encerramento'))
    start_date = models.DateField(_('Data de início das inscrições'))
    end_date = models.DateField(_('Data de fim das inscrições'))
    status = models.CharField(_('Status'), max_length=1, choices=NOTICE_STATUS_CHOICES)

    class Meta:
        verbose_name = _('Curso de Graduação')
        verbose_name_plural = _('Cursos de Graduação')

    def __str__(self):
        return f'{self.title}'

class Vacancy(BaseModel):
    quantity = models.IntegerField(_('Quantidade'))
    modality = models.ForeignKey(Modality, on_delete=models.CASCADE)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name="vacancies")

    class Meta:
        verbose_name = _('Vaga para Modalidade de Edital')
        verbose_name_plural = _('Vagas para Modalidade de Edital')

    def __str__(self):
        return f'{self.notice.title} - {self.modality.name}'

ATTACHMENT_TYPES = (
    ('A', 'Adendo'),
    ('M', 'Modelo'),
    ('C', 'Caderno de Provas')
)

class NoticeAttachment(BaseModel):
    name = models.CharField(_('Nome'), max_length=25)
    type = models.CharField(_('Tipo'), max_length=1, choices=ATTACHMENT_TYPES)
    file = models.FileField(_('Arquivo'), upload_to='uploads/')
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name="attachments")

    class Meta:
        verbose_name = _('Anexo de Edital')
        verbose_name_plural = _('Anexos de Edital')

    def __str__(self):
        return f'{self.notice.title} - {self.name}'

class NoticeStep(BaseModel):
    order = models.IntegerField(_('Ordem'))
    passing_score = models.DecimalField(_('Nota de corte'), max_digits=3, decimal_places=2)
    release_date = models.DateField(_('Data de publicação'))
    resource_limit_date = models.DateField(_('Data de limite para recurso'))
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name="notice_steps")
    step = models.ForeignKey(Step, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Etapa de Edital')
        verbose_name_plural = _('Etapa de Edital')

    def __str__(self):
        return f'{self.notice.title} - {self.step.name}'

DOCUMENT_TYPE_CHOICES = (
    ('D', 'Documento'),
)

class RequiredDocument(BaseModel):
    name = models.CharField(_('Nome'), max_length=25)
    file = models.FileField(_('Arquivo'), upload_to='uploads/')
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name="notice_steps")
    type = models.CharField(_('Tipo'), max_length=1, choices=DOCUMENT_TYPE_CHOICES)
    optional = models.BooleanField(_('Opcional'))
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name="required_documents")

    class Meta:
        verbose_name = _('Documento Solicitado')
        verbose_name_plural = _('Documentos Solicitados')

    def __str__(self):
        return f'{self.notice.title} - {self.name}'

SUBSCRIPTION_CHOICES = (
    ('P', 'Pendente'),
    ('I', 'Indeferida'),
    ('D', 'Deferida')
)

class Subscription(BaseModel):
    date = models.DateTimeField(_('Data de inscrição'))
    stump_voucher = models.FileField(_('Comprovante de cota'), upload_to="uploads/")
    lattes = models.CharField(_("Currículo Lattes"), max_length=50)
    status = models.CharField(_("Status"), max_length=1, choices=SUBSCRIPTION_CHOICES)
    scholarship = models.BooleanField(_("Bolsa Capes"))
    full_name = models.CharField(_("Nome completo"), max_length=255)
    email = models.EmailField(_("Email"), max_length=50)
    address = models.CharField(_('Endereço Residencial'), max_length=90)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Inscrição')
        verbose_name_plural = _('Inscrições')

    def __str__(self):
        return f'{self.full_name} - {self.notice.title}'

class SentDocument(BaseModel):
    answer = models.CharField(_("Resposta"), max_length=50)
    file = models.FileField(_('Arquivo'), upload_to='uploads/')
    required_document = models.ForeignKey(RequiredDocument, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='sent_documents')

    class Meta:
        verbose_name = _('Documento Enviado')
        verbose_name_plural = _('Documentos Enviados')

    def __str__(self):
        return f'{self.subscription.id}'

class StepResult(BaseModel):
    score = models.DecimalField(_('Nota'), max_digits=3, decimal_places=2)
    obs = models.CharField(_('Observações'), max_length=255)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="step_results")
    notice_step = models.ForeignKey(NoticeStep, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Resultados de Etapa')
        verbose_name_plural = _('Resultados de Etapa')

    def __str__(self):
        return f'{self.subscription.id} - {self.notice_step.step.name}'

RESOURCE_STATUS_CHOICES = (
    ('P', 'Pendente'),
    ('A', 'Aceito'),
    ('R', 'Rejeitado')
)

class Resource(BaseModel):
    text = models.CharField(_('Texto'), max_length=255)
    file = models.FileField(_('Arquivo'), upload_to='uploads/')
    status = models.CharField(_('Status'), max_length=1, choices=RESOURCE_STATUS_CHOICES)
    date = models.DateTimeField(_('Data de postagem'))
    step_result = models.ForeignKey(StepResult, on_delete=models.CASCADE, related_name="resources")

    class Meta:
        verbose_name = _('Recurso de Etapa')
        verbose_name_plural = _('Recursos de Etapa')

    def __str__(self):
        return f'{self.subscription.id} - {self.notice_step.step.name}'

class ResourceAnswer(BaseModel):
    text = models.CharField(_('Texto'), max_length=255)
    file = models.FileField(_('Arquivo'), upload_to='uploads/')
    date = models.DateTimeField(_('Data de postagem'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.OneToOneField(Resource, on_delete=models.CASCADE, related_name="answer")

    class Meta:
        verbose_name = _('Resposta a Recurso')
        verbose_name_plural = _('Respostas a Recurso')

    def __str__(self):
        return f'{self.id} - {self.text}'