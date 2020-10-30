from django.contrib import admin
from users.models import User

class UserAdmin(admin.ModelAdmin):

    list_display = (
        'email',
        'full_name',
        'cpf',
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser')

    '''fieldsets = (
        (None, {'fields': ('email', 'cpf', 'full_name', 'date_joined', 'is_active')}),
        (
            'Pesquisa',
            {'fields': ('music_group', 'week', 'next_form', 'complete_treatment')},
        ),
    )'''
    readonly_fields = ('created_at',)


# Register your models here.
admin.site.register(User, UserAdmin)