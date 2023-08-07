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
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name','gender','courses','payment_done')}),
        ('Permissions', {'fields': ('is_active', 'is_staff','is_admin', 'is_superadmin')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Contact', {'fields': ('phone_number',)}),)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),}),)
    

admin.site.register(Account, AccountAdmin)
admin.site.register(Assignment)
admin.site.register(Tutorial_video)
admin.site.register(Ebook)
admin.site.register(Duration)
admin.site.register(Total)



