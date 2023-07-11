from django.contrib import admin
from . models import *
from django.contrib.auth.admin import UserAdmin


class CustomPaystack(UserAdmin):
    list_display = ('email', 'amount', 'reference', 'verified', 'generated')
    list_filter = ('generated',)
    search_fields = ('reference','email')
    readonly_fields = ('generated', 'amount', 'reference')
    ordering = ('-generated',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Paystack, CustomPaystack)
admin.site.register(Voucher)
