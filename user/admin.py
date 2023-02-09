from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.html import format_html
from user.models import *
from .forms import CustomerChangeForm, CustomerCreationFrom


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomerChangeForm
    add_form = CustomerCreationFrom

    list_display = ('username', 'email', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'groups', 'last_login', 'date_joined')

    fieldsets = (
        ('Main info', {'fields': ('username', 'password', 'email', 'mobile')}),
        (None, {'fields': ('first_name', 'last_name', 'age', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'last_login', 'groups', 'user_permissions')})
    )

    add_fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'age', 'mobile', 'password1', 'password2')})
    )
    search_fields = ('email', 'username')
    ordering = ('date_joined',)
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = ('ostan', 'shahrestan', 'user', 'is_default')
    list_filter = ('is_default', 'ostan',)

    def user(self, obj):
        url = (
            reverse("admin:user_user_change", args=str(obj.user_id.id))

        )
        return format_html('<a href="{}">{}</a>', url, obj.user_id)

    fieldsets = (
        ('info', {'fields': ('user_id', 'ostan', 'shahrestan', 'is_default')}),
        ('more info', {'fields': ('street', 'postal_code', 'detail')}),
    )

    add_fieldsets = (
        (None, {'fields': ('user_id', 'ostan', 'shahrestan', 'is_default', 'street', 'postal_code', 'detail')})
    )

    search_fields = ('ostan', 'shahrestan')
    ordering = ('shahrestan',)


@admin.register(PayAccount)
class PayAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'term', 'user', 'is_default')
    list_filter = ('is_default',)

    def user(self, obj):
        return AddressAdmin.user(self, obj)

    def term(self, obj):
        date_remined = expiry_date_validate(obj.expiry_date)
        if date_remined:
            if date_remined < 5:
                return f' -- {date_remined} days --'

            return f'{date_remined} days'

        else:
            return 'expired'

    search_fields = ('account_number',)


admin.site.register(OptCode)