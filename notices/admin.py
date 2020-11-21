from django.contrib import admin
from .models import *

admin.site.register(Notice)
admin.site.register(Vacancy)
admin.site.register(NoticeAttachment)
admin.site.register(NoticeStep)
admin.site.register(RequiredDocument)
admin.site.register(Subscription)
admin.site.register(SentDocument)
admin.site.register(StepResult)
admin.site.register(Resource)
admin.site.register(ResourceAnswer)