from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'date_joined', 'is_active')
    list_filter = ('date_joined',)
    search_fields = ('first_name','last_name', 'email')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)